import networkx as nx
import matplotlib.pyplot as plt
import random

def random_graph(num_nodes):
    graph_bool = False
    # generate a graphically meaningful degree sequence
    while not graph_bool:
        degree_lst = [random.randint(1,6) for i in range(num_nodes)]
        graph_bool = nx.is_graphical(degree_lst)
        print degree_lst
    gene_bool = False
    # Use try here because sometimes an the graph can not be generated within 10 tries
    # so try as long as it works
    while not gene_bool:
        try:
            graph = nx.random_degree_sequence_graph(degree_lst)
            gene_bool = True
        finally:
            pass
    graph.remove_edges_from(graph.selfloop_edges())
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos)
    plt.show()


random_graph(5)

# def draw_graph(graph):
#
#     # extract nodes from graph
#     nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])
#
#     # create networkx graph
#     G=nx.Graph()
#
#     # add nodes
#     for node in nodes:
#         G.add_node(node)
#
#     # add edges
#     for edge in graph:
#         G.add_edge(edge[0], edge[1])
#
#     # draw graph
#     pos = nx.shell_layout(G)
#     nx.draw(G, pos)
#
#     # show graph
#     plt.show()
#
# # draw example
# graph = [(20, 21),(21, 22),(22, 23), (23, 24),(24, 25), (25, 20)]
# draw_graph(graph)