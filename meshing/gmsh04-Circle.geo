// Circle
SetFactory("Built-in");
Point(1) = {0, 0, 0, 1.0};
Point(2) = {5, 0, 0, 1.0};
Point(3) = {0, 5, 0, 1.0};

//Circle(1) = {0, 0, 0, 5, 0, Pi/2};// OpenCASCADE factory
Circle(1) = {2, 1, 3};
Line(2) = {1, 2};
Line(3) = {1, 3};

Curve Loop(1) = {2, 1, -3};
Plane Surface(1) = {1};

//Transfinite Curve {2} = 10 Using Progression 1;
//Transfinite Curve {3} = 10 Using Progression 1;
