#!/usr/bin/env python3
"""
Interfaz gráfica del Asistente IA Local
Hecha con Tkinter (viene con Python, no necesita instalar nada extra)
"""

import tkinter as tk
from tkinter import scrolledtext, font
import threading

from core.brain import Brain
from core.memory import Memory
from core.voice import Voice


class AsistenteGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Asistente IA Local — Desde cero")
        self.root.geometry("720x560")
        self.root.minsize(500, 400)
        self.root.configure(bg="#0f172a")

        self.brain = Brain()
        self.memory = Memory()
        self.voice = Voice()

        self._build_ui()
        self._mostrar_bienvenida()

    def _build_ui(self):
        # Colores
        bg = "#0f172a"
        panel = "#1e293b"
        accent = "#38bdf8"
        text_color = "#e2e8f0"
        user_bg = "#1e3a5f"
        bot_bg = "#1e293b"

        # Título
        title_frame = tk.Frame(self.root, bg=bg)
        title_frame.pack(fill=tk.X, padx=16, pady=(16, 8))

        title = tk.Label(
            title_frame,
            text="Asistente IA Local",
            font=("Segoe UI", 18, "bold"),
            fg=accent,
            bg=bg
        )
        title.pack(side=tk.LEFT)

        subtitle = tk.Label(
            title_frame,
            text="100% desde cero · Sin modelos externos",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg=bg
        )
        subtitle.pack(side=tk.LEFT, padx=(12, 0), pady=(6, 0))

        # Área de chat
        self.chat = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            bg=panel,
            fg=text_color,
            insertbackground=text_color,
            relief=tk.FLAT,
            padx=12,
            pady=12,
            state=tk.DISABLED
        )
        self.chat.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)

        # Tags de colores para mensajes
        self.chat.tag_configure("user", foreground="#7dd3fc", font=("Segoe UI", 11, "bold"))
        self.chat.tag_configure("bot", foreground="#86efac", font=("Segoe UI", 11, "bold"))
        self.chat.tag_configure("msg", foreground=text_color)
        self.chat.tag_configure("system", foreground="#94a3b8", font=("Segoe UI", 9, "italic"))

        # Frame de entrada
        input_frame = tk.Frame(self.root, bg=bg)
        input_frame.pack(fill=tk.X, padx=16, pady=(0, 16))

        self.entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            bg=panel,
            fg=text_color,
            insertbackground=text_color,
            relief=tk.FLAT,
            bd=8
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
        self.entry.bind("<Return>", self._on_send)
        self.entry.focus()

        send_btn = tk.Button(
            input_frame,
            text="Enviar",
            font=("Segoe UI", 11, "bold"),
            bg=accent,
            fg="#0f172a",
            activebackground="#7dd3fc",
            activeforeground="#0f172a",
            relief=tk.FLAT,
            padx=18,
            pady=6,
            cursor="hand2",
            command=self._on_send
        )
        send_btn.pack(side=tk.LEFT, padx=(10, 0))

        # Checkbox voz
        self.voz_var = tk.BooleanVar(value=True)
        voz_check = tk.Checkbutton(
            input_frame,
            text="Voz",
            variable=self.voz_var,
            font=("Segoe UI", 10),
            fg=text_color,
            bg=bg,
            selectcolor=panel,
            activebackground=bg,
            activeforeground=text_color
        )
        voz_check.pack(side=tk.LEFT, padx=(12, 0))

    def _mostrar_bienvenida(self):
        self._agregar_mensaje("system", "Asistente listo. Escribe algo para empezar.")

    def _agregar_mensaje(self, rol: str, texto: str):
        self.chat.configure(state=tk.NORMAL)
        if rol == "user":
            self.chat.insert(tk.END, "Tú: ", "user")
            self.chat.insert(tk.END, texto + "\n\n", "msg")
        elif rol == "bot":
            self.chat.insert(tk.END, "Asistente: ", "bot")
            self.chat.insert(tk.END, texto + "\n\n", "msg")
        else:
            self.chat.insert(tk.END, texto + "\n\n", "system")
        self.chat.configure(state=tk.DISABLED)
        self.chat.see(tk.END)

    def _on_send(self, event=None):
        texto = self.entry.get().strip()
        if not texto:
            return

        self.entry.delete(0, tk.END)
        self._agregar_mensaje("user", texto)

        # Procesar en hilo para no congelar la interfaz
        threading.Thread(target=self._procesar, args=(texto,), daemon=True).start()

    def _procesar(self, texto: str):
        self.memory.add("user", texto)
        respuesta = self.brain.think(texto, self.memory.get_context())
        self.memory.add("assistant", respuesta)

        # Actualizar UI en el hilo principal
        self.root.after(0, lambda: self._agregar_mensaje("bot", respuesta))

        if self.voz_var.get():
            self.voice.speak(respuesta)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AsistenteGUI()
    app.run()
