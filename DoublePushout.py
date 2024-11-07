import networkx as nx

class DoublePushout:
    def __init__(self, G, L, K, R):
        self.G = nx.MultiDiGraph(G)  # Original graph G
        self.L = nx.MultiDiGraph(L)  # Left graph L
        self.K = nx.MultiDiGraph(K)  # Interface graph K
        self.R = nx.MultiDiGraph(R)  # Right graph R
        self.morphism = {}  # Morphism dictionary

    def define_morphism(self, L_to_G_mapping):
        self.morphism = L_to_G_mapping

    def calculate_mL_minus_mK(self):
        mL_nodes = set(self.morphism.values())
        mK_nodes = {self.morphism[n] for n in self.K.nodes if n in self.morphism}
        mL_minus_mK_nodes = mL_nodes - mK_nodes
        mL_minus_mK = self.G.subgraph(mL_minus_mK_nodes).copy()
        return mL_minus_mK

    def calculate_Z(self, mL_minus_mK):
        Z = self.G.copy()
        Z.remove_nodes_from(mL_minus_mK.nodes)
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