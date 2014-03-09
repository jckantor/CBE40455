
set NAMES;

param Age{NAMES};

table tin IN "CSV" "input.csv" : NAMES <- [Name], Age;
    
for {n in NAMES}: printf "%s\n", n;

end;
