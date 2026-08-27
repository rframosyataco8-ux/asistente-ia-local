# Asistente IA Local — 100% Desde Cero

**Sin Ollama. Sin modelos pre-entrenados. Sin APIs. Solo código propio.**

Este es un asistente construido completamente desde cero:

- Cerebro propio basado en reglas, intenciones y base de conocimiento
- Voz local (pyttsx3 — motor del sistema)
- Memoria de conversación
- Interfaz gráfica (Tkinter)
- Todo corre en tu PC sin internet

---

## Cómo ejecutarlo

```bash
git clone https://github.com/rframosyataco8-ux/asistente-ia-local.git
cd asistente-ia-local

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

pip install -r requirements.txt

# Opción 1: Interfaz gráfica (recomendado)
python gui.py

# Opción 2: Solo consola
python main.py
```

---

## Estructura del proyecto

```
asistente-ia-local/
├── gui.py              ← Interfaz gráfica
├── main.py             ← Versión de consola
├── requirements.txt
├── core/
│   ├── brain.py        ← Cerebro propio (reglas + intenciones)
│   ├── memory.py       ← Memoria de conversación
│   ├── voice.py        ← Voz local
│   └── stt.py          ← Escucha (en desarrollo)
└── README.md
```

---

## Qué puede hacer ahora

- Saludar y despedirse
- Decir la hora y la fecha
- Responder quién es
- Responder cómo está
- Mostrar ayuda básica
- Recordar el historial de la conversación actual
- Hablar con voz del sistema

---

## Cómo hacerlo más inteligente

Todo está en `core/brain.py`.

Puedes:
1. Agregar más intenciones (palabras clave)
2. Agregar más respuestas en la base de conocimiento
3. Agregar lógica más compleja (cálculos, control de archivos, etc.)
4. Guardar conocimiento en un archivo JSON para que aprenda de forma persistente

Ejemplo de cómo agregar conocimiento:

```python
brain.add_intent("clima", ["clima", "tiempo", "hace calor", "llueve"])
brain.add_knowledge("clima", ["No tengo acceso al clima todavía, pero puedo agregarlo."])
```

---

## Estado actual

| Módulo           | Estado   |
|------------------|----------|
| Cerebro propio   | Listo    |
| Memoria          | Listo    |
| Voz local        | Listo    |
| Interfaz gráfica | Listo    |
| Escucha (STT)    | Pendiente |
| Control de PC    | Pendiente |
| Aprendizaje      | Pendiente |

---

**Autor**: Fabricio Ramos  
**Creado**: Agosto 2026
