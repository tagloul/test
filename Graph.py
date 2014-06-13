"""
File contains all kind of functions related to output or graphical implementations.

Animated Barplot:
Class PlotBars -> Bar-agents for an animated Barplot.
animate function -> argument for the matplotlib.animation
bar_plot -> create the whole animated barplot

Iteration-plots:
Shows in which iteration step a node gets messges
from the other nodes in the network.

"""
# TODO find an appropriate way to save the animated plots

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import networkx as nx
import math


class PlotBars(object):
    """A plotbar object stands for a node to be plotted"""
    def __init__(self, bars):
        """Bars is a rectangle object form matplotlib"""
        self._bar = bars

    def set_width(self, width):
        """Change the length of a bar in the plot"""
        self._bar.set_width(width)

    def get_width(self):
        """Return the length of the Rectangle object"""
        return self._bar.get_width()


def animate(frame, mybars, widthHist):
    """perform animation step


    Arguments:
    Frame -- Number of total frames the resulting animation will have
    mybars -- rectanvle objects
    widthHist -- Matrix containing the iteration when the message was received

    Return-type:
    None
    """
    for i in range(len(mybars)):
        mybars[i].set_width(widthHist[i, frame])
        #time.sleep(0.15)


def bar_plot(graph, node_num, fig):
    """Create the animation to visualize the transmission

    Arguments:
    graph -- networkx Graph; contains whole topolgy information
    fig -- matplotlib Figure; will hold the animation

    Return-type:
    Show the animation and stores it as mp4 file

    """
    # contains the names for the yticks
    nodes = ["node_" + str(i + 1) for i in range(graph.number_of_nodes())]
    y_pos = np.arange(len(nodes)) + 0.5
    #fig = plt.figure(1)
    # this blocks calculates the length of the bars in the plot
    size = graph.number_of_nodes()
    x_values = [0 for i in range(size)]
    # setup the plot
    bars = plt.barh(y_pos, x_values, 0.4, align='center')
    # bars is a list with rectangle objects
    mybars = [PlotBars(bars[i]) for i in range(size)]
    plt.yticks(y_pos, nodes)
    plt.xlabel('Value')
    plt.title('Packets in the data_stack of node_' + str(node_num))
    plt.xlim(0, size)
    plt.ylim(0, size)
    nodes_names = nx.get_node_attributes(graph, "name")
    names_nodes = dict(zip(nodes_names.values(), nodes_names.keys()))
    width_hist = names_nodes[str(node_num)].packet_history

    ani = animation.FuncAnimation(fig, animate, len(width_hist[:, 0]),
                                  fargs=(mybars, width_hist),
                                  interval=2000, blit=False, repeat=False)
    ani.save('node_' + str(node_num) + '.mp4', codec = ffmpeg)
             # extra_args=['-vcodec', 'libx264'])
    # plt.show()


def iteration_plots(graph):
    """Create a barplot indicating when a message was received

    With the message history in every node create a barplot showing for each node
    in which iteration it received the message from the other nodes.
    Then save the plot in the same directory as the Main.py file
    as 'iteration.png'
    """
    size = len(graph.nodes())
    rows = int(math.ceil(size / 2.))
    cols = 2
    nodes = [str(i + 1) for i in range(size)]
    y_pos = [i + 0.5 for i in range(size)]
    nodes_names = nx.get_node_attributes(graph, "name")
    names_nodes = dict(zip(nodes_names.values(), nodes_names.keys()))

    fig, axarr = plt.subplots(rows, cols, sharex='col', sharey='row')
    fig.text(0.5, 0.05, 'iteration', ha='center', va='center')
    fig.text(0.05, 0.5, 'neighbor', ha='center', va='center', rotation='vertical')
    x_lim = len(graph.nodes()[0].packet_history[0])
    for row in range(rows):
        for col in range(cols):
            node_num = row * cols + col + 1
            if node_num - 1 >= size:
                break
            matrix = names_nodes[str(node_num)].packet_history
            # this line finds the index of the first nonzero value in the 1-D
            # ndarray.
            # could speed this up by writing a cpython function
            x_values = [np.nonzero(matrix[i])[0][0] for i in range(size)]
            # this block prints all the subplots and sets the ylabels
            axarr[row, col].set_title('node' + str(node_num))
            axarr[row, col].set_yticks(y_pos)
            axarr[row, col].set_yticklabels(nodes)
            axarr[row, col].set_ylim(0, size)
            axarr[row, col].set_xlim(0, x_lim)
            axarr[row, col].barh(y_pos, x_values, 0.4, align='center')

    fig.savefig("iteration.svg")


def print_graph(graph):
    """Print the graph and save the image as 'graph.png'"""
    fig = plt.figure()
    # stores the nodes and their name attributes in a dictionary
    nodes_names = nx.get_node_attributes(graph, "name")
    pos = nx.spring_layout(graph)
    # draw without labels, cuz it would label them with their adress, since we
    # initialized the node objects without a name
    nx.draw(graph, pos, with_labels=False)
    # draw the label with the nodes_names containing the name attribute
    nx.draw_networkx_labels(graph, pos, nodes_names)
    plt.title("graph topology: ")
    plt.show()
    fig.savefig("graph.svg")


def print_all_data_stacks(graph):
    """Print out data_stacks of all the nodes in the graph """
    for node in graph.nodes():
        print("node :", node.ID + 1)
        for item in node.data_stack:
            print(item.value)
        print('\n')
