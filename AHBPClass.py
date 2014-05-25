"""
This file contains all functions related to the Ad-Hoc Broadcast Protocol.
Note that since it does not inherit from the Node Class, the considered node
is always passed as an argument -> calling_node
"""
import networkx as nx


def del_brg(message):
    """deletes the BRG-Set in a node"""
    message.brg = []


def build_2_hop_graph(calling_node):
    """Build a graph containing 2-hop-neighborhood of calling_node

    With the 2-hop-neighborhood as a dictionary in the calling_node
    build a graph of the neighborhood with Node instances.
    Need to take the same Node objects as the ones in the total graph,
    in order to be able to check for Node objects in the graph.

    Arguments:
    calling_node -- node whose neighborhood is desired

    Return-type:
    my_graph -- networkx.Graph object
    """
    my_graph = nx.Graph()
    my_graph.add_node(calling_node)
    for node in calling_node.two_hop_dict:
        my_graph.add_node(node)
        my_graph.add_nodes_from(calling_node.two_hop_dict[node])
    for node in calling_node.two_hop_dict:
        my_graph.add_edge(calling_node, node)
        for neigh in calling_node.two_hop_dict[node]:
            my_graph.add_edge(node, neigh)
        #print('check: built the graph')
        #self.print_graph_id(my_graph)
    return my_graph


def check_path_node(calling_node, del_lst, path_lst, node):
    bool_check = False
    bool_check = node.ID + 1 != path_lst[-1]
    if bool_check == True:
        bool_check = node not in del_lst
        if bool_check == True:
            bool_check = node != calling_node
            return bool_check
    return False


def remove_path_nodes(calling_node, graph, message):
    """Delete nodes and their neighbors of the message path from the graph

    Arguments:
    calling_node -- Currently treated node
    graph -- networkx.Graph containg the 2-hop-neighborhood of calling_node
    message -- Packet-instace currently treated

    Return-type:
    None
    """
    del_lst = []
    ID_lst = [node.ID + 1 for node in graph.nodes()]
    for node_id in ID_lst:
        if node_id in message.path[:-1]:
            index = ID_lst.index(node_id)
            node = graph.nodes()[index]
            del_lst.append(node)
            for neigh in graph.neighbors(node):
                bool_check = check_path_node(calling_node, del_lst, message.path, neigh)
                if bool_check == True:
                    del_lst.append(neigh)
                #==============================================================
                # for edge in graph.edges_iter():
                #     if node in edge:
                #         node_1, node_2 = edge
                #         if node_1 not in del_lst:
                #             del_lst.append(node_1)
                #         if node_2 not in del_lst:
                #             del_lst.append(node_2)
                #==============================================================
    graph.remove_nodes_from(del_lst)


def remove_edges(calling_node, graph):
    """Detect edges between 1-hop neighbors in the graph and delete them

    Arguments:
    calling_node -- currently treated node
    graph -- networkx.Graph containing the 2-hop-neighborhood of calling-node

    Return-type:
    None
    """
    edges_lst = []
    for edge in graph.edges_iter():
        n1, n2 = edge
        if (n1 in graph.neighbors(calling_node)) and (n2 in graph.neighbors(calling_node)):
            edges_lst.append(edge)

    graph.remove_edges_from(edges_lst)
        #print('check: removed edges')
        #self.print_graph_id(graph)


def remove_nodes(calling_node, graph):
    """Remove isolated nodes and 1-hop-neighbors with degree = 1

    Arguments:
    calling_node -- currently treated node
    graph -- networkx.Graph containing the 2-hop-neighborhood of calling-node

    Return-type:
    None
    """
    node_lst = []
        # nodes with degree = 0
    for node in graph.nodes():
        if graph.degree(node) == 0:
            node_lst.append(node)
        # 1-hop neighbors with degree = 1
    for node in graph.neighbors(calling_node):
        if graph.degree(node) == 1:
            node_lst.append(node)
    graph.remove_nodes_from(node_lst)
        #print('check: removed nodes')
        #print('removed nodes:')
        #print([node.ID for node in node_lst])
        #self.print_graph_id(graph)


def add_to_BRG(calling_node, graph, message):
    """Add suiting nodes to the BRG-set of a message.

    Add suiting nodes according to tha AHBP of the remaining ones to the BRG-set
    of the message and then remove them from the graph.

    Arguments:
    calling_node -- currently treated node
    graph -- networkx.Graph containing the 2-hop-neighborhood of calling-node
    message -- currently treated message of calling_node

    Return-type:
    None
    """
    if graph.nodes() == []:
        return None
    one_hop = graph.neighbors(calling_node)
    two_hop = []
    counter = 0
    added_node = 0
        #build the two-hop neighbor list
    for node in one_hop:
        for neigh in graph.neighbors(node):
            if neigh in two_hop == False and neigh != calling_node:
                two_hop.append(neigh)
        # look for nodes in the two-hop neighborhood with degree one
    for node in two_hop:
        if graph.degree(node) == 1:
            counter = 1
            added_node = graph.neighbors(node)[0]
        # if there was no node with degree one take the one with the
        # highest degree from the one-hop neighbors
    if counter == 0:
        if one_hop != []:
            added_node = one_hop[0]
        else:
            return None
        for i in range(1, len(one_hop)):
            if graph.degree(one_hop[i]) > graph.degree(added_node):
                added_node = one_hop[i]
    message.brg.append(added_node.ID)
    del_lst = []
    if added_node != 0:
        del_lst.append(added_node)
        for neigh in graph.neighbors(added_node):
            if neigh != calling_node:
                del_lst.append(neigh)
    graph.remove_nodes_from(del_lst)
        #print('check: added to BRG')
        #print('removed node:')
        #print([node.ID for node in del_lst])
        #self.print_graph_id(graph)


def build_BRG(calling_node, message):
    """Build the BRG-set of a message

    Delete path-nodes and their neighbors and edges between one-hop-neighbors.
    As long as there are nodes in the graph delete isolated nodes,
    1-hop neighbors with degree 1 and then add suiting nodes to the BRG-set

    Arguments:
    calling_node -- Node object ; currently treated node
    message -- Packet object ; currently treated message

    Return-type:
    None
    """
    #print('actual node:')
    #print(calling_node.ID + 1)

    my_graph = build_2_hop_graph(calling_node)
        #print(self)
    del_brg(message)
    remove_path_nodes(calling_node, my_graph, message)
    remove_edges(calling_node, my_graph)
        # as long as there are nodes in the graph update the BRG-Set
    while(len(my_graph.nodes()) > 0):
        remove_nodes(calling_node, my_graph)
        add_to_BRG(calling_node, my_graph, message)
            #print('remaining nodes:')
            #print(len(my_graph.nodes()))


def check_receive_buffer(calling_node, column):
    """Check the recieve-buffer for unknown messages and if oneself is in the BRG-set

    Arguments:
    calling_node -- Node object ; currently treated node

    Return-type:
    None
    """
    for message in calling_node.receive_buffer:
            # add unknown messages to the data-list
        bool_ds = calling_node.check_data_stack(message)  # m in self.data_stack
        if bool_ds == False:
            message.add_to_path(calling_node)
            calling_node.data_stack.append(message)
            # size = len(calling_node.packet_history)
            # values = [ [message.value] for i in range(size)]
            # calling_node.packet_history = np.concatenate(calling_node.packet_history, values, axis=1)
                # if oneself is in the BRG-Set add it to the sending-list
            if calling_node.ID in message.brg:
                # calling_node.sender = True
                calling_node.sending_buffer.append(message)


    # only for debugging
def print_graph_id(calling_node, graph):
    """prints the node ID's of the graph used to compute the BRG-Set"""
    print('number of nodes in graph remaining:')
    print(len(graph.nodes()))
    print([node.ID for node in graph.nodes_iter()])
    print('center:')
    if calling_node in graph.nodes():
        print(calling_node.ID)
    else:
        return None
    for node in graph.neighbors(calling_node):
        print('one-hop:')
        print(node.ID)
        print('two-hop:')
        print([neigh.ID for neigh in graph.neighbors(node)])
