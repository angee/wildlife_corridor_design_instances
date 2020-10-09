### Grizzly Real-world instances 

The Grizzly instances are from [grizzly-instances.zip](http://computational-sustainability.cis.cornell.edu/Datasets/grizzly-instances.zip)
with added budget constants. The data set is based on the real-world problem of designing 
wildlife corridors in the Northern Rocky Mountains, with the goal of connecting the 
Yellowstone, Salmon-Selway, and Northern Continental Divide ecosystems spanning the 
states of Idaho, Wyoming, and Montana. 

#### Grizzly instance types

We have 3 instance variants for the same underlying problem that differ in the resolution
of the study area. The study area is represented as a set of cells or “parcels” that 
represent the nodes in the graph. 
Each instance has a different grid cell resolution where larger cells result in an 
easier problem. Here are the instances ordered by difficulty (least difficult first):

   * **Instance-1**: 40x40 km cells with 242 nodes, 3 reserves
   * **Instance-2**: 10x10 km cells with 3,299 nodes, 3 reserves
   * **Instance-3**: 5x5 km cells with 12,889 nodes, 3 reserves

We created variants of each instance type, with different budgets (5%, 10%, 15% and 
20% above the lower bound for the budget).

#### Helper files

For each main Grizzly instance `instance.cor`, there are additional helper files:
 
  * **instance.minsteiner**
	- Provides the Minimum Steiner Tree (MST) in terms of node costs that connects the terminals
	- First line specifies the cost and utility of the MST
	- Second line lists the nodes that form the MST (including the terminals)
	
  * **instance.dist3**
	- Provides information useful for pruning/preprocessing when optimizing for a specific budget
	- For each node, provides the path cost of the cheapest path that passes through that node and connects any 2 of the terminals
	- If the specified budget is smaller than the path cost of a node, then that node will not be part of a solution for this budget level
	- Each line corresponds to the node id of a node that is not a terminal followed by its path cost
	
#### Special Notes

  - Each reserve covers a large area (bigger than a cell) and is represented as one node in the respective graph.
  - Cells with cost 9999999 are not available for purchase and should be ignored (they are there for completeness of the grid only).
  - The number of reserves is always the same (3 nodes) and is therefore very small compared to the total set of nodes. 
