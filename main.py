#!/usr/bin/env python3
"""
Asistente por Comandos — Consola
100% desde cero. Sin modelos. Sin APIs.
"""

from rich.console import Console
from rich.panel import Panel

from core.brain import Brain
from core.memory import Memory
from core.voice import Voice

console = Console()


def main():
    console.print(Panel.fit(
        "[bold cyan]Asistente por Comandos[/bold cyan]\n"
        "[dim]100% desde cero · Solo comandos[/dim]",
        border_style="cyan"
    ))

    brain = Brain()
    memory = Memory()
    voice = Voice()

    console.print("[green]Listo.[/green] Escribe [bold]ayuda[/bold] para ver los comandos.\n")

    while True:
        try:
            user_input = console.input("[bold blue]> [/bold blue]").strip()

            if not user_input:
                continue

            memory.add("user", user_input)
            response = brain.think(user_input, memory.get_context())
            memory.add("assistant", response)

            console.print(f"[green]{response}[/green]\n")

            # Hablar solo la primera línea
            voice.speak(response.split("\n")[0])

            if brain.should_exit:
                break

        except KeyboardInterrupt:
            console.print("\n[cyan]Adiós.[/cyan]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
