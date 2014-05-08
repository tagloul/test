#=============================================================================
# this is the main file importing all other classes and executing all of it
#=============================================================================
# hello world!
import networkx as nx
import matplotlib.pyplot as plt
import Graph
import NodeClass as nde
import SBAClass as sba
import AHBPClass as ahbp
import random
import numpy as np
import itertools as it
from networkx.algorithms import bipartite
import planarity
import Package as pkt


# TODO still have to figure  out whx i cant write the sendingbuffer to the file
def write_lst_to_file(filename, node, iter_num, data_str):
    """arguments: filename of the designed file, the node to be handled,
    data_str -> which data-structure is going to be written to the file
    iter_num = the actual iteration as integer. """
    with open(filename + '.txt', 'a') as outfile:
        if data_str == "receive_buffer":
            outfile.write("receive_buffer:\n")
            for message in node.receive_buffer:
                outfile.write(message.return_str())
                #message.print_package()
            outfile.write("\n")
            outfile.flush()
        elif data_str == "sending_buffer":
            outfile.write("sending_buffer\n")
            for message in node.sending_buffer:
                #message.print_package()
                outfile.write(message.return_str())
            outfile.write("\n")
            outfile.flush()
        elif data_str == "data_stack":
            outfile.write("data_stack\n")
            for message in node.data_stack:
                outfile.write(message.return_str())
                #message.print_package()
            outfile.write("\n")
            outfile.flush()
        # outfile.write("\n")
        outfile.close()

def setup_sending_flooding(graph, iteration, FLAG):
    """method which handles sending messages in the network,
    only call it once for sending sweet packages in a network"""
    # initate all nodes with a datapacket
    for node in graph.nodes():
        node.init_1_data()
    # loop through all nodes and their neighbours and push data from
    # its own sending_buffer to its neighbour's receive_buffer
    for i in range(iteration):
        for node in graph.nodes():
            # check if node rebroadcasts any messages
            node.check_rebroadcast(i)
            for neigh in graph.neighbors_iter(node):
                node.send_to_neighbor(neigh)
        # before updating the sending_buffer delete already sent data
        # after update del receive_buffer not to check already known data twice
        for node in graph.nodes():
            node.del_sending_buffer()
            node.update_data(i + 1, FLAG)
            node.del_receive_buffer()
        #Graph.print_all_data_stacks(graph)


def setup_sending_SBA(graph, iteration, FLAG):
    """"performs the sending process for nodes with the
    scalable broadcast algorithm"""
    # initiate all nodes with a data packet
    for node in graph.nodes():
        node.init_1_data()
    # update each packet dict, containing all the packets that currently
    # have an active random timer
    for i in range(iteration):
        for node in graph.nodes():
            sba.update_packet_dict(node, i, graph)


        # forward packet in the sending list to neighbors
        for node in graph.nodes():
            # check if node rebroadcasts any messages
            node.check_rebroadcast(i)
            for neigh in graph.neighbors_iter(node):
                node.send_to_neighbor(neigh)

        # checks incoming packets if they are already known and adds
        # them if necessary to the packet dict and activates a timer
        for node in graph.nodes():
            for packet in node.receive_buffer:
                sba.check_receive_buffer(node, packet, i, graph)
        # before updating the sending_buffer delete already sent data
        # after update del receive_buffer not to check already known data twice
        for node in graph.nodes():
            node.del_sending_buffer()
            node.update_data(i + 1, FLAG)
            node.del_receive_buffer()


def setup_sending_AHBP(graph, iteration):
    """method to setup the sending process in the network
    with the AHBP"""
    # initiate the nodes with a data packet
    for node in graph.nodes_iter():
        node.init_1_data()
        # only use this until hello protocol is implemented
        # this gets the 2-hop neighbor hood form the 'master'-graph
        ahbp.build_2_hop(node, graph)
        # with open("node_" + str(node.ID + 1) + '.txt', 'w') as outfile:
        #     outfile.write("new file for node :" + str(node.ID + 1) + "\n")

    for i in range(iteration):
        # split up the process of checking the receive_buffer
        # and sending to neighbor, such that can only traverse
        # one edge during an iteration step
        for node in graph.nodes():
            # with open("node_" + str(node.ID + 1) + '.txt', 'a') as outfile:
            #     outfile.write(str(i) + "th iteration\n")
            #     #print 'node_ID :', node.ID + 1, '\n'
            #     #print 'receive_buffer'
            #     write_lst_to_file("node_" + str(node.ID + 1), node, i, "receive_buffer")

            ahbp.check_receive_buffer(node, i)
            node.del_receive_buffer()

                # #print 'sending_buffer'
                # write_lst_to_file("node_" + str(node.ID + 1), node, i, "sending_buffer")
                # #print 'data_stack'
                # write_lst_to_file("node_" + str(node.ID + 1), node, i, "data_stack")

                # for all messages in the sending_buffer build the BRG-Set
            for message in node.sending_buffer:
                ahbp.build_BRG(node, message)

        # rebroadcast the messages in the sending_buffer to the neighbors
        for node in graph.nodes_iter():
            #print node.sending_buffer
            # check if node rebroadcasts any messages
            node.check_rebroadcast(i)
            for neigh in node.two_hop_dict:
                node.send_to_neighbor(neigh)
            node.del_sending_buffer()

def setup_graph(laplacian, iteration=0):
    """ this function creates a graph object with the nodes and its edges
    already correct initialized"""
    # this block adds the nodes to the graph and creates two dict
    # in order to label the graph correctly
    size = len(laplacian[0, :])
    my_graph = nx.Graph()
    for i in range(size):
        my_graph.add_node(nde.Node(size, iteration), name=str(i + 1))
        #my_graph.add_node(nde.Node(size, iteration), name=str(i + 1))
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

    return my_graph


# def send_HELLO(node, graph):
#     my_hello = pkt.Hello(node)
#     for neighbor in node.neigh_dict:
#         my_hello.neigh_lst.append(neighbor)
#     for neigh in graph.neighbors(node):
#         neigh.receive_buffer.append(my_hello)

#===============================================================================
# def check_one_hop_edges(node):
#     """this method will establish edges between one-hop neighbors,
#     if not both of them already know it"""
#     for one_hop in node.neigh_dict:
#         for other_one in node.neigh_dict:
#             if other_one != one_hop:
#                 if one_hop in node.neigh_dict[other_one] and other_one not in node.neigh_dict[one_hop]:
#                     node.neigh_dict[one_hop].append(other_one)
# 
# 
# #===============================================================================
# # def check_two_hop_edges(node):
# #      
# #===============================================================================
# 
# def hello_operation(graph):
#     for node in graph.nodes_iter():
#         for hello in node.receive_buffer:
#             node.neigh_dict[hello.sender] = hello.neigh_lst
#             check_one_hop_edges(node)
#         send_HELLO(node, graph)
#     for node in graph.nodes_iter():
#         
#===============================================================================


def create_figure(graph):
    """"""
    Graph.iteration_plots(graph)

    # # creates all the animated plots for the nodes
    # size = len(graph.nodes())
    # for i in range(size):
    #     fig = plt.figure()
    #     Graph.bar_plot(graph, i + 1, fig)

    print 'check plot generating'


def set_sender_false(graph):
    for node in graph.nodes_iter():
        node.sender = False


def get_num_sender(graph):
    rebroadcaster = 0
    for node in graph.nodes_iter():
        if node.sender:
            rebroadcaster += 1
    return rebroadcaster


def average_degree(graph):
    av_deg = 0
    for node in graph.nodes_iter():
        av_deg += graph.degree(node)
    av_deg = av_deg/float(len(graph))
    return av_deg


def clear_graph_data(graph):
    """clear all the messages in the nodes in order to reuse the graph for
    further simulations"""
    for node in graph:
        node.del_sending_buffer()
        node.del_receive_buffer()
        node.del_data_stack()


def is_planar(G):
    """
    function checks if graph G has K(5) or K(3,3) as minors,
    returns True /False on planarity and nodes of "bad_minor"
    """
    result = True
    bad_minor = []
    n = len(G.nodes())
    if n > 5:
        for subnodes in it.combinations(G.nodes(),6):
            sub_graph = G.subgraph(subnodes)
            if bipartite.is_bipartite(G):  # check if the graph G has a subgraph K(3,3)
                X, Y = bipartite.sets(G)
                if len(X) == 3:
                    result = False
                    bad_minor = subnodes
    if n > 4 and result:
        for subnodes in it.combinations(G.nodes(), 5):
            sub_graph = G.subgraph(subnodes)
            if len(sub_graph.edges()) == 10:  # check if the graph G has a subgraph K(5)
                result = False
                bad_minor = subnodes
    return result, bad_minor


def random_graph(num_nodes):
    planar_bool = False
    while not planar_bool:
        graph_bool = False
        # generate a graphically meaningful degree sequence
        while not graph_bool:
            degree_lst = [random.randint(1,6) for i in range(num_nodes)]
            graph_bool = nx.is_graphical(degree_lst)
        gene_bool = False
        # Use try here because sometimes an the graph can not be generated within 10 tries
        # so try as long as it works
        while not gene_bool:
            try:
                graph = nx.random_degree_sequence_graph(degree_lst, tries=1000)
                gene_bool = True
            finally:
                pass
        graph.remove_edges_from(graph.selfloop_edges())
        planar_bool = planarity.is_planar(graph)
    matrix = nx.laplacian_matrix(graph)
    # getA() changes the type from matrix to array
    array = matrix.getA()
    rand_graph = setup_graph(array, num_nodes-1)
    return rand_graph

def sender_plot():
    x_lst = [i for i in xrange(2, 31)]
    y_flood = []
    y_ahbp = []
    y_sba = []
    for i in x_lst:
        print i
        flood_rebroadcast = 0
        ahbp_rebroadcast = 0
        sba_rebroadcast = 0
        # get the average of rebbroadcasting nodes over three different graph
        # because the degree_lst may vary quite a lot
        # TODO think of a way on how to take into account the average degree of graphs
        for a in range(3):
            # build random graph
            rand_graph = random_graph(i)
            # get values for flooding
            setup_sending_flooding(rand_graph, i-1, 'flooding')
            flood_rebroadcast += get_num_sender(rand_graph)
            # set all the sender flags to false again
            # so one can reuse the same graph
            set_sender_false(rand_graph)
            clear_graph_data(rand_graph)

            # get values for ahbp
            setup_sending_AHBP(rand_graph, i-1)
            ahbp_rebroadcast += get_num_sender(rand_graph)

            set_sender_false(rand_graph)
            clear_graph_data(rand_graph)

            setup_sending_SBA(rand_graph, i-1, 'SBA')
            sba_rebroadcast += get_num_sender(rand_graph)
            set_sender_false(rand_graph)
            clear_graph_data(rand_graph)
            # since SBA has a random timer get some more samples for an accurate result
            for b in range(2):
                rand_graph = random_graph(i)
                setup_sending_SBA(rand_graph, i-1, 'SBA')
                sba_rebroadcast += get_num_sender(rand_graph)

        y_flood.append(flood_rebroadcast/3.0)
        y_ahbp.append(ahbp_rebroadcast/3.0)
        y_sba.append(sba_rebroadcast/9.0)

    fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
    ax1.plot(x_lst, y_flood)
    ax1.set_title('pure flooding')

    ax2.plot(x_lst, y_ahbp)
    ax2.set_title('ad-hoc broadcast protocol')

    ax3.plot(x_lst, y_sba)
    ax3.set_title('scalabe broadcast algorithm')

    plt.show(fig)

    fig.savefig('sender_plots.png')



ITERATION = 10
FLAG = ""
HELLO_INTERVAL = 3
ALLOWED_HELLO_LOSS = 1



def main():
    """main function which performs the whole retransmission"""
    sender_plot()
    # # laplacian matrix -> has the information about the network-topology
    # graph_matrix = np.array([[ 3, -1,  0, -1, -1,  0,  0,  0,  0,  0,  0,  0,  0],
    #                          [-1,  3, -1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    #                          [ 0, -1,  4, -1,  0,  0, -1, -1,  0,  0,  0,  0,  0],
    #                          [-1, -1, -1,  6, -1, -1, -1,  0,  0,  0,  0,  0,  0],
    #                          [-1,  0,  0, -1,  3, -1,  0,  0,  0,  0,  0,  0,  0],
    #                          [ 0,  0,  0, -1, -1,  5, -1,  0,  0, -1, -1,  0,  0],
    #                          [ 0,  0, -1, -1,  0, -1,  6, -1, -1, -1,  0,  0,  0],
    #                          [ 0,  0, -1,  0,  0,  0, -1,  3, -1,  0,  0,  0,  0],
    #                          [ 0,  0,  0,  0,  0,  0, -1, -1,  3, -1,  0,  0,  0],
    #                          [ 0,  0,  0,  0,  0, -1, -1,  0, -1,  5, -1,  0, -1],
    #                          [ 0,  0,  0,  0,  0, -1,  0,  0,  0, -1,  4, -1, -1],
    #                          [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0, -1,  1,  0],
    #                          [ 0,  0,  0,  0,  0,  0,  0,  0,  0, -1, -1,  0,  2]])


    #==========================================================================
    # graph_matrix = np.array([[ 2, -1,  0,  0, -1,  0],
    #                          [-1,  3, -1,  0, -1,  0],
    #                          [ 0, -1,  2, -1,  0,  0],
    #                          [ 0,  0, -1,  3, -1, -1],
    #                          [-1, -1,  0, -1,  3,  0],
    #                          [ 0,  0,  0, -1,  0,  1]])
    #==========================================================================

    # my_graph = setup_graph(graph_matrix, ITERATION)
    # Graph.print_graph(my_graph, 1)
    # while True:
    #     clear_graph_data(my_graph)
    #     print "Your options are as follows:\n\n"\
    #       "flooding ->\tPure Flooding in the Network\n"\
    #       "SBA ->\t\tScalable Broadcast Algorithm\n"\
    #       "AHBP ->\t\tAd-Hoc Broadcast Protocol\n"
    #     FLAG = raw_input("Enter your Flag. To quit press enter\n")
    #     if FLAG == "":
    #         print 'Application is now shutting down'
    #         break
    #     elif FLAG == "SBA":
    #         setup_sending_SBA(my_graph, ITERATION, FLAG)
    #         print get_num_sender(my_graph)
    #         set_sender_false(my_graph)
    #         print 'check SBA calculations'
    #     elif FLAG == "AHBP":
    #         setup_sending_AHBP(my_graph, ITERATION)
    #         print get_num_sender(my_graph)
    #         set_sender_false(my_graph)
    #         print 'check AHBP calculations'
    #     elif FLAG == "flooding":
    #         setup_sending_flooding(my_graph, ITERATION, FLAG)
    #         print get_num_sender(my_graph)
    #         set_sender_false(my_graph)
    #         print 'check flooding calculations'
    #     create_figure(my_graph)




if __name__ == '__main__':
    main()
