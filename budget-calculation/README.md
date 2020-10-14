## Budget calculation

This folder provides Python scripts to calculate budget constants for instances of the 
Wildlife corridor design problem, in particular for the instance files generated with 
the [Wildlife corridor design instance file generator](http://computational-sustainability.cis.cornell.edu/Datasets/corGenerator.zip).


### Setting things up

The very first time, setup a local Python environment and install the required packages by running:

    virtualenv -p python3.7 venv
    source venv/bin/activate
    pip install -r requirements.txt
    
    
### Running the budget calculation
    
Once you have set things up, you can run the budget calculation to calculate a budget 
constant for a .cor instance file. You can either extend a given instance, 
such as `my_instance.cor`, with the budget constant by executing: 

    python budget_calculation.py -i my_instance.cor

which will append some lines to `my_instance.cor` to specify the budget constant.
Alternatively, you can specify an output file into which to write the resulting .cor 
instance with the budget constant:

    python budget_calculation.py -i my_instance.cor -o my_instance_with_budget.cor
    
You can also specify the "budget percentage" that states how much larger than the budget lower 
bound the budget constant should lie. For example, if you would like the budget constant 
to be 15% over the budget lower bound, you state:

    python budget_calculation.py -i my_instance.cor -b 0.15
    
The default budget percentage is 10%. You can also specify a seed for the budget calculation
with the option `-s`. Note that the program always sets a predefined seed, so running it
without seed will still be deterministic.


### Running budget calculation for all artificial instances

To run the budget calculation on all artificial instances files, execute the Bash shell
script `calculate_budget.sh` in your Bash terminal:

    ./calculate_budget.sh

This will use the `.cor.orig` files in the `instances/artificial/` directory to generate the
(existing) instance files in the same folder.