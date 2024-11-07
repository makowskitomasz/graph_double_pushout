from dash.dependencies import Input, Output, State
from dash import html
import dash_cytoscape as cyto
from ProductionParser import ProductionParser
from production_graph_store import ProductionGraphStore
from utils import parse_contents, nx_to_cytoscape_elements, is_subgraph, scale_positions

production_parser = ProductionParser()
graph_store = ProductionGraphStore()

def register_buttons(app):
    @app.callback(

    )
    def load_main_graph():
        pass


    @app.callback(

    )
    def clear_main_graph():
        pass


    @app.callback(

    )
    def add_node_to_main():
        pass


    @app.callback(

    )
    def remove_node_from_main():
        pass


    @app.callback(

    )
    def add_edge_to_main():
        pass


    @app.callback(

    )
    def remove_edge_from_main():
        pass


    @app.callback(

    )
    def rest_view_main_graph():
        pass

# PRODUCTION CONTROLS

    @app.callback(

    )
    def import_productions():
        pass


    @app.callback(

    )
    def remove_all_productions():
        pass


    @app.callback(

    )
    def remove_one_production():
        pass


    @app.callback(

    )
    def apply_production():
        pass


    @app.callback(

    )
    def previous_step():
        pass


    @app.callback(

    )
    def next_step():
        pass