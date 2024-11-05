import re
from Graph import Graph

class ProductionParser:
    def __init__(self):
        self.graphs = []

    def parse_production(self, production):
        graph = Graph()
        reversed = False
        if '<-' in production:
            reversed = True 
        labels = re.findall(r'-[a-zA-Z]-', production)
        connections = re.split(r'->|<-|-[a-zA-Z]->|<-[a-zA-Z]-', production)
        if len(connections) == 1:
            graph.add_node(connections[0])
        for i in range(len(connections) - 1):
            if reversed:
                source = connections[i + 1].strip()
                target = connections[i].strip()
            else:
                source = connections[i].strip()
                target = connections[i + 1].strip()
            if i < len(labels):
                label = labels[i].strip('-')
                graph.add_edge(source, target, label)
            else:
                graph.add_edge(source, target)
        self.graphs.append(graph)

    def parse_productions(self, productions):
        self.graphs = []
        for production in productions.split('\n'):
            production = production.strip()
            if production:
                self.parse_production(production)

    def get_graphs(self):
        return self.graphs