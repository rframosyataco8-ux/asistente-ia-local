"""
Cerebro del asistente — Solo por comandos
100% desde cero. Sin modelos. Sin APIs.

El usuario escribe comandos claros y el asistente los ejecuta.
"""

import os
import subprocess
import platform
from datetime import datetime
from typing import List, Dict, Tuple


class Brain:
    def __init__(self):
        self.name = "Asistente"
        self.system = platform.system()  # Windows / Linux / Darwin

        # Registro de comandos disponibles
        # formato: "comando": (descripción, función)
        self.commands = {
            "ayuda": ("Muestra la lista de comandos", self.cmd_ayuda),
            "hora": ("Muestra la hora actual", self.cmd_hora),
            "fecha": ("Muestra la fecha actual", self.cmd_fecha),
            "quien": ("Dice quién es el asistente", self.cmd_quien),
            "limpiar": ("Limpia la memoria de conversación", self.cmd_limpiar),
            "abrir": ("Abre un programa o carpeta. Uso: abrir calculadora | abrir notas | abrir documentos", self.cmd_abrir),
            "ip": ("Muestra la IP local", self.cmd_ip),
            "sistema": ("Muestra información del sistema", self.cmd_sistema),
            "eco": ("Repite el texto. Uso: eco hola mundo", self.cmd_eco),
            "salir": ("Cierra el asistente", self.cmd_salir),
        }

        self.should_exit = False

    def think(self, user_message: str, context: List[Dict] = None) -> str:
        """
        Interpreta el mensaje como un comando.
        Formato esperado: comando [argumentos]
        """
        if not user_message or not user_message.strip():
            return "Escribe un comando. Usa 'ayuda' para ver la lista."

        parts = user_message.strip().split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if cmd in self.commands:
            _, func = self.commands[cmd]
            return func(args)

        return f"Comando desconocido: '{cmd}'. Escribe 'ayuda' para ver los comandos disponibles."

    # ─── Comandos ───────────────────────────────────────────

    def cmd_ayuda(self, args: str = "") -> str:
        lineas = ["Comandos disponibles:\n"]
        for nombre, (desc, _) in sorted(self.commands.items()):
            lineas.append(f"  {nombre:<12} → {desc}")
        return "\n".join(lineas)

    def cmd_hora(self, args: str = "") -> str:
        return datetime.now().strftime("Hora actual: %H:%M:%S")

    def cmd_fecha(self, args: str = "") -> str:
        now = datetime.now()
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                 "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        return f"Hoy es {dias[now.weekday()]} {now.day} de {meses[now.month-1]} de {now.year}"

    def cmd_quien(self, args: str = "") -> str:
        return (
            "Soy un asistente local creado 100% desde cero. "
            "No uso ninguna IA externa. Solo respondo a comandos."
        )

    def cmd_limpiar(self, args: str = "") -> str:
        return "Memoria limpiada. (El historial se reinicia en la interfaz)"

    def cmd_abrir(self, args: str = "") -> str:
        if not args:
            return "Uso: abrir <programa o carpeta>\nEjemplos: abrir calculadora | abrir notas | abrir documentos"

        target = args.strip().lower()

        # Mapeo de nombres amigables → comandos reales
        mapping_win = {
            "calculadora": "calc",
            "notas": "notepad",
            "bloc": "notepad",
            "paint": "mspaint",
            "explorador": "explorer",
            "documentos": os.path.expanduser("~\\Documents"),
            "descargas": os.path.expanduser("~\\Downloads"),
            "escritorio": os.path.expanduser("~\\Desktop"),
            "cmd": "cmd",
            "powershell": "powershell",
            "navegador": "start https://www.google.com",
            "chrome": "start chrome",
            "edge": "start msedge",
        }

        mapping_linux = {
            "calculadora": "gnome-calculator",
            "notas": "gedit",
            "explorador": "xdg-open ~",
            "documentos": "xdg-open ~/Documents",
            "descargas": "xdg-open ~/Downloads",
            "escritorio": "xdg-open ~/Desktop",
            "navegador": "xdg-open https://www.google.com",
        }

        mapping_mac = {
            "calculadora": "open -a Calculator",
            "notas": "open -a TextEdit",
            "explorador": "open ~",
            "documentos": "open ~/Documents",
            "descargas": "open ~/Downloads",
            "escritorio": "open ~/Desktop",
            "navegador": "open https://www.google.com",
        }

        try:
            if self.system == "Windows":
                if target in mapping_win:
                    cmd = mapping_win[target]
                    if cmd.startswith("start "):
                        os.system(cmd)
                    else:
                        subprocess.Popen(cmd, shell=True)
                else:
                    # Intentar abrir lo que el usuario escribió directamente
                    os.startfile(args) if hasattr(os, "startfile") else os.system(f'start "" "{args}"')
                return f"Abriendo: {args}"

            elif self.system == "Linux":
                cmd = mapping_linux.get(target, f"xdg-open {args}")
                subprocess.Popen(cmd, shell=True)
                return f"Abriendo: {args}"

            elif self.system == "Darwin":
                cmd = mapping_mac.get(target, f"open {args}")
                subprocess.Popen(cmd, shell=True)
                return f"Abriendo: {args}"

            return "Sistema operativo no reconocido."
        except Exception as e:
            return f"No se pudo abrir '{args}': {e}"

    def cmd_ip(self, args: str = "") -> str:
        try:
            import socket
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return f"IP local: {ip}"
        except Exception as e:
            return f"No se pudo obtener la IP: {e}"

    def cmd_sistema(self, args: str = "") -> str:
        return (
            f"Sistema: {platform.system()} {platform.release()}\n"
            f"Máquina: {platform.machine()}\n"
            f"Procesador: {platform.processor() or 'N/A'}\n"
            f"Python: {platform.python_version()}"
        )

    def cmd_eco(self, args: str = "") -> str:
        if not args:
            return "Uso: eco <texto>"
        return args

    def cmd_salir(self, args: str = "") -> str:
        self.should_exit = True
        return "Cerrando asistente..."

    def is_available(self) -> bool:
        return True

    def list_commands(self) -> List[str]:
        return list(self.commands.keys())
