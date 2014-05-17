#=============================================================================
# this is the main file importing all other files and classes and executing all of it
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


def setup_sending_flooding(graph, iteration, FLAG):
    """Perfrom the sending process according to pure flooding

    Iterates through all nodes in the graph.
    The sending part and message-updating part are split.
    -> a message is not rebroadcasted mulitpletimes in the same iteration

    Arguments:
    graph -- a graph with node instances as vertices
    iteration -- number of iteration done during the sending
    FLAG -- string which indicates the broadcast algorithm

    Return-type:
    none"""
    # initate all nodes with a datapacket
    for node in graph.nodes():
        node.init_1_data()
    # loop through all nodes and their neighbours and push data from
    # its own sending_buffer to its neighbour's receive_buffer
    for i in range(iteration):
        for node in graph.nodes():
            # check if node rebroadcasts any messages
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
    """Perform the sending process according to the SBA

    Iterates through all nodes in the graph.
    The sending part and message-updating part are split.
    -> a message is not rebroadcasted mulitpletimes in the same iteration
    Message-updating:
    - Check vertex-message pairs with an active random timer
    - After sending check the receive-buffer for unknown messages

    Arguments:
    graph -- a graph with node instances as vertices
    iteration -- number of iteration done during the sending
    FLAG -- string which indicates the broadcast algorithm

    Return-type:
    none"""
    # initiate all nodes with a data packet
    for node in graph.nodes():
        node.init_1_data()
    # update each packet_dict, containing all the packets
    # that currently have an active random timer
    for i in range(iteration):
        for node in graph.nodes():
            sba.update_packet_dict(node, i, graph)

        # forward packet in the sending list to neighbors
        for node in graph.nodes():
            # check if node rebroadcasts any messages
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
    """Perfrom the sending process according to the AHBP

    Iterates through all nodes in the graph.
    The sending part and message-updating part are split.
    -> a message is not rebroadcasted mulitpletimes in the same iteration
    Message-updating:Check the receive-buffer and if needed build the BRG-set

    Arguments:
    graph -- a graph with node instances as vertices
    iteration -- number of iteration done during the sending

    Return-type:
    none"""
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
            ahbp.check_receive_buffer(node, i)
            node.del_receive_buffer()

            # for all messages in the sending_buffer build the BRG-Set
            for message in node.sending_buffer:
                ahbp.build_BRG(node, message)

        # rebroadcast the messages in the sending_buffer to the neighbors
        for node in graph.nodes_iter():
            #print node.sending_buffer
            # check if node rebroadcasts any messages
            for neigh in node.two_hop_dict:
                node.send_to_neighbor(neigh)
            node.del_sending_buffer()


def setup_graph(laplacian, iteration=0):
    """Create a graph object with Node-instances according to the laplacian

    Arguments:
    laplacian -- numpy.array with the laplacian matrix of the graph
    iteration -- number of iteration for the sending-history (default = 0)

    Return-type:
    my_graph -- networkx Graph object
    """
    # this block adds the nodes to the graph and creates two dict
    # in order to label the graph correctly
    size = len(laplacian[0, :])
    my_graph = nx.Graph()
    for i in range(size):
        # depending on the mode add the arguments in the node initiator
        my_graph.add_node(nde.Node(), name=str(i + 1), color='blue')
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


def create_figure(graph):
    """ calls other functions to create the plots"""
    Graph.iteration_plots(graph)

    # # creates all the animated plots for the nodes
    # size = len(graph.nodes())
    # for i in range(size):
    #     fig = plt.figure()
    #     Graph.bar_plot(graph, i + 1, fig)

    print 'check plot generating'


def set_sender_false(graph):
    """Set all sender flags in the graph to False"""
    for node in graph.nodes_iter():
        node.sender = False


def get_num_sender(graph):
    """Iterate through graph and count true sender flags"""
    rebroadcaster = 0
    for node in graph.nodes_iter():
        if node.sender:
            rebroadcaster += 1
    return rebroadcaster


def average_degree(graph):
    """Compute the average degree of all the vertices in the graph"""
    av_deg = 0
    for node in graph.nodes_iter():
        av_deg += graph.degree(node)
    av_deg /= float(len(graph))
    return av_deg


def clear_graph_data(graph):
    """Clear all the messages in the Node isntances"""
    for node in graph:
        node.del_sending_buffer()
        node.del_receive_buffer()
        node.del_data_stack()


def random_graph(num_nodes):
    # planar_bool = False
    # conn_bool = False
    # while not planar_bool or not conn_bool:
    #     graph_bool = False
    #     # generate a graphically meaningful degree sequence
    #     while not graph_bool:
    #         degree_lst = [random.randint(1,6) for i in range(num_nodes)]
    #         graph_bool = nx.is_graphical(degree_lst)
    #     gene_bool = False
    #     # Use try here because sometimes an the graph can not be generated within 10 tries
    #     # so try as long as it works
    #     while not gene_bool:
    #         try:
    #             graph = nx.random_degree_sequence_graph(degree_lst, tries=1000)
    #             gene_bool = True
    #         finally:
    #             pass
    #     graph.remove_edges_from(graph.selfloop_edges())
    #     planar_bool = planarity.is_planar(graph)
    #     for node in graph:
    #         if nx.clustering(graph, node) != 1 and graph.degree(node) > 1:
    #             planar_bool = False
    #     conn_bool = nx.is_connected(graph)
    # matrix = nx.laplacian_matrix(graph)
    # # getA() changes the type from matrix to array
    # array = matrix.getA()
    laplacian_array = build_rand_graph(num_nodes)
    rand_graph = setup_graph(laplacian_array, num_nodes-1)
    return rand_graph, laplacian_array


def build_line_laplacian(size):
    """Build laplacian of line-graph and return it as numpy.array"""
    my_ar = np.eye(size)
    for i in range(1, size-1):
        my_ar[i, i] += 1
        my_ar[i-1, i] = -1
        my_ar[i+1, i] = -1
        my_ar[i, i-1] = -1
        my_ar[i, i+1] = -1
    return my_ar


def test_rebroadcasting():
    y_flood = []
    y_ahbp = []
    y_sba = []
    x_lst = [i for i in xrange(2, 10)]
    for i in x_lst:
        laplacian = build_line_laplacian(i)
        graph = setup_graph(laplacian)
        # get values for flooding
        setup_sending_flooding(graph, i-1, 'flooding')
        flood_rebroadcast = get_num_sender(graph)
        # set all the sender flags to false again
        # so one can reuse the same graph
        set_sender_false(graph)
        clear_graph_data(graph)
        # get values for ahbp
        setup_sending_AHBP(graph, i-1)
        ahbp_rebroadcast = get_num_sender(graph)

        set_sender_false(graph)
        clear_graph_data(graph)

        setup_sending_SBA(graph, i-1, 'SBA')
        sba_rebroadcast = get_num_sender(graph)
        set_sender_false(graph)
        clear_graph_data(graph)

        y_flood.append(flood_rebroadcast)
        y_ahbp.append(ahbp_rebroadcast)
        y_sba.append(sba_rebroadcast)

    fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
    ax1.plot(x_lst, y_flood)
    ax1.set_title('pure flooding')

    ax2.plot(x_lst, y_ahbp)
    ax2.set_title('ad-hoc broadcast protocol')

    ax3.plot(x_lst, y_sba)
    ax3.set_title('scalabe broadcast algorithm')

    plt.show()


def sender_plot():  # TODO add some other plots in this function
    """Plot the number of rebroadcasting nodes in the network

    Generate for every graph size a certain number of random graphs
    and perform the sending process in order to gather the number of
    rebroadcasting nodes. For SBA gather 3-times more data
    since it has a random timer.
    Then plot the average and a boxplot for each graph size

    function parameters:
    max_nodes -- up to which network size data should gathered
    samples -- number of samples per graph size

    Return-type:
    Stores the plots as png.
    """
    max_nodes = 10
    samples = 10
    x_lst = [i for i in xrange(2, max_nodes)]
    y_flood = np.zeros((samples, max_nodes-2))
    y_ahbp = np.zeros((samples, max_nodes-2))
    y_sba = np.zeros((3*samples, max_nodes-2))
    y_flood_mean = []
    y_ahbp_mean = []
    y_sba_mean = []
    y_deg_flood_ahbp = []
    y_deg_sba = []
    y_connectivity_flood_ahbp = []
    y_conectitvity_sba = []
    for i in x_lst:
        print i
        flood_rebroadcast = 0
        sba_rebroadcast = 0
        ahbp_rebroadcast = 0
        flood_ahbp_deg = 0
        sba_deg = 0
        # get the average of rebbroadcasting nodes over three different graph
        # because the degree_lst may vary quite a lot
        for a in range(samples):
            # build random graph
            rand_graph, laplacian = random_graph(i)

            val, vec = np.linalg.eig(laplacian)
            val.sort()
            y_connectivity_flood_ahbp.append(val[1])
            y_conectitvity_sba.append(val[1])
            # nx.draw(rand_graph, with_labels=False)
            # plt.show()
            flood_ahbp_deg += average_degree(rand_graph)
            sba_deg += average_degree(rand_graph)
            # get values for flooding
            setup_sending_flooding(rand_graph, i-1, 'flooding')
            y_flood[a, i-2] = get_num_sender(rand_graph)
            flood_rebroadcast += get_num_sender(rand_graph)
            # set all the sender flags to false again
            # so one can reuse the same graph
            set_sender_false(rand_graph)
            clear_graph_data(rand_graph)
            # get values for ahbp
            setup_sending_AHBP(rand_graph, i-1)
            y_ahbp[a, i-2] = get_num_sender(rand_graph)
            ahbp_rebroadcast += get_num_sender(rand_graph)

            set_sender_false(rand_graph)
            clear_graph_data(rand_graph)

            setup_sending_SBA(rand_graph, i-1, 'SBA')
            y_sba[a, i-2] = get_num_sender(rand_graph)
            sba_rebroadcast += get_num_sender(rand_graph)

            set_sender_false(rand_graph)
            clear_graph_data(rand_graph)
            # since SBA has a random timer get some more samples for an accurate result
            for b in range(2):
                rand_graph, laplacian = random_graph(i)

                val, vec = np.linalg.eig(laplacian)
                val.sort()
                y_conectitvity_sba.append(val[1])

                sba_deg += average_degree(rand_graph)
                setup_sending_SBA(rand_graph, i-1, 'SBA')
                y_sba[a*3 + b + 1, i-2] = get_num_sender(rand_graph)
                sba_rebroadcast += get_num_sender(rand_graph)

        y_flood_mean.append(flood_rebroadcast/float(samples))
        y_ahbp_mean.append(ahbp_rebroadcast/float(samples))
        y_sba_mean.append(sba_rebroadcast/float(3*samples))

        y_deg_flood_ahbp.append(flood_ahbp_deg/float(samples))
        y_deg_sba.append(sba_deg/float(3*samples))
    print np.std(y_flood, axis=1)
    print y_ahbp
    print y_sba
    print y_flood_mean
    print y_ahbp_mean
    print y_sba_mean

    # fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
    # # ax1.errorbar(x_lst, y_flood_mean, y_flood, ecolor='red')
    # ax1.plot(x_lst, y_flood_mean, y_ahbp_mean, y_sba_mean)
    # # ax1.boxplot(y_flood)
    # ax1.set_title('pure flooding')
    #
    # # ax2.boxplot(y_ahbp)
    # # ax1.plot(x_lst, y_ahbp_mean, color='red')
    # # ax2.errorbar(x_lst, y_ahbp_mean, y_ahbp, ecolor='red')
    # ax2.set_title('ad-hoc broadcast protocol')
    #
    # # ax3.errorbar(x_lst, y_sba_mean, y_sba, ecolor='red')
    # # ax3.boxplot(y_sba)
    # # ax1.plot(x_lst, y_sba_mean, color='green')
    # ax3.set_title('scalabe broadcast algorithm')
    # x_pos = [i for i in range(1, x_lst[-1]+1)]
    # # plt.xticks(x_pos, x_lst)
    # # plt.ylim(0, x_lst[-1])
    fig = plt.figure(1)
    plt.plot(x_lst, y_flood_mean, label='flood')
    plt.plot(x_lst, y_ahbp_mean, color='red', label='ahbp')
    plt.plot(x_lst, y_sba_mean, color='green', label='sba')
    plt.legend()
    fig2, (axi1, axi2) = plt.subplots(2, sharex=True, sharey=True)
    axi1.plot(x_lst, y_deg_flood_ahbp)
    axi1.set_title('average degree for flooding and ahbp')

    axi2.plot(x_lst, y_deg_sba)
    axi2.set_title('average degree for sba graphs')

    plt.show()

    fig.savefig('sender_plots.png')
    fig2.savefig('degree_plots.png')


def lattice_graph(length):
    """Build a hexagonally gridded graph of a square shaped form

    The grid has a squared shape of size = length.
    First create a square grid graph then add edges on the diagonals.

    Arguments:
    length -- integer determining the size of the square

    Return-type:
    graph -- networkx.Graph object
    """
    # builds a square grid graph
    graph = nx.grid_2d_graph(length, length)
    # in each square add an edge on the diagonal -> hexagonal shape
    # add edges to seperate list, cuz cannot modifiy the graph during iteration
    edge_lst = []
    for n in graph:
        x, y = n
        if y > 0 and x < length-1:
            edge_lst.append((n, (x+1, y-1)))
    graph.add_edges_from(edge_lst)
    return graph


def build_rand_graph(num_nodes):
    """Build the DFA-like random graph

    First build a hexagonally gridded graph -> call 'lattice_graph()'
    Then delete random nodes till num_nodes nodes remain.
    If deleting a node results in cutting the graph into mutliple components
    check if one of the subgraphs has still enough vertices.
    Continue computation with this subgraph.
    Else delete another vertex.
    Return the laplacian representation of the graph

    Arguments:
    num_nodes -- number of nodes the resulting graph should have

    Return-type:
    laplacian-matrix -- numpy array
    """
    # root = math.sqrt(num_nodes)
    # length = int(math.ceil(root))
    graph = lattice_graph(num_nodes)
    for node_name in graph.node:
        graph.node[node_name]['color'] = 'red'
    pos = nx.spring_layout(graph)
    while len(graph) > num_nodes:
        # as long as the graph is not connect
        # after removing a node try another one
        connect_bool = False
        while not connect_bool:
            node_index = random.randint(0, len(graph)-1)
            removed_node = graph.nodes()[node_index]
            removed_edges = graph.edges(removed_node)
            # graph.node[removed_node]['color'] = 'blue'
            # colors = []
            # for node_name in graph.node:
            #     colors.append(graph.node[node_name]['color'])
            # nx.draw(graph,pos, node_color=colors)
            # plt.show()
            graph.remove_node(removed_node)
            # check if graph is still connected
            connect_bool = nx.is_connected(graph)
            if not connect_bool:
                sub_graphs_worked = False
                sub_graphs = nx.connected_component_subgraphs(graph)
                for sub in sub_graphs:
                    if len(sub) >= num_nodes:
                        sub_graphs_worked = True
                        break
                if sub_graphs_worked:
                    # for node_name in sub:
                    #     graph.node[node_name]['color'] = 'blue'
                    # colors = []
                    # for node_name in graph.node:
                    #     colors.append(graph.node[node_name]['color'])
                    # nx.draw(graph,pos, node_color=colors)
                    # plt.show()
                    graph = sub
                    connect_bool = True
                    # for node_name in graph.node:
                    #     graph.node[node_name]['color'] = 'red'

            # if graph is not connected anymore put removed node back
                else:
                    graph.add_node(removed_node)  # , color = 'red')
                    graph.add_edges_from(removed_edges)

    # nx.draw(graph)
    # plt.show()

    laplacian_matrix = nx.laplacian_matrix(graph)
    return laplacian_matrix.getA()

ITERATION = 10
FLAG = ""
HELLO_INTERVAL = 3
ALLOWED_HELLO_LOSS = 1


def main():
    """main function which performs the whole retransmission"""
    # test_rebroadcasting()
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
    # graph_matrix = np.array([[ 6, -1, -1, -1, -1, -1, -1],
    #                          [-1,  3, -1,  0,  0,  0, -1],
    #                          [-1, -1,  3, -1,  0,  0,  0],
    #                          [-1,  0, -1,  3, -1,  0,  0],
    #                          [-1,  0,  0, -1,  3, -1,  0],
    #                          [-1,  0,  0,  0, -1,  3, -1],
    #                          [-1, -1,  0,  0,  0, -1, 3]])

    # my_graph = setup_graph(graph_matrix, ITERATION)
    # print nx.laplacian_matrix(my_graph)
    # print nx.clustering(my_graph)
    # build_rand_graph(5)
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
