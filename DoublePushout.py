import networkx as nx
from networkx.algorithms.isomorphism import DiGraphMatcher

class DoublePushout:
    def __init__(self, G, L, K, R):
        self.G = nx.MultiDiGraph(G)  # Original graph G
        self.L = nx.MultiDiGraph(L)  # Left graph L
        self.K = nx.MultiDiGraph(K)  # Interface graph K
        self.R = nx.MultiDiGraph(R)  # Right graph R
        self.morphism = {}  # Morphism dictionary

    def define_morphism(self):
        def node_match(n1, n2):
            return n1['label'] == n2['label']

        matcher = DiGraphMatcher(self.G, self.L, node_match=node_match)
        if matcher.subgraph_is_isomorphic():
            self.morphism = {L_node: G_node for G_node, L_node in matcher.mapping.items()}
            self.mL = nx.relabel_nodes(self.L, self.morphism).copy()
            self.mK = nx.relabel_nodes(self.K, self.morphism).copy()
            self.mR = nx.relabel_nodes(self.R, self.morphism).copy()
        else:
            raise ValueError("No isomorphic subgraph found")

    def calculate_mL_minus_mK(self):
        mL_minus_mK_nodes = list(self.mL.nodes - self.mK.nodes)
        self.nodes_to_remove = mL_minus_mK_nodes
        self.edges_to_remove = list()
        mL_minus_mK = self.G.subgraph(mL_minus_mK_nodes).copy()
        L_subgraph_from_K_nodes = self.mL.subgraph(self.mK.nodes).copy()
        for edge in L_subgraph_from_K_nodes.edges:
            if edge not in self.mK.edges:
                self.edges_to_remove.append(edge)
                mL_minus_mK.add_edge(edge[0], edge[1], edge[2])
        return mL_minus_mK

    def calculate_Z(self, mL_minus_mK):
        Z = self.G.copy()
        Z.remove_nodes_from(self.nodes_to_remove)
        Z.remove_edges_from(self.edges_to_remove)
        return Z

    def calculate_mR_minus_mK(self):
        mK_nodes = set(self.K.nodes)
        mR_minus_mK_nodes = [node for node in self.R.nodes if node not in mK_nodes]
        mR_minus_mK = self.R.subgraph(mR_minus_mK_nodes).copy()
        return mR_minus_mK

    def create_G_prime(self, Z, mR_minus_mK):
        edges_to_add = list()
        for edge in self.R.edges:
            source, target, frequency = edge
            if (source in mR_minus_mK.nodes or target in mR_minus_mK.nodes) and edge not in mR_minus_mK.edges:
                edges_to_add.append(edge)

        for index, edge in enumerate(edges_to_add):
            source, target, frequency = edge
            if source in self.morphism.keys():
                source = self.morphism[source]
            if target in self.morphism.keys():
                target = self.morphism[target]
            edges_to_add[index] = (source, target)

        self.G_prime = nx.compose(Z, mR_minus_mK)
        self.G_prime.add_edges_from(edges_to_add)
        return self.G_prime