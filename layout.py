from dash import html, dcc
import dash_cytoscape as cyto

def create_layout(base_graph_elements):
    return html.Div([
        dcc.Store(id='first-line-store'),
        dcc.Store(id='second-line-store'),

        html.Div(style={'backgroundColor': '#f0f0f0', 'width': '100vw', 'height': '220vh', 'position': 'relative'}),

        cyto.Cytoscape(
            id='base-graph',
            elements=base_graph_elements,
            style={
                'width': '40vw',
                'height': '80vh',
                'position': 'absolute',
                'left': '5vw',
                'top': '10vh',
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

        html.Div(
            dcc.Upload(
                id='upload-data',
                children=html.Div(['Drag and Drop']),
                style={
                    'width': '150px',
                    'height': '40px',
                    'lineHeight': '40px',
                    'borderWidth': '1px',
                    'borderStyle': 'solid',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '1px'
                }
            ),
            style={'position': 'absolute', 'top': '10vh', 'right': '10vw'}
        ),

        html.Div([
            html.Div(id='first-line', style={
                'width': '300px',
                'height': '300px',
                'border': '1px solid #ccc',
                'display': 'inline-block',
                'marginRight': '10px'
            }),
            html.Div(id='second-line', style={
                'width': '300px',
                'height': '300px',
                'border': '1px solid #ccc',
                'display': 'inline-block'
            })
        ], style={'position': 'absolute', 'top': '25vh', 'right': '10vw'}),

        html.Div(
            html.Button("Add to the transformation", id="add-production-button", n_clicks=0, disabled=True),
            style={
                'position': 'absolute',
                'top': '70vh',
                'right': '10vw',
                'padding': '5px',
                'border': '1px solid #ccc',
                'borderRadius': '5px',
                'textAlign': 'center'
            }
        ),

        html.Div(id='production-list', style={
            'position': 'absolute',
            'top': '85vh',
            'right': '10vw',
            'width': '300px',
            'border': '1px solid #ccc',
            'padding': '10px'
        }),

        html.Div(
            html.Button("Apply", id='transformation-list-finish'), style={
            'position': 'absolute',
            'top': '110vh',
            'right': '10vw',
            'width': '50px',
            'border': '1px solid #ccc',
            'padding': '10px'
        }),

        html.Hr(style={
            'position': 'absolute',
            'top': '120vh',
            'width': '150vw'
        }),

        html.Div(
            id='base-graph-1',
            style={
                'width': '40vw',
                'height': '80vh',
                'position': 'absolute',
                'left': '5vw',
                'top': '130vh',
                'border': '2px solid #ccc'
            }
        ),

        html.Div(id='production-list-1', style={
            'position': 'absolute',
            'top': '130vh',
            'right': '10vw',
            'width': '300px',
            'border': '1px solid #ccc',
            'padding': '10px'
        }),

        html.Div(
            html.Button("NEXT STEP", id="next-step-button", n_clicks=0),
            style={
                'position': 'absolute',
                'top': '170vh',
                'right': '10vw',
                'padding': '5px',
                'border': '1px solid #ccc',
                'borderRadius': '5px',
                'textAlign': 'center'
            }
        )
        
    ], style={'position': 'relative'})