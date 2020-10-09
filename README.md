## Wildlife corridor design instances

### Overview

This repository contains instances for the [Wildlife corridor design problem](http://www.cs.cornell.edu/~bistra/papers/CPAIOR2010_dilkina.pdf),
as proposed by researchers at the 
[Institute of Computational Sustainability at Cornell University](http://computational-sustainability.cis.cornell.edu/).
Furthermore, it contains a tool to extend instances with budget constants.



#### 1. Wildlife corridor design instances 

* [Artificially generated instances](instances/artificial) 
  Generated using this [instance generator](http://computational-sustainability.cis.cornell.edu/Datasets/corGenerator.zip) 
  with the slight adaption that assures that the utility values are always non-negative.

* [Grizzly instances with budget constants](instances/grizzly) based on the instances 
  [grizzly-instances.zip](http://computational-sustainability.cis.cornell.edu/Datasets/grizzly-instances.zip). 

All instances are extended with budget constants in the last line of the instance.
  
#### 2. Budget calculator 
  
  An algorithm to calculate the budget for the generated .cor instances including:
  
   - Two graph algorithms implemented in the [NetworkX](https://networkx.github.io/) graph library:
       - Minimum node-cost path calculation
       - Minimum node-cost Steiner tree approximation