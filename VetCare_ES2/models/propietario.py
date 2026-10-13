from models.base import EntidadBase, propiedad_validada
from models.mascota import Mascota
from utils.validaciones import (validar_entero, validar_texto, validar_email,
                                validar_telefono)


class Propietario(EntidadBase):
    CAMPOS = ("id_propietario", "nombre", "telefono", "direccion", "email")

    id_propietario = propiedad_validada("id_propietario", validar_entero, minimo=1)
    nombre = propiedad_validada("nombre", validar_texto, largo_max=80)
    telefono = propiedad_validada("telefono", validar_telefono)
    direccion = propiedad_validada("direccion", validar_texto, largo_max=120)
    email = propiedad_validada("email", validar_email)

    def __init__(self, id_propietario, nombre, telefono, direccion, email):
        self.id_propietario = id_propietario
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.email = email

    def registrar_mascota(self, id_mascota, nombre, especie, raza,
                          fecha_nacimiento, sexo, esterilizado) -> Mascota:
        return Mascota(id_mascota, nombre, especie, raza, fecha_nacimiento,
                       sexo, esterilizado, self.id_propietario)

    def actualizar_datos(self, telefono, direccion, email) -> bool:
        self.telefono = telefono
        self.direccion = direccion
        self.email = email
        return True
