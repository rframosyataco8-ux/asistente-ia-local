# Asistente Inteligente — Conversación natural

Habla con él como con una persona. Entiende, responde con naturalidad y puede buscar en internet.

- Conversación libre
- Memoria de la charla
- Acceso a internet (búsqueda)
- Voz
- Interfaz gráfica

Corre **en tu PC** con Ollama (gratis, sin APIs de pago).

---

## Instalación

### 1. Instalar Ollama

Ve a https://ollama.com y descárgalo.

Luego en una terminal:

```bash
ollama pull llama3.2
```

(Otros modelos buenos: `qwen2.5:3b`, `phi3`, `gemma2:2b`)

### 2. Clonar e instalar

```bash
git clone https://github.com/rframosyataco8-ux/asistente-ia-local.git
cd asistente-ia-local

python -m venv venv
venv\Scripts\activate          # Windows

pip install -r requirements.txt
```

### 3. Ejecutar

```bash
python gui.py      # Interfaz gráfica (recomendado)
# o
python main.py     # Consola
```

---

## Qué puede hacer

- Conversar de forma natural
- Responder preguntas
- Buscar información en internet cuando hace falta
- Recordar el contexto de la conversación
- Hablar con voz del sistema
- Despedirse con "salir" o "adiós"

---

## Estructura

```
core/
  brain.py    → inteligencia + internet
  memory.py   → memoria de conversación
  voice.py    → voz
gui.py        → interfaz gráfica
main.py       → versión consola
```

---

**Autor**: Fabricio Ramos  
**Agosto 2026**
