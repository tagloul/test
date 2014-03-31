#=============================================================================
# this is the main file importing all other classes and executing all of it
#=============================================================================


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import Graph
import NodeClass as nde
import SBAClass as sbac


def setup_sending_flooding(graph, iteration):
    """method which handles sending messages in the network,
    only call it once for sending sweet packages in a network"""
    for node in graph.nodes():
        node.init_1_data()
    # loop through all nodes and their neighbours and push data from
    # its own sending_buffer to its neighbour's receive_buffer
    for i in range(iteration):
        for node in graph.nodes():
            for neigh in graph.neighbors_iter(node):
                node.send_to_neighbor(neigh)
        # before updating the sending_buffer delete already sent data
        # after update del receive_buffer not to check already known data twice
        for node in graph.nodes():
            node.del_sending_buffer()
            node.update_data(i + 1)
            node.del_receive_buffer()
        print(i + 1, "th step")
        Graph.print_all_data_stacks(graph)
    for node in graph.nodes():
        for item in node.data_stack:
            item.print_package()
        print(node.packet_history)
        print('\n')
        print(node.packet_history)
    create_figure(graph)


def setup_sending_SBA(graph, iteration):
    """"performs the sending process for nodes with the
    scalable broadcast algorithm"""
    for node in graph.nodes():
        node.init_1_data()
    for i in range(iteration):
        print('ITERATION :', i)
        print()
        for node in graph.nodes():
            node.update_packet_dict(i, graph)
            #print('node_'+str(node.ID+1))
            #for packet in node.receive_buffer:
            #    node.check_receive_buffer(packet, i, graph)
            for neigh in graph.neighbors_iter(node):
                node.send_to_neighbor(neigh)
        for node in graph.nodes():
            print('node_'+str(node.ID+1))
            for packet in node.receive_buffer:
                node.check_receive_buffer(packet, i, graph)
        # before updating the sending_buffer delete already sent data
        # after update del receive_buffer not to check already known data twice
        for node in graph.nodes():
            print('node_'+str(node.ID+1))
            print(node.packet_dict)
            print('data_stack')
            for item in node.data_stack:
                item.print_package()
            print('sending_buffer')
            for item in node.sending_buffer:
                item.print_package()
            node.del_sending_buffer()
            node.update_data(i + 1)
            print('receive_buffer')
            for item in node.receive_buffer:
                item.print_package()
            node.del_receive_buffer()
    for node in graph.nodes():
        print('node_'+str(node.ID+1))
        for item in node.data_stack:
            item.print_package()
        print(node.packet_history)
        print('\n')
    create_figure(graph)


def setup_graph(laplacian, iteration):
    """ this function creates a graph object with the nodes and its edges
    already correct initialized"""
    # this block adds the nodes to the graph and creates two dict
    # in order to label the graph correctly
    size = len(laplacian[0, :])
    my_graph = nx.Graph()
    for i in range(size):
        #my_graph.add_node(sbac.SBA(size, iteration, my_graph), name=str(i + 1))
        my_graph.add_node(nde.Node(size, iteration), name=str(i + 1))
    print(my_graph.nodes())
    # stores the nodes and their name attributes in a dictionary
    nodes_names = nx.get_node_attributes(my_graph, "name")
    # switches key and values--> thus names_nodes
    names_nodes = dict(zip(nodes_names.values(), nodes_names.keys()))

    # this block adds the edges between the nodes
    for i in range(0, size):
        for j in range(i + 1, size):
            if laplacian[i, j] == -1:
                node_1 = names_nodes[str(i + 1)]
                node_2 = names_nodes[str(j + 1)]
                my_graph.add_edge(node_1, node_2)

    print(my_graph.edges())

    return my_graph


def create_figure(graph):
    """print the two graphs in one window"""
    Graph.print_graph(graph)
    Graph.iteration_plots(graph)

    # creates all the animated plots for the nodes
    size = len(graph.nodes())
    for i in range(size):
        fig = plt.figure()
        Graph.bar_plot(graph, i + 1, fig)


ITERATION = 5


def main():
    """main function which performs the whole retransmission"""
    graph_matrix = np.array([[ 2, -1,  0,  0, -1,  0],
                             [-1,  3, -1,  0, -1,  0],
                             [ 0, -1,  2, -1,  0,  0],
                             [ 0,  0, -1,  3, -1, -1],
                             [-1, -1,  0, -1,  3,  0],
                             [ 0,  0,  0, -1,  0,  1]])
    my_graph = setup_graph(graph_matrix, ITERATION)
    setup_sending_flooding(my_graph, ITERATION)


if __name__ == '__main__':
    main()
