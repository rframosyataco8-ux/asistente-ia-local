"""
Voz natural — sin abrir ventanas de reproductor
Usa edge-tts + reproducción silenciosa en Windows
"""

import asyncio
import tempfile
import os
import platform
import subprocess
import time
from typing import Optional


class Voice:
    def __init__(self, voice: str = "es-MX-DaliaNeural"):
        self.voice_name = voice
        self.enabled = True
        self.engine = None
        self.use_edge = False
        self.use_pygame = False

        # Preferir edge-tts (voz natural)
        try:
            import edge_tts  # noqa: F401
            self.use_edge = True
        except ImportError:
            self.use_edge = False

        # pygame para reproducir sin abrir ventanas
        try:
            import pygame
            pygame.mixer.init()
            self.use_pygame = True
        except Exception:
            self.use_pygame = False

        # Fallback pyttsx3 (voz del sistema, sin archivos)
        if not self.use_edge:
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 175)
                self.engine.setProperty("volume", 1.0)
                for v in self.engine.getProperty("voices"):
                    name = (v.name or "").lower()
                    if "spanish" in name or "español" in name or "es-" in name:
                        self.engine.setProperty("voice", v.id)
                        break
            except Exception:
                if not self.use_edge:
                    self.enabled = False

    def speak(self, text: str):
        if not self.enabled or not text or not text.strip():
            return

        # No leer respuestas enormes enteras
        if len(text) > 500:
            text = text[:500] + "..."

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

        try:
            await communicate.save(path)
            self._play_file(path)
        finally:
            # Esperar un poco antes de borrar (por si el player aún lo usa)
            time.sleep(0.3)
            try:
                os.unlink(path)
            except Exception:
                pass

    def _play_file(self, path: str):
        """Reproduce el audio sin abrir ventanas."""
        system = platform.system()

        # 1) pygame (mejor opción, silencioso)
        if self.use_pygame:
            try:
                import pygame
                pygame.mixer.music.load(path)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                return
            except Exception as e:
                print(f"[pygame]: {e}")

        # 2) Windows: PowerShell con MediaPlayer silencioso (sin ventana visible)
        if system == "Windows":
            try:
                # Usa Windows Media Player COM en modo oculto vía PowerShell
                ps = (
                    f'$p = New-Object -ComObject WMPlayer.OCX; '
                    f'$p.URL = \"{path}\"; '
                    f'$p.controls.play(); '
                    f'while ($p.playState -ne 1) {{ Start-Sleep -Milliseconds 200 }}; '
                    f'$p.close()'
                )
                subprocess.run(
                    ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps],
                    check=False,
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0
                )
                return
            except Exception:
                pass

            # Fallback: start minimizado (último recurso)
            try:
                os.system(f'start /min "" "{path}"')
                time.sleep(min(len(path) * 0.01 + 2, 15))
                return
            except Exception:
                pass

        # 3) macOS
        if system == "Darwin":
            subprocess.run(["afplay", path], check=False)
            return

        # 4) Linux
        for cmd in (
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", path],
            ["mpg123", "-q", path],
            ["aplay", path],
        ):
            try:
                subprocess.run(cmd, check=False)
                return
            except FileNotFoundError:
                continue

    def set_voice(self, voice: str):
        self.voice_name = voice

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True
