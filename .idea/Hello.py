__author__ = 'tagloul'

# def send_HELLO(node, graph):
#     my_hello = pkt.Hello(node)
#     for neighbor in node.neigh_dict:
#         my_hello.neigh_lst.append(neighbor)
#     for neigh in graph.neighbors(node):
#         neigh.receive_buffer.append(my_hello)

#===============================================================================
# def check_one_hop_edges(node):
#     """this method will establish edges between one-hop neighbors,
#     if not both of them already know it"""
#     for one_hop in node.neigh_dict:
#         for other_one in node.neigh_dict:
#             if other_one != one_hop:
#                 if one_hop in node.neigh_dict[other_one] and other_one not in node.neigh_dict[one_hop]:
#                     node.neigh_dict[one_hop].append(other_one)
#
#
# #===============================================================================
# # def check_two_hop_edges(node):
# #
# #===============================================================================
#
# def hello_operation(graph):
#     for node in graph.nodes_iter():
#         for hello in node.receive_buffer:
#             node.neigh_dict[hello.sender] = hello.neigh_lst
#             check_one_hop_edges(node)
#         send_HELLO(node, graph)
#     for node in graph.nodes_iter():
#
#===============================================================================