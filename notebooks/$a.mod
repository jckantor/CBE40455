
param a := 12.3;
param b := 13.0;

var x >= 0;
var y >= 0;

s.t. Ca : 2*x + 3*y <= a;
s.t. Cb : 3*x + 1*y <= b;

maximize obj: x + y;

solve;

display x,y;
   
end;