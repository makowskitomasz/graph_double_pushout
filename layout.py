from dash import html, dcc
import dash_cytoscape as cyto

def create_layout(base_graph_elements):
    return html.Div([        
        html.Div([
            html.Div([
                cyto.Cytoscape(
                    id='main-graph',
                    elements=base_graph_elements,
                    style={'width': '40%', 'height': '60vh', 'backgroundColor': 'white'},
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
                    },
                    {
                        'selector': 'edge:selected',
                        'style': {
                            'line-color': '#0074D9',
                            'target-arrow-color': '#0074D9',
                            'width': 4
                        }
                    }
                ]
                )
            ]),

            html.Div([
                html.Button('Add Node', id='add-node-button', n_clicks=0),
                html.Button('Add Edge', id='add-edge-button', n_clicks=0),
                html.Button('Remove Selected', id='remove-selected-button', n_clicks=0),
                html.Button('Reset View', id='reset-view-button', n_clicks=0),
                html.Button('Load Graph', id='load-graph-button', n_clicks=0),
                html.Button('Clear Graph', id='clear-graph-button', n_clicks=0)
            ], style={'textAlign': 'left', 'marginBottom': '20px'}),
        ])
    ])