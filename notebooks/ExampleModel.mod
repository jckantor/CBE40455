
# model section
param a;
param b;

var x >= 0;
var y >= 0;

subject to Ca: 3.0*x + 4.0*y <= a;
subject to Cb: 4.0*x + 2.0*y <= b;

maximize obj: x + y;
solve;
printf "x = %6.3f\n", x;
printf "y = %6.3f\n", y;

end;