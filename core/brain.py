"""
Cerebro del asistente — 100% desde cero
Sin Ollama, sin modelos pre-entrenados, sin APIs.

Funciona con:
- Detección de intenciones por palabras clave
- Base de conocimiento propia
- Respuestas generadas por reglas + plantillas
- Memoria de conversación
"""

import re
import random
from datetime import datetime
from typing import List, Dict, Optional


class Brain:
    def __init__(self):
        self.name = "Asistente"
        self.owner = "Fabricio"

        # Base de conocimiento simple (se puede ampliar mucho)
        self.knowledge = {
            "saludo": [
                "¡Hola! ¿En qué te puedo ayudar?",
                "Hola Fabricio, ¿qué necesitas?",
                "¡Buenas! Estoy listo.",
            ],
            "despedida": [
                "Hasta luego. Cualquier cosa me avisas.",
                "Adiós, que te vaya bien.",
                "Nos vemos. Cuídate.",
            ],
            "gracias": [
                "De nada.",
                "Para eso estoy.",
                "Con gusto.",
            ],
            "hora": None,  # se calcula en tiempo real
            "fecha": None,
            "quien_eres": [
                "Soy tu asistente local, creado desde cero por ti. No uso ninguna IA externa.",
                "Soy un asistente hecho completamente con código propio. Sin APIs ni modelos de fuera.",
            ],
            "como_estas": [
                "Todo bien, listo para ayudarte.",
                "Funcionando correctamente.",
                "Bien, gracias por preguntar.",
            ],
            "ayuda": [
                "Puedo responder saludos, decir la hora y fecha, recordar cosas de la conversación y más. "
                "Ve agregando conocimiento y reglas para que sea más inteligente.",
            ],
        }

        # Intenciones: palabra clave → nombre de intención
        self.intents = {
            "saludo": ["hola", "buenas", "buenos días", "buenas tardes", "buenas noches", "hey", "qué tal"],
            "despedida": ["adiós", "adios", "chao", "hasta luego", "nos vemos", "bye", "salir"],
            "gracias": ["gracias", "te agradezco", "muy amable"],
            "hora": ["qué hora", "que hora", "hora es", "hora actual", "dime la hora"],
            "fecha": ["qué fecha", "que fecha", "qué día", "fecha de hoy", "día es"],
            "quien_eres": ["quién eres", "quien eres", "qué eres", "que eres", "tu nombre", "cómo te llamas"],
            "como_estas": ["cómo estás", "como estas", "qué tal estás", "todo bien"],
            "ayuda": ["ayuda", "qué puedes hacer", "que puedes hacer", "comandos", "opciones"],
        }

    def _normalize(self, text: str) -> str:
        text = text.lower().strip()
        # Quitar signos básicos
        text = re.sub(r"[¿?¡!.,;:]", "", text)
        return text

    def _detect_intent(self, text: str) -> Optional[str]:
        normalized = self._normalize(text)
        for intent, keywords in self.intents.items():
            for kw in keywords:
                if kw in normalized:
                    return intent
        return None

    def _get_time(self) -> str:
        now = datetime.now()
        return now.strftime("Son las %H:%M")

    def _get_date(self) -> str:
        now = datetime.now()
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                 "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        dia_semana = dias[now.weekday()]
        return f"Hoy es {dia_semana} {now.day} de {meses[now.month-1]} de {now.year}"

    def think(self, user_message: str, context: List[Dict] = None) -> str:
        """
        Genera una respuesta usando solo lógica propia.
        """
        if not user_message or not user_message.strip():
            return "No escuché nada. ¿Puedes repetir?"

        intent = self._detect_intent(user_message)

        if intent == "saludo":
            return random.choice(self.knowledge["saludo"])

        if intent == "despedida":
            return random.choice(self.knowledge["despedida"])

        if intent == "gracias":
            return random.choice(self.knowledge["gracias"])

        if intent == "hora":
            return self._get_time()

        if intent == "fecha":
            return self._get_date()

        if intent == "quien_eres":
            return random.choice(self.knowledge["quien_eres"])

        if intent == "como_estas":
            return random.choice(self.knowledge["como_estas"])

        if intent == "ayuda":
            return random.choice(self.knowledge["ayuda"])

        # Si no reconoce la intención
        return (
            "Todavía no sé responder eso. "
            "Estoy aprendiendo con reglas propias. "
            "Puedes enseñarme agregando más conocimiento en el código."
        )

    def is_available(self) -> bool:
        return True  # Siempre disponible, no depende de nada externo

    def add_knowledge(self, intent: str, responses: List[str]):
        """Permite ampliar la base de conocimiento en tiempo de ejecución."""
        self.knowledge[intent] = responses

    def add_intent(self, intent: str, keywords: List[str]):
        self.intents[intent] = keywords
