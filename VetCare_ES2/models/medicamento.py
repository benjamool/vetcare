from models.base import EntidadBase, propiedad_validada
from utils.validaciones import validar_entero, validar_texto, validar_decimal_positivo, validar_bool
from exceptions.errores_clinica import ReglaNegocioError


class Medicamento(EntidadBase):
    CAMPOS = ("id_medicamento", "nombre", "laboratorio", "stock",
              "precio_unitario", "via_administracion", "requiere_receta")

    id_medicamento = propiedad_validada("id_medicamento", validar_entero, minimo=1)
    nombre = propiedad_validada("nombre", validar_texto, largo_max=80)
    laboratorio = propiedad_validada("laboratorio", validar_texto, largo_max=80)
    stock = propiedad_validada("stock", validar_entero, minimo=0)
    precio_unitario = propiedad_validada("precio_unitario", validar_decimal_positivo)
    via_administracion = propiedad_validada("via_administracion", validar_texto, largo_max=40)
    requiere_receta = propiedad_validada("requiere_receta", validar_bool)

    def __init__(self, id_medicamento, nombre, laboratorio, stock,
                 precio_unitario, via_administracion, requiere_receta):
        self.id_medicamento = id_medicamento
        self.nombre = nombre
        self.laboratorio = laboratorio
        self.stock = stock
        self.precio_unitario = precio_unitario
        self.via_administracion = via_administracion
        self.requiere_receta = requiere_receta

    def descontar_stock(self, cantidad: int):
        validar_entero(cantidad, "cantidad", minimo=1)
        if cantidad > self.stock:
            raise ReglaNegocioError(
                f"Stock insuficiente de {self.nombre}: disponible {self.stock}, solicitado {cantidad}.")
        self.stock -= cantidad
