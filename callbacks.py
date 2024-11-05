from dash.dependencies import Input, Output, State
from dash import html
import dash_cytoscape as cyto
from ProductionParser import ProductionParser
from production_graph_store import ProductionGraphStore
from utils import parse_contents, nx_to_cytoscape_elements, is_subgraph, scale_positions
import dash

production_parser = ProductionParser()
graph_store = ProductionGraphStore()

def register_callbacks(app, base_graph):
    @app.callback(
        [Output('first-line', 'children'),
         Output('second-line', 'children'),
         Output('first-line-store', 'data'),
         Output('second-line-store', 'data'),
         Output('add-production-button', 'disabled')],
        Input('upload-data', 'contents')
    )
    def update_graphs_from_upload(contents):
        if contents:
            content_string = parse_contents(contents)
            lines = content_string.split('\n')
            first_line_text = lines[0] if len(lines) > 0 else ''
            second_line_text = lines[1] if len(lines) > 1 else ''

            production_parser.parse_productions(content_string)
            parsed_graphs = production_parser.get_graphs()
            for i in range(0, len(parsed_graphs), 2):
                left_graph = parsed_graphs[i]
                right_graph = parsed_graphs[i + 1] if i + 1 < len(parsed_graphs) else None
                graph_store.add_graph_pair(left_graph, right_graph)

            scaled_positions = scale_positions(base_graph.positions, scale_factor=0.5)
            first_graph_elements = nx_to_cytoscape_elements(parsed_graphs[0].graph, scaled_positions)
            print(parsed_graphs[0].graph)
            print(parsed_graphs[0].graph.nodes)
            second_graph_elements = nx_to_cytoscape_elements(parsed_graphs[1].graph, scaled_positions)

            first_graph = create_cytoscape_graph('first-graph', first_graph_elements)
            second_graph = create_cytoscape_graph('second-graph', second_graph_elements)

            return first_graph, second_graph, first_line_text, second_line_text, False

        return '', '', '', '', True

    @app.callback(
        Output('production-list', 'children'),
        Input('add-production-button', 'n_clicks'),
        State('first-line-store', 'data'),
        State('second-line-store', 'data'),
        State('production-list', 'children')
    )
    def add_to_production_list(n_clicks, first_line, second_line, current_list):
        if n_clicks is not None and n_clicks > 0 and first_line and second_line:
            new_entry = html.Div([
                html.Div(first_line, style={'display': 'inline-block', 'width': '50%'}),
                html.Div(second_line, style={'display': 'inline-block', 'width': '50%'})
            ])
            if not current_list:
                current_list = []
            current_list.append(new_entry)
            return current_list
        return current_list

    @app.callback(
        Output('production-list-1', 'children'),
        Input('transformation-list-finish', 'n_clicks'),
        State('production-list', 'children')
    )
    def display_current_list(n_clicks, current_list):
        if n_clicks is not None and n_clicks > 0 and current_list:
            return current_list
        return []

    @app.callback(
        Output('base-graph', 'elements'),
        [Input('add-node-button', 'n_clicks'),
         Input('add-edge-button', 'n_clicks'),
         Input('remove-node-button', 'n_clicks'),
         Input('remove-edge-button', 'n_clicks')],
        [State('base-graph', 'elements')]
    )
    def update_graph(add_node_clicks, add_edge_clicks, remove_node_clicks, remove_edge_clicks, elements):
        ctx = dash.callback_context

        if not ctx.triggered:
            return elements

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'add-node-button':
            new_node_id = f'N-{len(elements) + 1}'
            base_graph.add_node(new_node_id)
        elif button_id == 'add-edge-button':
            if len(base_graph.nodes) >= 2:
                source = base_graph.nodes[-2]
                target = base_graph.nodes[-1]
                base_graph.add_edge(source, target)
        elif button_id == 'remove-node-button':
            if base_graph.nodes:
                node_to_remove = base_graph.nodes[-1]
                base_graph.remove_node(node_to_remove)
        elif button_id == 'remove-edge-button':
            if base_graph.edges:
                edge_to_remove = base_graph.edges[-1]
                base_graph.remove_edge(edge_to_remove[0], edge_to_remove[1])

        return base_graph.to_cyto_elements()

def create_cytoscape_graph(graph_id, elements):
    """Helper function to create a Cytoscape graph layout."""
    return cyto.Cytoscape(
        id=graph_id,
        elements=elements,
        style={'width': '100%', 'height': '100%'},
        layout={'name': 'preset'},
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'width': '15px',
                    'height': '15px',
                    'label': 'data(label)',
                    'font-size': '15px'
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'width': 1,
                    'line-color': '#ccc',
                    'target-arrow-shape': 'triangle',
                    'target-arrow-color': '#ccc',
                    'arrow-scale': 2,
                    'curve-style': 'bezier'
                }
            }
        ]
    )