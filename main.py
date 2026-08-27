#!/usr/bin/env python3
"""
Asistente Inteligente — Conversación natural + internet
"""

from rich.console import Console
from rich.panel import Panel

from core.brain import Brain
from core.memory import Memory
from core.voice import Voice

console = Console()


def main():
    console.print(Panel.fit(
        "[bold cyan]Asistente Inteligente[/bold cyan]\n"
        "[dim]Conversación natural · Internet · Voz[/dim]",
        border_style="cyan"
    ))

    brain = Brain(model="llama3.2")
    memory = Memory(max_messages=24)
    voice = Voice()

    if not brain.is_available():
        console.print("[red]Ollama no está disponible.[/red]")
        console.print("1. Instala: https://ollama.com")
        console.print("2. Ejecuta: ollama pull llama3.2")
        return

    console.print("[green]Listo.[/green] Habla con normalidad. Escribe 'salir' para terminar.\n")

    while True:
        try:
            user_input = console.input("[bold blue]Tú > [/bold blue]").strip()
            if not user_input:
                continue

            memory.add("user", user_input)
            console.print("[dim]Pensando...[/dim]")
            response = brain.think(user_input, memory.get_context())
            memory.add("assistant", response)

            console.print(f"[bold green]Asistente > [/bold green]{response}\n")
            voice.speak(response)

            if brain.should_exit:
                break

        except KeyboardInterrupt:
            console.print("\n[cyan]Adiós.[/cyan]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
