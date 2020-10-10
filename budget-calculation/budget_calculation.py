# ---------------------------------------------------------------------------------------------------------------------
# Calculates the budget for a Wildlife Corridor Design instance
#
# Given a Wildlife corridor design .cor instance as generated by the instance generator from:
# http://computational-sustainability.cis.cornell.edu/Datasets/corGenerator.zip
# this program calculates the budget constant by:
#
# 1. Computing a minimum node-weighted Steiner Tree approximation for the instance
# 2. Taking the Steiner tree cost, and increasing it by X%
# 3. Extending the given .cor file with the budget constant, adding the line "b Y" where Y is the budget constant
#
# This file is part of the wildlife_corridor_design_instances repository which is released under the MIT license.
# See file at https://github.com/angee/wildlife_corridor_design_instances/blob/master/LICENSE for full license details.
#
# Author: Andrea Rendl-Pitrey, Satalia, October 2020
# ---------------------------------------------------------------------------------------------------------------------

import os
from argparse import ArgumentParser

from instance_reader import extract_info_from_cor_file, create_graph_from_adjacency_matrix
from steiner_tree_approximation import approximate_steiner_tree


def is_valid_file(parser, arg):
    """
    check if the given input file exists
    :param parser: command line argument parser
    :param arg: a given file (possibly including a path)
    :return:
    """
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def parse_args():
    """
    Parsing the command line arguments
    :return:
    """
    parser = ArgumentParser(description="Wildlife corridor design instance budget calculator")
    parser.add_argument("-i", dest="instance_file", required=True,
                        help=".cor instance file", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument("-o", dest="output_file", required=False, default="",
                        help="the file into which to write the .cor instance with budget constant", metavar="FILE")
    parser.add_argument("-b", dest="budget_percent", required=False, default=0.1,
                        help="the percentage to add to lower bound for budget, e.g. 0.1 for 10 percent")
    parser.add_argument("-s", dest="seed", required=False, default=11,
                        help="the seed for the steiner tree approximation algorithm")
    return parser.parse_args()


def calculate_lower_bound_for_budget(instance_file: str, seed: int) -> int:
    """
    Calculates a lower bound for the necessary budget to solve the Wildlife corridor design problem. This is done by
    finding an approximation for the minimum node-weighted Steiner Tree where the reserves are the terminals of the
    Steiner tree. The sum of all node costs of the nodes in the Steiner tree is a lower bound for the problem.

    :param instance_file: the .cor instance file that describes the graph and the reserves
    :param seed: the seed for the Steiner tree approximation algorithm.
    :return: the total node cost of the minimum node-weighted Steiner tree
    """
    nb_nodes, nb_reserves, is_reserve, profit, cost, adjacency_matrix = extract_info_from_cor_file(instance_file)
    graph = create_graph_from_adjacency_matrix(nb_nodes, adjacency_matrix, cost)
    reserves = [] # extract the nodes that are reserves, which will be the terminals in the Steiner tree
    for node in range(1, nb_nodes):
        if is_reserve[node]:
            reserves.append(node)
    steiner_tree, steiner_tree_cost = approximate_steiner_tree(graph=graph, terminals=reserves, seed=seed)
    return steiner_tree_cost


def append_budget_constant_to_instance_file(instance_file: str, budget: int, percentage: float)-> None:
    """
    Appends a line to the instance file with the budget

    :param instance_file: the .cor instance file
    :param budget: the calculated budget to be written into the instance file
    :param percentage: the percentage that was added on top of the lower bound for the budget
    :return:
    """
    with open(instance_file, "a") as f:
        f.write("c the budget calculated from the minimum Steiner tree cost plus " + str(float(percentage)*100) + "%.\n")
        f.write("b " + str(budget) + "\n")
    print("Appended budget \"" + str(budget) + "\" to instance file: " + str(instance_file))
    f.close()


def create_new_cor_instance_with_budget_constant(input_file: str, output_file: str, budget: int, percentage: float):
    new_instance_file = open(output_file, "w")
    with open(input_file, "r") as f:
        new_instance_file.write(f.read())
    new_instance_file.close()
    append_budget_constant_to_instance_file(output_file, budget, percentage)


def main():
    args = parse_args()
    lower_bound_for_budget = calculate_lower_bound_for_budget(args.instance_file, args.seed)
    budget = round(lower_bound_for_budget + lower_bound_for_budget*float(args.budget_percent))
    if args.output_file == "": # if no output file is specified, then extend input file
        append_budget_constant_to_instance_file(args.instance_file, budget, args.budget_percent)
    else:
        create_new_cor_instance_with_budget_constant(args.instance_file, args.output_file, budget, args.budget_percent)


if __name__ == "__main__":
    main()