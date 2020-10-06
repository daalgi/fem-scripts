// L-shaped section - sub-divisions
Point(1) = {0, 0, 0, 1.0};
Point(2) = {3.5, 0, 0, 1.0};
Point(3) = {5, 0, 0, 1.0};
Point(4) = {5, 1, 0, 1.0};
Point(5) = {5, 5, 0, 1.0};
Point(6) = {3.5, 5, 0, 1.0};
Point(7) = {3.5, 1, 0, 1.0};
Point(8) = {0, 1, 0, 1.0};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 5};
Line(5) = {5, 6};
Line(6) = {6, 7};
Line(7) = {7, 8};
Line(8) = {8, 1};

Line(9) = {2, 7};

Curve Loop(1) = {1, 9, 7, 8};
Plane Surface(1) = {1};

Curve Loop(2) = {2, 3, 4, 5, 6, -9};
Plane Surface(2) = {2};

Physical Curve("inlet") = {8};
Physical Curve("top") = {5};
Physical Surface("Fluid") = {1};
