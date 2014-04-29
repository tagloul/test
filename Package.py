from __future__ import print_function
import numpy as np
#==============================================================================
# This class is basically a data structure for the packet transmitted
# in the network. Very simple class.
#==============================================================================


class Package(object):
    """fancy class containing all kind of stuff which defines a data packet"""
    def __init__(self, value, sqn, origin, data_type, node):
        self.value = value  # the actual data
        self.seq_number = sqn   # this number stands for the sequence of this
                                # packagetype with respect to the origin
        self.origin = origin + 1    # node.id of creator node
        self.path = []
        self.type = data_type
        self.last_node = node
        self.brg = []

    def add_to_path(self, node):
        """the name says it, add a node.id to the package path"""
        import NodeClass
        assert (type(node) == NodeClass.Node)
        self.path.append(node.ID + 1)

    def print_package(self):
        """prints a package in a formated way"""
        print("value: {0}". format(self.value), end=" ")
        print("seq_num: {0}".format(self.seq_number), end=" ")
        print("origin: {0}".format(self.origin), end=" ")
        print("path: {0}".format(self.path), end=" ")
        print("type: {0}".format(self.type), end=" ")
        print('BRG-Set: ', [node_id + 1 for node_id in self.brg])

    def return_str(self):
        content = ''
        content += "value: {0} ".format(self.value)
        content += "seq_num: {0} ".format(self.seq_number)
        content += "origin: {0} ".format(self.origin)
        content += "path: {0} ".format(self.path)
        content += "type: {0} ".format(self.type)
        if self.brg != []:
            content += "BRG-Set: {0}".format(self.brg)
        content += "\n"
        # content = np.array(content).reshape(1,)
        return content


#===============================================================================
# class Hello(object):
#     """hello messages"""
#     def __init__(self, sender):
#         self.sender = sender
#         self.neigh_lst = []
# 
#     def set_sender(self, sender):
#         self.sender = sender
# 
#     def add_neigh(self, neighbor):
#         if neighbor not in self.neigh_lst:
#             self.neigh_lst.append(neighbor)
#     
#===============================================================================