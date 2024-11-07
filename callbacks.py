from dash.dependencies import Input, Output, State
from dash import html, dcc
import dash_cytoscape as cyto
from Graph import Graph
import dash
from utils import get_default_graph_layout
from Graph import deterministic_layout
from ProductionParser import ProductionParser
from DoublePushout import DoublePushout
import base64
import io

def register_callbacks(app, base_graph):
    @app.callback(
        [Output('main-graph', 'elements'),
         Output('main-graph-data', 'data'),
         Output('graph-description', 'children')],
        [Input('add-node-button', 'n_clicks'),
         Input('add-edge-button', 'n_clicks'),
         Input('remove-selected-button', 'n_clicks'),
         Input('load-graph-button', 'n_clicks'),
         Input('clear-graph-button', 'n_clicks'),
         Input('apply-production-button', 'n_clicks'),
         Input('next-step-button', 'n_clicks'),
         Input('previous-step-button', 'n_clicks')],
        [State('main-graph', 'elements'),
         State('main-graph', 'selectedNodeData'),
         State('main-graph', 'selectedEdgeData'),
         State('graph-l', 'elements'),
         State('graph-k', 'elements'),
         State('graph-r', 'elements'),
         State('main-graph-data', 'data')]
    )
    def update_graph(n_clicks_node, n_clicks_edge, n_clicks_remove, n_clicks_load, n_clicks_clear, n_clicks_apply, n_clicks_next, n_clicks_prev, elements, selected_nodes, selected_edges, l_elements, k_elements, r_elements, graph_data):
        ctx = dash.callback_context
        if not ctx.triggered:
            return elements, graph_data, ""

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        descriptions = [
            "Base Graph (G)",
            "m(L) - m(K): Nodes to be removed",
            "Graph Z after removing m(L) - m(K)",
            "m(R) - m(K): Nodes and edges to be added",
            "Final Graph G'"
        ]

        if button_id == 'add-node-button':
            base_graph.copy_from(elements)
            node_id = str(len([element for element in base_graph.elements if 'source' not in element['data']]) + 1)
            base_graph.add_node(node_id)
            return base_graph.elements, graph_data, descriptions[0]

        elif button_id == 'add-edge-button':
            base_graph.copy_from(elements)
            if selected_nodes and len(selected_nodes) >= 2:
                for i in range(len(selected_nodes)):
                    for j in range(i + 1, len(selected_nodes)):
                        source, target = selected_nodes[i]['id'], selected_nodes[j]['id']
                        base_graph.add_edge(source, target)
            return base_graph.elements, graph_data, descriptions[0]

        elif button_id == 'remove-selected-button':
            base_graph.copy_from(elements)
            base_graph.remove_elements(selected_nodes, selected_edges)
            return base_graph.elements, graph_data, descriptions[0]

        elif button_id == 'load-graph-button':
            base_graph.from_csv('data/edges.csv')
            return base_graph.elements, graph_data, descriptions[0]

        elif button_id == 'clear-graph-button':
            base_graph.clear()
            return base_graph.elements, graph_data, descriptions[0]

        elif button_id == 'apply-production-button':
            base_graph.copy_from(elements)

            L = Graph()
            L.copy_from(l_elements)

            K = Graph()
            K.copy_from(k_elements)

            R = Graph()
            R.copy_from(r_elements)

            dpo = DoublePushout(base_graph.graph, L.graph, K.graph, R.graph)
            dpo.define_morphism({'A': 'A', 'B': 'G', 'C': 'G'})

            mL_minus_mK = dpo.calculate_mL_minus_mK()
            Z = dpo.calculate_Z(mL_minus_mK)
            mR_minus_mK = dpo.calculate_mR_minus_mK()
            G_prime = dpo.create_G_prime(Z, mR_minus_mK)

            graphs = [base_graph.graph, mL_minus_mK, Z, mR_minus_mK, G_prime]
            graph_elements = []
            for i, g in enumerate(graphs):
                tmp_graph = Graph()
                if i == 0:
                    tmp_graph.from_nodes_edges(g.nodes, g.edges)
                else:
                    tmp_graph.multi_digraph_from_nodes_edges(g.nodes, g.edges)
                graph_elements.append(tmp_graph.elements)
                
            graph_data = {'current_index': 0, 'graphs': graph_elements}
            return graph_elements[0], graph_data, descriptions[0]

        elif button_id in ['next-step-button', 'previous-step-button']:
            if graph_data is None or 'graphs' not in graph_data:
                return dash.no_update, dash.no_update, dash.no_update

            current_index = graph_data['current_index']
            graphs = graph_data['graphs']

            if button_id == 'next-step-button':
                current_index = (current_index + 1) % len(graphs)
            elif button_id == 'previous-step-button':
                current_index = (current_index - 1) % len(graphs)

            graph_data['current_index'] = current_index
            return graphs[current_index], graph_data, descriptions[current_index]

        return dash.no_update, dash.no_update, ""

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