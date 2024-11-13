import dash
from Graph import Graph
from new_layout import layout
from callbacks import register_callbacks

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True 

base_graph = Graph()
base_graph.from_csv('data/edges.csv')
base_graph_elements = base_graph.to_cyto_elements()

register_callbacks(app, base_graph)

# app.layout = create_layout(base_graph_elements)
app.layout = layout()

if __name__ == '__main__':
    app.run_server(debug=True)