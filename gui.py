#!/usr/bin/env python3
"""
Interfaz gráfica — Solo por comandos
"""

import tkinter as tk
from tkinter import scrolledtext
import threading
import sys

from core.brain import Brain
from core.memory import Memory
from core.voice import Voice


class AsistenteGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Asistente por Comandos")
        self.root.geometry("740x580")
        self.root.minsize(520, 420)
        self.root.configure(bg="#0f172a")

        self.brain = Brain()
        self.memory = Memory()
        self.voice = Voice()

        self._build_ui()
        self._mostrar_inicio()

    def _build_ui(self):
        bg = "#0f172a"
        panel = "#1e293b"
        accent = "#38bdf8"
        text_color = "#e2e8f0"

        # Título
        title_frame = tk.Frame(self.root, bg=bg)
        title_frame.pack(fill=tk.X, padx=16, pady=(16, 4))

        tk.Label(
            title_frame,
            text="Asistente por Comandos",
            font=("Segoe UI", 18, "bold"),
            fg=accent,
            bg=bg
        ).pack(side=tk.LEFT)

        tk.Label(
            title_frame,
            text="100% desde cero",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg=bg
        ).pack(side=tk.LEFT, padx=(12, 0), pady=(8, 0))

        # Área de salida
        self.chat = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg=panel,
            fg=text_color,
            insertbackground=text_color,
            relief=tk.FLAT,
            padx=14,
            pady=12,
            state=tk.DISABLED
        )
        self.chat.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)

        self.chat.tag_configure("cmd", foreground="#7dd3fc", font=("Consolas", 11, "bold"))
        self.chat.tag_configure("out", foreground="#86efac")
        self.chat.tag_configure("sys", foreground="#94a3b8", font=("Consolas", 10, "italic"))
        self.chat.tag_configure("err", foreground="#f87171")

        # Entrada
        input_frame = tk.Frame(self.root, bg=bg)
        input_frame.pack(fill=tk.X, padx=16, pady=(0, 16))

        tk.Label(
            input_frame,
            text=">",
            font=("Consolas", 14, "bold"),
            fg=accent,
            bg=bg
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.entry = tk.Entry(
            input_frame,
            font=("Consolas", 12),
            bg=panel,
            fg=text_color,
            insertbackground=text_color,
            relief=tk.FLAT,
            bd=8
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
        self.entry.bind("<Return>", self._on_send)
        self.entry.focus()

        tk.Button(
            input_frame,
            text="Ejecutar",
            font=("Segoe UI", 10, "bold"),
            bg=accent,
            fg="#0f172a",
            activebackground="#7dd3fc",
            relief=tk.FLAT,
            padx=14,
            pady=5,
            cursor="hand2",
            command=self._on_send
        ).pack(side=tk.LEFT, padx=(10, 0))

        self.voz_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            input_frame,
            text="Voz",
            variable=self.voz_var,
            font=("Segoe UI", 10),
            fg=text_color,
            bg=bg,
            selectcolor=panel,
            activebackground=bg,
            activeforeground=text_color
        ).pack(side=tk.LEFT, padx=(12, 0))

    def _mostrar_inicio(self):
        self._print("sys", "Escribe un comando. Ejemplo: ayuda")
        self._print("sys", "────────────────────────────────────")

    def _print(self, tag: str, texto: str):
        self.chat.configure(state=tk.NORMAL)
        self.chat.insert(tk.END, texto + "\n", tag)
        self.chat.configure(state=tk.DISABLED)
        self.chat.see(tk.END)

    def _on_send(self, event=None):
        texto = self.entry.get().strip()
        if not texto:
            return

        self.entry.delete(0, tk.END)
        self._print("cmd", f"> {texto}")

        threading.Thread(target=self._ejecutar, args=(texto,), daemon=True).start()

    def _ejecutar(self, texto: str):
        self.memory.add("user", texto)
        respuesta = self.brain.think(texto, self.memory.get_context())
        self.memory.add("assistant", respuesta)

        self.root.after(0, lambda: self._print("out", respuesta))
        self.root.after(0, lambda: self._print("sys", ""))

        if self.voz_var.get():
            # Hablar solo la primera línea para no ser muy largo
            primera = respuesta.split("\n")[0]
            self.voice.speak(primera)

        if self.brain.should_exit:
            self.root.after(800, self.root.destroy)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AsistenteGUI()
    app.run()
