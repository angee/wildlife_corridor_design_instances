# ----------------------------------------------------------------------------------------------------------------------
# Minimum node-cost path calculation.
#
# Implementation for finding the minimal node-cost path from a source to a target node
# on an undirected graph.
#
# The implementation creates the respective line graph (where nodes are converted into
# edges) and calculates the shortest path on the line graph and converts the result for
# the original graph.
#
# This file is part of the wildlife_corridor_design_instances repository which is released under the MIT license.
# See file at https://github.com/angee/wildlife_corridor_design_instances/blob/master/LICENSE for full license details.
#
# Author: Andrea Rendl-Pitrey, Satalia, October 2020
# ----------------------------------------------------------------------------------------------------------------------

import networkx as nx


def adjust_line_graph(source_node: int, target_node: int, line_graph: nx.Graph, original_graph: nx.Graph) -> (
        nx.Graph, int, int):
    """
    Adjust the line graph so that we can apply the shortest path algorithm on it that would represent the min cost
    algorithm wrt node costs. This means we perform the following steps: First, we need to set the edge weights by
    applying the cost of the respective node each edge represents. Second, we contract all the terminals in the
    line graph into one node to simplify calculating the shortest path. Finally, we return the adjusted line graph and
    the source and target nodes to calculate the shortest path.

    :param source_node: the source node from the main graph from which we want to compute the min cost path to the target
    :param target_node: the target node from the main graph
    :param line_graph: the line graph obtained by NetworkX for the main graph
    :param original_graph: the original graph that the line graph represents
    :return: the adjusted line graph and the source and target node in the line graph for the shortest path computation
    """
    # set the costs on the edges of the line graph to the cost of the node that appears in both adjacent nodes
    node_costs = nx.get_node_attributes(original_graph, 'cost')
    for edge in list(line_graph.edges()):
        # the edge connects two nodes: (n1, n2) <--> (n3, n4), where (n1, n2) is node_a, and (n3,n4) is node_b, and
        # n1, n2, n3, n4 are nodes in the original graph, and 2 nodes of n1, n2, n3, n4 are the same. We set the edge
        # weight as the cost of the node that appears twice in n1, n2, n3, n4.
        node_a = edge[0]
        node_b = edge[1]
        if node_a[0] == node_b[0] or node_a[0] == node_b[1]:
            node_appearing_twice = node_a[0]
        else:
            node_appearing_twice = node_a[1]
        line_graph[node_a][node_b]["cost"] = node_costs[node_appearing_twice]
        line_graph[node_b][node_a]["cost"] = node_costs[node_appearing_twice]

    # contract the nodes for the source and target terminal
    source_nodes = []
    target_nodes = []
    # find all nodes that are associated with the source or target nodes
    for node in list(line_graph.nodes()):
        if node[0] == source_node or node[1] == source_node:
            source_nodes.append(node)
        elif node[0] == target_node or node[1] == target_node:
            target_nodes.append(node)

    # pick the first terminal-1 node as source node and contract all other nodes to it
    source = source_nodes[0]
    # TODO: check if contracting makes sense
    # if len(source_nodes) > 1:
    #     for i in range(1, len(source_nodes) - 1):
    #         line_graph = nx.contracted_nodes(line_graph, source, source_nodes[i])
    # pick the first terminal-2 node as target node and contract all other nodes to it
    target = target_nodes[0]
    # if len(target_nodes) > 1:
    #     for i in range(1, len(target_nodes) - 1):
    #         line_graph = nx.contracted_nodes(line_graph, target, target_nodes[i])

    return line_graph, source, target


def calculate_path_cost_on_line_graph(path: list, line_graph: nx.Graph) -> int:
    edge_costs = nx.get_edge_attributes(line_graph, 'cost')
    cost = 0
    for i in range(0, len(path) - 1):
        if (path[i], path[i + 1]) in edge_costs.keys():
            cost = cost + edge_costs[(path[i], path[i + 1])]
        else:
            cost = cost + edge_costs[(path[i + 1], path[i])]
    return cost


def convert_line_graph_path(path: list) -> list:
    """
    Converts the given shortest path for the line graph into the min cost path in the original path. In principle, this
    means extracting the nodes in the right order from the given line graph path. The given line-graph path looks like:
    (n1, n2), (n3, n4) ... (ni, ni+1) where each (ni,nj) is a node in the line graph, and each ni is a node in the
    original graph. The nodes in (ni, nj) are ordered so that ni < nj. So we need to determine the "right order" to
    extract the path, by determining the nodes that are the same.

    Example:
    line graph path: (10, 11), (9, 10), (8, 9), (8, 14) represents the path: 11 -> 10 -> 9 -> 8 -> 14,
    This means the interpretation of line graph path is: (11, 10), (10, 9), (9, 8), (8, 14)
    and the returned path: (11, 10, 9, 8, 14)
    :param path: the shortest path on the line graph
    :return: the equivalent min cost path on the original graph
    """
    # finding the source and target node from the first path element
    node_a = path[0][0]
    node_b = path[0][1]
    if node_a == path[1][0] or node_a == path[1][1]:
        node_source = node_b
        node_target = node_a
    else:
        node_source = node_a
        node_target = node_b
    converted_path = [node_source]
    node_source = node_target

    # iterate over path, adding the next node ni
    for i in range(1, len(path)):
        node_a = path[i][0]
        node_b = path[i][1]
        if node_a == node_source:
            node_target = node_b
        else:
            node_target = node_a
        converted_path.append(node_source)
        node_source = node_target
    converted_path.append(node_source)  # add the last node

    return converted_path


def calculate_min_cost_path(source_node: int, target_node: int, graph: nx.Graph) -> (list, int):
    """
    Calculates the minimal cost path with respect to node-weights from terminal1 to terminal2 on the given graph by
    converting the graph into a line graph (converting nodes to edges) and solving the respective shortest path problem
    on the edges.

    :param source_node: the source node from the given graph from which to calculate the min cost path to the target
    :param target_node: the target node from the given graph
    :param graph: the graph on which we want to find the min cost path from source to target with respect to
    the node weights that are labelled with 'cost'
    :return: the min cost path from source to target, and the cost of the path, with respect to the node costs
    """
    line_graph = nx.line_graph(graph)
    line_graph, source, target = adjust_line_graph(source_node, target_node, line_graph, graph)
    path = nx.shortest_path(line_graph, source, target, weight="cost")
    cost = calculate_path_cost_on_line_graph(path, line_graph)
    path = convert_line_graph_path(path)
    return path, cost
