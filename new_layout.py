from dash import html, dcc
import dash_cytoscape as cyto

def layout():
    return html.Div(
        className = 'content',
        children = [
            dcc.Store(id='main-graph-data'),
            dcc.Store(id='left-graph-data'),
            dcc.Store(id='right-graph-data'),
            _left_section(),
            _right_section()
        ]
    )

def _left_section():
    return html.Div(
        className = 'leftSection',
        children = [
            html.Div(
                id = 'master-graph',
                className = 'cytoscape',
                style = {
                    'width': '100%',
                    'height': '700px',
                },
                children = [
                    cyto.Cytoscape(
                    id='main-graph',
                    elements = [],
                    style={'width': '100%', 'height': '100%'},
                    layout={'name': 'preset'},
                    stylesheet=[
                    {
                        'selector': 'node',
                        'style': {
                            'width': '35px',
                            'height': '35px',
                            'backgroundColor': 'red',
                            'label': 'data(label)'
                        }
                    },
                    {
                        'selector': 'node:selected',
                        'style': {
                            'width': '45px',
                            'height': '45px',
                            'backgroundColor': 'blue',
                            'label': 'data(label)'
                        }
                    },
                    {
                        'selector': 'edge',
                        'style': {
                            'width': 4,
                            'line-color': '#222',
                            'target-arrow-shape': 'triangle',
                            'target-arrow-color': '#222',
                            'curve-style': 'bezier'
                        }
                    },
                    {
                        'selector': 'edge:selected',
                        'style': {
                            'line-color': '#0074D9',
                            'target-arrow-color': '#0074D9',
                            'width': 6
                        }
                    }
                ] 
                    )
                ]
            ),
            html.Div(
                className = 'buttonRow',
                children = [
                    html.Button('Load Graph', id='load-graph-button', className='button normalButton'),
                    html.Button('Add Node', id='add-node-button', className='button normalButton'),
                    html.Button('Add Edge', id='add-edge-button', className='button normalButton'),
                    html.Button('Reset view', id='reset-view-button', className='button normalButton')
                ]
            ),
            html.Div(
                className = 'buttonRow',
                children = [
                    html.Button('Clear Graph', id='clear-graph-button', className='button dangerButton'),
                    html.Button('Remove Selected', id='remove-selected-button', className='button dangerButton')
                ]
            )
        ]
    )

def _right_section():
    return html.Div(
        className = 'rightSection',
        children = [
            html.Div(
                className = 'production-visualizer',
                children = [
                    html.Div(
                        id = 'production-graph-l',
                        className = 'cytoscape',
                        style = {
                            'height': '450px',
                            'width': '50%'
                        }
                    ),
                    html.Div(
                        id = 'production-graph-r',
                        className = 'cytoscape',
                        style = {
                            'height': '450px',
                            'width': '50%'
                        }
                    )
                ]
            ),
            html.Div(
                className = 'production-options',
                children = [
                    html.Div(
                        className = 'production-controls',
                        children = [
                            html.Div(
                                className = 'buttonRow',
                                children = [
                                    dcc.Upload('Import Productions', id='import-productions-button', className='button normalButton'),
                                    html.Button('Remove Production', id='remove-production-button', className='button dangerButton')
                                ]
                            ),
                            html.Div(
                                className = 'buttonRow',
                                children = [
                                    html.Button('Apply Production', id='apply-production-button', className='button normalButton'),
                                    html.Button('Remove All', id='remove-all-productions-button', className='button dangerButton')
                                ]
                            ),
                            html.Div(
                                className = 'buttonRow',
                                children = [
                                    html.Button('Previous Step', id='previous-step-button', className='button normalButton'),
                                    html.Button('Next Step', id='next-step-button', className='button normalButton')
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        className = 'production-list',
                        children = [
                            html.Button('Remove Production', id='remove-production-buttona', className='button secondaryButton')
                        ]
                    )
                ]
            )
        ]
    )
