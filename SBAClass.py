"""
This file contains all functions related to the Scalable Broadcast Algorithm.
Note that since it does not inherit from the Node Class, the considered node
is always passed as an argument -> calling_node
"""
import random
import math


    #==========================================================================
    # def __init__(self, size, iteration):
    #     super(SBA, self).__init__(size, iteration)
    #     # contains all messages currently processed by SBA
    #     self.packet_dict = {}
    #     self.cover_dict = {}
    #==========================================================================

# packet_dict contains the iteration when the message was received and the actual iteration
# it contains all messages in the data_stack which are currently processed by the SBAlgorithm
def update_packet_dict(calling_node, iteration, graph):
# TODO message problem
# todo replace graph with two_hopdict
    """
    Update all messages with an active random timer

    Check the timers of all the messages in the packet_dict
    and if not all the neighbors of the calling_node have been covered
    by the incoming messages pushes the messages into the sending_buffer
    to be rebroadcast.

    Arguments:
    iteration -- iteration in which this method is called
    graph/two_hop_dict -- contains neighborhood
    calling_node -- currently treated node

    Return-type:
    None
    """
    packets_to_del = []
    for packet in calling_node.packet_dict:
        # retreive times from the packet_dict
        t, start_iter = calling_node.packet_dict[packet]
        # check if random_timer expired
        if (start_iter + t) < iteration:
            # if expired delete it from the packet_dict
            packets_to_del.append(packet)
            # check for each node the calculated cover_set
            for node in graph.neighbors_iter(calling_node):
                bool_cs = node in calling_node.cover_dict[packet]
                if not bool_cs:
                    break
            # cover-set != 2-hop neighborhood
            # i.e has to rebroadcast packets
            if not bool_cs:
                # calling_node.sender = True
                calling_node.sending_buffer.append(packet)
        # if timer has not yet expired-> update cover_set
        else:
            update_cover_set(calling_node, packet, graph)
    for pack in packets_to_del:
        del calling_node.packet_dict[pack]


def check_packet_dict(calling_node, packet):
    #TODO message problem
    """ checks if a package is known

    Return True if message is known and False if it is unknown

    Argument:
    packet -- message to be checked

    Return-type:
    Boolean
    """
        #assert type(packet) == packet.Package
    origin_check = 0
    seq_check = 0
    type_check = 0
    for item in calling_node.packet_dict.keys():
        if packet.origin == item.origin:
            origin_check = 1
        if packet.type == item.type:
            type_check = 1
        if packet.seq_number == item.seq_number:
            seq_check = 1
    if origin_check == 0 or seq_check == 0 or type_check == 0:
        return False
    else:
        return True


def check_receive_buffer(calling_node, message, iteration, graph):
#TODO messge problem
# todo replace graph by two_hop_dict
    """Perform the SBA for a message on the calling_node

    First check if message is unknown and wether it already has an active random-timer or not
    Depending on the outcome of these checks either only update messages with random-timers
    or activate a random-timer for the message-node pair and adds them to the packet_dict.

    Arguments:
    calling_node -- currently treated node
    message -- message to be handled
    iteration -- Iteration in which method is called
    graph/two_hop_dict -- contains the two-hop neigborhood

    Return-type:
    None
    """
    bool_ds = calling_node.check_data_stack(message)  # message in self.data_stack
    bool_pd = check_packet_dict(calling_node, message)  # message in self.packet_dict
    # if the message is already known to the node just update the cover_set
    if bool_pd == True and bool_ds == True:
        update_cover_set(calling_node, message, graph)
    elif bool_pd == False and bool_ds == False:
        # check for this unknown message if the neighbors of the current node
        # are already covered by the last node
        bool_neigh = check_neigh(calling_node, graph, message.last_node)
        # if the are not known push this message into the packet_dict
        # and activate a random_timer
        if not bool_neigh:
            t = 0
            #t = self.get_random_timer(graph)
            calling_node.packet_dict[message] = (t, iteration)
            update_cover_set(calling_node, message, graph)


def check_neigh(calling_node, graph, neigh):
    """Check if the own neighborhood is covered by the senders one

    Return False if there are node in the calling_node neighborhood
    not covered by the senders neighborhood else return True

    Return-type:
    Boolean
    """
    for node in graph.neighbors_iter(calling_node):
        bool_value = (node in graph.neighbors(neigh) or node == neigh)
        if bool_value == False:
            break
    return bool_value


def get_random_timer(calling_node, graph):
    """Compute the random-timer

    Return an iteration_timestep from a uniform distribution defined by random_timer.
    -> random_timer is a design-parameter
    Graph only used to get the nodes degree, no topology information used

    Arguments:
    calling_node -- currently treated node
    graph -- networkx Graph containing the whole network

    Return-type:
    t -- random timestep integer
    """
        # calculates the quotient T_0 of the 1 + max degree of neighbors
        # and 1 + degree of message receiver
    degree_neigh = 0
    for neigh in graph.neighbors_iter(calling_node):
        if graph.degree(neigh) > degree_neigh:
            degree_neigh = graph.degree(neigh)
    degree_node = graph.degree(calling_node)
    T_0 = float(1 + degree_neigh) / (1 + degree_node)
        # set the random time value for the argument of the
        # uniform-distribution
    # this is a tuning-parameter, which is still open
    random_timer = 3
    t = random.randint(0, math.ceil(T_0 * random_timer))
    return t


def update_cover_set(calling_node, message, graph): # TODO
    """update the cover_set for a message and its node

    If the message is not yet known create a new key in the cover_dict.
    If necessary add the message sender and its neighbors to the cover_dict values

    Arguments:
    calling_node -- currently treated node
    message -- message about which the operations are performed
    graph/two_hop_dict -- contains topology information
    """
    if message not in calling_node.cover_dict:
        calling_node.cover_dict[message] = []

    if message.last_node not in calling_node.cover_dict[message]:
        calling_node.cover_dict[message].append(message.last_node)
    for neigh in graph.neighbors_iter(message.last_node):
        if neigh not in calling_node.cover_dict[message]:
            calling_node.cover_dict[message].append(neigh)
