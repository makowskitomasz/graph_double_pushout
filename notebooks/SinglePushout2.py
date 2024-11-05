class Graph:
    def __init__(self, nodes, edges, marked_nodes=None, marked_edges=None):
        self.nodes = set(nodes)
        self.edges = set(edges)  # Each edge is a tuple (source, target)
        self.marked_nodes = set(marked_nodes) if marked_nodes else set()
        self.marked_edges = set(marked_edges) if marked_edges else set()

    def add_node(self, node, marked=False):
        self.nodes.add(node)
        if marked:
            self.marked_nodes.add(node)

    def add_edge(self, source, target, marked=False):
        self.edges.add((source, target))
        if marked:
            self.marked_edges.add((source, target))

    def __repr__(self):
        return f"Graph(nodes={self.nodes}, edges={self.edges}, marked_nodes={self.marked_nodes}, marked_edges={self.marked_edges})"
    
class Morphism:
    def __init__(self, node_mapping, edge_mapping):
        self.node_mapping = node_mapping  # Dict mapping nodes from L to nodes in R or G
        self.edge_mapping = edge_mapping  # Dict mapping edges from L to edges in R or G


def single_pushout(graph, rule, occurrence):
    # Extract components from the rule
    L, R, morphism_LR = rule
    morphism_LG = occurrence
    
    # Create new graph H as the pushout of L -> G and L -> R
    H_nodes = {morphism_LG.node_mapping[n] if n in morphism_LG.node_mapping else n for n in R.nodes}
    H_edges = {morphism_LG.edge_mapping[e] if e in morphism_LG.edge_mapping else e for e in R.edges}
    
    # Add nodes and edges from G that are not in the image of L
    for node in graph.nodes:
        if node not in morphism_LG.node_mapping.values():
            H_nodes.add(node)
    for edge in graph.edges:
        if edge not in morphism_LG.edge_mapping.values():
            H_edges.add(edge)
    
    # Mark any leftover nodes/edges from G as "garbage"
    marked_nodes = {node for node in graph.marked_nodes if node not in morphism_LG.node_mapping.values()}
    marked_edges = {edge for edge in graph.marked_edges if edge not in morphism_LG.edge_mapping.values()}
    
    # Return new graph as H (the rewritten graph)
    return Graph(H_nodes, H_edges, marked_nodes, marked_edges)

