## Artificially generated Wildlife corridor design instances

The instance files in this directory were first generated with 
the [Wildlife corridor design instance file generator](http://computational-sustainability.cis.cornell.edu/Datasets/corGenerator.zip),
and then extended with a budget constant using the budget calculator in this repository.

### Instance naming convention

The files are named as follows:

    {$X}P_{$Y}R_{$Z}b_{corr|uncorr}.cor

where `{$X}` is the total number of parcels (nodes) in the graph, `{$Y}` is the number of 
reserves (distinguished nodes) that we want to connect. Note that this means that `{$X} - {$Y}` 
parcels (nodes) are not reserves. `{$Z}` represents the budget percentage, i.e. how much more
than the budget's lower bound the budget is. For example, if the budget percentage is `10`,
then the budget constant will be 10% higher than the lower bound for the budget.   

The utlities and costs of each parcel are generated in two different ways with the instances 
generator that are represented by either `corr` or `uncorr`. With the `corr` option, the 
utility/costs between adjacent parcels/nodes are weakly correlated, and with `uncorr` the 
utility/cost values are randomly assigned to the parcels. This means that the `corr` 
variant is slightly more realistic than the `uncorr` variant. 

#### Example

    16P_2R_05b_corr.cor 
    
has 16 parcels (nodes) of which 2 are reserves, with a budget percentage of 5%, generated 
with weakly correlated cost/utility values.

#### Notes

Please note that I slightly adapted the instance generator to assure that all generated 
utility values are non-negative. The exact command to generate the instance is given in 
the comment section of each instance.