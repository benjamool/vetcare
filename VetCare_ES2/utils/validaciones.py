"""Funciones de validación reutilizadas por todos los modelos.
Todas reciben (valor, nombre_del_campo, ...) y devuelven el valor limpio o lanzan
TypeError (tipo incorrecto) / ValueError (valor fuera de regla)."""
import re
from datetime import date, datetime
from enum import Enum


def validar_entero(valor, nombre, minimo=None):
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise TypeError(f"'{nombre}' debe ser un entero. Se recibió: {type(valor).__name__}")
    if minimo is not None and valor < minimo:
        raise ValueError(f"'{nombre}' debe ser >= {minimo}. Valor recibido: {valor}")
    return valor


def validar_decimal_positivo(valor, nombre):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise TypeError(f"'{nombre}' debe ser numérico. Se recibió: {type(valor).__name__}")
    if valor <= 0:
        raise ValueError(f"'{nombre}' debe ser mayor a 0. Valor recibido: {valor}")
    return float(valor)


def validar_texto(valor, nombre, largo_max=100, obligatorio=True):
    if not isinstance(valor, str):
        raise TypeError(f"'{nombre}' debe ser texto. Se recibió: {type(valor).__name__}")
    limpio = valor.strip()
    if obligatorio and not limpio:
        raise ValueError(f"'{nombre}' no puede estar vacío.")
    if len(limpio) > largo_max:
        raise ValueError(f"'{nombre}' no puede superar {largo_max} caracteres.")
    return limpio


def validar_opcion(valor, nombre, opciones):
    texto = validar_texto(valor, nombre, 30)
    for opcion in opciones:
        if opcion.lower() == texto.lower():
            return opcion
    raise ValueError(f"'{nombre}' debe ser uno de: {', '.join(opciones)}. Recibido: '{texto}'")


def validar_bool(valor, nombre):
    if isinstance(valor, bool):
        return valor
    if valor in (0, 1):  # SQLite guarda los booleanos como 0/1
        return bool(valor)
    raise TypeError(f"'{nombre}' debe ser verdadero/falso.")


def validar_fecha(valor, nombre, permitir_futuro=True):
    if isinstance(valor, datetime):
        valor = valor.date()
    elif isinstance(valor, str):
        try:
            valor = date.fromisoformat(valor.strip())
        except ValueError:
            raise ValueError(f"'{nombre}' debe tener formato AAAA-MM-DD. Recibido: '{valor}'")
    elif not isinstance(valor, date):
        raise TypeError(f"'{nombre}' debe ser una fecha.")
    if not permitir_futuro and valor > date.today():
        raise ValueError(f"'{nombre}' no puede ser una fecha futura.")
    return valor


def validar_enum(valor, nombre, enum_cls):
    if isinstance(valor, enum_cls):
        return valor
    if isinstance(valor, str):
        try:
            return enum_cls[valor.strip().upper()]
        except KeyError:
            validos = ", ".join(e.name for e in enum_cls)
            raise ValueError(f"'{nombre}' debe ser uno de: {validos}. Recibido: '{valor}'")
    raise TypeError(f"'{nombre}' debe ser un {enum_cls.__name__}.")


def validar_email(valor, nombre="email"):
    texto = validar_texto(valor, nombre, 100)
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", texto):
        raise ValueError(f"'{nombre}' no tiene un formato válido: '{texto}'")
    return texto


def validar_telefono(valor, nombre="telefono"):
    texto = validar_texto(valor, nombre, 20)
    if not re.fullmatch(r"\+?\d[\d ]{7,14}", texto):
        raise ValueError(f"'{nombre}' debe tener entre 8 y 15 dígitos (puede iniciar con +). Recibido: '{texto}'")
    return texto
