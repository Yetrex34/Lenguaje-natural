import graphviz
import base64
import os

def render_dot_to_image(dot_string):
    """
    Recibe código DOT y devuelve una imagen en base64 lista para HTML.
    """
    try:
        # Creamos un objeto Source de Graphviz
        src = graphviz.Source(dot_string)
        
        # Renderizamos a formato PNG en memoria (pipe)
        png_data = src.pipe(format='png')
        
        # Codificamos a base64 para enviarlo al frontend sin guardar archivos
        encoded_image = base64.b64encode(png_data).decode('utf-8')
        return f"data:image/png;base64,{encoded_image}"
    
    except Exception as e:
        print(f"Error generando diagrama: {e}")
        return None