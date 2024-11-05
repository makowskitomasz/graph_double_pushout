from dash import html, dcc, Input, Output, callback
import dash_cytoscape as cyto

def create_layout(base_graph_elements):
    return html.Div([
        dcc.Store(id='graph-elements-store', data=base_graph_elements),
        dcc.Store(id='first-line-store'),
        dcc.Store(id='second-line-store'),

        html.Div(style={'backgroundColor': '#f0f0f0', 'width': '96vw', 'height': '96vh', 'position': 'relative'}),

        # Cytoscape component to display the base graph
        cyto.Cytoscape(
            id='base-graph',
            elements=base_graph_elements,
            style={
                'width': '35vw',
                'height': '70vh',
                'position': 'absolute',
                'left': '2vw',
                'top': '5vh',
                'border': '2px solid #ccc'
            },
            layout={'name': 'preset'},
            stylesheet=[
                {
                    'selector': 'node',
                    'style': {
                        'width': '15px',
                        'height': '15px',
                        'label': 'data(label)'
                    }
                },
                {
                    'selector': 'edge',
                    'style': {
                        'width': 2,
                        'line-color': '#ccc',
                        'target-arrow-shape': 'triangle',
                        'target-arrow-color': '#ccc',
                        'curve-style': 'bezier'
                    }
                }
            ]
        ),
        
        # Container for buttons
        html.Div([
            html.Button("Add node", id="add-node-button", n_clicks=0, style={'margin': '5px'}),
            html.Button("Add edge", id="add-edge-button", n_clicks=0, style={'margin': '5px'}),
            html.Button("Remove node", id="remove-node-button", n_clicks=0, style={'margin': '5px'}),
            html.Button("Remove edge", id="remove-edge-button", n_clicks=0, style={'margin': '5px'}),
        ], style={'position': 'absolute', 'left': '40vw', 'top': '5vh', 'display': 'flex', 'flex-direction': 'column'})
        
    ], style={'position': 'relative'})
