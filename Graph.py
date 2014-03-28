#==============================================================================
# this file handles everything realted to visula output.
# so far you will find a part for the animated barplots,
# a plotted graph topology
#==============================================================================


import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import networkx as nx
import math




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


def animate(frame, mybars, widthHist):
    """perform animation step"""
    for i in range(len(mybars)):
        mybars[i].set_width(widthHist[i, frame])
        #time.sleep(0.15)


def bar_plot(graph, node_num, fig):
    """create animated barplot to visualize
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
    plt.title('Packets in the data_stack of node_' + str(node_num))
    plt.xlim(0, size)
    plt.ylim(0, size)
    nodes_names = nx.get_node_attributes(graph, "name")
    names_nodes = dict(zip(nodes_names.values(), nodes_names.keys()))
    width_hist = names_nodes[str(node_num)].packet_history
    print(width_hist)

    ani = animation.FuncAnimation(fig, animate, len(width_hist[0, :]),
                                  fargs=(mybars, width_hist),
                                  interval=100, blit=False, repeat=False)
    ani.save('node_' + str(node_num) + '.mp4', writer='ffmpeg')


def iteration_plots(graph):
    size = len(graph.nodes())
    rows = math.ceil(size / 2.)
    cols = 2
    nodes = [str(i + 1) for i in range(size)]
    y_pos = [i + 0.5 for i in range(size)]
    nodes_names = nx.get_node_attributes(graph, "name")
    names_nodes = dict(zip(nodes_names.values(), nodes_names.keys()))

    fig, axarr = plt.subplots(rows, cols, sharex='col', sharey='row')
    fig.text(0.5, 0.04, 'iteration', ha='center', va='center')
    fig.text(0.06, 0.5, 'neighbor', ha='center', va='center', rotation='vertical')
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
            axarr[row, col].set_xlim(0, size)
            axarr[row, col].barh(y_pos, x_values, 0.4, align='center')

    fig.savefig("iteration.png")


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


def print_all_data_stacks(graph):
    """prints data_stacks of all the nodes in the graph argument"""
    for node in graph.nodes():
        print("node :", node.ID + 1)
        for item in node.data_stack:
            print(item.value)
        print('\n')
