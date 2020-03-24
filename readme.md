# Barnes-Hut Python Simulations

**THE CURRENT VERSION IS INCOMPATIBLE WITH PYTHON2**
I mean for a start python2 is discontinued, but I tried running this software again in 2020. The PIL and pillow libraries have changed drastically, even within python2, and since I was still new to python development when I wrote this code, I didn't understand the importance of correctly documenting dependencies. As such, I am just leaving this here for legacy -- I may update it one day for a laugh, but for now it remains testimony to my coding origins :)

Created by FB Nov/Dec 2017 for PH2140 at Royal Holloway   

Currently still in Alpha

----
The Barnes-Hut algorithm is an approximation for an N-Body problem, commonly used to solve gravitational simulations. The algorithm divides the region of space into a quadtree, reccursively itterating until there is only one object per node of the tree. Then, instead of computing acceleration between each body (N^2 time problem), if the node of the tree is a certain distance from the object under consideration, all masses in that space are assumed one, and the centre of mass used for position.
For more detail, see [here](http://arborjs.org/docs/barnes-hut).

----
<img src="https://github.com/Dustpancake/Barnes-Hut/blob/master/header.png" align="left" height="400" width="400" >
