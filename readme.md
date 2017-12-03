# Barnes-Hut Python Simulations

Created by F Baker Nov/Dec 2017 for PH2140 at Royal Holloway   

Currently still in Alpha

----
The Barnes-Hut algorithm is an approximation for an N-Body problem, commonly used to solve gravitational simulations. The algorithm divides the region of space into a quadtree, reccursively itterating until there is only one object per node of the tree. Then, instead of computing acceleration between each body (N^2 time problem), if the node of the tree is a certain distance from the object under consideration, all masses in that space are assumed one, and the centre of mass used for position.
For more detail, see [here](http://arborjs.org/docs/barnes-hut).

----
![alt text](https://github.com/Moontemple/Barnes-Hut/blob/master/header.png "1000 Bodies")
