class VetCareException(Exception):
    """Excepción raíz de todos los errores previstos del sistema."""


class EntidadNoEncontradaError(VetCareException):
    def __init__(self, entidad: str, identificador):
        self.entidad = entidad
        self.identificador = identificador
        super().__init__(f"No existe ningún registro de tipo '{entidad}' con ID #{identificador}.")


class ReglaNegocioError(VetCareException):
    """Se viola una regla de negocio (stock insuficiente, estado inválido, etc.)."""


class PersistenciaError(VetCareException):
    """Fallo originado en la base de datos."""


class RegistroDuplicadoError(PersistenciaError):
    """Clave primaria o campo UNIQUE repetido."""


class ReferenciaIntegridadError(PersistenciaError):
    """Se viola una clave foránea (padre inexistente o hijos asociados)."""
