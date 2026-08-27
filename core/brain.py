"""
Cerebro del asistente — Conversación natural + inteligencia + internet
Usa Ollama (modelo local en tu PC). Sin APIs de pago.
"""

import ollama
import requests
import re
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import quote


class Brain:
    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.should_exit = False

        self.system_prompt = (
            "Eres un asistente inteligente, amable y natural. "
            "Hablas siempre en español de forma clara y conversacional. "
            "Eres el asistente personal de Fabricio Ramos. "
            "Puedes responder cualquier pregunta, conversar libremente, "
            "dar opiniones, explicar temas y ayudar en lo que necesite. "
            "Si te dan información de internet, úsala para responder mejor. "
            "Sé conciso cuando haga falta y más detallado cuando el tema lo pida. "
            "Si no sabes algo con certeza, dilo."
        )

    def is_available(self) -> bool:
        try:
            models = ollama.list()
            names = [m.get("name", "") for m in models.get("models", [])]
            return any(self.model in n for n in names)
        except Exception:
            return False

    def _needs_search(self, text: str) -> bool:
        """Decide si la pregunta necesita buscar en internet."""
        t = text.lower()
        triggers = [
            "busca", "buscar", "qué es", "que es", "quién es", "quien es",
            "noticias", "último", "ultima", "actualidad", "clima",
            "precio", "cotización", "cómo se", "como se",
            "wikipedia", "define", "definición", "información sobre",
            "dime sobre", "explícame", "explica",
            "hoy", "ahora", "actual", "reciente"
        ]
        # También buscar si parece una pregunta de conocimiento
        if any(w in t for w in triggers):
            return True
        if t.endswith("?") and len(t.split()) > 3:
            return True
        return False

    def _web_search(self, query: str, max_results: int = 4) -> str:
        """Búsqueda web simple usando DuckDuckGo (sin API key)."""
        try:
            url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            r = requests.get(url, headers=headers, timeout=8)
            r.raise_for_status()

            # Extraer resultados de forma simple
            results = []
            # Buscar títulos y snippets aproximados
            titles = re.findall(r'class="result__a"[^>]*>(.*?)</a>', r.text, re.DOTALL)
            snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', r.text, re.DOTALL)
            # Limpiar HTML básico
            clean = lambda s: re.sub(r'<[^>]+>', '', s).strip()

            for i, title in enumerate(titles[:max_results]):
                t = clean(title)
                s = clean(snippets[i]) if i < len(snippets) else ""
                if t:
                    results.append(f"- {t}: {s}" if s else f"- {t}")

            if not results:
                return "No se encontraron resultados claros en internet."

            return "Información encontrada en internet:\n" + "\n".join(results)
        except Exception as e:
            return f"(No se pudo buscar en internet: {e})"

    def think(self, user_message: str, context: List[Dict] = None) -> str:
        if not user_message or not user_message.strip():
            return "¿Sí? Dime."

        # Detectar comando de salida
        if user_message.strip().lower() in ("salir", "adiós", "adios", "exit", "cerrar"):
            self.should_exit = True
            return "Hasta luego. ¡Que te vaya bien!"

        # Buscar en internet si hace falta
        extra_info = ""
        if self._needs_search(user_message):
            extra_info = self._web_search(user_message)

        messages = [{"role": "system", "content": self.system_prompt}]

        if context:
            # Limitar contexto para no saturar
            messages.extend(context[-12:])

        if extra_info:
            messages.append({
                "role": "system",
                "content": f"Usa esta información reciente de internet para responder si es útil:\n{extra_info}"
            })

        messages.append({"role": "user", "content": user_message})

        try:
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": 0.75,
                    "num_predict": 600,
                }
            )
            return response["message"]["content"].strip()
        except Exception as e:
            return (
                f"No pude pensar bien: {e}\n\n"
                "Asegúrate de tener Ollama instalado y el modelo descargado:\n"
                "  ollama pull llama3.2"
            )

    def set_model(self, model: str):
        self.model = model
