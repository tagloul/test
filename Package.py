from __future__ import print_function
#===============================================================================
# This class is basically a data structure for the packet transmitted
# in the network. Very simple class.
#===============================================================================

import Node as nde


class Package(object):
    """fancy class containing all kind of stuff which defines a data packet"""
    def __init__(self, value, sqn, origin, data_type=""):
        self.value = value  # the actual data
        self.seq_number = sqn   # this number stands for the sequence of this
                                # packagetype with respect to the origin
        self.origin = origin + 1    # node.id of creator node
        self.path = []
        self.type = data_type

    def add_to_path(self, node):
        """the name says it, add a node.id to the package path"""
        assert type(node) == nde.Node
        self.path.append(node.ID + 1)

    def print_package(self):
        """prints a package in a formated way"""
        print("value: {0}". format(self.value), end=" ")
        print("seq_num: {0}".format(self.seq_number), end=" ")
        print("origin: {0}".format(self.origin), end=" ")
        print("path: {0}".format(self.path), end=" ")
        print("type: {0}".format(self.type))
