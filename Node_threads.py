__author__ = 'tagloul'
import threading

# here insert the sending flow
# flooding:
# def setup_sending_flooding(graph, iteration, FLAG):
#     """method which handles sending messages in the network,
#     only call it once for sending sweet packages in a network"""
#     # initate all nodes with a datapacket
#     for node in graph.nodes():
#         node.init_1_data()
#     # loop through all nodes and their neighbours and push data from
#     # its own sending_buffer to its neighbour's receive_buffer
#     for i in range(iteration):
#         for node in graph.nodes():
#             for neigh in graph.neighbors_iter(node):
#                 node.send_to_neighbor(neigh)
#         # before updating the sending_buffer delete already sent data
#         # after update del receive_buffer not to check already known data twice
#         for node in graph.nodes():
#             node.del_sending_buffer()
#             node.update_data(i + 1, FLAG)
#             node.del_receive_buffer()

class Node_thread(object, threading, flag):
    """ class which creates thread for a node and its different
    run methods -> corresponding to the protocol"""
    locker = threading.Lock()

    def __init__(self, node, topo_graph):
        threading.Thread.__init__(name=node.ID)
        self.node = node
        self.graph = topo_graph
        self.flag = flag

    def run(self):
        """"this will then execute the sending process for a node""""
        # initiate this node with data
        self.node.init_1_data()
        # for neigh in self.graph.neighbors(self.node):
        #     self.node.send_to_neighbor(neigh)
        # this block will forward messages in the sending_buffer to its neigh
        #Node_thread.locker.acquire()
        for message in self.node.sending_buffer:
            # not sure if I really need a locker here, prolly not
            #Node_thread.locker.acquire()
            for neigh in self.graph.neighbors(self.node):
                self.send_one_message(message, neigh)
            self.node.sending_buffer.remove(message)
        #Node_thread.locker.release()
        # this block will handle incoming messages
        # will need the locker since I append data
        while len(self.node.receive_buffer) > 0:
            for packet in self.node.receive_buffer:
                self.check_message(packet)


    def check_message(self, data):
        bool_data = self.node.check_data_stack(data)
        if not bool_data:
            data.add_to_path(self.node)
            self.node.data_stack.append(data)
            self.node.sending_buffer.append(data)
        self.node.receive_buffer.remove(data)

class Read_thread(object, threading.Thread):
    def __ini__(self, node, topo_graph):
        threading.Thread.__init__(name='read'+str(node.ID))
        self.node = node
        self.graph = topo_graph

    def run(self):