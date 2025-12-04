from dash import html, dcc
import dash_bootstrap_components as dbc

def create_output_area():
    return dbc.Card([
        dbc.CardHeader("2. Arquitectura Generada", className="card-header-custom"),
        dbc.CardBody([
            dcc.Loading(
                id="loading-spinner",
                type="default",
                children=dbc.Tabs([
                    dbc.Tab(label="Diagrama de Flujo", tab_id="tab-diagram"),
                    dbc.Tab(label="Pseudocódigo", tab_id="tab-code"),
                    dbc.Tab(label="Stack Tecnológico", tab_id="tab-stack"),
                ], id="tabs", active_tab="tab-diagram")
            ),
            html.Div(id="tab-content", className="p-4")
        ])
    ], className="shadow-sm")