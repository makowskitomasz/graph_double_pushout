# GRAPH.PY
import pandas as pd
import networkx as nx
import numpy as np
import random

class Graph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.positions = {}
        self.elements = []

    def get_elements_data(self):
        return [element['data'] for element in self.elements]
    
    def add_node(self, node_id, label=None, position=None, locked=False, **attrs):
        self.graph.add_node(node_id, label=label, **attrs)
        if position:
            self.positions[node_id] = (position['x'], position['y'])
        else:
            self.positions[node_id] = calculate_position_of_new_node(self)
        self.elements.append({
            'data': {'id': node_id, 'label': label or node_id},
            'position': {'x': self.positions[node_id][0], 'y': self.positions[node_id][1]},
            'locked': locked
        })

    def add_edge(self, source, target, label=None):
        if source in self.graph.nodes() and target in self.graph.nodes():
            edge_id = f"{source}-{target}"
            self.graph.add_edge(source, target, label=label)
            self.elements.append({
                'data': {
                    'id': edge_id,
                    'source': source,
                    'target': target,
                    'label': label
                }
            })

    def remove_node(self, node_id):
        if node_id in self.graph:
            self.graph.remove_node(node_id)
            self.elements = [el for el in self.elements if el['data']['id'] != node_id]

    def remove_edge(self, source, target):
        if self.graph.has_edge(source, target):
            self.graph.remove_edge(source, target)
            edge_id = f"{source}-{target}"
            self.elements = [el for el in self.elements if el['data']['id'] != edge_id]

    def from_nodes_edges(self, nodes, edges, label_dict=None):
        self.graph.add_nodes_from(nodes)
        self.graph.add_edges_from(edges)
        self.positions = deterministic_layout(self.graph)
        self.elements = self.to_cyto_elements(label_dict)

    def multi_digraph_from_nodes_edges(self, nodes, edges, label_dict=None):
        self.graph = nx.MultiDiGraph()
        self.graph.add_nodes_from(nodes)
        self.graph.add_edges_from(edges)
        self.positions = deterministic_layout(self.graph)
        self.elements = self.to_cyto_elements(label_dict)

    def from_csv(self, file_path):
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            self.add_node(row['source_id'], label=row['source_label'])
            if pd.isna(row['target_id']):
                continue
            self.add_node(row['target_id'], label=row['target_label'])
            self.add_edge(row['source_id'], row['target_id'])
        self.positions = deterministic_layout(self.graph)
        self.elements = self.to_cyto_elements()

    def to_cyto_elements(self, label_dict=None):
        cyto_elements = []
        for node, pos in self.positions.items():
            cyto_elements.append({
                'data': {'id': node, 'label': label_dict[node] if label_dict else self.graph.nodes[node].get('label', node)},
                'position': {'x': pos[0], 'y': pos[1]}
            })
        for edge in self.graph.edges(data=True):
            cyto_elements.append({
                'data': {
                    'source': edge[0],
                    'target': edge[1],
                    'label': edge[2].get('label', '')
                }
            })
        return cyto_elements

    def is_subgraph(self, subgraph):
        return nx.is_isomorphic(self.graph, subgraph.graph, node_match=lambda n1, n2: n1['label'] == n2['label'], edge_match=lambda e1, e2: e1.get('label') == e2.get('label'))
    
    def clear(self):
        self.graph.clear()
        self.positions.clear()
        self.elements.clear()

    def copy_from(self, elements):
        self.clear()
        for el in elements:
            if 'source' in el['data']:
                self.add_edge(el['data']['source'], el['data']['target'], el['data'].get('label'))
            else:
                if 'locked' in el:
                    self.add_node(el['data']['id'], label=el['data'].get('label'), position=el['position'], locked=el['locked'])
                else:
                    self.add_node(el['data']['id'], label=el['data'].get('label'), position=el['position'])

    
    def remove_elements(self, selected_nodes, selected_edges):
        if selected_nodes is not None:
            for node in selected_nodes:
                self.remove_node(node['id'])
        if selected_edges is not None:
            for edge in selected_edges:
                self.remove_edge(edge['source'], edge['target'])


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


def calculate_position_of_new_node(G):
    num_nodes = len(G.elements)
    radius = 500
    center_x, center_y = 0, 0

    def calculate_minimum_distance(G, _x, _y):
        min_distance = float('inf')
        for node, (x, y) in G.positions.items():
            distance = np.sqrt((_x - x) ** 2 + (_y - y) ** 2)
            if distance < min_distance:
                min_distance = distance
        return min_distance

    if num_nodes == 0:
        return center_x - radius, center_y - radius

    max_distance = 0
    best_position = (center_x, center_y)
    for angle in np.linspace(0, 2 * np.pi, 360):
        x = center_x + radius * np.cos(angle)
        y = center_y + radius * np.sin(angle)
        distance = calculate_minimum_distance(G, x, y)
        if distance > max_distance:
            max_distance = distance
            best_position = (x, y)
    
    if max_distance < 50:
        radius = random.randint(300, 600)
        max_distance = 0
        best_position = (center_x, center_y)
        for angle in np.linspace(0, 2 * np.pi, 360):
            x = center_x + radius * np.cos(angle)
            y = center_y + radius * np.sin(angle)
            distance = calculate_minimum_distance(G, x, y)
            if distance > max_distance:
                max_distance = distance
                best_position = (x, y)

    return best_position