"""
Módulo de voz (Text-to-Speech)

Por ahora usa edge-tts (voces neurales de Microsoft, gratis y de alta calidad).
Más adelante se puede reemplazar por Piper TTS 100% offline.

Nota: edge-tts no requiere API key ni cuenta. Es un endpoint público gratuito.
Si quieres 100% offline sin internet, cambia a pyttsx3 o Piper.
"""

import asyncio
import edge_tts
import tempfile
import os
import subprocess
import platform


class Voice:
    def __init__(self, voice: str = "es-MX-DaliaNeural"):
        """
        Voces recomendadas en español:
        - es-MX-DaliaNeural (femenina, natural)
        - es-MX-JorgeNeural (masculina)
        - es-ES-ElviraNeural
        - es-AR-ElenaNeural
        """
        self.voice = voice
        self.enabled = True

    def speak(self, text: str):
        if not self.enabled or not text.strip():
            return
        try:
            asyncio.run(self._speak_async(text))
        except Exception as e:
            # Fallback silencioso si falla la voz
            print(f"[Voz no disponible: {e}]")

    async def _speak_async(self, text: str):
        communicate = edge_tts.Communicate(text, self.voice)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tmp_path = f.name

        await communicate.save(tmp_path)

        # Reproducir según el sistema operativo
        system = platform.system()
        try:
            if system == "Windows":
                # Usa el reproductor por defecto de Windows
                os.startfile(tmp_path)
                # Pequeña espera aproximada (mejorable con playsound o pygame)
                await asyncio.sleep(len(text) * 0.06 + 1.0)
            elif system == "Darwin":  # macOS
                subprocess.run(["afplay", tmp_path], check=False)
            else:  # Linux
                subprocess.run(["mpg123", "-q", tmp_path], check=False)
        finally:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass

    def set_voice(self, voice: str):
        self.voice = voice

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True
