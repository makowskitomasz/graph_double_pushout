import networkx as nx
import matplotlib.pyplot as plt

class SinglePushout:
    def __init__(self):
        # Initialize the graphs
        self.graph_L = nx.DiGraph()  # For the left graph
        self.graph_R = nx.DiGraph()  # For the right graph
        self.graph_K = nx.DiGraph()  # For the interface graph
        self.pushout_graph = nx.DiGraph()  # For the pushout graph
        self.morphism_L_to_K = {}  # Mapping from L to K
        self.morphism_R_to_K = {}  # Mapping from R to K

    def add_edge_L(self, u, v):
        """Add an edge to graph L."""
        self.graph_L.add_edge(u, v)

    def add_edge_R(self, u, v):
        """Add an edge to graph R."""
        self.graph_R.add_edge(u, v)

    def add_edge_K(self, u, v):
        """Add an edge to graph K."""
        self.graph_K.add_edge(u, v)

    def add_morphism_L_to_K(self, u_L, u_K):
        """Add a mapping from node in L to node in K."""
        self.morphism_L_to_K[u_L] = u_K

    def add_morphism_R_to_K(self, u_R, u_K):
        """Add a mapping from node in R to node in K."""
        self.morphism_R_to_K[u_R] = u_K

    def compute_pushout(self):
        """Compute the pushout graph."""
        # Clear the pushout graph
        self.pushout_graph.clear()

        # Add nodes and edges from K to the pushout graph
        for node in self.graph_K.nodes():
            self.pushout_graph.add_node(node)
        for u, v in self.graph_K.edges():
            self.pushout_graph.add_edge(u, v)

        # Add nodes and edges from L to the pushout graph
        for u, v in self.graph_L.edges():
            u_mapped = self.morphism_L_to_K.get(u, u)
            v_mapped = self.morphism_L_to_K.get(v, v)
            self.pushout_graph.add_edge(u_mapped, v_mapped)

        # Add nodes and edges from R to the pushout graph
        for u, v in self.graph_R.edges():
            u_mapped = self.morphism_R_to_K.get(u, u)
            v_mapped = self.morphism_R_to_K.get(v, v)
            self.pushout_graph.add_edge(u_mapped, v_mapped)

        return self.pushout_graph

    def display_graph(self, graph, node_color='lightblue'):
        """Display the graph using Matplotlib (can be replaced with Cytoscape later)."""
        pos = nx.spring_layout(graph)  # Positions for all nodes
        nx.draw(graph, pos, with_labels=True, arrows=True, node_color=node_color)
        plt.show()