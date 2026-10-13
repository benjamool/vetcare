import sqlite3
from contextlib import contextmanager

from exceptions.errores_clinica import (EntidadNoEncontradaError, PersistenciaError,
                                        RegistroDuplicadoError, ReferenciaIntegridadError)


@contextmanager
def traducir_errores_sql():
    """Convierte los errores técnicos de sqlite3 en excepciones propias del sistema."""
    try:
        yield
    except sqlite3.IntegrityError as error:
        mensaje = str(error).upper()
        if "FOREIGN KEY" in mensaje:
            raise ReferenciaIntegridadError(
                "Operación rechazada por integridad referencial: el registro relacionado "
                "no existe o tiene registros asociados.") from error
        if "UNIQUE" in mensaje:
            raise RegistroDuplicadoError("Ya existe un registro con ese ID o con un valor único repetido.") from error
        raise PersistenciaError(f"Restricción de la base de datos violada: {error}") from error
    except sqlite3.Error as error:
        raise PersistenciaError(f"Error de base de datos: {error}") from error


class BaseDAO:
    """CRUD genérico. Cada DAO concreto define MODELO, TABLA y DDL.
    Los nombres de tabla/columnas son constantes del código (nunca vienen del usuario);
    TODOS los valores viajan como parámetros '?'."""
    MODELO = None
    TABLA = ""
    DDL = ""

    def __init__(self, conexion_db):
        self.db = conexion_db
        self.crear_tabla()

    @property
    def _columnas(self):
        return self.MODELO.CAMPOS

    def _select(self) -> str:
        return f"SELECT {', '.join(self._columnas)} FROM {self.TABLA}"

    def crear_tabla(self):
        with traducir_errores_sql(), self.db.obtener_conexion() as conn:
            conn.execute(self.DDL)

    def insertar(self, entidad):
        marcas = ", ".join("?" for _ in self._columnas)
        sql = f"INSERT INTO {self.TABLA} ({', '.join(self._columnas)}) VALUES ({marcas})"
        with traducir_errores_sql(), self.db.obtener_conexion() as conn:
            conn.execute(sql, entidad.a_fila())

    def obtener_por_id_estricto(self, identificador: int):
        sql = f"{self._select()} WHERE {self._columnas[0]} = ?"
        with traducir_errores_sql(), self.db.obtener_conexion() as conn:
            fila = conn.execute(sql, (identificador,)).fetchone()
        if fila is None:
            raise EntidadNoEncontradaError(self.MODELO.__name__, identificador)
        return self.MODELO(*fila)  # hidratación: fila SQL -> objeto (pasa por las validaciones)

    def listar_todos(self) -> list:
        sql = f"{self._select()} ORDER BY {self._columnas[0]}"
        with traducir_errores_sql(), self.db.obtener_conexion() as conn:
            filas = conn.execute(sql).fetchall()
        return [self.MODELO(*fila) for fila in filas]

    def actualizar(self, entidad) -> bool:
        asignaciones = ", ".join(f"{c} = ?" for c in self._columnas[1:])
        sql = f"UPDATE {self.TABLA} SET {asignaciones} WHERE {self._columnas[0]} = ?"
        fila = entidad.a_fila()
        with traducir_errores_sql(), self.db.obtener_conexion() as conn:
            cursor = conn.execute(sql, fila[1:] + (fila[0],))
            if cursor.rowcount == 0:
                raise EntidadNoEncontradaError(self.MODELO.__name__, fila[0])
        return True

    def eliminar(self, identificador: int) -> bool:
        sql = f"DELETE FROM {self.TABLA} WHERE {self._columnas[0]} = ?"
        with traducir_errores_sql(), self.db.obtener_conexion() as conn:
            cursor = conn.execute(sql, (identificador,))
            if cursor.rowcount == 0:
                raise EntidadNoEncontradaError(self.MODELO.__name__, identificador)
        return True
