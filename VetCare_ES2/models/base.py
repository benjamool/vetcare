from datetime import date
from enum import Enum


def propiedad_validada(nombre, validar, *args, **kwargs):
    """Crea una property con encapsulamiento: el valor se guarda en un atributo
    protegido (_nombre) y SIEMPRE pasa por 'validar' al asignarse (incluso en __init__)."""
    privado = f"_{nombre}"

    def getter(self):
        return getattr(self, privado)

    def setter(self, valor):
        setattr(self, privado, validar(valor, nombre, *args, **kwargs))

    return property(getter, setter)


def _a_sql(valor):
    """Convierte un valor de dominio en algo que SQLite pueda guardar."""
    if isinstance(valor, Enum):
        return valor.name
    if isinstance(valor, bool):
        return int(valor)
    if isinstance(valor, date):
        return valor.isoformat()
    return valor


class EntidadBase:
    """Clase padre de todos los modelos. CAMPOS define el orden de los atributos,
    que coincide con el orden de los parámetros del constructor y de las columnas SQL."""
    CAMPOS: tuple = ()

    def a_diccionario(self) -> dict:
        return {campo: getattr(self, campo) for campo in self.CAMPOS}

    def a_fila(self) -> tuple:
        return tuple(_a_sql(getattr(self, campo)) for campo in self.CAMPOS)

    def __repr__(self):
        datos = ", ".join(f"{k}={v!r}" for k, v in self.a_diccionario().items())
        return f"{type(self).__name__}({datos})"
