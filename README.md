## Wildlife corridor design instances



This repository contains instances for the [Wildlife corridor design problem](http://www.cs.cornell.edu/~bistra/papers/CPAIOR2010_dilkina.pdf),
as proposed by researchers at the 
[Institute of Computational Sustainability at Cornell University](http://computational-sustainability.cis.cornell.edu/).
Furthermore, it contains a tool to extend instances with budget constants.


#### 1. Wildlife corridor design instances 

Two different instance sets for the wildlife corridor design problem:

* [Artificially generated instances](instances/artificial)  and
* Real-world [Grizzly instances with budget constants](instances/grizzly).

  
#### 2. Budget calculator 
  
  An algorithm to calculate the budget for the generated .cor instances including:
  
   - Two graph algorithms implemented in the [NetworkX](https://networkx.github.io/) graph library:
       - Minimum node-cost path calculation
       - Minimum node-cost Steiner tree approximation
       
       
### Wildlife corridor design problem

Given a connected, undirected graph G = (V,E) with non-negative costs c(v) and profits p(v) 
associated with the vertices v in V, a positive budget b, and a set of distinguished 
vertices V_T that is a strict subset of V. The goal is to find a connected subgraph 
of G that contains the subset V_T. The objective is to maximize the total profit of the 
vertices in the subgraph subject to a budget constraint on its total cost.

In wildlife corridor design, the set of distinguished vertices represents the wildlife 
reserves that we seek to connect. The vertex costs represent land purchasing costs, and 
profits represent the benefit for the wildlife species.

For more details, check out the paper:

[Solving Connected Subgraph Problems in Wildlife Conservation](http://www.cs.cornell.edu/~bistra/papers/CPAIOR2010_dilkina.pdf). 
Bistra Dilkina, Carla P. Gomes: CPAIOR 2010: 102-116.