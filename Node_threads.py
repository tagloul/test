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
        self.node.init_1_data()
        # for neigh in self.graph.neighbors(self.node):
        #     self.node.send_to_neighbor(neigh)
        for message in self.node.sending_buffer:
            pass