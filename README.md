# Asistente Inteligente

Conversación natural, herramientas, internet y voz.
Corre 100% en tu PC con Ollama.

---

## Instalación rápida

### 1. Ollama

1. Descarga: https://ollama.com  
2. Instala y ejecuta:

```bash
ollama pull llama3.2
```

**Modelos recomendados (de mejor a más ligero):**

| Modelo            | Calidad      | RAM aprox |
|-------------------|--------------|-----------|
| `qwen2.5:14b`     | Muy alta     | 12+ GB    |
| `llama3.1:8b`     | Alta         | 8+ GB     |
| `qwen2.5:7b`      | Alta         | 8 GB      |
| `llama3.2`        | Buena        | 4–6 GB    |
| `phi3`            | Aceptable    | 4 GB      |

Para cambiar el modelo en el código, edita en `gui.py` o `main.py`:

```python
self.brain = Brain(model="qwen2.5:7b")
```

### 2. Proyecto

```bash
git clone https://github.com/rframosyataco8-ux/asistente-ia-local.git
cd asistente-ia-local

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python gui.py
```

---

## Capacidades actuales

- Conversación natural y fluida
- Memoria de contexto de la conversación
- Búsqueda en internet automática cuando hace falta
- Herramientas locales: hora, fecha, IP, abrir programas, cálculos
- Voz natural (edge-tts)
- Interfaz gráfica limpia
- Sin APIs de pago

---

## Estructura

```
core/
  brain.py   → inteligencia + internet + herramientas
  memory.py  → memoria de conversación
  voice.py   → voz natural
gui.py       → interfaz gráfica
main.py      → versión consola
```

---

## Próximas mejoras posibles

- Streaming de respuestas (texto que aparece poco a poco)
- Escucha por micrófono (hablar en vez de escribir)
- Memoria a largo plazo (recordar cosas entre sesiones)
- Más herramientas (archivos, navegador, etc.)

---

**Autor**: Fabricio Ramos  
**2026**
