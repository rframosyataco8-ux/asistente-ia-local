"""
Cerebro avanzado del asistente
Conversación natural + herramientas + internet + memoria
"""

import ollama
import requests
import re
import os
import platform
import subprocess
import socket
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import quote


class Brain:
    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.should_exit = False
        self.system = platform.system()

        self.system_prompt = """Eres un asistente de IA avanzado, inteligente, útil y conversacional.
Hablas siempre en español de forma natural, clara y cercana (como un buen amigo experto).
Eres el asistente personal de Fabricio Ramos.

Tus capacidades:
- Conversar con naturalidad sobre cualquier tema
- Razonar paso a paso cuando sea necesario
- Usar información de internet cuando la tengas
- Ayudar con código, ideas, explicaciones, planificación, etc.
- Ser sincero: si no sabes algo, lo dices
- Ser conciso o detallado según el contexto

Estilo:
- Natural, no robótico
- Amable pero directo
- Sin rodeos innecesarios
- Puedes usar humor ligero cuando encaje

Si te dan resultados de internet, intégralos de forma natural en tu respuesta.
Si el usuario pide acciones del sistema (abrir programas, hora, etc.), responde de forma útil."""

    def is_available(self) -> bool:
        try:
            models = ollama.list()
            names = [m.get("name", "") for m in models.get("models", [])]
            return any(self.model in n for n in names)
        except Exception:
            return False

    def available_models(self) -> List[str]:
        try:
            models = ollama.list()
            return [m.get("name", "") for m in models.get("models", [])]
        except Exception:
            return []

    # ─── Herramientas locales ───────────────────────────────

    def tool_time(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def tool_date(self) -> str:
        now = datetime.now()
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                 "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        return f"{dias[now.weekday()]} {now.day} de {meses[now.month-1]} de {now.year}"

    def tool_system_info(self) -> str:
        return (
            f"Sistema: {platform.system()} {platform.release()}\n"
            f"Arquitectura: {platform.machine()}\n"
            f"Python: {platform.python_version()}"
        )

    def tool_ip(self) -> str:
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except Exception:
            return "No disponible"

    def tool_open(self, target: str) -> str:
        target = target.strip().lower()
        mapping = {
            "calculadora": "calc" if self.system == "Windows" else "gnome-calculator",
            "notas": "notepad" if self.system == "Windows" else "gedit",
            "explorador": "explorer" if self.system == "Windows" else "xdg-open ~",
            "documentos": os.path.expanduser("~/Documents"),
            "descargas": os.path.expanduser("~/Downloads"),
            "escritorio": os.path.expanduser("~/Desktop"),
            "chrome": "start chrome" if self.system == "Windows" else "google-chrome",
            "navegador": "start https://google.com" if self.system == "Windows" else "xdg-open https://google.com",
        }
        try:
            cmd = mapping.get(target, target)
            if self.system == "Windows":
                if cmd.startswith("start "):
                    os.system(cmd)
                else:
                    subprocess.Popen(cmd, shell=True)
            else:
                subprocess.Popen(cmd, shell=True)
            return f"Abierto: {target}"
        except Exception as e:
            return f"No se pudo abrir: {e}"

    def tool_calc(self, expression: str) -> str:
        try:
            # Solo operaciones matemáticas seguras
            allowed = set("0123456789+-*/().% ")
            if not all(c in allowed for c in expression):
                return "Expresión no permitida"
            result = eval(expression, {"__builtins__": {}})
            return str(result)
        except Exception:
            return "No se pudo calcular"

    # ─── Búsqueda web mejorada ──────────────────────────────

    def web_search(self, query: str, max_results: int = 5) -> str:
        try:
            url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            }
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            html = r.text

            def clean(s):
                s = re.sub(r"<[^>]+>", "", s)
                s = re.sub(r"\s+", " ", s)
                return s.strip()

            titles = re.findall(r'class="result__a"[^>]*>(.*?)</a>', html, re.DOTALL)
            snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</(?:a|div)>', html, re.DOTALL)

            results = []
            for i, title in enumerate(titles[:max_results]):
                t = clean(title)
                s = clean(snippets[i]) if i < len(snippets) else ""
                if t and len(t) > 3:
                    results.append(f"• {t}\n  {s}" if s else f"• {t}")

            if not results:
                return "No se encontraron resultados relevantes."

            return "Resultados de internet:\n\n" + "\n\n".join(results)
        except Exception as e:
            return f"Error al buscar en internet: {e}"

    def _should_search(self, text: str) -> bool:
        t = text.lower()
        keys = [
            "busca", "buscar", "qué es", "que es", "quién es", "quien es",
            "noticias", "actualidad", "último", "reciente", "hoy",
            "precio", "clima", "tiempo en", "definición", "define",
            "información sobre", "explica qué", "dime sobre",
            "cómo funciona", "como funciona", "wikipedia",
            "cuánto", "cuanto cuesta", "dónde queda", "donde queda"
        ]
        if any(k in t for k in keys):
            return True
        # Preguntas abiertas largas
        if "?" in t and len(t.split()) >= 4:
            return True
        return False

    def _detect_local_tools(self, text: str) -> Optional[str]:
        """Ejecuta herramientas locales si el mensaje es claramente una acción."""
        t = text.lower().strip()

        if any(w in t for w in ["qué hora", "que hora", "hora es", "hora actual"]):
            return f"Son las {self.tool_time()}."

        if any(w in t for w in ["qué fecha", "que fecha", "qué día", "fecha de hoy", "día es hoy"]):
            return f"Hoy es {self.tool_date()}."

        if "mi ip" in t or "ip local" in t or "cuál es mi ip" in t:
            return f"Tu IP local es {self.tool_ip()}."

        if "info del sistema" in t or "información del sistema" in t or "datos del pc" in t:
            return self.tool_system_info()

        # Abrir algo
        m = re.search(r"(?:abre|abrir|abreme|ábreme)\s+(.+)", t)
        if m:
            return self.tool_open(m.group(1))

        # Cálculo simple
        m = re.search(r"(?:calcula|cuánto es|cuanto es)\s+(.+)", t)
        if m:
            expr = m.group(1).replace("x", "*").replace("÷", "/")
            return f"Resultado: {self.tool_calc(expr)}"

        return None

    # ─── Pensar ─────────────────────────────────────────────

    def think(self, user_message: str, context: List[Dict] = None) -> str:
        if not user_message or not user_message.strip():
            return "¿Sí? Dime en qué te ayudo."

        low = user_message.strip().lower()
        if low in ("salir", "adiós", "adios", "exit", "cerrar", "chao"):
            self.should_exit = True
            return "Hasta luego, Fabricio. Cuando me necesites aquí estaré."

        # Primero intentar herramientas locales rápidas
        local = self._detect_local_tools(user_message)
        if local:
            return local

        # Búsqueda web si hace falta
        extra = ""
        if self._should_search(user_message):
            extra = self.web_search(user_message)

        messages = [{"role": "system", "content": self.system_prompt}]

        if context:
            messages.extend(context[-16:])  # más contexto

        if extra:
            messages.append({
                "role": "system",
                "content": (
                    "Información actual obtenida de internet. "
                    "Úsala si es relevante para responder de forma precisa:\n\n" + extra
                )
            })

        # Contexto de fecha/hora siempre disponible
        messages.append({
            "role": "system",
            "content": f"Fecha y hora actual: {self.tool_date()} — {self.tool_time()}"
        })

        messages.append({"role": "user", "content": user_message})

        try:
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 800,
                }
            )
            return response["message"]["content"].strip()
        except Exception as e:
            return (
                f"Error al generar respuesta: {e}\n\n"
                "Verifica que Ollama esté corriendo y que tengas el modelo:\n"
                f"  ollama pull {self.model}"
            )

    def set_model(self, model: str):
        self.model = model
