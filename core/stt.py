"""
Speech-to-Text local (offline)

Primera versión: estructura lista para Vosk.
Vosk es 100% offline y funciona bien en español.

Para activarlo:
1. pip install vosk sounddevice
2. Descargar modelo: https://alphacephei.com/vosk/models
   (recomendado: vosk-model-small-es-0.42)
3. Descomprimir en carpeta models/
"""

from typing import Optional


class STT:
    def __init__(self, model_path: str = "models/vosk-model-small-es-0.42"):
        self.model_path = model_path
        self.available = False
        self._model = None
        self._try_load()

    def _try_load(self):
        try:
            from vosk import Model, KaldiRecognizer
            import os
            if os.path.exists(self.model_path):
                self._model = Model(self.model_path)
                self.available = True
        except Exception:
            self.available = False

    def listen(self, timeout: float = 5.0) -> Optional[str]:
        """
        Escucha del micrófono y devuelve el texto reconocido.
        Por ahora retorna None si no está configurado.
        """
        if not self.available:
            return None

        # Implementación completa se agregará en la siguiente iteración
        # (requiere sounddevice + loop de audio)
        return None

    def is_available(self) -> bool:
        return self.available
