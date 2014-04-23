#==============================================================================
# Scalable Broadcast Algortihm
#==============================================================================
import random
import math
import NodeClass as nde

    #==========================================================================
    # def __init__(self, size, iteration):
    #     super(SBA, self).__init__(size, iteration)
    #     # contains all messages currently processed by SBA
    #     self.packet_dict = {}
    #     self.cover_dict = {}
    #==========================================================================

# packet_dict contains the iteration when the message was received and the actual iteration
# it contains all messages in the data_stack which are currently processed by the SBAlgorithm
def update_packet_dict(node_caller, actual_iter, graph):
    """Checks the timers of all the messages in the packet_dict
    and if necessary pushes them into the sending_buffer to be rebroadcast"""
    packets_to_del = []
    for packet in node_caller.packet_dict:
        t, start_iter = node_caller.packet_dict[packet]
        # actual iteration is past the random_timer
        # so start to check the cover_dict
        if (start_iter + t) < actual_iter:
            packets_to_del.append(packet)
            for node in graph.neighbors_iter(node_caller):
                bool_cs = node in node_caller.cover_dict[packet]
                if bool_cs == False:
                    break
            if bool_cs == False:
                node_caller.sending_buffer.append(packet)
        else:
            update_cover_set(node_caller, packet, graph)
    for pack in packets_to_del:
        del node_caller.packet_dict[pack]


def check_packet_dict(node_caller, packet):
    """ checks if a package is known, returns a boolean"""
        #assert type(packet) == packet.Package
    origin_check = 0
    seq_check = 0
    type_check = 0
    for item in node_caller.packet_dict.keys():
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


def check_receive_buffer(node_caller, m, actual_iter, graph):
    bool_ds = node_caller.check_data_stack(m)  # m in self.data_stack
    bool_pd = check_packet_dict(node_caller, m)  # m in self.packet_dict
    if bool_pd == True and bool_ds == True:
        update_cover_set(node_caller, m, graph)
    elif bool_pd == False and bool_ds == False:
            #self.data_stack.append(m)
        bool_neigh = check_neigh(node_caller, graph, m.last_node)
        if bool_neigh == True:
            pass
        elif bool_neigh == False:
            t = 0
                #t = self.get_random_timer(graph)
            node_caller.packet_dict[m] = (t, actual_iter)
            update_cover_set(node_caller, m, graph)


def check_neigh(node_caller, graph, neigh):
    """checks if the neighborhood of the receiver node is contained
    in the neihgborhood and of the sender and itself"""
    for node in graph.neighbors_iter(node_caller):
        bool_value = (node in graph.neighbors(neigh) or node == neigh)
        if bool_value == False:
            break
    return bool_value


def get_random_timer(node_caller, graph):
    """returns an iteration_timestep from a uniform distribution.
    -> random_timer is design parameter"""
        # calculates the quotient T_0 of the 1 + max degree of neighbors
        # and 1 + degree of message receiver
    degree_neigh = 0
    for neigh in graph.neighbors_iter(node_caller):
        if graph.degree(neigh) > degree_neigh:
            degree_neigh = graph.degree(neigh)
    degree_node = graph.degree(node_caller)
    T_0 = float(1 + degree_neigh) / (1 + degree_node)
        # set the random time value for the argument of the
        # uniform-distribution
    random_timer = 2
    t = random.randint(0, math.ceil(T_0 * random_timer))
    return t


def update_cover_set(node_caller, m, graph):
    """if not yet known, add the node_caller and its neighbors to the cover_dict"""
    if m not in node_caller.cover_dict:
        node_caller.cover_dict[m] = []

    if m.last_node not in node_caller.cover_dict[m]:
        node_caller.cover_dict[m].append(m.last_node)
    for neigh in graph.neighbors_iter(m.last_node):
        if neigh not in node_caller.cover_dict[m]:
            node_caller.cover_dict[m].append(neigh)
