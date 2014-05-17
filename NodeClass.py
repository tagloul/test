#==============================================================================
# Big class defining everything a basic node in our network needs to be able
# to do and contain as data elements. You will find at the end to methods
# generating random or determined Messages
#==============================================================================

import numpy as np
import copy
import random
import this  # quit thinking about this module. too hard for you!!
import Package as pac
import threading


class Node(object):
    """cool class containing stuff related to nodes

    class attributes:
    obj_counter -- counter in order to get for every node a different ID


    """
    obj_counter = 0  # in order to initiate the node.id

# just cancelled out the arguments in the init method
    def __init__(self): # , size, iteration): # just removed the number of iteration for the packet_history
        """Initialize a node instance

        Note: each time a new node is initialized the obj_counter is incremented

        Instance attributes:
        ID -- identification number of a node
        data_stack -- list with all messages known to the node
        receive_buffer -- list with all incoming messages during an iteration
        sending_buffer -- list with all outgoing messages during an iteration
        sender -- Flag indicating if a node rebroadcasts any messages
        flag -- Indicate which sending algorithm is used
        two_hop_dict -- Dict with 1-hop neighbors as key and 2-hop neigh as their values
        cover_dict -- Cover-set for the SBA

        Most important Methods:
        send_to_neighbor -- send the whole sending_buffer to a neighbor
        update_data -- check the receive_buffer for unknown messages
        init_1_data -- initiate the nodes with a message
        """
        self._ID = self.__class__.obj_counter
        self._data_stack = []
        self.receive_buffer = []  # packet list for incoming data
        self.sending_buffer = []  # list conaining the packets to be send
        self.__class__.obj_counter += 1
        self.sender = False
        # matrix which stores the info when a node receive a packet
        # self.packet_history = np.zeros((size, iteration))
        self.flag = ""
        # is a dict for SBA; contains packets with an active random timer
        self.packet_dict = {}
        # cover-set for SBA; keys are the covered 1-hop neighbors
        # and the values are their neighbors
        self.cover_dict = {}
        # both are the same, just use two different dict for now, cuz
        # i want to test the hello-messages
        self.two_hop_dict = {}
        self.neigh_dict = {}

    def get_ID(self):
        """ID getter"""
        return self._ID

    def get_data_stack(self):
        """data_stack getter"""
        return self._data_stack

    def set_data_stack(self, data_list):
        """data_stack setter"""
        self._data_stack = data_list

    def check_data_stack(self, data):
        """ checks if a message is known

        Returns  True if the message is already known and False if it is unknown

        Return-type:
        Boolean
        """
        assert type(data) == pac.Packet
        #======================================================================
        # bool_data = data in self.data_stack
        # return bool_data
        #----------------------------------------------------------------------
        # this does not work..
        #======================================================================
        origin_check = 0
        seq_check = 0
        type_check = 0
        for item in self.data_stack:
            if data.origin == item.origin:
                origin_check = 1
            if data.type == item.type:
                type_check = 1
            if data.seq_number == item.seq_number:
                seq_check = 1
        if origin_check == 0 or seq_check == 0 or type_check == 0:
            return False
        else:
            return True

    def del_data_stack(self):
        """Delete the data_stack of a node"""
        self.data_stack = []

    def del_sending_buffer(self):
        """Delete the sending_buffer of a node"""
        self.sending_buffer = []

    def del_receive_buffer(self):
        """Delete the receive_buffer"""
        self.receive_buffer = []

    def send_to_neighbor(self, neighbor):
        """Push the sending_buffer to the receive_buffer of the neighbor

        Argument:
        neighbor -- node instance
        """
        for item in self.sending_buffer:
            if neighbor != item.last_node:
                # deepcopy guarantees everything is copied
                neighbor.receive_buffer.append(copy.deepcopy(item))
                neighbor.receive_buffer[-1].last_node = self
                # set the sender flag to true only for sending nodes
                # which are not the source of the message
                if item.last_node.ID != self.ID:
                    self.sender = True


    def update_data(self, column, FLAG):
        """Check the receive_buffer for unknown messages

        Any unknown message will be appended to the data_stack of the node.
        Depending on the Algorithm used, it may also be added to the sending_buffer.

        Arguments:
        column -- Iteration in which this method is called
        FLAG -- string - Aglorithm used
        """
        for data in self.receive_buffer:
            boolean = self.check_data_stack(data)
            if not boolean:
                data.add_to_path(self)
                self.data_stack.append(data)
                if FLAG != "SBA":
                    self.sending_buffer.append(data)
                # the value is stored in the row = to the origin of the packet
                # row = data.origin - 1
                # self.packet_history[row, column:] = data.value
            elif boolean:
                pass

    def init_1_data(self):
        """Create a data-message and append it to the node

        New message with sequence number 1, origin = ID
        and last_node equals oneself

        Appends the message to the data_stack and sending_bufffer
        """
        new_packet = pac.Packet(self.ID + 1, 1, self.ID, "height", self)
        new_packet.add_to_path(self)
        self.data_stack.append(new_packet)
        self.sending_buffer.append(new_packet)
        # self.packet_history[self.ID, :] = new_packet.value

    def init_data(self):  # todo find a way to eliminate these if statements
        """ugly random data generator -.- yet still does what it is supposed
        to do. ONLY for testing; creates random packets """
        init_rand = random.randint(0, 5)
        if init_rand != 0:  # prob of 1 over range of randint()
            pass
        else:
            type_rand = random.randint(1, 3)  # determines the type of packet
            data = 5 * random.random()  # actual data
            if type_rand == 1:
                max_seq = 0
                for item in self.data_stack:
                    if item.type == "height" and item.origin == self.ID:
                        if item.seq_number > max_seq:
                            max_seq = item.seq_number
                new_packet = pac.Packet(data, max_seq + 1, self.ID, "height")
                new_packet.add_to_path(self)
            elif type_rand == 2:
                max_seq = 0
                for item in self.data_stack:
                    if item.type == "angles" and item.origin == self.ID:
                        if item.seq_number > max_seq:
                            max_seq = item.seq_number
                new_packet = pac.Packet(data, max_seq + 1, self.ID, "angles")
                new_packet.add_to_path(self)
            elif type_rand == 3:
                max_seq = 0
                for item in self.data_stack:
                    if item.type == "velocity" and item.origin == self.ID:
                        if item.seq_number > max_seq:
                            max_seq = item.seq_number
                new_packet = pac.Packet(data, max_seq + 1, self.ID, "velocity")
                new_packet.add_to_path(self)
            self.data_stack.append(new_packet)
            self.sending_buffer.append(new_packet)

    ID = property(get_ID)
    data_stack = property(get_data_stack, set_data_stack)
