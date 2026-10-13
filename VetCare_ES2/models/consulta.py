from datetime import date

from models.base import EntidadBase, propiedad_validada
from models.enums import EstadoConsulta
from models.detalle_consulta import DetalleConsulta
from models.receta_medica import RecetaMedica
from utils.validaciones import validar_entero, validar_texto, validar_fecha, validar_enum
from exceptions.errores_clinica import ReglaNegocioError


class Consulta(EntidadBase):
    CAMPOS = ("id_consulta", "fecha", "motivo", "estado", "id_veterinario", "id_mascota")

    id_consulta = propiedad_validada("id_consulta", validar_entero, minimo=1)
    fecha = propiedad_validada("fecha", validar_fecha)
    motivo = propiedad_validada("motivo", validar_texto, largo_max=200)
    estado = propiedad_validada("estado", validar_enum, EstadoConsulta)
    id_veterinario = propiedad_validada("id_veterinario", validar_entero, minimo=1)
    id_mascota = propiedad_validada("id_mascota", validar_entero, minimo=1)

    def __init__(self, id_consulta, fecha, motivo, estado, id_veterinario, id_mascota):
        self.id_consulta = id_consulta
        self.fecha = fecha
        self.motivo = motivo
        self.estado = estado
        self.id_veterinario = id_veterinario
        self.id_mascota = id_mascota

    def registrar_detalle(self, id_detalle, diagnostico, tratamiento, observaciones) -> DetalleConsulta:
        return DetalleConsulta(id_detalle, diagnostico, tratamiento, observaciones, self.id_consulta)

    def emitir_receta(self, id_receta, indicaciones) -> RecetaMedica:
        if self.estado == EstadoConsulta.CANCELADA:
            raise ReglaNegocioError("No se puede emitir una receta en una consulta cancelada.")
        return RecetaMedica(id_receta, date.today(), indicaciones, self.id_consulta)
