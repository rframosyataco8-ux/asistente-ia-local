"""
Voz natural de alta calidad
Prioridad: edge-tts (voces neurales) → fallback pyttsx3
"""

import asyncio
import tempfile
import os
import platform
import subprocess
from typing import Optional


class Voice:
    def __init__(self, voice: str = "es-MX-DaliaNeural"):
        self.voice_name = voice
        self.enabled = True
        self.engine = None
        self.use_edge = False

        # Intentar edge-tts primero (mucho más natural)
        try:
            import edge_tts  # noqa
            self.use_edge = True
        except ImportError:
            self.use_edge = False
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 175)
                self.engine.setProperty("volume", 1.0)
                voices = self.engine.getProperty("voices")
                for v in voices:
                    name = (v.name or "").lower()
                    if "spanish" in name or "español" in name or "es-" in name:
                        self.engine.setProperty("voice", v.id)
                        break
            except Exception:
                self.enabled = False

    def speak(self, text: str):
        if not self.enabled or not text or not text.strip():
            return

        # Limitar longitud para no hablar textos enormes
        if len(text) > 600:
            text = text[:600] + "..."

        try:
            if self.use_edge:
                asyncio.run(self._speak_edge(text))
            elif self.engine:
                self.engine.say(text)
                self.engine.runAndWait()
        except Exception as e:
            print(f"[Voz]: {e}")

    async def _speak_edge(self, text: str):
        import edge_tts
        communicate = edge_tts.Communicate(text, self.voice_name)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            path = f.name

        await communicate.save(path)

        system = platform.system()
        try:
            if system == "Windows":
                # playsound-like con powershell / start
                os.system(f'start /min "" "{path}"')
                # Espera aproximada
                await asyncio.sleep(min(len(text) * 0.055 + 0.8, 25))
            elif system == "Darwin":
                subprocess.run(["afplay", path], check=False)
            else:
                # Linux
                for player in (["mpg123", "-q"], ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet"]):
                    try:
                        subprocess.run(player + [path], check=False)
                        break
                    except FileNotFoundError:
                        continue
        finally:
            try:
                os.unlink(path)
            except Exception:
                pass

    def set_voice(self, voice: str):
        self.voice_name = voice

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True
