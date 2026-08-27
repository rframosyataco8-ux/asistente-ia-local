# Asistente IA Local — 100% Offline

**Sin APIs externas. Sin costos. Todo corre en tu PC.**

Este proyecto construye un asistente de inteligencia artificial que funciona completamente en local:

- Escucha tu voz (STT local)
- Razona con un modelo local (Ollama / Llama / Phi / Qwen)
- Responde con voz natural (TTS local)
- Tiene memoria de conversación
- Puede controlar tu PC y archivos

> **Importante**: No es un modelo de lenguaje entrenado desde cero (eso requiere millones de dólares y miles de GPUs).  
> Es un **sistema completo de IA local** construido desde cero, usando solo software open-source que corre en tu máquina sin enviar datos a internet.

---

## Arquitectura

```
Micrófono → STT Local (Vosk) → Cerebro (Ollama) → TTS Local (Piper) → Altavoces
                              ↓
                         Memoria local
```

## Requisitos

- Windows / Linux / macOS
- Python 3.10+
- [Ollama](https://ollama.com) instalado
- Micrófono y altavoces

## Instalación rápida

```bash
git clone https://github.com/rframosyataco8-ux/asistente-ia-local.git
cd asistente-ia-local

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt

# Descargar modelo de IA local (elige uno)
ollama pull llama3.2          # recomendado
# ollama pull qwen2.5:3b      # excelente en español
# ollama pull phi3            # más ligero

python main.py
```

## Estado del proyecto

| Módulo              | Estado         | Notas                          |
|---------------------|----------------|--------------------------------|
| Cerebro (Ollama)    | Listo          | Conversación local             |
| Voz (TTS)           | En progreso    | Piper (local) + fallback       |
| Escucha (STT)       | En progreso    | Vosk offline                   |
| Memoria             | En progreso    | Historial de conversación      |
| Control de PC       | Pendiente      | Abrir apps, archivos, etc.     |
| Interfaz            | Pendiente      | Consola primero, luego GUI     |

## Filosofía

- Cero APIs de pago
- Todo el código es tuyo
- Puedes afinar el modelo localmente más adelante
- Se mejora continuamente en este repositorio

---

**Autor**: Fabricio Ramos  
**Creado**: Agosto 2026
