
set PLANTS;                            # Set of plant types
set DEMAND;                            # Demand Segments
set SCENARIOS;                         # Planning Scenarios

param e{PLANTS};                       # Current Plant Capacity
param C{PLANTS};                       # Capital Cost per unit Expansion
param O{PLANTS};                       # Operating Cost [k$/GWh]

param T{DEMAND};                       # Time Periods for Demand Segments
param D{DEMAND,SCENARIOS};             # Demand Scenarios

var x {PLANTS} >= 0;                   # Plant Expansion
var y {PLANTS,DEMAND,SCENARIOS} >= 0;  # Operating Schedule
var v {SCENARIOS};                     # Variable Cost
var capcost;                           # Capital Cost

minimize COST: capcost + sum {s in SCENARIOS} 0.25*v[s];

s.t. CAPCOST: capcost = sum{p in PLANTS} C[p]*(e[p]+x[p]);
s.t. VARCOST {s in SCENARIOS}:
   v[s] = sum {p in PLANTS, d in DEMAND} T[d]*O[p]*y[p,d,s];
s.t. DEMANDS {p in PLANTS, s in SCENARIOS}: 
   e[p] + x[p] >= sum {d in DEMAND} y[p,d,s];
s.t. C4 {d in DEMAND, s in SCENARIOS} :
   D[d,s] = sum {p in PLANTS} y[p,d,s];
   
solve;

table results {p in PLANTS} OUT "CSV" "tmp/PlantExpansion.csv" "Table" :
    p~Plant,
    O[p]~Unit_Cost,
    e[p]~Current_Cap,
    x[p]~Exp_Cap,
    x[p]+e[p]~Total_Cap;

end;