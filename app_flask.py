"""
JECA - Backend Flask
====================
Servidor web para JECA con interfaz HTML/CSS
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import json
import re
import random

app = Flask(__name__)
CORS(app)

# API configuración
import os
API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyDBlECjubZ12ZeylFh7UamQg0KgAfFtjEc')
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def es_problema_no_programacion(problema):
    """
    Detecta si la pregunta NO es un problema de programación.
    Retorna True si NO es programación (rechaza).
    Retorna False si SÍ es programación (acepta).
    """
    problema_lower = problema.lower()
    
    palabras_programacion = [
        "programa", "algoritmo", "código", "función", "variable",
        "array", "matriz", "lista", "bucle", "for", "while", "if",
        "clase", "método", "objeto", "datos", "estructura",
        "ordenar", "buscar", "recursión", "suma", "resta",
        "multiplicar", "dividir", "procesar", "calcular",
        "implementar", "desarrolla", "crea", "haz", "resuelve",
        "número", "cadena", "string", "int", "float", "boolean",
        "java", "python", "c++", "javascript", "sql", "html",
        "web", "api", "base de datos", "query", "loop", "sort"
    ]
    
    preguntas_prohibidas = [
        "quién eres", "quién soy yo", "quién es tu creador",
        "música", "canción", "canta", "baila", "chiste",
        "hola", "cómo estás", "qué hora es", "qué día es",
        "receta", "cocina", "comida", "bebida",
        "historia", "película", "deportes", "fútbol",
        "medicina", "doctor", "síntomas",
        "astrología", "horóscopo", "filosofía", "religión"
    ]
    
    tiene_prohibida = any(palabra in problema_lower for palabra in preguntas_prohibidas)
    tiene_programacion = any(palabra in problema_lower for palabra in palabras_programacion)
    
    if tiene_prohibida and not tiene_programacion:
        return True
    if tiene_programacion:
        return False
    return True

def limpiar_texto(texto):
    """
    Limpia el texto devuelto por la IA.
    """
    texto = re.sub(r'\n{2,}', '\n', texto)
    texto = texto.strip()
    return texto

def obtener_respuesta_ia(problema, lenguaje):
    """
    Envía la consulta a la API de Gemini siguiendo la metodología JECA.
    """
    try:
        prompt = f"""
        Resuelve este problema de programación SIGUIENDO EXACTAMENTE ESTA ESTRUCTURA:
        
        1. IDENTIFICACIÓN Y CLARIFICACIÓN DEL PROBLEMA
           a) Qué se pide
           b) Entradas y salidas esperadas
        
        2. ANÁLISIS DEL PROBLEMA
           a) Complejidad esperada
           b) Casos especiales
        
        3. SOLUCIONES ALTERNATIVAS
           a) Enfoque 1
           b) Enfoque 2
           c) Ventajas y desventajas de cada uno
        
        4. MEJOR SOLUCIÓN SELECCIONADA
           a) Justificación
        
        5. SEUDOCÓDIGO
           a) Código paso a paso
        
        6. DIAGRAMA DE FLUJO (en texto ASCII)
           a) Representación visual del flujo
        
        7. CÓDIGO EN {lenguaje}
           a) Implementación completa y comentada
        
        8. EJEMPLO DE EJECUCIÓN
           a) Entrada
           b) Salida
        
        9. EXPLICACIÓN BREVE DE RESULTADOS
           a) Explicación breve
        
        PROBLEMA: {problema}
        """

        user_part = {"text": prompt}
        contenido = {"role": "user", "parts": [user_part]}
        configuracion = {"temperature": 0.3}
        datos = {"contents": [contenido], "generationConfig": configuracion}
        
        respuesta = requests.post(
            f"{API_URL}?key={API_KEY}",
            headers={"Content-Type": "application/json"},
            data=json.dumps(datos),
            timeout=100
        )
        
        if respuesta.status_code != 200:
            return {
                "success": False,
                "error": f"❌ [ERROR {respuesta.status_code}] No se pudo obtener respuesta de la API"
            }
        
        resultado = respuesta.json()

        if "candidates" in resultado and len(resultado["candidates"]) > 0:
            texto = resultado["candidates"][0]["content"]["parts"][0]["text"]
            return {
                "success": True,
                "respuesta": limpiar_texto(texto)
            }
        else:
            return {
                "success": False,
                "error": "❌ No se recibió una respuesta válida de la API"
            }
            
    except requests.Timeout:
        return {
            "success": False,
            "error": "⏱️ Tiempo de espera agotado. Revisa tu conexión a Internet."
        }
    except requests.ConnectionError:
        return {
            "success": False,
            "error": "🌐 Error de conexión. Verifica tu conexión a Internet."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"❌ Error inesperado: {str(e)}"
        }

@app.route('/')
def index():
    """
    Renderiza la página principal.
    """
    return render_template('index.html')

@app.route('/resolver', methods=['POST'])
def resolver():
    """
    Endpoint para resolver problemas de programación.
    """
    data = request.get_json()
    problema = data.get('problema', '').strip()
    lenguaje = data.get('lenguaje', 'Python')
    
    if not problema:
        return jsonify({
            "success": False,
            "error": "⚠️ Por favor, describe un problema."
        })
    
    # Validar si es problema de programación
    if es_problema_no_programacion(problema):
        mensajes_rechazo = [
            "🎵 Eso suena interesante, pero yo solo hablo el lenguaje de los algoritmos 🎵",
            "❌ Eso no es un problema de programación. Necesitas otro tipo de asistente.",
            "😄 Vaya pregunta divertida, pero mi especialidad es CODE, no comedy.",
            "🎸 Estoy aquí para código, no para conciertos 🎸",
            "🤖 Mi cerebro de silicio solo entiende de algoritmos, no de filosofía existencial.",
            "⚠️ Eso está fuera de mi área de especialización. Soy solo un asistente de programación.",
            "🚫 No compute. Solo proceso problemas de programación.",
            "💻 Error 404: Respuesta no encontrada. Solo respondo sobre código y algoritmos."
        ]
        return jsonify({
            "success": False,
            "rechazo": True,
            "error": random.choice(mensajes_rechazo)
        })
    
    # Obtener respuesta de la IA
    resultado = obtener_respuesta_ia(problema, lenguaje)
    return jsonify(resultado)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print("\n" + "="*80)
    print("🤖 JECA - Servidor Web Iniciado 🤖")
    print("="*80)
    print(f"\n✅ Servidor corriendo en puerto: {port}")
    print("\n" + "="*80 + "\n")
    app.run(debug=False, host='0.0.0.0', port=port)