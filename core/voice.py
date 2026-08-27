"""
Voz del asistente — 100% local
Usa pyttsx3 (motor de texto a voz del sistema operativo).
No necesita internet ni APIs.
"""

import pyttsx3
from typing import Optional


class Voice:
    def __init__(self, rate: int = 175, volume: float = 1.0):
        self.enabled = True
        self.engine: Optional[pyttsx3.Engine] = None
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", rate)
            self.engine.setProperty("volume", volume)

            # Intentar poner voz en español si existe
            voices = self.engine.getProperty("voices")
            for v in voices:
                # Buscar voces que suenen a español
                name = (v.name or "").lower()
                lang = str(getattr(v, "languages", [])).lower()
                if "spanish" in name or "español" in name or "es_" in lang or "es-" in name:
                    self.engine.setProperty("voice", v.id)
                    break
        except Exception as e:
            print(f"[Aviso] No se pudo iniciar el motor de voz: {e}")
            self.enabled = False

    def speak(self, text: str):
        if not self.enabled or not text or not self.engine:
            return
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"[Voz error]: {e}")

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def set_rate(self, rate: int):
        if self.engine:
            self.engine.setProperty("rate", rate)
