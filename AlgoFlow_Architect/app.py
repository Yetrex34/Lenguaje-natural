import dash
from dash import html, dcc, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
import json

# Importamos nuestros módulos locales
from components.header import create_header
from components.input_section import create_input_area
from components.output_section import create_output_area
from logic.ai_client import consult_architect
from logic.diagram_gen import render_dot_to_image

# Inicializar la app con tema Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "AlgoFlow Architect"

# Layout Principal
app.layout = dbc.Container([
    # --- COMPONENTE DE MEMORIA (Invisible) ---
    # Aquí guardaremos la respuesta de la IA para no perderla al cambiar de tab
    dcc.Store(id='memory-store', storage_type='memory'),
    
    create_header(),
    
    dbc.Row([
        dbc.Col(create_input_area(), width=4),
        dbc.Col(create_output_area(), width=8)
    ])
], fluid=True)

# --- CALLBACK 1: LLAMADA A LA IA ---
# Solo se activa cuando presionas el botón. Guarda el resultado en la memoria.
@callback(
    Output("memory-store", "data"),
    Input("generate-btn", "n_clicks"),
    State("user-input", "value"),
    prevent_initial_call=True
)
def call_ai_architect(n_clicks, user_input):
    if not user_input:
        return no_update # No hacemos nada si está vacío
    
    # Llamamos a tu módulo de IA (Gemini)
    architecture_data = consult_architect(user_input)
    
    # Guardamos el resultado JSON en la memoria del navegador
    return architecture_data

# --- CALLBACK 2: VISUALIZACIÓN ---
# Se activa cuando llega nueva data a la memoria O cuando cambias de tab.
# Es instantáneo porque ya no llama a Google, solo lee la memoria.
@callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
    Input("memory-store", "data") # Escuchamos cambios en la memoria
)
def render_content(active_tab, data):
    # Si la memoria está vacía (inicio), pedimos que generen algo
    if data is None:
        return html.Div(
            html.P("👈 Escribe un requerimiento y presiona 'Generar' para comenzar."),
            className="text-muted text-center mt-5"
        )

    # Si hubo error en la IA
    if "error" in data:
        return dbc.Alert(f"Error: {data['error']}", color="danger")

    # Renderizar según el tab seleccionado usando los datos de memoria
    if active_tab == "tab-diagram":
        dot_code = data.get("graphviz_dot", "")
        if not dot_code:
             return dbc.Alert("La IA no generó código para el diagrama.", color="warning")
             
        img_src = render_dot_to_image(dot_code)
        
        if img_src:
            return html.Div([
                html.H5("Flujo del Sistema", className="mb-3 text-center"),
                html.Div(
                    html.Img(src=img_src, style={"maxWidth": "100%", "height": "auto", "borderRadius": "8px"}),
                    style={"textAlign": "center", "overflow": "auto"}
                )
            ], className="diagram-container")
        else:
            return dbc.Alert(
                "Error de Graphviz: No se pudo generar la imagen. Verifica que Graphviz esté instalado en el PATH del sistema.", 
                color="danger"
            )

    elif active_tab == "tab-code":
        return html.Div([
            html.H5("Lógica del Sistema (Pseudocódigo)", className="mb-3"),
            html.Pre(data.get("pseudocode", "Sin datos"), className="code-container")
        ])

    elif active_tab == "tab-stack":
        return dbc.Card([
            dbc.CardBody([
                html.H4("🛠️ Stack Tecnológico Recomendado", className="card-title text-info"),
                html.Hr(),
                html.P(data.get("tech_stack", "Sin datos"), className="card-text lead")
            ])
        ], color="light", outline=True)

    return html.P("Selecciona una pestaña.")

# Ejecutar servidor
if __name__ == "__main__":
    app.run_server(debug=True)