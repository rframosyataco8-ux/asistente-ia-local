#!/usr/bin/env python3
"""
Asistente Inteligente — Consola con streaming
"""

from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.text import Text

from core.brain import Brain
from core.memory import Memory
from core.voice import Voice

console = Console()


def main():
    console.print(Panel.fit(
        "[bold cyan]Asistente Inteligente[/bold cyan]\n"
        "[dim]Conversación · Internet · Memoria · Voz[/dim]",
        border_style="cyan"
    ))

    brain = Brain(model="llama3.2")
    memory = Memory(max_messages=30)
    voice = Voice()

    if not brain.is_available():
        console.print("[red]Ollama no disponible.[/red]")
        console.print("1. Instala: https://ollama.com")
        console.print("2. Ejecuta: ollama pull llama3.2")
        return

    console.print("[green]Listo.[/green] Habla con naturalidad. Escribe 'salir' para terminar.\n")

    while True:
        try:
            user_input = console.input("[bold blue]Tú > [/bold blue]").strip()
            if not user_input:
                continue

            memory.add("user", user_input)

            full = []
            console.print("[bold green]Asistente > [/bold green]", end="")

            for chunk in brain.think_stream(user_input, memory.get_context(), memory=memory):
                full.append(chunk)
                console.print(chunk, end="")

            console.print("\n")
            respuesta = "".join(full).strip()
            memory.add("assistant", respuesta)
            voice.speak(respuesta)

            if brain.should_exit:
                break

        except KeyboardInterrupt:
            console.print("\n[cyan]Adiós.[/cyan]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
