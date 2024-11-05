import base64
import networkx as nx
import numpy as np

def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        return decoded.decode('utf-8')
    except Exception as e:
        return str(e)

def nx_to_cytoscape_elements(G, positions=None):
    elements = []
    new_node_positions = {}
    
    if positions:
        center_x = sum(pos[0] for pos in positions.values()) / len(positions)
        center_y = sum(pos[1] for pos in positions.values()) / len(positions)
        radius_increment = 100

    for node, data in G.nodes(data=True):
        element = {
            'data': {
                'id': node,
                'label': str(node)
            }
        }
        if positions and node in positions.keys():
            element['position'] = {'x': positions[node][0], 'y': positions[node][1]}
        elif positions and node not in positions.keys():
            angle = 2 * np.pi * len(new_node_positions) / (len(G.nodes) - 1 - len(positions))
            radius = radius_increment * (len(new_node_positions) + 1)
            x = center_x + radius * np.cos(angle)
            y = center_y + radius * np.sin(angle)
            new_node_positions[node] = (x, y)
            element['position'] = {'x': x, 'y': y}
        elements.append(element)

    for source, target, data in G.edges(data=True):
        elements.append({
            'data': {
                'source': source,
                'target': target,
                'label': data.get('label', '')
            }
        })
    return elements

def is_subgraph(G, H):
    G_sub = G.subgraph(H.nodes).copy()
    return nx.is_isomorphic(G_sub, H)

def scale_positions(positions, scale_factor):
    center_x = sum(pos[0] for pos in positions.values()) / len(positions)
    center_y = sum(pos[1] for pos in positions.values()) / len(positions)
    
    scaled_positions = {}
    for node, (x, y) in positions.items():
        scaled_x = center_x + (x - center_x) * scale_factor
        scaled_y = center_y + (y - center_y) * scale_factor
        scaled_positions[node] = (scaled_x, scaled_y)
    
    return scaled_positions