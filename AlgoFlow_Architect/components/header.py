from dash import html
import dash_bootstrap_components as dbc

def create_header():
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Documentación", href="#")),
            dbc.NavItem(dbc.NavLink("Exportar PDF", href="#")),
        ],
        brand="AlgoFlow Architect 1.0",
        brand_href="#",
        color="dark",
        dark=True,
        className="mb-4"
    )