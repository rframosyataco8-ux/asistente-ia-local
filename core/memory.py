"""
Memoria del asistente
- Memoria de la conversación actual
- Memoria a largo plazo (se guarda en disco)
"""

import json
import os
from typing import List, Dict
from collections import deque
from pathlib import Path


class Memory:
    def __init__(self, max_messages: int = 30):
        self.history: deque = deque(maxlen=max_messages)

        # Carpeta de datos del usuario
        self.data_dir = Path.home() / ".asistente-ia"
        self.data_dir.mkdir(exist_ok=True)
        self.long_term_file = self.data_dir / "memoria_larga.json"
        self.long_term: Dict[str, str] = self._load_long_term()

    def add(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def get_context(self) -> List[Dict]:
        return list(self.history)

    def clear(self):
        self.history.clear()

    def last(self, n: int = 1) -> List[Dict]:
        return list(self.history)[-n:]

    # ─── Memoria a largo plazo ──────────────────────────────

    def _load_long_term(self) -> Dict[str, str]:
        if self.long_term_file.exists():
            try:
                with open(self.long_term_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_long_term(self):
        try:
            with open(self.long_term_file, "w", encoding="utf-8") as f:
                json.dump(self.long_term, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[Memoria] No se pudo guardar: {e}")

    def remember(self, key: str, value: str):
        """Guarda un dato importante para futuras sesiones."""
        self.long_term[key.strip().lower()] = value.strip()
        self._save_long_term()

    def recall(self, key: str) -> str:
        return self.long_term.get(key.strip().lower(), "")

    def forget(self, key: str):
        k = key.strip().lower()
        if k in self.long_term:
            del self.long_term[k]
            self._save_long_term()

    def list_memories(self) -> Dict[str, str]:
        return dict(self.long_term)

    def get_long_term_context(self) -> str:
        if not self.long_term:
            return ""
        lines = ["Cosas que recuerdo de Fabricio:"]
        for k, v in self.long_term.items():
            lines.append(f"- {k}: {v}")
        return "\n".join(lines)
