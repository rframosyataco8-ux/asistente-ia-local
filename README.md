# Asistente por Comandos — 100% Desde Cero

**Sin modelos de IA. Sin APIs. Solo comandos.**

Escribes un comando → el asistente lo ejecuta.

---

## Ejecutar

```bash
git clone https://github.com/rframosyataco8-ux/asistente-ia-local.git
cd asistente-ia-local

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python gui.py      # Interfaz gráfica
# o
python main.py     # Consola
```

---

## Comandos disponibles

| Comando        | Qué hace                                      |
|----------------|-----------------------------------------------|
| `ayuda`        | Lista todos los comandos                      |
| `hora`         | Muestra la hora                               |
| `fecha`        | Muestra la fecha                              |
| `quien`        | Dice quién es el asistente                    |
| `sistema`      | Info del sistema operativo                    |
| `ip`           | Muestra la IP local                           |
| `abrir <algo>` | Abre programas o carpetas                     |
| `eco <texto>`  | Repite el texto                               |
| `limpiar`      | Limpia la memoria                             |
| `salir`        | Cierra el asistente                           |

### Ejemplos de `abrir`

```
abrir calculadora
abrir notas
abrir documentos
abrir descargas
abrir explorador
abrir chrome
```

---

## Cómo agregar más comandos

Edita `core/brain.py` y agrega una nueva función + regístrala en `self.commands`.

---

**Autor**: Fabricio Ramos  
**Creado**: Agosto 2026
