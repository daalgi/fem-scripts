//+
Point(1) = {0, 0, 0, 1};
Point(2) = {20, 0, 0, 1};
Point(3) = {-20, 0, 0, 1};
Point(4) = {-30, 0, 0, 1};
Point(5) = {30, 0, 0, 1};
Point(6) = {30, -30, 0, 1};
Point(7) = {-30, -30, 0, 1};
Point(8) = {-14.1421356237, -14.1421356237, 0, 1.0};
Point(9) = {14.1421356237, -14.1421356237, 0, 1.0};

Line(1) = {4, 7};
Line(2) = {4, 3};
Line(3) = {2, 5};
Line(4) = {5, 6};
Circle(8) = {3, 1, 8};
Circle(9) = {8, 1, 9};
Circle(10) = {9, 1, 2};
Line(11) = {8, 7};
Line(12) = {9, 6};
Line(13) = {7, 6};

Line Loop(13) = {2, 8, 11, -5, -1};
Plane Surface(14) = {13};
Line Loop(15) = {10, 3, 4, -12};
Plane Surface(16) = {15};
Line Loop(19) = {11, 13, -12, -9};
Plane Surface(20) = {19};

Physical Line("curve") = {2, 8, 9, 10, 3};
Physical Line("inlet") = {1};
Physical Line("outlet") = {4};
Physical Line("wall") = {5, 6, 7};
Physical Surface("fluid") = {14, 16, 18};

Transfinite Curve {2, 11, 12, 3} = 5 Using Progression 1;
Transfinite Curve {1, 8, 4, 10} = 8 Using Progression 1;
Transfinite Curve {13, 9} = 10 Using Progression 1;
Transfinite Surface {14} = {4, 3, 8, 7};
Transfinite Surface {20} = {8, 9, 6, 7};
Transfinite Surface {16} = {9, 2, 5, 6};
Recombine Surface {14, 16, 20};
