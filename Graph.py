import pandas as pd
import networkx as nx
import numpy as np
import random

class Graph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.positions = {}
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.graph.add_node(node)
        self.positions[node] = position_next_node(self)
        self.nodes = list(self.graph.nodes)
        self.edges = list(self.graph.edges)

    def add_edge(self, source, target, label=None):
        if label:
            self.graph.add_edge(source, target, label=label)
        else:
            self.graph.add_edge(source, target)
        self.nodes = list(self.graph.nodes)
        self.edges = list(self.graph.edges)

    def remove_node(self, node):
        if node in self.graph:
            self.graph.remove_node(node)
        self.nodes = list(self.graph.nodes)
        self.edges = list(self.graph.edges)

    def remove_edge(self, source, target):
        if self.graph.has_edge(source, target):
            self.graph.remove_edge(source, target)
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

def position_next_node(G):
    num_nodes = len(G.nodes) + 1
    radius = 500
    def calculate_distance_to_the_closest(G, _x, _y):
        distances = []
        for node in G.nodes:
            x, y = G.positions[node]
            distance = np.sqrt((_x - x) ** 2 + (_y - y) ** 2)
            distances.append(distance)
        return min(distances)
    
    center_x, center_y = 0, 0
    i = 0
    while i < 100:
        radius_variation = random.randint(0, 100)
        next_angle = radius_variation * np.pi * (num_nodes - 1) / num_nodes
        next_x = center_x + radius * np.cos(next_angle)
        next_y = center_y + radius * np.sin(next_angle)
        i += 1
        min_distance = calculate_distance_to_the_closest(G, next_x, next_y)
        if min_distance > 100:
            break

    if i == 100:
        radius = random.randint(100, 600)
        i = 0
        while i < 100:
            radius_variation = random.randint(0, 100)
            next_angle = radius_variation * np.pi * (num_nodes - 1) / num_nodes
            next_x = center_x + radius * np.cos(next_angle)
            next_y = center_y + radius * np.sin(next_angle)
            i += 1
            min_distance = calculate_distance_to_the_closest(G, next_x, next_y)
            if min_distance > 100:
                break
        
    return (next_x, next_y)
