
# Example: ProjectCPM.mod

set TASKS;
set ARCS within {TASKS cross TASKS};

/* Parameters are the durations for each task */
param dur{TASKS} >= 0;
param desc{TASKS} symbolic;

/* Decision Variables associated with each task*/
var Tes{TASKS} >= 0;     # Earliest Start
var Tef{TASKS} >= 0;     # Earliest Finish
var Tls{TASKS} >= 0;     # Latest Start
var Tlf{TASKS} >= 0;     # Latest Finish
var Tsl{TASKS} >= 0;     # Slacks

/* Global finish time */
var Tf >= 0;

/* Minimize the global finish time and, secondarily, maximize slacks */
minimize ProjectFinish : card(TASKS)*Tf - sum {j in TASKS} Tsl[j];

/* Finish is the least upper bound on the finish time for all tasks */
s.t. Efnsh {j in TASKS} : Tef[j] <= Tf;
s.t. Lfnsh {j in TASKS} : Tlf[j] <= Tf;

/* Relationship between start and finish times for each task */
s.t. Estrt {j in TASKS} : Tef[j] = Tes[j] + dur[j];
s.t. Lstrt {j in TASKS} : Tlf[j] = Tls[j] + dur[j];

/* Slacks */
s.t. Slack {j in TASKS} : Tsl[j] = Tls[j] - Tes[j];

/* Task ordering */
s.t. Eordr {(i,j) in ARCS} : Tef[i] <= Tes[j];
s.t. Lordr {(j,k) in ARCS} : Tlf[j] <= Tls[k];

/* Compute Solution  */
solve;

/* Print Report */
printf 'PROJECT LENGTH = %8g\n',Tf;

/* Critical Tasks are those with zero slack */

/* Rank-order tasks on the critical path by earliest start time */
param r{j in TASKS : Tsl[j] = 0} := sum{k in TASKS : Tsl[k] = 0}
   if (Tes[k] <= Tes[j]) then 1;

printf '\nCRITICAL PATH\n';
printf '    TASK    DUR     Start    Finish    Description\n';
printf {k in 1..card(TASKS), j in TASKS : Tsl[j]=0 && k==r[j]}
   '%8s %6g  %8g  %8g    %-25s\n', j, dur[j], Tes[j], Tef[j], desc[j];

/* Noncritical Tasks have positive slack */

/* Rank-order tasks not on the critical path by earliest start time */
param s{j in TASKS : Tsl[j] > 0} := sum{k in TASKS : Tsl[k] = 0}
   if (Tes[k] <= Tes[j]) then 1;

printf '\nNON-CRITICAL TASKS\n';
printf '                 Earliest  Earliest    Latest    Latest \n';
printf '    TASK    DUR     Start    Finish     Start    Finish     Slack   Description\n';
printf {k in 1..card(TASKS), j in TASKS : Tsl[j] > 0 && k==s[j]}
   '%8s %6g  %8g  %8g  %8g  %8g  %8g   %-25s\n', 
   j,dur[j],Tes[j],Tef[j],Tls[j],Tlf[j],Tsl[j],desc[j];
printf '\n';

end;