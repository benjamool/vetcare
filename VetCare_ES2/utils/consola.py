"""Utilidades de entrada/salida por consola (solo las usa la capa de pantallas)."""
import os
from datetime import date
from enum import Enum

from exceptions.errores_clinica import VetCareException


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausar(mensaje="\nPresione [ENTER] para continuar..."):
    input(mensaje)


def _a_bool(crudo: str) -> bool:
    if crudo.lower() in ("s", "si", "sí", "1", "true"):
        return True
    if crudo.lower() in ("n", "no", "0", "false"):
        return False
    raise ValueError("Responda s/n.")


def _convertir(crudo: str, tipo):
    """Convierte el texto ingresado al tipo pedido. Lanza ValueError si no se puede."""
    if isinstance(tipo, type) and issubclass(tipo, Enum):
        nombres = [e.name for e in tipo]
        if crudo.upper() in nombres:
            return tipo[crudo.upper()]
        if crudo.isdigit() and 1 <= int(crudo) <= len(nombres):
            return list(tipo)[int(crudo) - 1]
        raise ValueError(f"Opción inválida. Elija: {', '.join(nombres)}")
    if tipo == "int":
        return int(crudo)
    if tipo == "float":
        return float(crudo.replace(",", "."))
    if tipo == "bool":
        return _a_bool(crudo)
    if tipo == "fecha":
        return date.fromisoformat(crudo)
    return crudo  # texto: las reglas las valida el modelo


def pedir_valor(etiqueta: str, tipo, actual=None):
    """Pide un dato hasta que tenga el formato correcto.
    Si 'actual' viene informado, ENTER conserva el valor actual (se usa al actualizar)."""
    ayudas = {"int": "número entero", "float": "número", "bool": "s/n", "fecha": "AAAA-MM-DD"}
    if isinstance(tipo, type) and issubclass(tipo, Enum):
        ayuda = "/".join(e.name for e in tipo)
    else:
        ayuda = ayudas.get(tipo, "")
    ayuda = f" ({ayuda})" if ayuda else ""
    sufijo = f" [actual: {formatear(actual)}]" if actual is not None else ""
    while True:
        crudo = input(f"{etiqueta}{ayuda}{sufijo}: ").strip()
        if crudo == "" and actual is not None:
            return actual
        try:
            return _convertir(crudo, tipo)
        except ValueError as error:
            print(f"  [!] Entrada inválida. {error}")


def formatear(valor) -> str:
    if isinstance(valor, Enum):
        return valor.name
    if isinstance(valor, bool):
        return "Sí" if valor else "No"
    return str(valor)


def ejecutar_seguro(accion, *args):
    """Ejecuta una acción de pantalla y muestra los errores sin cerrar el programa."""
    try:
        accion(*args)
    except (ValueError, TypeError) as error:
        print(f"\n[!] Dato inválido: {error}")
    except VetCareException as error:
        print(f"\n[!] {error}")
    except Exception as error:  # último recurso: el sistema nunca se cae
        print(f"\n[X] Error inesperado: {error}")
    pausar()
