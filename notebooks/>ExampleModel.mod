
param a := 12.3;
param b := 10.4;

var x >= 0;
var y >= 0;

s.t. Ca: 3.0*x + 4.0*x <= a;
s.t. Cb: 4.0*x + 2.0*x <= b;

maximize obj: x + y;
solve;

end;