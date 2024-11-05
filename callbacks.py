from dash.dependencies import Input, Output, State
from dash import html
import dash_cytoscape as cyto
from Graph import Graph
import dash
from utils import get_default_graph_layout

def register_callbacks(app, base_graph):
    @app.callback(
        Output('main-graph', 'elements'),
        [Input('add-node-button', 'n_clicks'),
         Input('add-edge-button', 'n_clicks'),
         Input('remove-selected-button', 'n_clicks'),
         Input('load-graph-button', 'n_clicks'),
         Input('clear-graph-button', 'n_clicks')],
        [State('main-graph', 'elements'),
         State('main-graph', 'selectedNodeData'),
         State('main-graph', 'selectedEdgeData')]
    )
    def update_graph(n_clicks_node, n_clicks_edge, n_clicks_remove, n_clicks_load, n_clicks_clear, elements, selected_nodes, selected_edges):
        ctx = dash.callback_context
        if not ctx.triggered:
            return elements

        base_graph = Graph()
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'add-node-button':
            base_graph.copy_from(elements)
            node_id = str(len([element for element in base_graph.elements if 'source' not in element['data']]) + 1)
            base_graph.add_node(node_id)
        elif button_id == 'add-edge-button':
            base_graph.copy_from(elements)
            if selected_nodes and len(selected_nodes) >= 2:
                for i in range(len(selected_nodes)):
                    for j in range(i + 1, len(selected_nodes)):
                        source, target = selected_nodes[i]['id'], selected_nodes[j]['id']
                        base_graph.add_edge(source, target)
        elif button_id == 'remove-selected-button':
            base_graph.copy_from(elements)
            base_graph.remove_elements(selected_nodes, selected_edges)
        elif button_id == 'load-graph-button':
            base_graph.from_csv('data/edges.csv')
        elif button_id == 'clear-graph-button':
            base_graph.clear()

        return base_graph.elements

    @app.callback(
        Output('main-graph', 'layout'),
        Input('reset-view-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def reset_graph_view(n_clicks):
        ctx = dash.callback_context
        if ctx.triggered:
            return get_default_graph_layout()
        return dash.no_update