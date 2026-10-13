from models.base import EntidadBase, propiedad_validada
from utils.validaciones import validar_entero, validar_texto


class DetalleReceta(EntidadBase):
    CAMPOS = ("id_detalle_receta", "cantidad", "dosis", "frecuencia",
              "duracion_tratamiento", "id_receta", "id_medicamento")

    id_detalle_receta = propiedad_validada("id_detalle_receta", validar_entero, minimo=1)
    cantidad = propiedad_validada("cantidad", validar_entero, minimo=1)
    dosis = propiedad_validada("dosis", validar_texto, largo_max=60)
    frecuencia = propiedad_validada("frecuencia", validar_texto, largo_max=60)
    duracion_tratamiento = propiedad_validada("duracion_tratamiento", validar_texto, largo_max=60)
    id_receta = propiedad_validada("id_receta", validar_entero, minimo=1)
    id_medicamento = propiedad_validada("id_medicamento", validar_entero, minimo=1)

    def __init__(self, id_detalle_receta, cantidad, dosis, frecuencia,
                 duracion_tratamiento, id_receta, id_medicamento):
        self.id_detalle_receta = id_detalle_receta
        self.cantidad = cantidad
        self.dosis = dosis
        self.frecuencia = frecuencia
        self.duracion_tratamiento = duracion_tratamiento
        self.id_receta = id_receta
        self.id_medicamento = id_medicamento
