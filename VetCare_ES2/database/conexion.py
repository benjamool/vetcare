import os
import sqlite3
from contextlib import contextmanager

from exceptions.errores_clinica import PersistenciaError

RUTA_POR_DEFECTO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clinica_vetcare.db")


class ConexionDB:
    def __init__(self, ruta_db: str = RUTA_POR_DEFECTO):
        self.ruta_db = ruta_db

    @contextmanager
    def obtener_conexion(self):
        try:
            os.makedirs(os.path.dirname(os.path.abspath(self.ruta_db)), exist_ok=True)
            conn = sqlite3.connect(self.ruta_db)
            conn.execute("PRAGMA foreign_keys = ON;")  # SQLite las trae desactivadas
        except (OSError, sqlite3.Error) as error:
            raise PersistenciaError(f"No se pudo conectar a la base de datos: {error}") from error
        try:
            yield conn
            conn.commit()      # todo el bloque 'with' terminó bien
        except Exception:
            conn.rollback()    # algo falló: se deshace la transacción
            raise
        finally:
            conn.close()       # siempre se libera la conexión
