from datetime import date

from models.base import EntidadBase, propiedad_validada
from utils.validaciones import validar_entero, validar_decimal_positivo, validar_opcion, validar_fecha

METODOS_PAGO = ("Efectivo", "Débito", "Crédito", "Transferencia")


class Factura(EntidadBase):
    CAMPOS = ("id_factura", "monto_total", "metodo_pago", "fecha_emision", "id_consulta")

    id_factura = propiedad_validada("id_factura", validar_entero, minimo=1)
    monto_total = propiedad_validada("monto_total", validar_decimal_positivo)
    metodo_pago = propiedad_validada("metodo_pago", validar_opcion, METODOS_PAGO)
    fecha_emision = propiedad_validada("fecha_emision", validar_fecha, permitir_futuro=False)
    id_consulta = propiedad_validada("id_consulta", validar_entero, minimo=1)

    def __init__(self, id_factura, monto_total, metodo_pago, fecha_emision, id_consulta):
        self.id_factura = id_factura
        self.monto_total = monto_total
        self.metodo_pago = metodo_pago
        self.fecha_emision = fecha_emision
        self.id_consulta = id_consulta

    @classmethod
    def generar_factura(cls, id_factura, id_consulta, monto_total, metodo_pago) -> "Factura":
        return cls(id_factura, monto_total, metodo_pago, date.today(), id_consulta)
