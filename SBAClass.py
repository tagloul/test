#==============================================================================
# Scalable Broadcast Algortihm
#==============================================================================
import random
import math
import NodeClass as nde


class SBA(nde.Node):
    """Scalable Broadcast Algorithm"""
    def __init__(self, size, iteration):
        super(SBA, self).__init__(size, iteration)
        # contains all messages currently processed by SBA
        self.packet_dict = {}
        self.cover_dict = {}

    def update_packet_dict(self, actual_iter, graph):
        packets_to_del = []
        for packet in self.packet_dict:
            t, start_iter = self.packet_dict[packet]
            if (start_iter + t) < actual_iter:
                packets_to_del.append(packet)
                for node in graph.neighbors_iter(self):
                    bool_cs = node in self.cover_dict[packet]
                    if bool_cs == False:
                        break
                if bool_cs == False:
                    self.sending_buffer.append(packet)
            else:
                self.update_cover_set(packet, graph)
        for pack in packets_to_del:
            del self.packet_dict[pack]

    def check_packet_dict(self, packet):
        """ checks if a package is known, returns a boolean"""
        #assert type(packet) == packet.Package
        origin_check = 0
        seq_check = 0
        type_check = 0
        for item in self.packet_dict.keys():
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

    def check_receive_buffer(self, m, actual_iter, graph):
        bool_ds = self.check_data_stack(m)  # m in self.data_stack
        bool_pd = self.check_packet_dict(m)  # m in self.packet_dict
        if bool_pd == True and bool_ds == True:
            self.update_cover_set(m, graph)
        elif bool_pd == False and bool_ds == False:
            #self.data_stack.append(m)
            bool_neigh = self.check_neigh(graph, m.last_node)
            if bool_neigh == True:
                pass
            elif bool_neigh == False:
                t = 0
                #t = self.get_random_timer(graph)
                self.packet_dict[m] = (t, actual_iter)
                self.update_cover_set(m, graph)

    def check_neigh(self, graph, neigh):
        for node in graph.neighbors_iter(self):
            bool_value = (node in graph.neighbors(neigh) or node == neigh)
            if bool_value == False:
                break
        return bool_value

    def get_random_timer(self, graph):
        # calculates the quotient T_0 of the 1 + max degree of neighbors
        # and 1 + degree of message receiver
        degree_neigh = 0
        for neigh in graph.neighbors_iter(self):
            if graph.degree(neigh) > degree_neigh:
                degree_neigh = graph.degree(neigh)
        degree_node = graph.degree(self)
        T_0 = float(1 + degree_neigh) / (1 + degree_node)
        # set the random time value for the argument of the
        # uniform-distribution
        random_timer = 2
        t = random.randint(0, math.ceil(T_0 * random_timer))
        return t

    def update_cover_set(self, m, graph):
        if m not in self.cover_dict:
            self.cover_dict[m] = []

        if m.last_node not in self.cover_dict[m]:
            self.cover_dict[m].append(m.last_node)
        for neigh in graph.neighbors_iter(m.last_node):
            if neigh not in self.cover_dict[m]:
                self.cover_dict[m].append(neigh)
