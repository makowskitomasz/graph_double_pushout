from dash import html, dcc
import dash_cytoscape as cyto

def layout():
    return html.Div(
        className='content',
        children=[
            dcc.Store(id='main-graph-data', data={'current_index': 0}),
            dcc.Store(id='left-graph-data'),
            dcc.Store(id='right-graph-data'),
            _left_section(),
            _right_section()
        ]
    )

def _left_section():
    return html.Div(
        className='leftSection',
        children=[
            html.Div(
                id='master-graph',
                className='cytoscape',
                style={
                    'width': '100%',
                    'height': '700px',
                },
                children=[
                    html.Div(
                        className='graph-caption',
                        children=['Master Graph']
                    ),
                    html.Div(
                        id='graph-description',
                        className='graph-description centered',
                        children=['Base Graph (G)']
                    ),
                    cyto.Cytoscape(
                        id='main-graph',
                        elements=[],
                        style={'width': '100%', 'height': '100%'},
                        layout={'name': 'preset'},
                        stylesheet=[
                            {
                                'selector': 'node',
                                'style': {
                                    'width': '50px',
                                    'height': '50px',
                                    'backgroundColor': '#16d4fa',
                                    'label': 'data(label)',
                                    'font-size': '20px'
                                }
                            },
                            {
                                'selector': 'node:selected',
                                'style': {
                                    'width': '60px',
                                    'height': '60px',
                                    'backgroundColor': '#ad3ef7',
                                    'label': 'data(label)',
                                    'font-size': '20px'
                                }
                            },
                            {
                                'selector': 'edge',
                                'style': {
                                    'width': 6,
                                    'line-color': '#16d4fa',
                                    'target-arrow-shape': 'triangle',
                                    'target-arrow-color': '#16d4fa',
                                    'curve-style': 'bezier'
                                }
                            },
                            {
                                'selector': 'edge:selected',
                                'style': {
                                    'line-color': '#ad3ef7',
                                    'target-arrow-color': '#ad3ef7',
                                    'width': 8
                                }
                            },
                            {
                                'selector': '.added',
                                'style': {
                                    'line-color': 'green',
                                    'target-arrow-color': 'green',
                                    'background-color': 'green',
                                }
                            },
                            {
                                'selector': '.to-remove',
                                'style': {
                                    'line-color': 'red',
                                    'target-arrow-color': 'red',
                                    'background-color': 'red',
                                }
                            }
                        ]
                    )
                ]
            ),
            html.Div(
                className='buttonRow',
                children=[
                    html.Button('Load Graph', id='load-graph-button', className='button normalButton'),
                    html.Button('Add Node', id='add-node-button', className='button normalButton'),
                    html.Button('Add Edge', id='add-edge-button', className='button normalButton'),
                    html.Button('Reset view', id='reset-view-button', className='button normalButton')
                ]
            ),
            html.Div(
                className='buttonRow',
                children=[
                    html.Button('Clear Graph', id='clear-graph-button', className='button dangerButton'),
                    html.Button('Remove Selected', id='remove-selected-button', className='button dangerButton')
                ]
            )
        ]
    )

def _right_section():
    return html.Div(
        className='rightSection',
        children=[
            html.Div(
                className='production-options',
                children=[
                    html.Div(
                        className='production-controls',
                        children=[
                            html.Div(
                                className='buttonRow',
                                children=[
                                    dcc.Upload('Import Productions', id='import-productions-button', className='button normalButton'),
                                    html.Button('Remove Production', id='remove-production-button', className='button dangerButton')
                                ]
                            ),
                            html.Div(
                                className='buttonRow',
                                children=[
                                    html.Button('Apply Production', id='apply-production-button', className='button normalButton'),
                                    html.Button('Remove All', id='remove-all-productions-button', className='button dangerButton')
                                ]
                            ),
                            html.Div(
                                className='buttonRow',
                                children=[
                                    html.Button('Previous Step', id='previous-step-button', className='button normalButton', disabled=True),
                                    html.Button('Next Step', id='next-step-button', className='button normalButton', disabled=True)
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        className='production-list',
                        children=[
                            html.Button('Remove Production', id='remove-production-buttona', className='button secondaryButton')
                        ]
                    ),
                    html.Div(
                        className='feedback',
                        children = [
                            html.P(id='feedback', children=[''])
                        ]
                    )
                ]
            ),
            html.Div(
                className='production-visualizer',
                children=[
                    html.Div(
                        id='production-graph-l',
                        className='cytoscape',
                        style={
                            'height': '30vh',
                            'width': '450px'
                        },
                        children=[
                            html.Div(
                                className='graph-caption',
                                children=['Graph L']
                            ),
                            cyto.Cytoscape(
                                id='graph-l',
                                elements=[],
                                style={'width': '100%', 'height': '100%'},
                                layout={'name': 'preset'},
                                stylesheet=[
                                    {
                                        'selector': 'node',
                                        'style': {
                                            'width': '50px',
                                            'height': '50px',
                                            'backgroundColor': '#16d4fa',
                                            'label': 'data(label)',
                                            'font-size': '40px'
                                        }
                                    },
                                    {
                                        'selector': 'node:selected',
                                        'style': {
                                            'width': '60px',
                                            'height': '60px',
                                            'backgroundColor': '#ad3ef7',
                                            'label': 'data(label)',
                                            'font-size': '40px'
                                        }
                                    },
                                    {
                                        'selector': 'edge',
                                        'style': {
                                            'width': 6,
                                            'line-color': '#16d4fa',
                                            'target-arrow-shape': 'triangle',
                                            'target-arrow-color': '#16d4fa',
                                            'curve-style': 'bezier'
                                        }
                                    },
                                    {
                                        'selector': 'edge:selected',
                                        'style': {
                                            'line-color': '#ad3ef7',
                                            'target-arrow-color': '#ad3ef7',
                                            'width': 8
                                        }
                                    },
                                    {
                                        'selector': '.added',
                                        'style': {
                                            'line-color': 'green',
                                            'target-arrow-color': 'green',
                                            'background-color': 'green',
                                        }
                                    },
                                    {
                                        'selector': '.to-remove',
                                        'style': {
                                            'line-color': 'red',
                                            'target-arrow-color': 'red',
                                            'background-color': 'red',
                                        }
                                    }
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        id='production-graph-k',
                        className='cytoscape',
                        style={
                            'height': '30vh',
                            'width': '450px'
                        },
                        children=[
                            html.Div(
                                className='graph-caption',
                                children=['Graph K']
                            ),
                            cyto.Cytoscape(
                                id='graph-k',
                                elements=[],
                                style={'width': '100%', 'height': '100%'},
                                layout={'name': 'preset'},
                                stylesheet=[
                                    {
                                        'selector': 'node',
                                        'style': {
                                            'width': '50px',
                                            'height': '50px',
                                            'backgroundColor': '#16d4fa',
                                            'label': 'data(label)',
                                            'font-size': '40px'
                                        }
                                    },
                                    {
                                        'selector': 'node:selected',
                                        'style': {
                                            'width': '60px',
                                            'height': '60px',
                                            'backgroundColor': '#ad3ef7',
                                            'label': 'data(label)',
                                            'font-size': '40px'
                                        }
                                    },
                                    {
                                        'selector': 'edge',
                                        'style': {
                                            'width': 6,
                                            'line-color': '#16d4fa',
                                            'target-arrow-shape': 'triangle',
                                            'target-arrow-color': '#16d4fa',
                                            'curve-style': 'bezier'
                                        }
                                    },
                                    {
                                        'selector': 'edge:selected',
                                        'style': {
                                            'line-color': '#ad3ef7',
                                            'target-arrow-color': '#ad3ef7',
                                            'width': 8
                                        }
                                    },
                                    {
                                        'selector': '.added',
                                        'style': {
                                            'line-color': 'green',
                                            'target-arrow-color': 'green',
                                            'background-color': 'green',
                                        }
                                    },
                                    {
                                        'selector': '.to-remove',
                                        'style': {
                                            'line-color': 'red',
                                            'target-arrow-color': 'red',
                                            'background-color': 'red',
                                        }
                                    }
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        id='production-graph-r',
                        className='cytoscape',
                        style={
                            'height': '30vh',
                            'width': '450px'
                        },
                        children=[
                            html.Div(
                                className='graph-caption',
                                children=['Graph R']
                            ),
                            cyto.Cytoscape(
                                id='graph-r',
                                elements=[],
                                style={'width': '100%', 'height': '100%'},
                                layout={'name': 'preset'},
                                stylesheet=[
                                    {
                                        'selector': 'node',
                                        'style': {
                                            'width': '50px',
                                            'height': '50px',
                                            'backgroundColor': '#16d4fa',
                                            'label': 'data(label)',
                                            'font-size': '40px'
                                        }
                                    },
                                    {
                                        'selector': 'node:selected',
                                        'style': {
                                            'width': '60px',
                                            'height': '60px',
                                            'backgroundColor': '#ad3ef7',
                                            'label': 'data(label)',
                                            'font-size': '40px'
                                        }
                                    },
                                    {
                                        'selector': 'edge',
                                        'style': {
                                            'width': 6,
                                            'line-color': '#16d4fa',
                                            'target-arrow-shape': 'triangle',
                                            'target-arrow-color': '#16d4fa',
                                            'curve-style': 'bezier'
                                        }
                                    },
                                    {
                                        'selector': 'edge:selected',
                                        'style': {
                                            'line-color': '#ad3ef7',
                                            'target-arrow-color': '#ad3ef7',
                                            'width': 8
                                        }
                                    },
                                    {
                                        'selector': '.added',
                                        'style': {
                                            'line-color': 'green',
                                            'target-arrow-color': 'green',
                                            'background-color': 'green',
                                        }
                                    },
                                    {
                                        'selector': '.to-remove',
                                        'style': {
                                            'line-color': 'red',
                                            'target-arrow-color': 'red',
                                            'background-color': 'red',
                                        }
                                    }
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )