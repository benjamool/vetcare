from models.base import EntidadBase, propiedad_validada
from utils.validaciones import validar_entero, validar_texto, validar_fecha


class Vacuna(EntidadBase):
    CAMPOS = ("id_vacuna", "tipo_vacuna", "fecha_aplicacion", "proxima_dosis",
              "id_mascota", "id_veterinario")

    id_vacuna = propiedad_validada("id_vacuna", validar_entero, minimo=1)
    tipo_vacuna = propiedad_validada("tipo_vacuna", validar_texto, largo_max=80)
    fecha_aplicacion = propiedad_validada("fecha_aplicacion", validar_fecha, permitir_futuro=False)
    proxima_dosis = propiedad_validada("proxima_dosis", validar_fecha)
    id_mascota = propiedad_validada("id_mascota", validar_entero, minimo=1)
    id_veterinario = propiedad_validada("id_veterinario", validar_entero, minimo=1)

    def __init__(self, id_vacuna, tipo_vacuna, fecha_aplicacion, proxima_dosis, id_mascota, id_veterinario):
        self.id_vacuna = id_vacuna
        self.tipo_vacuna = tipo_vacuna
        self.fecha_aplicacion = fecha_aplicacion
        self.proxima_dosis = proxima_dosis
        self.id_mascota = id_mascota
        self.id_veterinario = id_veterinario
        if self.proxima_dosis < self.fecha_aplicacion:
            raise ValueError("'proxima_dosis' no puede ser anterior a 'fecha_aplicacion'.")
