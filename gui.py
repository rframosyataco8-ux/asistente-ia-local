#!/usr/bin/env python3
"""
Interfaz gráfica avanzada del Asistente Inteligente
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading

from core.brain import Brain
from core.memory import Memory
from core.voice import Voice


class AsistenteGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Asistente Inteligente")
        self.root.geometry("820x660")
        self.root.minsize(580, 480)
        self.root.configure(bg="#0b1220")

        self.brain = Brain(model="llama3.2")
        self.memory = Memory(max_messages=30)
        self.voice = Voice()
        self.busy = False

        self._build_ui()
        self._check_brain()

    def _build_ui(self):
        bg = "#0b1220"
        panel = "#151e2e"
        accent = "#38bdf8"
        text = "#e2e8f0"

        # Header
        header = tk.Frame(self.root, bg=bg)
        header.pack(fill=tk.X, padx=18, pady=(16, 4))

        tk.Label(
            header, text="Asistente Inteligente",
            font=("Segoe UI", 18, "bold"), fg=accent, bg=bg
        ).pack(side=tk.LEFT)

        self.status = tk.Label(
            header, text="Iniciando...",
            font=("Segoe UI", 9), fg="#94a3b8", bg=bg
        )
        self.status.pack(side=tk.RIGHT, pady=(8, 0))

        # Toolbar
        tools = tk.Frame(self.root, bg=bg)
        tools.pack(fill=tk.X, padx=18, pady=(0, 4))

        def btn(text, cmd):
            b = tk.Button(
                tools, text=text, command=cmd,
                font=("Segoe UI", 9), bg=panel, fg=text,
                activebackground="#1e293b", activeforeground=text,
                relief=tk.FLAT, padx=10, pady=3, cursor="hand2"
            )
            b.pack(side=tk.LEFT, padx=(0, 6))
            return b

        btn("Limpiar chat", self._clear_chat)
        btn("Modelos", self._show_models)

        self.voz_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            tools, text="Voz", variable=self.voz_var,
            font=("Segoe UI", 9), fg=text, bg=bg,
            selectcolor=panel, activebackground=bg, activeforeground=text
        ).pack(side=tk.RIGHT)

        # Chat
        self.chat = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, font=("Segoe UI", 11),
            bg=panel, fg=text, insertbackground=text,
            relief=tk.FLAT, padx=14, pady=12, state=tk.DISABLED
        )
        self.chat.pack(fill=tk.BOTH, expand=True, padx=18, pady=8)

        self.chat.tag_configure("user", foreground="#7dd3fc", font=("Segoe UI", 11, "bold"))
        self.chat.tag_configure("bot", foreground="#4ade80", font=("Segoe UI", 11, "bold"))
        self.chat.tag_configure("msg", foreground=text)
        self.chat.tag_configure("sys", foreground="#94a3b8", font=("Segoe UI", 9, "italic"))

        # Input
        bar = tk.Frame(self.root, bg=bg)
        bar.pack(fill=tk.X, padx=18, pady=(0, 16))

        self.entry = tk.Entry(
            bar, font=("Segoe UI", 12), bg=panel, fg=text,
            insertbackground=text, relief=tk.FLAT, bd=8
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        self.entry.bind("<Return>", self._on_send)
        self.entry.focus()

        tk.Button(
            bar, text="Enviar", font=("Segoe UI", 10, "bold"),
            bg=accent, fg="#0b1220", activebackground="#7dd3fc",
            relief=tk.FLAT, padx=18, pady=7, cursor="hand2",
            command=self._on_send
        ).pack(side=tk.LEFT, padx=(10, 0))

    def _check_brain(self):
        if self.brain.is_available():
            self.status.config(text=f"Listo · {self.brain.model}", fg="#4ade80")
            self._add("sys", "Hola. Puedes hablarme con naturalidad. Pregúntame lo que quieras.")
        else:
            self.status.config(text="Ollama no detectado", fg="#f87171")
            self._add("sys",
                "No se detectó Ollama o el modelo.\n\n"
                "1. Instala Ollama → https://ollama.com\n"
                "2. Ejecuta en terminal:  ollama pull llama3.2\n"
                "3. Vuelve a abrir esta aplicación.\n\n"
                "Modelos recomendados:\n"
                "  ollama pull llama3.2\n"
                "  ollama pull qwen2.5:7b\n"
                "  ollama pull llama3.1:8b"
            )

    def _add(self, rol, texto):
        self.chat.configure(state=tk.NORMAL)
        if rol == "user":
            self.chat.insert(tk.END, "Tú\n", "user")
            self.chat.insert(tk.END, texto + "\n\n", "msg")
        elif rol == "bot":
            self.chat.insert(tk.END, "Asistente\n", "bot")
            self.chat.insert(tk.END, texto + "\n\n", "msg")
        else:
            self.chat.insert(tk.END, texto + "\n\n", "sys")
        self.chat.configure(state=tk.DISABLED)
        self.chat.see(tk.END)

    def _clear_chat(self):
        self.memory.clear()
        self.chat.configure(state=tk.NORMAL)
        self.chat.delete("1.0", tk.END)
        self.chat.configure(state=tk.DISABLED)
        self._add("sys", "Chat limpiado. ¿En qué te ayudo?")

    def _show_models(self):
        models = self.brain.available_models()
        if not models:
            messagebox.showinfo("Modelos", "No se detectaron modelos.\nEjecuta: ollama list")
            return
        msg = "Modelos instalados:\n\n" + "\n".join(f"• {m}" for m in models)
        msg += f"\n\nActual: {self.brain.model}"
        messagebox.showinfo("Modelos", msg)

    def _on_send(self, event=None):
        if self.busy:
            return
        texto = self.entry.get().strip()
        if not texto:
            return
        self.entry.delete(0, tk.END)
        self._add("user", texto)
        self.busy = True
        self.status.config(text="Pensando...", fg="#fbbf24")
        threading.Thread(target=self._procesar, args=(texto,), daemon=True).start()

    def _procesar(self, texto):
        self.memory.add("user", texto)
        respuesta = self.brain.think(texto, self.memory.get_context())
        self.memory.add("assistant", respuesta)

        self.root.after(0, lambda: self._add("bot", respuesta))
        self.root.after(0, lambda: self.status.config(
            text=f"Listo · {self.brain.model}", fg="#4ade80"
        ))
        self.root.after(0, lambda: setattr(self, "busy", False))

        if self.voz_var.get():
            self.voice.speak(respuesta)

        if self.brain.should_exit:
            self.root.after(1200, self.root.destroy)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AsistenteGUI()
    app.run()
