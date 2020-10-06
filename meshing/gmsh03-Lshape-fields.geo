// L-shaped section
h1=0.5;
Point(1) = {0, 0, 0, h1};
Point(2) = {5, 0, 0, h1};
Point(3) = {5, 5, 0, h1};
Point(4) = {3.5, 5, 0, h1};
Point(5) = {3.5, 1, 0, h1};
Point(6) = {0, 1, 0, h1};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 5};
Line(5) = {5, 6};
Line(6) = {6, 1};

Curve Loop(1) = {5, 6, 1, 2, 3, 4};
Plane Surface(1) = {1};

Physical Curve("Left") = {6};
Physical Curve("Top") = {3};
Physical Surface("Fluid") = {1};

Field[1] = Cylinder;
Field[1].Radius = 0.25;
Field[1].VIn = 0.05;
Field[1].VOut = 0.5;
Field[1].XAxis = 1;
Field[1].XCenter = 2.5;
Field[1].YAxis = 0.5;
Field[1].ZAxis = 0;
Field[1].YAxis = 0;
Field[1].YCenter = 1;
Field[1].YCenter = 0.5;
Field[1].XCenter = 3.5;
Background Field = 1;