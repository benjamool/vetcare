from models.base import EntidadBase, propiedad_validada
from utils.validaciones import validar_entero, validar_texto, validar_opcion

NIVELES_GRAVEDAD = ("Leve", "Moderada", "Grave")


class Alergia(EntidadBase):
    CAMPOS = ("id_alergia", "nombre", "nivel_gravedad", "id_mascota")

    id_alergia = propiedad_validada("id_alergia", validar_entero, minimo=1)
    nombre = propiedad_validada("nombre", validar_texto, largo_max=80)
    nivel_gravedad = propiedad_validada("nivel_gravedad", validar_opcion, NIVELES_GRAVEDAD)
    id_mascota = propiedad_validada("id_mascota", validar_entero, minimo=1)

    def __init__(self, id_alergia, nombre, nivel_gravedad, id_mascota):
        self.id_alergia = id_alergia
        self.nombre = nombre
        self.nivel_gravedad = nivel_gravedad
        self.id_mascota = id_mascota
