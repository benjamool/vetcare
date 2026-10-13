from models.base import EntidadBase, propiedad_validada
from models.enums import EspecieAnimal
from models.alergia import Alergia
from utils.validaciones import (validar_entero, validar_texto, validar_enum,
                                validar_fecha, validar_opcion, validar_bool)


class Mascota(EntidadBase):
    CAMPOS = ("id_mascota", "nombre", "especie", "raza", "fecha_nacimiento",
              "sexo", "esterilizado", "id_propietario")

    id_mascota = propiedad_validada("id_mascota", validar_entero, minimo=1)
    nombre = propiedad_validada("nombre", validar_texto, largo_max=60)
    especie = propiedad_validada("especie", validar_enum, EspecieAnimal)
    raza = propiedad_validada("raza", validar_texto, largo_max=60)
    fecha_nacimiento = propiedad_validada("fecha_nacimiento", validar_fecha, permitir_futuro=False)
    sexo = propiedad_validada("sexo", validar_opcion, ("Macho", "Hembra"))
    esterilizado = propiedad_validada("esterilizado", validar_bool)
    id_propietario = propiedad_validada("id_propietario", validar_entero, minimo=1)

    def __init__(self, id_mascota, nombre, especie, raza, fecha_nacimiento,
                 sexo, esterilizado, id_propietario):
        self.id_mascota = id_mascota
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.fecha_nacimiento = fecha_nacimiento
        self.sexo = sexo
        self.esterilizado = esterilizado
        self.id_propietario = id_propietario

    def registrar_alergia(self, id_alergia, nombre, nivel_gravedad) -> Alergia:
        return Alergia(id_alergia, nombre, nivel_gravedad, self.id_mascota)
    # obtenerHistorialConsultas() del UML necesita la BD: vive en ClinicaService.historial_consultas()
