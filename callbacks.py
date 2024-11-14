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
from networkx.algorithms.isomorphism import DiGraphMatcher
import networkx as nx

def register_callbacks(app, base_graph):
    descriptions = [
        "Base Graph (G)",
        "Base Graph (G) with highlighted  m(L)",
        "Base Graph (G) with highlighted m(L) - m(K)",
        "Graph Z after removing m(L) - m(K)",
        "Final Graph G with highlighted  m(R) - m(K)'",
        "Final Graph G'",
    ]
    
    @app.callback(
        [Output('main-graph', 'elements'),
         Output('main-graph-data', 'data'),
         Output('graph-description', 'children'),
         Output('feedback', 'children'),
         Output('next-step-button', 'disabled'),
         Output('previous-step-button', 'disabled'),
         Output('graph-l', 'elements'),
         Output('graph-k', 'elements'),
         Output('graph-r', 'elements'),
         Output('import-productions-button', 'contents'),
         Output('apply-production-button', 'disabled')],
        [Input('add-node-button', 'n_clicks'),
         Input('add-edge-button', 'n_clicks'),
         Input('remove-selected-button', 'n_clicks'),
         Input('load-graph-button', 'n_clicks'),
         Input('clear-graph-button', 'n_clicks'),
         Input('apply-production-button', 'n_clicks'),
         Input('next-step-button', 'n_clicks'),
         Input('previous-step-button', 'n_clicks'),
         Input('remove-production-button', 'n_clicks'),
         Input('remove-all-productions-button', 'n_clicks'),
         Input('import-productions-button', 'contents')],
        [State('main-graph', 'elements'),
         State('main-graph', 'selectedNodeData'),
         State('main-graph', 'selectedEdgeData'),
         State('graph-l', 'elements'),
         State('graph-k', 'elements'),
         State('graph-r', 'elements'),
         State('main-graph-data', 'data')],
    )
    def update_graph(n_clicks_node, n_clicks_edge, n_clicks_remove, n_clicks_load, n_clicks_clear, n_clicks_apply, n_clicks_next, n_clicks_prev, n_clicks_remove_prod, n_clicks_remove_all, contents, elements, selected_nodes, selected_edges, l_elements, k_elements, r_elements, graph_data):
        ctx = dash.callback_context
        if not ctx.triggered:
            return elements, graph_data, "", "", True, True, l_elements, k_elements, r_elements, dash.no_update, True

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'add-node-button':
            base_graph.copy_from(elements)
            node_id = str(len([element for element in base_graph.elements if 'source' not in element['data']]) + 1)
            base_graph.add_node(node_id)
            return base_graph.elements, graph_data, descriptions[0], "", True, True, l_elements, k_elements, r_elements, dash.no_update, False

        elif button_id == 'add-edge-button':
            base_graph.copy_from(elements)
            if selected_nodes and len(selected_nodes) >= 2:
                for i in range(len(selected_nodes)):
                    for j in range(i + 1, len(selected_nodes)):
                        source, target = selected_nodes[i]['id'], selected_nodes[j]['id']
                        base_graph.add_edge(source, target)
            return base_graph.elements, graph_data, descriptions[0], "", True, True, l_elements, k_elements, r_elements, dash.no_update, False

        elif button_id == 'remove-selected-button':
            base_graph.copy_from(elements)
            base_graph.remove_elements(selected_nodes, selected_edges)
            return base_graph.elements, graph_data, descriptions[0], "", True, True, l_elements, k_elements, r_elements, dash.no_update, False

        elif button_id == 'load-graph-button':
            from app import GRAPH_FILE_PATH
            base_graph.from_csv(GRAPH_FILE_PATH)
            base_graph.elements = add_lock_to_all_graph_elements(base_graph.elements)
            return base_graph.elements, graph_data, descriptions[0], "", True, True, l_elements, k_elements, r_elements, dash.no_update, False

        elif button_id == 'clear-graph-button':
            base_graph.clear()
            return base_graph.elements, graph_data, descriptions[0], "", True, True, l_elements, k_elements, r_elements, dash.no_update, True

        elif button_id == 'apply-production-button':
            base_graph.copy_from(elements)

            L = Graph()
            L.copy_from(l_elements)

            K = Graph()
            K.copy_from(k_elements)

            R = Graph()
            R.copy_from(r_elements)

            dpo = DoublePushout(base_graph.graph, L.graph, K.graph, R.graph)

            if all(edge in base_graph.graph.edges() for edge in L.graph.edges()):
                morphism = {}
                for node in L.elements:
                    if 'source' in node['data']:
                        continue
                    morphism[node['data']['id']] = node['data']['id']
                dpo.define_morphism(morphism)
            else:
                return dash.no_update, dash.no_update, "Please check the input graphs. Cannot apply the DPO production.", "Please check the input graphs. Cannot apply the DPO production.", True, True, l_elements, k_elements, r_elements, dash.no_update, False   

            mL_minus_mK = dpo.calculate_mL_minus_mK()
            graph_mL_minus_mK = Graph()
            graph_mL_minus_mK.multi_digraph_from_nodes_edges(mL_minus_mK.nodes, mL_minus_mK.edges)
            graph_mL_minus_mK.elements = add_lock_to_all_graph_elements(graph_mL_minus_mK.elements)

            Z = dpo.calculate_Z(mL_minus_mK)
            graph_Z = Graph()
            graph_Z.multi_digraph_from_nodes_edges(Z.nodes, Z.edges)
            graph_Z.elements = add_lock_to_all_graph_elements(graph_Z.elements)

            mR_minus_mK = dpo.calculate_mR_minus_mK()
            graph_mR_minus_mK = Graph()
            graph_mR_minus_mK.multi_digraph_from_nodes_edges(mR_minus_mK.nodes, mR_minus_mK.edges)
            graph_mR_minus_mK.elements = add_lock_to_all_graph_elements(graph_mR_minus_mK.elements)

            G_prime = dpo.create_G_prime(Z, mR_minus_mK)
            graph_G_prime = Graph()
            graph_G_prime.multi_digraph_from_nodes_edges(G_prime.nodes, G_prime.edges)
            graph_G_prime.elements = add_lock_to_all_graph_elements(graph_G_prime.elements)


            G_highlight_L = highlit_subgraf_in_graph(base_graph.elements, L.elements, 'added')
            G_highlight_L_minus_K = highlit_left_elements_which_does_not_exist_in_right(base_graph.elements, graph_Z.elements, 'to-remove')
            G_prime_highlited_mR_minus_mK = highlit_left_elements_which_does_not_exist_in_right(graph_G_prime.elements, graph_Z.elements, 'added')

            G_highlight_L = add_lock_to_all_graph_elements(G_highlight_L)
            G_highlight_L_minus_K = add_lock_to_all_graph_elements(G_highlight_L_minus_K)
            G_prime_highlited_mR_minus_mK = add_lock_to_all_graph_elements(G_prime_highlited_mR_minus_mK)

            if not nx.is_weakly_connected(Z) or not nx.is_weakly_connected(G_prime):
                return dash.no_update, dash.no_update, "Please check the input graphs. Cannot apply the DPO production.", "Please check the input graphs. Cannot apply the DPO production.", True, True, l_elements, k_elements, r_elements, dash.no_update, False            

            graph_elements = [base_graph.elements, G_highlight_L, G_highlight_L_minus_K, graph_Z.elements, G_prime_highlited_mR_minus_mK, graph_G_prime.elements]

            graph_elements = [fill_classes_as_empty_if_does_not_exist(i) for i in graph_elements]                
            graph_data = {'current_index': 0, 'graphs': graph_elements}
            return graph_elements[0], graph_data, descriptions[0], "", False, True, l_elements, k_elements, r_elements, dash.no_update, False

        elif button_id == 'next-step-button' or button_id == 'previous-step-button':
            def can_go_backward(graph_data):
                return graph_data['current_index'] > 0
            def can_go_forward(graph_data):
                return graph_data['current_index'] < len(graph_data['graphs']) - 1

            if graph_data is None or 'graphs' not in graph_data:
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, True, True, l_elements, k_elements, r_elements, dash.no_update, False

            current_index = graph_data['current_index']
            graphs = graph_data['graphs']

            if button_id == 'next-step-button' and current_index + 1 < len(graphs):
                current_index = (current_index + 1)
            elif button_id == 'previous-step-button' and current_index - 1 >= 0:
                current_index = (current_index - 1)

            graph_data['current_index'] = current_index
            return graphs[current_index], graph_data, descriptions[current_index], "", not can_go_forward(graph_data), not can_go_backward(graph_data), l_elements, k_elements, r_elements, dash.no_update, False

        elif button_id == 'remove-production-button':
            if base_graph.elements:
                return base_graph.elements, {'current_index': 0, 'graphs': [base_graph.elements]}, descriptions[0], "", True, True, [], [], [], dash.no_update, True
            else:
                return [], {'current_index': 0, 'graphs': []}, "", "", True, True, [], [], [], dash.no_update, True

        elif button_id == 'remove-all-productions-button':
            return [], {'current_index': 0, 'graphs': []}, "", "", True, True, [], [], [], dash.no_update, True

        elif button_id == 'import-productions-button':
            if contents is None:
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, True

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
            
            l_highlighted = highlit_left_elements_which_does_not_exist_in_right(l_graph.elements, k_graph.elements, 'to-remove')
            r_highlighted = highlit_left_elements_which_does_not_exist_in_right(r_graph.elements, k_graph.elements, 'added')

            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, l_highlighted, k_graph.elements, r_highlighted, "", False

        return dash.no_update, dash.no_update, "", "", True, True, l_elements, k_elements, r_elements, dash.no_update, True

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

def highlit_subgraf_in_graph(base_graph_elements, subgraph_elements, tag):
    output_elements = []
    for element in base_graph_elements:
        element_copy = element.copy()
        element_copy['classes'] = ''
        if element_copy['data'] in [i['data'] for i in subgraph_elements]:
            if 'classes' in element_copy.keys():
                element_copy['classes'] += f' {tag}'
            else:
                element_copy['classes'] = f' {tag}'
        output_elements.append(element_copy)
    return output_elements

def highlit_left_elements_which_does_not_exist_in_right(left_graph_elements, right_graph_elements, tag):
    output_elements = []
    right_edges = [[right_element['data']['source'], right_element['data']['target']] for right_element in right_graph_elements if ('source' in right_element['data'].keys())]
    for element in left_graph_elements:
        element_copy = element.copy()
        element_copy['classes'] = ''
        left_edge = []
        if 'source' in element_copy['data'].keys():
            left_edge = [element_copy['data']['source'], element_copy['data']['target']]

        if len(left_edge) != 0 and left_edge in right_edges:
            output_elements.append(element_copy)
            continue

        if element_copy['data'] in [i['data'] for i in right_graph_elements]:
            output_elements.append(element_copy)
            continue
        if 'classes' in element_copy.keys():
            element_copy['classes'] += f' {tag}'
        else:
            element_copy['classes'] = f' {tag}'

        output_elements.append(element_copy)
    return output_elements

def highlit_left_elements_which_exist_in_right(left_graph_elements, right_graph_elements, tag):
    output_elements = []
    right_edges = [[right_element['data']['source'], right_element['data']['target']] for right_element in right_graph_elements if ('source' in right_element['data'].keys())]
    for element in left_graph_elements:
        element_copy = element.copy()
        element_copy['classes'] = ''
        left_edge = []
        if 'source' in element_copy['data'].keys():
            left_edge = [element_copy['data']['source'], element_copy['data']['target']]
        if element_copy['data'] in [i['data'] for i in right_graph_elements] or left_edge in right_edges:
            if 'classes' in element_copy.keys():
                element_copy['classes'] += f' {tag}'
            else:
                element_copy['classes'] = f' {tag}'
        output_elements.append(element_copy)
    return output_elements

def fill_classes_as_empty_if_does_not_exist(elements):
    for i, x in enumerate(elements):
        if 'classes' not in x.keys():
             elements[i]['classes'] = ''
    return elements

def add_lock_to_all_graph_elements(elements):
    new_elements = []
    for i in elements:
        z = i.copy()
        z['locked'] = True
        new_elements.append(z)
    return new_elements