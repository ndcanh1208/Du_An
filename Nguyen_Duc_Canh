import networkx as nx
import numpy as np

# Tạo đồ thị vô hướng có trọng số
G = nx.Graph()
nodes = ['1', '2', '3', '4', '5', '6', '7']
edges = [
    ('1', '2', 2),
    ('1', '3', 4),
    ('1', '4', 2),
    ('2', '4', 6),
    ('2', '5', 3),
    ('3', '4', 7),
    ('3', '6', 4),
    ('4', '5', 1),
    ('4', '6', 2),
    ('4', '7', 5),
    ('5', '7', 8),
    ('6', '7', 5),
]
G.add_nodes_from(nodes)
G.add_weighted_edges_from(edges)

matrix = nx.to_numpy_array(G, nodelist=nodes, weight="weight", dtype=int)
print("Ma trận trọng số:")
print(matrix)
