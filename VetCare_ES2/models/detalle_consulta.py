from models.base import EntidadBase, propiedad_validada
from utils.validaciones import validar_entero, validar_texto


class DetalleConsulta(EntidadBase):
    CAMPOS = ("id_detalle", "diagnostico", "tratamiento", "observaciones", "id_consulta")

    id_detalle = propiedad_validada("id_detalle", validar_entero, minimo=1)
    diagnostico = propiedad_validada("diagnostico", validar_texto, largo_max=300)
    tratamiento = propiedad_validada("tratamiento", validar_texto, largo_max=300)
    observaciones = propiedad_validada("observaciones", validar_texto, largo_max=300, obligatorio=False)
    id_consulta = propiedad_validada("id_consulta", validar_entero, minimo=1)

    def __init__(self, id_detalle, diagnostico, tratamiento, observaciones, id_consulta):
        self.id_detalle = id_detalle
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.observaciones = observaciones
        self.id_consulta = id_consulta
