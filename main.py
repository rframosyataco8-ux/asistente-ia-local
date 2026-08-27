#!/usr/bin/env python3
"""
Asistente IA Local — 100% desde cero
Sin Ollama, sin modelos externos, sin APIs.
"""

import sys
from rich.console import Console
from rich.panel import Panel

from core.brain import Brain
from core.memory import Memory
from core.voice import Voice

console = Console()


def banner():
    console.print(Panel.fit(
        "[bold cyan]Asistente IA Local[/bold cyan]\n"
        "[dim]100% desde cero · Sin modelos externos · Sin APIs[/dim]",
        border_style="cyan"
    ))


def main():
    banner()
    console.print("\n[yellow]Iniciando...[/yellow]\n")

    memory = Memory()
    brain = Brain()
    voice = Voice()

    console.print("[green]✓ Cerebro propio listo[/green]")
    console.print("[green]✓ Memoria lista[/green]")
    console.print("[green]✓ Voz local lista[/green]")
    console.print("\n[bold]Escribe tu mensaje. Escribe 'salir' para terminar.[/bold]\n")

    while True:
        try:
            user_input = console.input("[bold blue]Tú > [/bold blue]").strip()

            if not user_input:
                continue

            if user_input.lower() in ("salir", "exit", "quit"):
                msg = "Hasta luego."
                console.print(f"[cyan]{msg}[/cyan]")
                voice.speak(msg)
                break

            memory.add("user", user_input)
            response = brain.think(user_input, memory.get_context())
            memory.add("assistant", response)

            console.print(f"[bold green]Asistente > [/bold green]{response}\n")
            voice.speak(response)

        except KeyboardInterrupt:
            console.print("\n[cyan]Adiós.[/cyan]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
