import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar entorno
load_dotenv()

# Configurar Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("ERROR CRÍTICO: No hay API KEY en el archivo .env")

genai.configure(api_key=api_key)

def consult_architect(requirement):
    """
    Usa el modelo ultra-avanzado Gemini 2.5 Pro para arquitectura.
    """
    # CAMBIO FINAL: Usamos el nombre exacto que salió en tu lista
    model = genai.GenerativeModel('gemini-2.5-pro')

    system_prompt = """
    Actúa como un Arquitecto de Software Senior experto en Graphviz.
    Tu tarea es analizar el requerimiento y generar una respuesta técnica en JSON.
    
    REGLAS ESTRICTAS DE FORMATO JSON:
    1. Responde SOLO con el objeto JSON válido.
    2. NO escribas nada antes (ni "Aquí está el JSON").
    3. NO uses bloques de código markdown (```json ... ```).
    4. La estructura debe ser exactamente:
    {
        "tech_stack": "Tecnologías recomendadas",
        "pseudocode": "Pseudocódigo lógico paso a paso",
        "graphviz_dot": "Código DOT válido para diagrama"
    }
    
    REGLAS PARA GRAPHVIZ (DOT):
    - Usa 'digraph G { rankdir=TB; ... }'
    - Usa nodos simples: node [shape=box]
    - NO uses caracteres especiales complejos dentro de las etiquetas.
    """

    full_prompt = f"{system_prompt}\n\nRequerimiento del usuario: {requirement}"

    try:
        # Generamos la respuesta
        response = model.generate_content(full_prompt)
        
        # Limpieza de seguridad robusta
        text = response.text
        # Quitamos posibles bloques de código si la IA desobedece
        text = text.replace("```json", "").replace("```", "").strip()
        
        # Intentamos encontrar donde empieza y termina el JSON
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end != -1:
            text = text[start:end]
        
        return json.loads(text)
    
    except json.JSONDecodeError:
        return {"error": "La IA no generó un JSON válido. Intenta simplificar tu requerimiento."}
    except Exception as e:
        return {"error": f"Error técnico: {str(e)}"}