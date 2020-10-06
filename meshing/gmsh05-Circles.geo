// Gmsh project created on Tue Oct 06 20:43:01 2020
// PARAMETERS
h1 = 1;
in_r = 2;
out_r = 2.4;
ped_r = 3;
slab_r = 10;

div_in = 5;
div_load = 2;
div_out = 3;
div_slab = 10;
div_circ = 12;

// FIRST QUADRANT
Point(1) = {0, 0, 0, h1};
Point(2) = {in_r, 0, 0, h1};
Point(3) = {out_r, 0, 0, h1};
Point(4) = {ped_r, 0, 0, h1};
Point(5) = {slab_r, 0, 0, h1};

Point(6) = {0, in_r, 0, h1};
Point(7) = {0, out_r, 0, h1};
Point(8) = {0, ped_r, 0, h1};
Point(9) = {0, slab_r, 0, h1};

Circle(1) = {2, 1, 6};
Circle(2) = {3, 1, 7};
Circle(3) = {4, 1, 8};
Circle(4) = {5, 1, 9};

Line(5) = {1, 2};
Line(6) = {2, 3};
Line(7) = {3, 4};
Line(8) = {4, 5};

Line(9) = {1, 6};
Line(10) = {6, 7};
Line(11) = {7, 8};
Line(12) = {8, 9};

Curve Loop(1) = {5, 1, -9};
Plane Surface(1) = {1};

Curve Loop(2) = {6, 2, -10, -1};
Plane Surface(2) = {2};

Curve Loop(3) = {7, 3, -11, -2};
Plane Surface(3) = {3};

Curve Loop(4) = {8, 4, -12, -3};
Plane Surface(4) = {4};

Transfinite Curve {1, 2, 3, 4} = div_circ Using Progression 1;
Transfinite Curve {5, 9} = div_in Using Progression 1;
Transfinite Curve {6, 10} = div_load Using Progression 1;
Transfinite Curve {7, 11} = div_out Using Progression 1;
Transfinite Curve {8, 12} = div_slab Using Progression 1;

// When the surface has only 3-4 points on its boundaries, the list 
// of corners can be omitted in the `Transfinite Surface` constraint.
Transfinite Surface {2};// = {2, 3, 8, 7};
Transfinite Surface {3};
Transfinite Surface {4};
//Recombine Surface {1, 2, 3, 4};

// SYMMETRY Y
Symmetry {1, 0, 0, 0}{Duplicata{Surface{1, 2, 3, 4};}};

Transfinite Curve {15, 19, 24, 29} = div_circ Using Progression 1;
Transfinite Curve {14} = div_in Using Progression 1;
Transfinite Curve {18} = div_load Using Progression 1;
Transfinite Curve {23} = div_out Using Progression 1;
Transfinite Curve {28} = div_slab Using Progression 1;

Transfinite Surface {17};
Transfinite Surface {22};
Transfinite Surface {27};

// SYMMETRY X
Symmetry {0, 1, 0, 0}{Duplicata{Surface{1, 2, 3, 4, 13, 17, 22, 27};}};

Transfinite Curve {51, 55, 60, 65, 32, 36, 41, 46} = div_circ Using Progression 1;
Transfinite Curve {33} = div_in Using Progression 1;
Transfinite Curve {37} = div_load Using Progression 1;
Transfinite Curve {42} = div_out Using Progression 1;
Transfinite Curve {47} = div_slab Using Progression 1;

Transfinite Surface {53};
Transfinite Surface {58};
Transfinite Surface {63};

Transfinite Surface {34};
Transfinite Surface {39};
Transfinite Surface {44};
