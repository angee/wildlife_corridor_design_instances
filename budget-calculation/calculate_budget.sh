#!/bin/bash
#
# Script to calculate the budgets of all artificial problem instances.
# Make sure you have started your Python environment and that
# all required packages are installed!

INSTANCES_DIR=../instances/artificial/
SUFFIX=".cor.orig"

declare -a budget_limits=(0.05 0.1 0.15)

for f in ${INSTANCES_DIR}*${SUFFIX}; do
    for budget_limit in "${budget_limits[@]}"; do

	budget_limit_str=${budget_limit#"0."}
	if [ "${#budget_limit_str}" == 1 ]; then
	    budget_limit_str=${budget_limit_str}0
	fi

	output=""
	if [[ $f == *"uncorr"* ]]; then	    
	    output=${f%"uncorr${SUFFIX}"}${budget_limit_str}b
	    output=${output}_uncorr.cor
	else
	    output=${f%"corr${SUFFIX}"}${budget_limit_str}b	   
	    output=${output}_corr.cor
	fi
	
	echo "python budget_calculation.py -i $f -o ${output} -b ${budget_limit}"
	python budget_calculation.py -i $f -o ${output} -b ${budget_limit}
    done
done
