from models.enums import EstadoConsulta
from models.detalle_receta import DetalleReceta
from models.factura import Factura
from services.crud_service import CrudService
from utils.validaciones import validar_enum
from exceptions.errores_clinica import ReglaNegocioError, RegistroDuplicadoError

# Estados a los que se puede pasar desde cada estado
TRANSICIONES = {
    EstadoConsulta.PROGRAMADA: {EstadoConsulta.EN_CURSO, EstadoConsulta.CANCELADA},
    EstadoConsulta.EN_CURSO: {EstadoConsulta.COMPLETADA, EstadoConsulta.CANCELADA},
    EstadoConsulta.COMPLETADA: set(),
    EstadoConsulta.CANCELADA: set(),
}


class ClinicaService:
    """Reglas de negocio que involucran varias entidades. El CRUD simple está en self.crud[...]."""

    def __init__(self, daos: dict):
        self._daos = daos
        self.crud = {clave: CrudService(dao) for clave, dao in daos.items() if clave != "contraindicacion"}

    def historial_consultas(self, id_mascota: int) -> list:
        self._daos["mascota"].obtener_por_id_estricto(id_mascota)  # falla si la mascota no existe
        return self._daos["consulta"].listar_por_mascota(id_mascota)

    def cambiar_estado_consulta(self, id_consulta: int, nuevo_estado):
        consulta = self._daos["consulta"].obtener_por_id_estricto(id_consulta)
        nuevo = validar_enum(nuevo_estado, "estado", EstadoConsulta)
        if nuevo not in TRANSICIONES[consulta.estado]:
            raise ReglaNegocioError(
                f"No se puede pasar de {consulta.estado.name} a {nuevo.name}.")
        consulta.estado = nuevo
        self._daos["consulta"].actualizar(consulta)
        return consulta

    def agregar_medicamento_a_receta(self, id_detalle_receta, id_receta, id_medicamento,
                                     cantidad, dosis, frecuencia, duracion) -> DetalleReceta:
        receta = self._daos["receta"].obtener_por_id_estricto(id_receta)
        consulta = self._daos["consulta"].obtener_por_id_estricto(receta.id_consulta)
        if consulta.estado == EstadoConsulta.CANCELADA:
            raise ReglaNegocioError("La consulta de esta receta está cancelada.")
        medicamento = self._daos["medicamento"].obtener_por_id_estricto(id_medicamento)
        if self._daos["contraindicacion"].hay_contraindicacion(consulta.id_mascota, id_medicamento):
            raise ReglaNegocioError(
                f"{medicamento.nombre} está contraindicado por una alergia registrada de la mascota.")

        detalle = DetalleReceta(id_detalle_receta, cantidad, dosis, frecuencia,
                                duracion, id_receta, id_medicamento)  # valida los datos
        medicamento.descontar_stock(cantidad)                         # valida el stock
        self._daos["detalle_receta"].insertar(detalle)
        self._daos["medicamento"].actualizar(medicamento)
        return detalle

    def facturar_consulta(self, id_factura, id_consulta, monto_total, metodo_pago) -> Factura:
        consulta = self._daos["consulta"].obtener_por_id_estricto(id_consulta)
        if consulta.estado != EstadoConsulta.COMPLETADA:
            raise ReglaNegocioError("Solo se pueden facturar consultas COMPLETADAS.")
        factura = Factura.generar_factura(id_factura, id_consulta, monto_total, metodo_pago)
        try:
            self._daos["factura"].insertar(factura)
        except RegistroDuplicadoError as error:
            raise ReglaNegocioError("Esa consulta ya tiene factura o el ID de factura ya existe.") from error
        return factura

    def buscar_medicamentos(self, termino: str) -> list:
        return self._daos["medicamento"].buscar_por_termino_seguro(termino)

    def registrar_contraindicacion(self, id_alergia: int, id_medicamento: int) -> None:
        self._daos["alergia"].obtener_por_id_estricto(id_alergia)
        self._daos["medicamento"].obtener_por_id_estricto(id_medicamento)
        self._daos["contraindicacion"].agregar(id_alergia, id_medicamento)
