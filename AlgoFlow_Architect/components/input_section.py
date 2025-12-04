from dash import html, dcc
import dash_bootstrap_components as dbc

def create_input_area():
    return dbc.Card([
        dbc.CardHeader("1. Definición de Requerimientos", className="card-header-custom"),
        dbc.CardBody([
            html.P("Describe qué sistema quieres construir (ej. 'Un sistema de login con huella digital'):"),
            dbc.Textarea(
                id="user-input",
                placeholder="Escribe tu idea aquí...",
                style={"height": "150px"},
                className="mb-3"
            ),
            dbc.Button("Generar Arquitectura", id="generate-btn", color="primary", n_clicks=0, className="w-100")
        ])
    ], className="mb-4 shadow-sm")