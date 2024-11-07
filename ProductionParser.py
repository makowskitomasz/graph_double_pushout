import networkx as nx

class ProductionParser:
    def __init__(self):
        self.graphs = []

    def parse_production(self, production):
        nodes_part, edges_part = production.split(';')
        nodes = eval(nodes_part)
        edges = eval(edges_part)
        
        graph = nx.DiGraph()
        graph.add_nodes_from(nodes)
        graph.add_edges_from(edges)
        
        return graph

    def parse_productions(self, productions):
        lines = productions.strip().split('\n')
        if len(lines) != 3:
            raise ValueError("Input should contain exactly three lines for L, K, and R graphs.")
        
        L = self.parse_production(lines[0])
        K = self.parse_production(lines[1])
        R = self.parse_production(lines[2])
        
        return L, K, R

    def parse_productions_from_file(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        return self.parse_productions(content)