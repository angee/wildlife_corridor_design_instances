# ---------------------------------------------------------------------------------------------------------------------
# Greedy node-weighted Minimal Steiner Tree approximation
#
# Implements a greedy heuristic to calculate an approximation of the node-weighted
# minimal Steiner tree. Given an undirected graph with weighted nodes and a set of
# terminal nodes, compute the minimal Steiner tree (approximation) that connects
# all terminal nodes.
#
# ------ Algorithm: -----------------------------------------------------------------
#
# The algorithm is based on one of the heuristics from:
# "A nearly best-possible approximation algorithm for node-weighted Steiner trees"
#  Klein, P. N., and Ravi, R. (1995), J. Algorithms 19, pages 104-114.
#
# Given an undirected graph G=(V,E) with costs c_v associated with each vertex v in V,
# and a set of terminal vertices Vt subset V.
#
# 1. For each terminal t in Vt, create a single-node graph (a tree) and group these
#    "terminal trees" in the tree list T.
# 2. While |T| > 2:   (while the number of trees in the tree list is greater than 2)
#    a. Calculate the minimal node-cost path p_ij between all trees in T, i.e. for each
#       t_i, t_j in T, where i,j in 1..|T| and i < j. We say path p_ij has cost c_ij.
#    b. Determine the two trees t_i, t_j in T with the smallest path cost c_ij
#    c. Connect the trees t_i and t_j through their min cost path p_ij and merge them
#       into tree t'
#    d. Remove t_i and t_j from T and add the merged tree t' to T
# 3. Calculate the minimal node cost path between the two remaining trees in T
# 4. Connect the remaining two trees in T through their min cost path which yields a
#    Steiner tree approximation
#
# This file is part of the wildlife_corridor_design_instances repository which is released under the MIT license.
# See file at https://github.com/angee/wildlife_corridor_design_instances/blob/master/LICENSE for full license details.
#
# Author: Andrea Rendl-Pitrey, September 2020
# ---------------------------------------------------------------------------------------------------------------------

import random

import networkx as nx

from min_cost_path_calculation import calculate_min_cost_path


def initialise_trees(terminals: list) -> list:
    """
    Create a tree for each terminal and return a list of pairs: the tree graph paired with the terminal.
    :param terminals: the terminals of the Steiner tree
    :return: a list of graphs paired with the terminal the graph represents
    """
    trees = []
    for terminal in terminals:
        tree = nx.Graph()
        tree.add_node(terminal)
        trees.append((tree, terminal))
    return trees


def copy_and_initialise_main_graph(graph: nx.graph, terminals: list) -> nx.graph:
    """ Create a copy of the given graph which we will use to calculate the Steiner tree. """
    copied_graph = graph.copy()
    # set the node costs of the terminals to zero
    for terminal in terminals:
        copied_graph.nodes()[terminal]['cost'] = 0
    return copied_graph


def pick_random_node(tree: nx.Graph) -> int:
    """ Picks a random node from the given graph and returns it. """
    size = tree.size()
    return tree.nodes()[random.randint(0, size - 1)]


def merge_two_trees(tree_pair1: (nx.Graph, int), tree_pair2: (nx.Graph, int), path: list, main_graph: nx.Graph) -> (
        nx.Graph, int):
    """
    Merge the given two trees into one tree by using the given path between the two trees. The merged tree is returned.
    Note that the nodes of the two trees are contracted into one node in the main_graph. This is done to facilitate
    calculating the min cost paths between other trees in the future.

    :param tree_pair1: the first tree to merge, consisting of the tree graph and the terminal it represents
    :param tree_pair2: the second tree to merge, consisting of the tree graph and the terminal it represents
    :param path: the path from tree1 to tree2 through which the trees are to be merged
    :param main_graph: the underlying graph (containing both trees) is used to obtain node costs
    :return: the tree resulting when merging tree1 with tree2 via the given path, and the terminal it represents
    """
    costs = nx.get_node_attributes(main_graph, 'cost')
    tree1 = tree_pair1[0]
    tree2 = tree_pair2[0]
    # draw_trees_to_merge(tree1, tree2, path, main_graph)
    # first add the path to tree1
    prev_node = -1
    union_edge = None  # this is the edge that joins the connecting path with tree2
    for node in path:
        if tree2.has_node(node):
            union_edge = (prev_node, node)
            break  # the nodes of tree2 will be added when applying the union of the two trees
        if not tree1.has_node(node):
            tree1.add_node(node, cost=costs[node])
            if prev_node >= 0:
                if not tree1.has_edge(prev_node, node):
                    tree1.add_edge(prev_node, node)
                    # contract the newly added nodes in the tree
                    main_graph = nx.contracted_nodes(main_graph, prev_node, node, self_loops=False)
        prev_node = node
    # contract all nodes of tree2 in the main graph
    for node in tree2.nodes():
        main_graph = nx.contracted_nodes(main_graph, prev_node, node, self_loops=False)
        prev_node = node
    # join tree1 with tree2 (which should be disjoint, and connected with "union_edge")
    # draw_trees_to_merge(tree1, tree2, path, main_graph) # DEBUG
    merged_tree = nx.union(tree1, tree2)
    merged_tree.add_edge(union_edge[0], union_edge[1])
    # draw_merged_tree(merged_tree, main_graph) # DEBUG
    # associate the merged tree with the terminal of the first tree
    return merged_tree, tree_pair1[1]


def connect_closest_two_trees(trees: list, main_graph: nx.graph) -> list:
    """
    Connects the two closest trees in the given tree list, and replaces the connected trees in the list with the new
    merged tree.

    :param trees: list of trees, where each element is a pair of the tree graph and the terminal it represents
    :param main_graph: the underlying graph that is used to calculate the minimal node-cost path
    :return: the updated list of trees where the connected trees are replaced by the connected tree representing them
    """
    # FIXME: improve performance by only computing paths to "new" trees
    min_cost = float("inf")
    min_cost_path = []
    best_tree_pair = None
    nb_trees = len(trees)
    for i in range(0, nb_trees - 2):
        for j in range(i + 1, nb_trees - 1):
            path, cost = calculate_min_cost_path(trees[i][1], trees[j][1], main_graph)
            if cost < min_cost:
                min_cost = cost
                min_cost_path = path
                best_tree_pair = (i, j)
    index_tree1 = best_tree_pair[0]  # the indices of the two trees to be merged
    index_tree2 = best_tree_pair[1]
    new_tree = merge_two_trees(trees[index_tree1], trees[index_tree2], min_cost_path, main_graph)
    trees.remove(trees[index_tree2])  # first remove the higher indexed tree -> j > i
    trees.remove(trees[index_tree1])
    trees.append(new_tree)
    return trees


def connect_last_two_trees(tree_pair1: (nx.Graph, int), tree_pair2: (nx.Graph, int), main_graph: nx.Graph) -> nx.Graph:
    path, cost = calculate_min_cost_path(tree_pair1[1], tree_pair2[1], main_graph)
    return (merge_two_trees(tree_pair1, tree_pair2, path, main_graph))[0]


def generate_approx_steiner_tree(trees: list, main_graph: nx.Graph) -> nx.Graph:
    """
    Greedily connects the closest terminals by combining them into trees, forming a minimal Steiner tree approximation.

    :param trees: the list of terminals, each represented as a tree graph
    :param main_graph: the underlying graph used to calculate the min node cost path
    :return: the approximate minimal Steiner tree that connects all terminals
    """
    while len(trees) > 2:
        trees = connect_closest_two_trees(trees, main_graph)
    return connect_last_two_trees(trees[0], trees[1], main_graph)


def calculate_steiner_tree_costs(steiner_tree: nx.Graph, main_graph: nx.Graph) -> int:
    costs = nx.get_node_attributes(main_graph, 'cost')
    cost = 0
    for node in list(steiner_tree.nodes()):
        cost = cost + costs[node]
    return cost


def approximate_steiner_tree(graph: nx.Graph, terminals: list, seed: int) -> (nx.Graph, int):
    """
    Returns an approximate node-weighted minimal Steiner tree using a greedy heuristic.

    :param graph: the underlying graph with weighted nodes with "cost" label
    :param terminals: the terminals of the Steiner tree, which must be nodes in the given graph
    :param seed: random number generator seed
    :return: the graph representing the Steiner tree and its node cost
    """
    trees = initialise_trees(terminals)
    graph_copy = copy_and_initialise_main_graph(graph,
                                                terminals)  # we will modify the copied graph
    random.seed(seed)
    steiner_tree = generate_approx_steiner_tree(trees, graph_copy)
    cost = calculate_steiner_tree_costs(steiner_tree, graph)
    print("Calculated approximated minimal node-weighted steiner tree with cost: " + str(cost))
    # draw_steiner_tree_in_graph(graph, steiner_tree) # DEBUG
    return steiner_tree, cost
