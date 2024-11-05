class ProductionGraphStore:
    def __init__(self):
        self.graphs = []

    def add_graph_pair(self, left_graph, right_graph):
        self.graphs.append([left_graph, right_graph])

    def get_graphs(self):
        return self.graphs