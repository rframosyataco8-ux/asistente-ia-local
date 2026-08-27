#!/usr/bin/env python3
"""
Asistente IA Local - 100% offline
Punto de entrada principal
"""

import sys
import time
from rich.console import Console
from rich.panel import Panel

from core.brain import Brain
from core.memory import Memory
from core.voice import Voice

console = Console()


def banner():
    console.print(Panel.fit(
        "[bold cyan]Asistente IA Local[/bold cyan]\n"
        "[dim]100% offline · Sin APIs · Todo en tu PC[/dim]",
        border_style="cyan"
    ))


def main():
    banner()
    console.print("\n[yellow]Iniciando componentes...[/yellow]\n")

    # Inicializar módulos
    memory = Memory()
    brain = Brain(model="llama3.2")  # Cambia el modelo si quieres
    voice = Voice()

    # Verificar que Ollama esté corriendo
    if not brain.is_available():
        console.print("[red]ERROR: Ollama no está corriendo o no tiene el modelo.[/red]")
        console.print("1. Instala Ollama desde https://ollama.com")
        console.print("2. Ejecuta: ollama pull llama3.2")
        console.print("3. Asegúrate de que Ollama esté activo")
        sys.exit(1)

    console.print("[green]✓ Cerebro listo (Ollama)[/green]")
    console.print("[green]✓ Memoria lista[/green]")
    console.print("[green]✓ Voz lista[/green]")
    console.print("\n[bold]Escribe o habla. Escribe 'salir' para terminar.[/bold]\n")

    # Bucle principal de conversación
    while True:
        try:
            # Por ahora usamos texto (la voz se integra después)
            user_input = console.input("[bold blue]Tú > [/bold blue]").strip()

            if not user_input:
                continue

            if user_input.lower() in ("salir", "exit", "quit", "adiós", "adios"):
                voice.speak("Hasta luego. Fue un placer ayudarte.")
                console.print("[cyan]Adiós.[/cyan]")
                break

            # Guardar en memoria
            memory.add("user", user_input)

            # Pensar
            console.print("[dim]Pensando...[/dim]")
            response = brain.think(user_input, memory.get_context())

            # Guardar respuesta
            memory.add("assistant", response)

            # Mostrar y hablar
            console.print(f"[bold green]Asistente > [/bold green]{response}\n")
            voice.speak(response)

        except KeyboardInterrupt:
            console.print("\n[cyan]Interrumpido. Adiós.[/cyan]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
