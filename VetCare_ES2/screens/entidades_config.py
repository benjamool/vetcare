"""Describe qué datos se piden por pantalla para cada entidad.
Cada campo: (nombre del parámetro del constructor, etiqueta, tipo).
El primer campo siempre es el ID (clave primaria)."""
from models.enums import EspecieAnimal, EstadoConsulta
from models.propietario import Propietario
from models.mascota import Mascota
from models.veterinario import Veterinario
from models.medicamento import Medicamento
from models.consulta import Consulta
from models.detalle_consulta import DetalleConsulta
from models.receta_medica import RecetaMedica
from models.detalle_receta import DetalleReceta
from models.vacuna import Vacuna
from models.alergia import Alergia
from models.factura import Factura

# (clave del servicio, título del menú, clase del modelo, campos)
ENTIDADES = [
    ("propietario", "Propietarios", Propietario, [
        ("id_propietario", "ID propietario", "int"), ("nombre", "Nombre", "texto"),
        ("telefono", "Teléfono", "texto"), ("direccion", "Dirección", "texto"),
        ("email", "Email", "texto")]),
    ("mascota", "Mascotas", Mascota, [
        ("id_mascota", "ID mascota", "int"), ("nombre", "Nombre", "texto"),
        ("especie", "Especie", EspecieAnimal), ("raza", "Raza", "texto"),
        ("fecha_nacimiento", "Fecha de nacimiento", "fecha"),
        ("sexo", "Sexo (Macho/Hembra)", "texto"), ("esterilizado", "¿Esterilizado?", "bool"),
        ("id_propietario", "ID del propietario", "int")]),
    ("veterinario", "Veterinarios", Veterinario, [
        ("id_veterinario", "ID veterinario", "int"), ("nombre", "Nombre", "texto"),
        ("especialidad", "Especialidad", "texto"), ("numero_licencia", "N° de licencia", "texto")]),
    ("medicamento", "Medicamentos", Medicamento, [
        ("id_medicamento", "ID medicamento", "int"), ("nombre", "Nombre", "texto"),
        ("laboratorio", "Laboratorio", "texto"), ("stock", "Stock", "int"),
        ("precio_unitario", "Precio unitario", "float"),
        ("via_administracion", "Vía de administración", "texto"),
        ("requiere_receta", "¿Requiere receta?", "bool")]),
    ("consulta", "Consultas", Consulta, [
        ("id_consulta", "ID consulta", "int"), ("fecha", "Fecha", "fecha"),
        ("motivo", "Motivo", "texto"), ("estado", "Estado", EstadoConsulta),
        ("id_veterinario", "ID del veterinario", "int"), ("id_mascota", "ID de la mascota", "int")]),
    ("detalle_consulta", "Detalles de consulta", DetalleConsulta, [
        ("id_detalle", "ID detalle", "int"), ("diagnostico", "Diagnóstico", "texto"),
        ("tratamiento", "Tratamiento", "texto"), ("observaciones", "Observaciones (opcional)", "texto"),
        ("id_consulta", "ID de la consulta", "int")]),
    ("receta", "Recetas médicas", RecetaMedica, [
        ("id_receta", "ID receta", "int"), ("fecha_emision", "Fecha de emisión", "fecha"),
        ("indicaciones", "Indicaciones", "texto"), ("id_consulta", "ID de la consulta", "int")]),
    ("detalle_receta", "Detalles de receta (sin descontar stock)", DetalleReceta, [
        ("id_detalle_receta", "ID detalle", "int"), ("cantidad", "Cantidad", "int"),
        ("dosis", "Dosis", "texto"), ("frecuencia", "Frecuencia", "texto"),
        ("duracion_tratamiento", "Duración", "texto"), ("id_receta", "ID de la receta", "int"),
        ("id_medicamento", "ID del medicamento", "int")]),
    ("vacuna", "Vacunas", Vacuna, [
        ("id_vacuna", "ID vacuna", "int"), ("tipo_vacuna", "Tipo de vacuna", "texto"),
        ("fecha_aplicacion", "Fecha de aplicación", "fecha"), ("proxima_dosis", "Próxima dosis", "fecha"),
        ("id_mascota", "ID de la mascota", "int"), ("id_veterinario", "ID del veterinario", "int")]),
    ("alergia", "Alergias", Alergia, [
        ("id_alergia", "ID alergia", "int"), ("nombre", "Nombre", "texto"),
        ("nivel_gravedad", "Gravedad (Leve/Moderada/Grave)", "texto"),
        ("id_mascota", "ID de la mascota", "int")]),
    ("factura", "Facturas (CRUD directo)", Factura, [
        ("id_factura", "ID factura", "int"), ("monto_total", "Monto total", "float"),
        ("metodo_pago", "Método de pago (Efectivo/Débito/Crédito/Transferencia)", "texto"),
        ("fecha_emision", "Fecha de emisión", "fecha"), ("id_consulta", "ID de la consulta", "int")]),
]
