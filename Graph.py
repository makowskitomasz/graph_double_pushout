import pandas as pd
import networkx as nx
import numpy as np

class Graph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.positions = {}
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.graph.add_node(node)
        self.nodes = list(self.graph.nodes)
        self.edges = list(self.graph.edges)

    def add_edge(self, source, target, label=None):
        if label:
            self.graph.add_edge(source, target, label=label)
        else:
            self.graph.add_edge(source, target)
        self.nodes = list(self.graph.nodes)
        self.edges = list(self.graph.edges)

    def from_csv(self, file_path):
        df = pd.read_csv(file_path)
        self.graph = nx.from_pandas_edgelist(df, 'source', 'target', create_using=nx.DiGraph())
        self.positions = deterministic_layout(self.graph)
        self.nodes = list(self.graph.nodes)
        self.edges = list(self.graph.edges)

    def to_cyto_elements(self, graph=None, positions=None):
        if graph is None:
            graph = self.graph
        if positions is None:
            positions = self.positions
        cyto_elements = []
        for node, pos in positions.items():
            cyto_elements.append({
                'data': {'id': node, 'label': node},
                'position': {'x': pos[0], 'y': pos[1]}
            })
        for edge in graph.edges(data=True):
            cyto_elements.append({
                'data': {
                    'source': edge[0], 
                    'target': edge[1],
                    'label': edge[2].get('label', '')
                }
            })
        return cyto_elements

    def is_subgraph(self, subgraph):
        return nx.is_isomorphic(self.graph, subgraph.graph, edge_match=lambda e1, e2: e1.get('label') == e2.get('label'))

def deterministic_layout(G):
    positions = {}
    nodes = list(G.nodes)
    num_nodes = len(nodes)
    
    if num_nodes == 0:
        return positions

    radius = 500
    center_x, center_y = 0, 0

    for i, node in enumerate(nodes):
        angle = 2 * np.pi * i / num_nodes
        x = center_x + radius * np.cos(angle)
        y = center_y + radius * np.sin(angle)
        positions[node] = (x, y)
    
    return positions

def calculate_position_of_new_node(G: Graph):
    num_nodes = len(G.nodes)
    radius = 500
    center_x, center_y = 0, 0
    angle = 2 * np.pi * num_nodes / (num_nodes + 1)
    x = center_x + radius * np.cos(angle)
    y = center_y + radius * np.sin(angle)
    return x, y