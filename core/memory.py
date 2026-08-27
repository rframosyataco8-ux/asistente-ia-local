"""
Memoria simple del asistente.
Guarda el historial de la conversación actual.
Más adelante se puede expandir con embeddings locales y persistencia.
"""

from typing import List, Dict
from collections import deque


class Memory:
    def __init__(self, max_messages: int = 20):
        """
        max_messages: cuántos mensajes recientes recordar
        (para no saturar el contexto del modelo)
        """
        self.history: deque = deque(maxlen=max_messages)

    def add(self, role: str, content: str):
        """role: 'user' o 'assistant'"""
        self.history.append({"role": role, "content": content})

    def get_context(self) -> List[Dict]:
        """Devuelve el historial en formato para Ollama."""
        return list(self.history)

    def clear(self):
        self.history.clear()

    def last(self, n: int = 1) -> List[Dict]:
        return list(self.history)[-n:]
