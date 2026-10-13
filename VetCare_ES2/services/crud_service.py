class CrudService:
    """CRUD genérico de una entidad: delega en su DAO. Los errores del DAO
    (EntidadNoEncontradaError, RegistroDuplicadoError, ...) suben tal cual a la pantalla."""

    def __init__(self, dao):
        self._dao = dao

    def registrar(self, entidad):
        self._dao.insertar(entidad)
        return entidad

    def obtener(self, identificador: int):
        return self._dao.obtener_por_id_estricto(identificador)

    def listar(self) -> list:
        return self._dao.listar_todos()

    def actualizar(self, entidad):
        self._dao.actualizar(entidad)
        return entidad

    def eliminar(self, identificador: int) -> None:
        self._dao.eliminar(identificador)
