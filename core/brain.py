"""
Cerebro del asistente - Usa Ollama local (sin APIs externas)
"""

import ollama
from typing import List, Dict


class Brain:
    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.system_prompt = (
            "Eres un asistente de IA local, útil, amable y conciso. "
            "Respondes siempre en español. "
            "Eres sincero: si no sabes algo, lo dices. "
            "No inventas información. "
            "Eres el asistente personal de Fabricio Ramos."
        )

    def is_available(self) -> bool:
        """Verifica si Ollama está corriendo y el modelo existe."""
        try:
            models = ollama.list()
            model_names = [m["name"] for m in models.get("models", [])]
            # Ollama a veces agrega :latest
            return any(self.model in name for name in model_names)
        except Exception:
            return False

    def think(self, user_message: str, context: List[Dict] = None) -> str:
        """
        Genera una respuesta usando el modelo local.
        context: lista de mensajes previos [{"role": "user/assistant", "content": "..."}]
        """
        messages = [{"role": "system", "content": self.system_prompt}]

        if context:
            messages.extend(context)

        messages.append({"role": "user", "content": user_message})

        try:
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": 0.7,
                    "num_predict": 512,  # límite de tokens de respuesta
                }
            )
            return response["message"]["content"].strip()
        except Exception as e:
            return f"Error al pensar: {str(e)}. ¿Está Ollama corriendo?"

    def set_model(self, model: str):
        self.model = model
