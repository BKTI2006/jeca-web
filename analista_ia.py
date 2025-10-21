"""
JECA - Gestor Experto de Código y Algoritmos
==============================================

REQUISITOS PREVIOS:
-------------------
1. Python 3.7 o superior
2. Librería requests: pip install requests
3. Conexión a Internet activa
4. API Key válida de Google Gemini

PALABRAS CLAVE QUE JECA RECONOCE:
----------------------------------
✅ ACEPTA: programa, algoritmo, código, función, variable, array, matriz,
   lista, bucle, for, while, if, clase, método, estructura de datos,
   ordenar, buscar, recursión, calcular, implementar, números, cadenas,
   Python, Java, C++, JavaScript, etc.

❌ RECHAZA: preguntas personales, música, recetas, medicina, deportes,
   filosofía, astrología, entretenimiento general, etc.

AUTOR: Sistema JECA
VERSIÓN: 2.0
"""

import requests
import json
import re
import random

# API configuración
API_KEY = "AIzaSyDBlECjubZ12ZeylFh7UamQg0KgAfFtjEc"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def presentar_JECA():
    """
    Presenta a JECA y su metodología de resolución.
    """
    print("\n" + "="*80)
    print("🤖 BIENVENIDO A JECA 🤖")
    print("Gestor Experto de Código y Algoritmos")
    print("="*80)
    print("\n📋 METODOLOGÍA DE RESOLUCIÓN:")
    print("1. Identificación y clarificación del problema")
    print("   a) Qué se pide")
    print("   b) Entradas y salidas esperadas")
    print("\n2. Análisis detallado del problema")
    print("   a) Complejidad esperada")
    print("   b) Casos especiales")
    print("\n3. Desarrollo de soluciones alternativas")
    print("   a) Enfoque 1")
    print("   b) Enfoque 2")
    print("   c) Ventajas y desventajas de cada uno")
    print("\n4. Selección de la mejor solución")
    print("   a) Justificación")
    print("\n5. Implementación del seudocódigo")
    print("   a) Código paso a paso")
    print("\n6. Diagrama de flujo")
    print("   a) Representación visual del flujo")
    print("\n7. Solución en el lenguaje de programación")
    print("   a) Implementación completa y comentada")
    print("\n8. Ejemplo de ejecución")
    print("   a) Entrada")
    print("   b) Salida")
    print("\n9. Explicación de resultados")
    print("   a) Explicación breve")
    print("\n⚠️  SOLO resuelvo PROBLEMAS ALGORÍTMICOS Y DE PROGRAMACIÓN ⚠️")
    print("\n💡 Escribe 'ayuda' para ver ejemplos de problemas válidos")
    print("💡 Escribe 'fin' para salir del programa")
    print("="*80 + "\n")

def mostrar_ayuda():
    """
    Muestra ejemplos de problemas válidos que JECA puede resolver.
    """
    print("\n" + "="*80)
    print("📚 EJEMPLOS DE PROBLEMAS QUE JECA PUEDE RESOLVER:")
    print("="*80)
    print("\n✅ Ejemplos válidos:")
    print("   • Crea un programa que ordene una lista de números")
    print("   • Algoritmo para buscar un elemento en un array")
    print("   • Función recursiva para calcular el factorial")
    print("   • Programa que invierta una cadena de texto")
    print("   • Implementa una calculadora básica")
    print("   • Algoritmo de búsqueda binaria")
    print("   • Suma de números pares de una lista")
    print("\n❌ Ejemplos NO válidos:")
    print("   • ¿Quién eres?")
    print("   • Cuéntame un chiste")
    print("   • ¿Qué hora es?")
    print("   • Dame una receta de cocina")
    print("   • ¿Cómo estás hoy?")
    print("="*80 + "\n")

def es_problema_no_programacion(problema):
    """
    Detecta si la pregunta NO es un problema de programación.
    Retorna True si NO es programación (rechaza).
    Retorna False si SÍ es programación (acepta).
    """
    problema_lower = problema.lower()
    
    # Palabras clave que INDICAN que ES un problema de programación
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
    
    # Preguntas que claramente NO son de programación
    preguntas_prohibidas = [
        "quién eres", "quién soy yo", "quién es tu creador", "quién te creó",
        "qué es jeca", "quién es jeca", "cuál es tu nombre", "tu nombre es",
        "música", "canción", "canta", "baila", "chiste",
        "hola", "cómo estás", "cómo va", "qué tal", "hey", "oye",
        "qué hora es", "qué día es", "cuándo es",
        "receta", "cocina", "comida", "bebida",
        "historia", "relato", "película", "actor",
        "deportes", "fútbol", "básquet", "tenis",
        "medicina", "doctor", "síntomas", "cura", "enfermedad",
        "astrología", "horóscopo", "tarot", "videncia",
        "filosofía", "religión", "dios", "alma", "amor"
    ]
    
    # Si tiene palabras prohibidas Y no tiene palabras de programación, rechaza
    tiene_prohibida = any(palabra in problema_lower for palabra in preguntas_prohibidas)
    tiene_programacion = any(palabra in problema_lower for palabra in palabras_programacion)
    
    if tiene_prohibida and not tiene_programacion:
        return True
    
    # Si tiene palabras de programación, siempre acepta
    if tiene_programacion:
        return False
    
    # Si no tiene ni una ni otra, rechaza (no es claro que sea programación)
    return True

def validar_lenguaje(lenguaje):
    """
    Valida que el lenguaje ingresado sea uno de los soportados.
    """
    lenguajes_validos = [
        "python", "java", "c++", "c", "javascript", "typescript",
        "go", "rust", "php", "ruby", "swift", "kotlin", "c#",
        "sql", "html", "css", "r", "matlab", "perl", "scala"
    ]
    
    if lenguaje.lower() in lenguajes_validos:
        return True
    return False

def limpiar_texto(texto):
    """
    Limpia el texto devuelto por la IA para que se vea más ordenado en la consola.
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
            return f"❌ [ERROR {respuesta.status_code}] No se pudo obtener la respuesta de la API"
        
        resultado = respuesta.json()

        if "candidates" in resultado and len(resultado["candidates"]) > 0:
            texto = resultado["candidates"][0]["content"]["parts"][0]["text"]
            return limpiar_texto(texto)
        else:
            return "❌ No se recibió una respuesta válida de la API"
            
    except requests.Timeout:
        return "⏱️ Tiempo de espera agotado. Revisa tu conexión a Internet."
    except requests.ConnectionError:
        return "🌐 Error de conexión. Verifica tu conexión a Internet."
    except Exception as e:
        return f"❌ Error inesperado: {e}"

def obtener_rechazo_creativo():
    """
    Devuelve mensajes creativos cuando rechaza preguntas no relacionadas.
    """
    mensajes = [
        "\n🎵 Eso suena interesante, pero yo solo hablo el lenguaje de los algoritmos 🎵\n",
        "\n❌ Eso no es un problema de programación. Necesitas otro tipo de asistente.\n",
        "\n😄 Vaya pregunta divertida, pero mi especialidad es CODE, no comedy.\n",
        "\n🎸 Estoy aquí para código, no para conciertos 🎸\n",
        "\n🤖 Mi cerebro de silicio solo entiende de algoritmos, no de filosofía existencial.\n",
        "\n⚠️ Eso está fuera de mi área de especialización. Soy solo un asistente de programación.\n",
        "\n🚫 No compute. Solo proceso problemas de programación.\n",
        "\n💻 Error 404: Respuesta no encontrada. Solo respondo sobre código y algoritmos.\n"
    ]
    return random.choice(mensajes)

def main():
    """
    Función principal que ejecuta el ciclo de interacción con JECA.
    """
    presentar_JECA()

    while True:
        problema = input("💬 Describe tu problema: ").strip()

        if problema.lower() == "fin":
            print("\n👋 Sesión cerrada. ¡Sigue mejorando tus habilidades de programación! 🚀\n")
            break

        if problema.lower() == "ayuda":
            mostrar_ayuda()
            continue

        if not problema:
            print("⚠️  Por favor, describe un problema.\n")
            continue

        # Validar si es una pregunta no relacionada a programación
        if es_problema_no_programacion(problema):
            print(obtener_rechazo_creativo())
            continue

        lenguaje = input("🔧 Lenguaje deseado (Python, Java, C++, JavaScript, etc.): ").strip()

        if not lenguaje:
            lenguaje = "Python"
            print(f"   → Usando lenguaje por defecto: {lenguaje}")

        if not validar_lenguaje(lenguaje):
            print(f"⚠️  '{lenguaje}' no es un lenguaje común. Se usará de todas formas.\n")

        print("\n⏳ Procesando tu problema... Por favor espera.\n")
        respuesta = obtener_respuesta_ia(problema, lenguaje)

        print("=" * 80)
        print(f"✅ SOLUCIÓN JECA (Lenguaje: {lenguaje.capitalize()})")
        print("=" * 80)
        print(respuesta)
        print("=" * 80 + "\n")
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario. ¡Hasta pronto! 👋\n")
    except Exception as e:
        print(f"\n❌ Error crítico en el programa: {e}\n")