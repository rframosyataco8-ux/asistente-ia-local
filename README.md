# Asistente Inteligente

Conversación natural, internet, voz, streaming y memoria a largo plazo.
Corre en tu PC con Ollama (sin APIs de pago).

---

## Novedades

- **Streaming**: el texto aparece poco a poco (como ChatGPT)
- **Memoria a largo plazo**: puedes decirle «recuerda que...» y lo guarda entre sesiones
- **Cambiar modelo** desde la interfaz
- **Ver memoria** guardada
- Voz natural + búsqueda web + herramientas locales

---

## Instalación

### 1. Ollama

https://ollama.com

```bash
ollama pull llama3.2
# Recomendado si tienes 8GB+ RAM:
ollama pull qwen2.5:7b
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

Si ya lo tenías instalado:

```bash
cd asistente-ia-local
git pull
venv\Scripts\activate
pip install -r requirements.txt
python gui.py
```

---

## Ejemplos de uso

```
Hola, ¿cómo estás?
¿Qué hora es?
Busca noticias sobre inteligencia artificial
Recuerda que mi color favorito es el azul
¿Qué recuerdas?
Abre la calculadora
Explícame qué es un transformer
```

---

## Botones de la interfaz

| Botón | Acción |
|-------|--------|
| Limpiar chat | Borra la conversación actual (no borra memoria larga) |
| Cambiar modelo | Elige otro modelo de Ollama |
| Ver memoria | Muestra lo que ha recordado |
| Voz | Activa/desactiva la voz |

La memoria larga se guarda en: `C:\Users\TU_USUARIO\.asistente-ia\`

---

**Autor**: Fabricio Ramos · 2026
