from datetime import date

from models.base import EntidadBase, propiedad_validada
from models.enums import EstadoConsulta
from models.consulta import Consulta
from models.vacuna import Vacuna
from utils.validaciones import validar_entero, validar_texto


class Veterinario(EntidadBase):
    CAMPOS = ("id_veterinario", "nombre", "especialidad", "numero_licencia")

    id_veterinario = propiedad_validada("id_veterinario", validar_entero, minimo=1)
    nombre = propiedad_validada("nombre", validar_texto, largo_max=80)
    especialidad = propiedad_validada("especialidad", validar_texto, largo_max=60)
    numero_licencia = propiedad_validada("numero_licencia", validar_texto, largo_max=30)

    def __init__(self, id_veterinario, nombre, especialidad, numero_licencia):
        self.id_veterinario = id_veterinario
        self.nombre = nombre
        self.especialidad = especialidad
        self.numero_licencia = numero_licencia

    def atender_consulta(self, id_consulta, id_mascota, motivo) -> Consulta:
        return Consulta(id_consulta, date.today(), motivo, EstadoConsulta.EN_CURSO,
                        self.id_veterinario, id_mascota)

    def aplicar_vacuna(self, id_vacuna, id_mascota, tipo_vacuna, proxima_dosis) -> Vacuna:
        return Vacuna(id_vacuna, tipo_vacuna, date.today(), proxima_dosis,
                      id_mascota, self.id_veterinario)
