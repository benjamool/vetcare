from models.base import EntidadBase, propiedad_validada
from models.detalle_receta import DetalleReceta
from utils.validaciones import validar_entero, validar_texto, validar_fecha


class RecetaMedica(EntidadBase):
    CAMPOS = ("id_receta", "fecha_emision", "indicaciones", "id_consulta")

    id_receta = propiedad_validada("id_receta", validar_entero, minimo=1)
    fecha_emision = propiedad_validada("fecha_emision", validar_fecha, permitir_futuro=False)
    indicaciones = propiedad_validada("indicaciones", validar_texto, largo_max=300)
    id_consulta = propiedad_validada("id_consulta", validar_entero, minimo=1)

    def __init__(self, id_receta, fecha_emision, indicaciones, id_consulta):
        self.id_receta = id_receta
        self.fecha_emision = fecha_emision
        self.indicaciones = indicaciones
        self.id_consulta = id_consulta

    def agregar_medicamento(self, id_detalle_receta, id_medicamento, cantidad,
                            dosis, frecuencia, duracion_tratamiento) -> DetalleReceta:
        return DetalleReceta(id_detalle_receta, cantidad, dosis, frecuencia,
                             duracion_tratamiento, self.id_receta, id_medicamento)
