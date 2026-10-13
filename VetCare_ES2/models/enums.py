from enum import Enum


class EspecieAnimal(Enum):
    PERRO = "Perro"
    GATO = "Gato"
    AVE = "Ave"
    ROEDOR = "Roedor"
    REPTIL = "Reptil"
    OTRO = "Otro"


class EstadoConsulta(Enum):
    PROGRAMADA = "Programada"
    EN_CURSO = "En curso"
    COMPLETADA = "Completada"
    CANCELADA = "Cancelada"
