""" import print form future to be able to execute print_package method"""
from __future__ import print_function

__author__ = 'Yassine'

import numpy as np
import copy
import random
import this  # quit thinking about this module. too hard for you!!
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# activate the interactive mode for matplotlib
#plt.ion()


class PlotBars(object):
    """a plotbar object stands for a node to be plotted"""
    def __init__(self, bars):
        self._bar = bars

    def set_width(self, width):
        """method to change the length of a bar in the plot"""
        self._bar.set_width(width)

    def get_width(self):
        """returns the widht of the Rectangle object"""
        return self._bar.get_width()


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
        assert type(node) == Node
        self.path.append(node.ID + 1)

    def print_package(self):
        """prints a package in a formated way"""
        print("value: {0}". format(self.value), end=" ")
        print("seq_num: {0}".format(self.seq_number), end=" ")
        print("origin: {0}".format(self.origin), end=" ")
        print("path: {0}".format(self.path), end=" ")
        print("type: {0}".format(self.type))


class Node(object):
    """cool class containing stuff related to nodes"""
    obj_counter = 0  # in order to initiate the node.id

    def __init__(self, size, iteration):
        self._ID = self.__class__.obj_counter
        self._data_stack = []
        self.receive_buffer = []  # package list for incoming data
        self.sending_buffer = []  # list conaining the packages to be send
        self.__class__.obj_counter += 1
        self._sent = 0
        self.packet_history = np.zeros((size, iteration + 1))

    def get_ID(self):
        """id getter"""
        return self._ID

    def get_sent(self):
        """sent setter"""
        return self._sent

    def set_sent(self, value):
        """sent setter"""
        self._sent = value

    def get_data_stack(self):
        """data_stack getter"""
        return self._data_stack

    def set_data_stack(self, data_list):
        """data_stack setter"""
        self._data_stack = data_list

    def check_data(self, data):
        """ checks if a package is known, returns a boolean"""
        assert type(data) == Package
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
            return True
        else:
            return False

    def del_sending_buffer(self):
        """clear the sending_buffer list"""
        self.sending_buffer = []

    def del_receive_buffer(self):
        """"same as last function only this time for the receive_buffer"""
        self.receive_buffer = []

    def send_to_neighbour(self, neighbour):
        """ pushes packages in its sending_buffer into the receive_buffer of
        its neighbours"""
        for item in self.sending_buffer:
            # deepcopy guarantees everything is copied
            neighbour.receive_buffer.append(copy.deepcopy(item))

    def update_data(self, column):
        """core function, check all the data in the receive_buffer and if they
        are unknown pushes them into the data_stack and the sending_buffer"""
        for data in self.receive_buffer:
            boolean = self.check_data(data)
            if boolean == True:
                self.data_stack.append(data)
                data.add_to_path(self)
                self.sending_buffer.append(data)
                # the value is stored in the row = to the origin of the packet
                row = data.origin - 1
                print(row, column, "row and column")
                self.packet_history[row, column:] = data.value
            elif boolean == False:
                pass

    def init_1_data(self):
        """ creates one package of type height and appends it to
        the data_stack and sending_buffer"""
        new_package = Package(self.ID + 1, 1, self.ID, "height")
        new_package.add_to_path(self)
        self.data_stack.append(new_package)
        self.sending_buffer.append(new_package)
        self.packet_history[self.ID, :] = new_package.value

    def init_data(self):
        """ugly random data generator -.- yet still does what it is supposed
        to do. ONLY for testing; creates random packages """
        init_rand = random.randint(0, 5)
        if init_rand != 0:  # prob of 1 over range of randint()
            pass
        else:
            type_rand = random.randint(1, 3)  # determines the type of package
            data = 5 * random.random()  # actual data
            if type_rand == 1:
                max_seq = 0
                for item in self.data_stack:
                    if item.type == "height" and item.origin == self.ID:
                        if item.seq_number > max_seq:
                            max_seq = item.seq_number
                new_package = Package(data, max_seq + 1, self.ID, "height")
                new_package.add_to_path(self)
            elif type_rand == 2:
                max_seq = 0
                for item in self.data_stack:
                    if item.type == "angles" and item.origin == self.ID:
                        if item.seq_number > max_seq:
                            max_seq = item.seq_number
                new_package = Package(data, max_seq + 1, self.ID, "angles")
                new_package.add_to_path(self)
            elif type_rand == 3:
                max_seq = 0
                for item in self.data_stack:
                    if item.type == "velocity" and item.origin == self.ID:
                        if item.seq_number > max_seq:
                            max_seq = item.seq_number
                new_package = Package(data, max_seq + 1, self.ID, "velocity")
                new_package.add_to_path(self)
            self.data_stack.append(new_package)
            self.sending_buffer.append(new_package)

    sent = property(get_sent, set_sent)
    ID = property(get_ID)
    data_stack = property(get_data_stack, set_data_stack)


def print_all_data_stacks(graph):
    """prints data_stacks of all the nodes in the passed graph"""
    for node in graph.nodes():
        print("node :", node.ID + 1)
        for item in node.data_stack:
            print(item.value)
        print('\n')


def animate(frame, mybars, widthHist):
    """perform animation step"""
    for i in range(len(mybars)):
        mybars[i].set_width(widthHist[i, frame])
        #time.sleep(0.15)


def bar_plot(graph, node_num, fig):
    """create barplot to visualize
    the packet transmission"""
    # contains the names for the yticks
    nodes = ["node_" + str(i + 1) for i in range(graph.number_of_nodes())]
    y_pos = np.arange(len(nodes)) + 0.5
    #fig = plt.figure(1)
    # this blocks calculates the length of the bars in the plot
    size = graph.number_of_nodes()
    x_values = [0 for i in range(size)]
    # setup the plot
    bars = plt.barh(y_pos, x_values, 0.4, align='center')
    mybars = [PlotBars(bars[i]) for i in range(size)]
    plt.yticks(y_pos, nodes)
    plt.xlabel('Value')
    plt.title('Packets in the data_stack of node_'+str(node_num))
    plt.xlim(0, size)
    plt.ylim(0, size)
    nodes_names = nx.get_node_attributes(graph, "name")
    names_nodes = dict(zip(nodes_names.values(), nodes_names.keys()))
    width_hist = names_nodes[str(node_num)].packet_history
    print(width_hist)

    ani = animation.FuncAnimation(fig, animate, frames=len(width_hist[0, :]),
                                  fargs=(mybars, width_hist),
                                  interval=100, blit=False, repeat=False)
    ani.save('node_'+str(node_num)+'.mp4', writer='ffmpeg')
    #plt.show()

def setup_sending(graph, iteration):
    """method which handles sending messages in the network,
    only call it once for sending sweet packages in a network"""
    for node in graph.nodes():
        node.init_1_data()
    # loop through all nodes and their neighbours and push data from
    # its own sending_buffer to its neighbour's receive_buffer
    for i in range(iteration):
        for node in graph.nodes():
            for neigh in graph.neighbors_iter(node):
                node.send_to_neighbour(neigh)
        # before updating the sending_buffer delete already sent data
        # after update del receive_buffer not to check already known data twice
        for node in graph.nodes():
            node.del_sending_buffer()
            node.update_data(i + 1)
            print('check')
            node.del_receive_buffer()
        print(i + 1, "th step")
        print_all_data_stacks(graph)
    for node in graph.nodes():
        for item in node.data_stack:
            item.print_package()
        print(node.packet_history)
        print('\n')
    #print_graph(graph)
    #bar_plot(graph, 1)
    create_figure(graph)
    #raw_input('Press enter to continue')


def setup_graph(laplacian, iteration):
    """ this fucntion creates a graph object with the nodes and its edges
    already correct initialized"""
    # this block adds the nodes to the graph and creates two dict
    # in order to label the graph correctly
    size = len(laplacian[0, :])
    my_graph = nx.Graph()
    for i in range(size):
        my_graph.add_node(Node(size, iteration), name=str(i + 1))
    print(my_graph.nodes())
    # stores the nodes and their name attributes in a dictionary
    nodes_names = nx.get_node_attributes(my_graph, "name")
    # switches key and values--> thus names_nodes
    names_nodes = dict(zip(nodes_names.values(), nodes_names.keys()))

    # this block adds the edges between the nodes
    for i in range(0, size):
        for j in range(i + 1, size):
            if laplacian[i, j] == -1:
                node_1 = names_nodes[str(i + 1)]
                node_2 = names_nodes[str(j + 1)]
                my_graph.add_edge(node_1, node_2)

    print(my_graph.edges())

    return my_graph


def print_graph(graph):
    """ prints the graph"""
    # stores the nodes and their name attributes in a dictionary
    nodes_names = nx.get_node_attributes(graph, "name")
    pos = nx.spring_layout(graph)
    # draw without labels, cuz it would label them with their adress, since we
    # initialized the node objects without a name
    nx.draw(graph, pos, with_labels=False)
    # draw the label with the nodes_names containing the name attribute
    nx.draw_networkx_labels(graph, pos, nodes_names)
    plt.title("graph topology")
    plt.savefig("graph.png")


def create_figure(graph):
    """print the two graphs in one window"""
    # activate the interactive mode
    # plt.ion()
    # choose adjusted size for the subplots
#===============================================================================
#     fig = plt.figure(figsize=(6, 8))
# 
#     # print first the network graph
#     plt.subplot(311)
#     print_graph(graph)
# 
#     # print the barplots
#     plt.subplot(312)
#     bar_plot(graph, 1, fig)
# 
#     plt.subplot(313)
#     bar_plot(graph, 2, fig)
#===============================================================================
    print_graph(graph)
    
    size = len(graph.nodes())
    for i in range(size):
        fig = plt.figure()
        bar_plot(graph, i+1, fig)
    #plt.show()

ITERATION = 5


def main():
    """main function which performs the whole retransmission"""
    graph_matrix = np.array([[ 2, -1,  0,  0, -1,  0],
                             [-1,  3, -1,  0, -1,  0],
                             [ 0, -1,  2, -1,  0,  0],
                             [ 0,  0, -1,  3, -1, -1],
                             [-1, -1,  0, -1,  3,  0],
                             [ 0,  0,  0, -1,  0,  1]])
    my_graph = setup_graph(graph_matrix, ITERATION)
    setup_sending(my_graph, 4)


if __name__ == '__main__':
    main()
#alkdfj