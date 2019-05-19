
/* Data Table 1. Tasks consist of Job, Machine, Dur data*/
set TASKS dimen 2;
param dur{TASKS};

/* Data Table 2 */
set TASKORDER within {TASKS,TASKS};

/* JOBS and MACHINES are inferred from the data tables*/
set JOBS := setof {(j,m) in TASKS} j;
set MACHINES := setof {(j,m) in TASKS} m;

/* Decision variables are start times for tasks, and the makespan */
var start{TASKS} >= 0;
var makespan >= 0;

/* BigM is set to be bigger than largest possible makespan */
param BigM := 1 + sum {(i,m) in TASKS} dur[i,m];

/* The primary objective is to minimize makespan, with a secondary
objective of starting tasks as early as possible */
minimize OBJ: BigM*makespan + sum{(i,m) in TASKS} start[i,m];

/* By definition, all jobs must be completed within the makespan */
s.t. A {(j,m) in TASKS}: start[j,m] + dur[j,m] <= makespan;

/* Must satisfy any orderings that were given for the tasks. */
s.t. B {(i,m,j,n) in TASKORDER}: start[i,m] + dur[i,m] <= start[j,n];

/* Eliminate conflicts if tasks are require the same machine */
/* y[i,m,j] = 1 if Job i is scheduled before job j on machine m*/
var y{(i,m) in TASKS,(j,m) in TASKS: i < j} binary;
s.t. C {(i,m) in TASKS,(j,m) in TASKS: i < j}:
   start[i,m] + dur[i,m] <= start[j,m] + BigM*(1-y[i,m,j]);
s.t. D {(i,m) in TASKS,(j,m) in TASKS: i < j}:
   start[j,m] + dur[j,m] <= start[i,m] + BigM*y[i,m,j];

solve;

printf "Makespan = %5.2f\n",makespan;

/* Post solution, compute finish times for each task to use in report */
param finish{(j,m) in TASKS} := start[j,m] + dur[j,m];

/* Task Summary Report */
printf "\n                TASK SUMMARY\n";
printf "\n     JOB   MACHINE     Dur   Start  Finish\n";
printf {(i,m) in TASKS} "%8s  %8s   %5.2f   %5.2f   %5.2f\n", 
   i, m, dur[i,m], start[i,m], finish[i,m];

/* Schedule of activities for each job */
set M{j in JOBS} := setof {(j,m) in TASKS} m;
param r{j in JOBS, m in M[j]} := 
   1+sum{n in M[j]: start[j,n] < start[j,m] || start[j,n]==start[j,m] && n < m} 1;
printf "\n\n           JOB SCHEDULES\n";
for {j in JOBS} {
   printf "\n%s:\n",j;
   printf "         MACHINE   Start   Finish\n";
   printf {k in 1..card(M[j]), m in M[j]: k==r[j,m]} 
      " %15s   %5.2f    %5.2f\n",m, start[j,m],finish[j,m];
}

/* Schedule of activities for each machine */
set J{m in MACHINES} := setof {(j,m) in TASKS} j;
param s{m in MACHINES, j in J[m]} := 
   1+sum{k in J[m]: start[k,m] < start[j,m] || start[k,m]==start[j,m] && k < j} 1;
printf "\n\n         MACHINE SCHEDULES\n";
for {m in MACHINES} {
   printf "\n%s:\n",m;
   printf "             JOB   Start   Finish\n";
   printf {k in 1..card(J[m]), j in J[m]: k==s[m,j]} 
      " %15s   %5.2f    %5.2f\n",j, start[j,m],finish[j,m];
}

end;