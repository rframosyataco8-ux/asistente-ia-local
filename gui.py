#!/usr/bin/env python3
"""
Interfaz gráfica — Conversación natural e inteligente
"""

import tkinter as tk
from tkinter import scrolledtext
import threading

from core.brain import Brain
from core.memory import Memory
from core.voice import Voice


class AsistenteGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Asistente Inteligente")
        self.root.geometry("780x620")
        self.root.minsize(560, 450)
        self.root.configure(bg="#0f172a")

        self.brain = Brain(model="llama3.2")
        self.memory = Memory(max_messages=24)
        self.voice = Voice()

        self._build_ui()
        self._check_brain()

    def _build_ui(self):
        bg = "#0f172a"
        panel = "#1e293b"
        accent = "#38bdf8"
        text_color = "#e2e8f0"

        # Header
        header = tk.Frame(self.root, bg=bg)
        header.pack(fill=tk.X, padx=16, pady=(16, 6))

        tk.Label(
            header,
            text="Asistente Inteligente",
            font=("Segoe UI", 18, "bold"),
            fg=accent,
            bg=bg
        ).pack(side=tk.LEFT)

        self.status = tk.Label(
            header,
            text="Iniciando...",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg=bg
        )
        self.status.pack(side=tk.RIGHT, pady=(6, 0))

        # Chat
        self.chat = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            bg=panel,
            fg=text_color,
            insertbackground=text_color,
            relief=tk.FLAT,
            padx=14,
            pady=12,
            state=tk.DISABLED
        )
        self.chat.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)

        self.chat.tag_configure("user", foreground="#7dd3fc", font=("Segoe UI", 11, "bold"))
        self.chat.tag_configure("bot", foreground="#86efac", font=("Segoe UI", 11, "bold"))
        self.chat.tag_configure("msg", foreground=text_color)
        self.chat.tag_configure("sys", foreground="#94a3b8", font=("Segoe UI", 9, "italic"))

        # Input
        bar = tk.Frame(self.root, bg=bg)
        bar.pack(fill=tk.X, padx=16, pady=(0, 16))

        self.entry = tk.Entry(
            bar,
            font=("Segoe UI", 12),
            bg=panel,
            fg=text_color,
            insertbackground=text_color,
            relief=tk.FLAT,
            bd=8
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=7)
        self.entry.bind("<Return>", self._on_send)
        self.entry.focus()

        tk.Button(
            bar,
            text="Enviar",
            font=("Segoe UI", 10, "bold"),
            bg=accent,
            fg="#0f172a",
            activebackground="#7dd3fc",
            relief=tk.FLAT,
            padx=16,
            pady=6,
            cursor="hand2",
            command=self._on_send
        ).pack(side=tk.LEFT, padx=(10, 0))

        self.voz_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            bar,
            text="Voz",
            variable=self.voz_var,
            font=("Segoe UI", 10),
            fg=text_color,
            bg=bg,
            selectcolor=panel,
            activebackground=bg,
            activeforeground=text_color
        ).pack(side=tk.LEFT, padx=(12, 0))

    def _check_brain(self):
        if self.brain.is_available():
            self.status.config(text="Listo · modelo local activo", fg="#86efac")
            self._add("sys", "Puedes hablarme con normalidad. Pregúntame lo que quieras.")
        else:
            self.status.config(text="Ollama no detectado", fg="#f87171")
            self._add("sys",
                "No se encontró Ollama o el modelo.\n"
                "1. Instala Ollama: https://ollama.com\n"
                "2. Ejecuta: ollama pull llama3.2\n"
                "3. Vuelve a abrir esta app."
            )

    def _add(self, rol: str, texto: str):
        self.chat.configure(state=tk.NORMAL)
        if rol == "user":
            self.chat.insert(tk.END, "Tú: ", "user")
            self.chat.insert(tk.END, texto + "\n\n", "msg")
        elif rol == "bot":
            self.chat.insert(tk.END, "Asistente: ", "bot")
            self.chat.insert(tk.END, texto + "\n\n", "msg")
        else:
            self.chat.insert(tk.END, texto + "\n\n", "sys")
        self.chat.configure(state=tk.DISABLED)
        self.chat.see(tk.END)

    def _on_send(self, event=None):
        texto = self.entry.get().strip()
        if not texto:
            return
        self.entry.delete(0, tk.END)
        self._add("user", texto)
        self.status.config(text="Pensando...", fg="#fbbf24")
        threading.Thread(target=self._procesar, args=(texto,), daemon=True).start()

    def _procesar(self, texto: str):
        self.memory.add("user", texto)
        respuesta = self.brain.think(texto, self.memory.get_context())
        self.memory.add("assistant", respuesta)

        self.root.after(0, lambda: self._add("bot", respuesta))
        self.root.after(0, lambda: self.status.config(text="Listo", fg="#86efac"))

        if self.voz_var.get():
            self.voice.speak(respuesta)

        if self.brain.should_exit:
            self.root.after(1000, self.root.destroy)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AsistenteGUI()
    app.run()
