from dash.dependencies import Input, Output, State
from dash import html, dcc
import dash_cytoscape as cyto
from Graph import Graph
import dash
from utils import get_default_graph_layout
from Graph import deterministic_layout
from ProductionParser import ProductionParser
import base64
import io

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

    @app.callback(
        [Output('graph-l', 'elements'),
         Output('graph-k', 'elements'),
         Output('graph-r', 'elements')],
        [Input('import-productions-button', 'contents')],
        prevent_initial_call=True
    )
    def import_productions(contents):
        if contents is None:
            return dash.no_update, dash.no_update, dash.no_update

        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        content = decoded.decode('utf-8')

        parser = ProductionParser()
        L, K, R = parser.parse_productions(content)
        l_graph = Graph()
        k_graph = Graph()
        r_graph = Graph()
        l_graph.from_nodes_edges(L.nodes, L.edges)
        k_graph.from_nodes_edges(K.nodes, K.edges)
        r_graph.from_nodes_edges(R.nodes, R.edges)
        deterministic_layout(l_graph.graph)
        deterministic_layout(k_graph.graph)
        deterministic_layout(r_graph.graph)


        return l_graph.elements, k_graph.elements, r_graph.elements