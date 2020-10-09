### Grizzly Real-world instances 

The Grizzly instances are from [grizzly-instances.zip](http://computational-sustainability.cis.cornell.edu/Datasets/grizzly-instances.zip)
with added budget constants. The data set is based on the real-world problem of designing 
wildlife corridors in the Northern Rocky Mountains, with the goal of connecting the 
Yellowstone, Salmon-Selway, and Northern Continental Divide ecosystems spanning the 
states of Idaho, Wyoming, and Montana. 


### Grizzly instance types

We have 3 instance variants for the same underlying problem. The study area is 
represented as a set of cells or “parcels” that represent the nodes in the graph. 
Each instance has a different grid cell resolution where larger cells result in an 
easier problem. Here are the instances ordered by difficulty (least difficult first):

   * **Instance-1**: 40x40 km cells with 242 nodes, 3 reserves
   * **Instance-2**: 10x10 km cells with 3,299 nodes, 3 reserves
   * **Instance-3**: 5x5 km cells with 12,889 nodes, 3 reserves

We created variants of each instance type, with different budgets (5%, 10%, 15% and 
20% above the lower bound for the budget).

Note that the distinguished set of vertices is always the same (consisting of 3 nodes) 
and is therefore very small compared to the total set of nodes. 