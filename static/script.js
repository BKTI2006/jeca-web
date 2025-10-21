// ========================================
// JECA - Script JavaScript
// Conecta el frontend con el backend Flask
// ========================================

// ========================================
// MANEJO DE TABS
// ========================================
function cambiarTab(index) {
    // Ocultar todos los contenidos
    const contents = document.querySelectorAll('.info-content');
    const tabs = document.querySelectorAll('.tab');
    
    contents.forEach(c => c.classList.remove('active'));
    tabs.forEach(t => t.classList.remove('active'));
    
    // Mostrar el seleccionado
    document.getElementById(`tab${index}`).classList.add('active');
    tabs[index].classList.add('active');
}

// ========================================
// MANEJO DE ENTER EN INPUT
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('problemInput');
    
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !document.getElementById('sendBtn').disabled) {
            enviarProblema();
        }
    });
});

// ========================================
// AGREGAR MENSAJES AL CHAT
// ========================================
function agregarMensaje(texto, tipo) {
    const messagesDiv = document.getElementById('messages');
    const mensaje = document.createElement('div');
    mensaje.className = `message ${tipo}`;
    
    // Convertir Markdown básico a HTML
    texto = texto.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    texto = texto.replace(/\n/g, '<br>');
    
    mensaje.innerHTML = texto;
    messagesDiv.appendChild(mensaje);
    
    // Scroll automático al final
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// ========================================
// FUNCIÓN PRINCIPAL: ENVIAR PROBLEMA
// ========================================
async function enviarProblema() {
    const problema = document.getElementById('problemInput').value.trim();
    const lenguaje = document.getElementById('lenguajeSelect').value;

    // Validación básica
    if (!problema) {
        agregarMensaje("⚠️ Por favor, describe un problema.", "error");
        return;
    }

    // Mostrar mensaje del usuario
    agregarMensaje(
        `<strong>Tu problema:</strong><br>${problema}<br><br><strong>Lenguaje:</strong> ${lenguaje}`, 
        "user"
    );
    
    // Limpiar input
    document.getElementById('problemInput').value = '';

    // Mostrar loading y deshabilitar botón
    document.getElementById('loading').classList.add('active');
    document.getElementById('sendBtn').disabled = true;

    try {
        // Enviar petición al backend Flask
        const response = await fetch('/resolver', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                problema: problema,
                lenguaje: lenguaje
            })
        });

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }

        const data = await response.json();

        // Verificar si fue rechazado
        if (data.rechazo) {
            agregarMensaje(data.error, "reject");
        }
        // Verificar si hubo error
        else if (!data.success) {
            agregarMensaje(data.error, "error");
        }
        // Mostrar respuesta exitosa
        else {
            agregarMensaje(
                `<strong>✅ SOLUCIÓN JECA (${lenguaje}):</strong><br><br>${data.respuesta}`, 
                "jeca"
            );
        }

    } catch (error) {
        agregarMensaje(
            `❌ <strong>Error de conexión:</strong><br>${error.message}<br><br>Verifica que el servidor Flask esté corriendo.`,
            "error"
        );
    } finally {
        // Ocultar loading y habilitar botón
        document.getElementById('loading').classList.remove('active');
        document.getElementById('sendBtn').disabled = false;
    }
}

// ========================================
// MOSTRAR AYUDA
// ========================================
function mostrarAyuda() {
    const ayuda = `
<strong>📚 GUÍA DE USO - JECA</strong><br><br>

<strong>✅ Ejemplos VÁLIDOS de problemas:</strong><br>
• Crea un programa que ordene una lista de números<br>
• Algoritmo para buscar un elemento en un array<br>
• Función recursiva para calcular el factorial<br>
• Programa que invierta una cadena de texto<br>
• Implementa una calculadora básica<br>
• Algoritmo de búsqueda binaria<br>
• Suma de números pares de una lista<br>
• Función que detecte si un número es primo<br>
• Convierte temperatura de Celsius a Fahrenheit<br><br>

<strong>❌ Ejemplos NO válidos:</strong><br>
• ¿Quién eres?<br>
• Cuéntame un chiste<br>
• ¿Qué hora es?<br>
• Dame una receta de cocina<br>
• ¿Cómo estás hoy?<br>
• Háblame sobre filosofía<br><br>

<strong>💡 CONSEJO:</strong> Sé específico en tu problema. Incluye detalles sobre:<br>
• Entradas esperadas<br>
• Salidas deseadas<br>
• Restricciones o casos especiales
    `;
    agregarMensaje(ayuda, "system");
}

// ========================================
// LIMPIAR CHAT
// ========================================
function limpiarChat() {
    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML = `
        <div class="message system">
            👋 <strong>¡Chat limpiado!</strong><br>
            Estoy listo para ayudarte con un nuevo problema de programación. 🚀
        </div>
    `;
}

// ========================================
// MENSAJE INICIAL AL CARGAR
// ========================================
window.onload = function() {
    console.log("🤖 JECA v2.0 - Frontend cargado correctamente");
    console.log("✅ Conectado con el backend Flask");
};