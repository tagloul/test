import NodeClass as nde
import networkx as nx


    #==========================================================================
    # def __init__(self, size, iteration, graph):
    #     super(AHBP, self).__init__(size, iteration, graph)
    #     self.two_hop_dict = {}
    #     self.flag = "AHBP"
    #==========================================================================


def dummy_method(node_caller):
    print 'check for dummies'
    other_dummy()


def other_dummy(node_caller):
    print 'another dummy ohh wow'

    # As soon as Hello messages are implemented remove this function
    # and build the two-hop neighborhood with the inforamtion from the
    # hello-messages


def build_2_hop(node_caller, graph):
    """this is gonna build the two-hop neighborhood of a node"""
    for node in graph.neighbors(node_caller):
        two_hop_lst = []
        for neigh in graph.neighbors(node):
            if neigh != node_caller and neigh not in graph.neighbors(node_caller):
                two_hop_lst.append(neigh)
        node_caller.two_hop_dict[node] = two_hop_lst


def del_brg(message):
    """deletes the BRG-Set in a node"""
    message.brg = []


def build_2_hop_graph(node_caller):
    """with the two-hop neighborhood information of a node
    builds a networkx graph, in order to perform the algorithm"""
    my_graph = nx.Graph()
    my_graph.add_node(node_caller)
    for node in node_caller.two_hop_dict:
        my_graph.add_node(node)
        my_graph.add_nodes_from(node_caller.two_hop_dict[node])
    for node in node_caller.two_hop_dict:
        my_graph.add_edge(node_caller, node)
        for neigh in node_caller.two_hop_dict[node]:
            my_graph.add_edge(node, neigh)
        #print('check: built the graph')
        #self.print_graph_id(my_graph)
    return my_graph


def check_path_node(node_caller, del_lst, path_lst, node):
    bool_check = False
    bool_check = node.ID + 1 != path_lst[-1]
    if bool_check == True:
        bool_check = node not in del_lst
        if bool_check == True:
            bool_check = node != node_caller
            return bool_check
    return False


def remove_path_nodes(node_caller, graph, message):
    """iterates through the path of the message and deletes nodes
    and their neighbors if they are in the path"""
    del_lst = []
    ID_lst = [node.ID + 1 for node in graph.nodes()]
    for node_id in ID_lst:
        if node_id in message.path[:-1]:
            index = ID_lst.index(node_id)
            node = graph.nodes()[index]
            del_lst.append(node)
            for neigh in graph.neighbors(node):
                bool_check = check_path_node(node_caller, del_lst, message.path, neigh)
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


def remove_edges(node_caller, graph):
    """detects edges between 1-hop neighbors and deletes them"""
    edges_lst = []
    for edge in graph.edges_iter():
        n1, n2 = edge
        if (n1 in graph.neighbors(node_caller)) and (n2 in graph.neighbors(node_caller)):
            edges_lst.append(edge)

    graph.remove_edges_from(edges_lst)
        #print('check: removed edges')
        #self.print_graph_id(graph)


def remove_nodes(node_caller, graph):
    """removes nodes with degree = 0 from the graph and 1-hop neighbors
    with no other neighbors, i.e. degree = 1"""
    node_lst = []
        # nodes with degree = 0
    for node in graph.nodes():
        if graph.degree(node) == 0:
            node_lst.append(node)
        # 1-hop neighbors with degree = 1
    for node in graph.neighbors(node_caller):
        if graph.degree(node) == 1:
            node_lst.append(node)
    graph.remove_nodes_from(node_lst)
        #print('check: removed nodes')
        #print('removed nodes:')
        #print([node.ID for node in node_lst])
        #self.print_graph_id(graph)


def add_to_BRG(node_caller, graph, message):
    """looks out for the required nodes and adds them to the
    BRG-Set"""
    if graph.nodes() == []:
        return None
    one_hop = graph.neighbors(node_caller)
    two_hop = []
    counter = 0
    added_node = 0
        #build the two-hop neighbor list
    for node in one_hop:
        for neigh in graph.neighbors(node):
            if neigh in two_hop == False and neigh != node_caller:
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
            if neigh != node_caller:
                del_lst.append(neigh)
    graph.remove_nodes_from(del_lst)
        #print('check: added to BRG')
        #print('removed node:')
        #print([node.ID for node in del_lst])
        #self.print_graph_id(graph)


def build_BRG(node_caller, message):
    """this function puts together the previous ones and uses them
    to build the BRG-Set of the calling node for a certain message"""
    #print('actual node:')
    #print(node_caller.ID + 1)

    my_graph = build_2_hop_graph(node_caller)
        #print(self)
    del_brg(message)
    remove_path_nodes(node_caller, my_graph, message)
    remove_edges(node_caller, my_graph)
        # as long as there are nodes in the graph update the BRG-Set
    while(len(my_graph.nodes()) > 0):
        remove_nodes(node_caller, my_graph)
        add_to_BRG(node_caller, my_graph, message)
            #print('remaining nodes:')
            #print(len(my_graph.nodes()))


def check_receive_buffer(node_caller, column):
    """loops through the receive-list and check if messages are
    unknown. If the message is unknown,
    checks the BRG-Set appended to the message"""
    for message in node_caller.receive_buffer:
            # add unknown messages to the data-list
        bool_ds = node_caller.check_data_stack(message)  # m in self.data_stack
        if bool_ds == False:
            message.add_to_path(node_caller)
            node_caller.data_stack.append(message)
            row = message.origin - 1
            node_caller.packet_history[row, column:] = message.value
                # if oneself is in the BRG-Set add it to the sending-list
            if node_caller.ID in message.brg:
                node_caller.sending_buffer.append(message)


    # only for debugging
def print_graph_id(node_caller, graph):
    """prints the node ID's of the graph used to compute the
    BRG-Set"""
    print('number of nodes in graph remaining:')
    print(len(graph.nodes()))
    print([node.ID for node in graph.nodes_iter()])
    print('center:')
    if node_caller in graph.nodes():
        print(node_caller.ID)
    else:
        return None
    for node in graph.neighbors(node_caller):
        print('one-hop:')
        print(node.ID)
        print('two-hop:')
        print([neigh.ID for neigh in graph.neighbors(node)])
