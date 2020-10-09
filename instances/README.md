## Wildlife corridor design instances

The instances in this folder are for solving the wildlife corridor design problem which
also corresponds to the Connected Subgraph Problem.

### Instance types

1. [Artificially generated instances](artificial/) 
  Generated using this [instance generator](http://computational-sustainability.cis.cornell.edu/Datasets/corGenerator.zip) 
  with the slight adaption that assures that the utility values are always non-negative.

2. [Grizzly instances with budget constants](grizzly/) based on the instances 
  [grizzly-instances.zip](http://computational-sustainability.cis.cornell.edu/Datasets/grizzly-instances.zip). 


### Instance format

The instance format is specified below (based on the description from the [grizzly-instances.zip](http://computational-sustainability.cis.cornell.edu/Datasets/grizzly-instances.zip)).


  - Lines starting with 'c' are comments
  - Line starting with 'p' specifies two integers: 
     - the number of nodes in the graph 
     - the number of terminals
  - Lines starting with 'n' describe nodes in the graph (one for each node) in the 
  following format: `n i b u c e i1 i2 ... ie` where:
  
    - i is the id number of the node; i is an integer;
    - b whether the node is a reserve; b is 0 or 1;
    - u is the profit/utility of the node; u is a non-negative integer;
    - c is the cost of the node; c is a non-negative integer;
    - e is the number of neighboring nodes; e is a positive integer;
    - ij is the id of neighbor node j (j=1,2, ... ,e)
  - Line starting with 'b' specifies the budget 

#### Example

Example file content of a `.cor` instance describing a graph with 9 nodes (parcels), 
2 reserves (nodes 0 and 8) and with a budget of 38. As an example, node 5 has a 
profit of 20 and a cost of 46, and is connected with 3 nodes: 2,4 and 8. 

``` 
c This is a comment
p 9 2
n 0 1 48 0 2 1 3
n 1 0 90 32 3 0 2 4
n 2 0 88 78 2 1 5
n 3 0 80 76 3 0 4 6
n 4 0 90 26 4 1 3 5 7
n 5 0 20 46 3 2 4 8
n 6 0 30 38 2 3 7
n 7 0 32 43 3 4 6 8
n 8 1 27 0 2 5 7
b 38
```

