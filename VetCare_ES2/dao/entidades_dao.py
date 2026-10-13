"""DAOs concretos: cada uno solo declara su modelo y su tabla; el CRUD lo hereda de BaseDAO.
Solo se escriben aquí las consultas propias de cada entidad."""
from dao.base_dao import BaseDAO, traducir_errores_sql
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


class PropietarioDAO(BaseDAO):
    MODELO, TABLA = Propietario, "PROPIETARIO"
    DDL = """CREATE TABLE IF NOT EXISTS PROPIETARIO (
        id_propietario INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL,
        direccion TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE)"""


class MascotaDAO(BaseDAO):
    MODELO, TABLA = Mascota, "MASCOTA"
    DDL = """CREATE TABLE IF NOT EXISTS MASCOTA (
        id_mascota INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        especie TEXT NOT NULL CHECK (especie IN ('PERRO','GATO','AVE','ROEDOR','REPTIL','OTRO')),
        raza TEXT NOT NULL,
        fecha_nacimiento TEXT NOT NULL,
        sexo TEXT NOT NULL CHECK (sexo IN ('Macho','Hembra')),
        esterilizado INTEGER NOT NULL CHECK (esterilizado IN (0,1)),
        id_propietario INTEGER NOT NULL REFERENCES PROPIETARIO(id_propietario))"""


class VeterinarioDAO(BaseDAO):
    MODELO, TABLA = Veterinario, "VETERINARIO"
    DDL = """CREATE TABLE IF NOT EXISTS VETERINARIO (
        id_veterinario INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        especialidad TEXT NOT NULL,
        numero_licencia TEXT NOT NULL UNIQUE)"""


class MedicamentoDAO(BaseDAO):
    MODELO, TABLA = Medicamento, "MEDICAMENTO"
    DDL = """CREATE TABLE IF NOT EXISTS MEDICAMENTO (
        id_medicamento INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        laboratorio TEXT NOT NULL,
        stock INTEGER NOT NULL CONSTRAINT chk_stock CHECK (stock >= 0),
        precio_unitario REAL NOT NULL CONSTRAINT chk_precio CHECK (precio_unitario > 0),
        via_administracion TEXT NOT NULL,
        requiere_receta INTEGER NOT NULL CHECK (requiere_receta IN (0,1)))"""

    def buscar_por_termino_seguro(self, termino: str) -> list:
        """Búsqueda parcial por nombre. El término del usuario va como parámetro, nunca dentro del SQL."""
        sql = f"{self._select()} WHERE nombre LIKE ? ORDER BY nombre"
        with traducir_errores_sql(), self.db.obtener_conexion() as conn:
            filas = conn.execute(sql, (f"%{termino}%",)).fetchall()
        return [Medicamento(*fila) for fila in filas]


class ConsultaDAO(BaseDAO):
    MODELO, TABLA = Consulta, "CONSULTA"
    DDL = """CREATE TABLE IF NOT EXISTS CONSULTA (
        id_consulta INTEGER PRIMARY KEY,
        fecha TEXT NOT NULL,
        motivo TEXT NOT NULL,
        estado TEXT NOT NULL CHECK (estado IN ('PROGRAMADA','EN_CURSO','COMPLETADA','CANCELADA')),
        id_veterinario INTEGER NOT NULL REFERENCES VETERINARIO(id_veterinario),
        id_mascota INTEGER NOT NULL REFERENCES MASCOTA(id_mascota))"""

    def listar_por_mascota(self, id_mascota: int) -> list:
        sql = f"{self._select()} WHERE id_mascota = ? ORDER BY fecha DESC"
        with traducir_errores_sql(), self.db.obtener_conexion() as conn:
            filas = conn.execute(sql, (id_mascota,)).fetchall()
        return [Consulta(*fila) for fila in filas]


class DetalleConsultaDAO(BaseDAO):  # composición: si se borra la consulta, se borran sus detalles
    MODELO, TABLA = DetalleConsulta, "DETALLE_CONSULTA"
    DDL = """CREATE TABLE IF NOT EXISTS DETALLE_CONSULTA (
        id_detalle INTEGER PRIMARY KEY,
        diagnostico TEXT NOT NULL,
        tratamiento TEXT NOT NULL,
        observaciones TEXT NOT NULL,
        id_consulta INTEGER NOT NULL REFERENCES CONSULTA(id_consulta) ON DELETE CASCADE)"""


class RecetaMedicaDAO(BaseDAO):  # una consulta produce 0..1 receta -> id_consulta UNIQUE
    MODELO, TABLA = RecetaMedica, "RECETA_MEDICA"
    DDL = """CREATE TABLE IF NOT EXISTS RECETA_MEDICA (
        id_receta INTEGER PRIMARY KEY,
        fecha_emision TEXT NOT NULL,
        indicaciones TEXT NOT NULL,
        id_consulta INTEGER NOT NULL UNIQUE REFERENCES CONSULTA(id_consulta))"""


class DetalleRecetaDAO(BaseDAO):  # composición con RecetaMedica
    MODELO, TABLA = DetalleReceta, "DETALLE_RECETA"
    DDL = """CREATE TABLE IF NOT EXISTS DETALLE_RECETA (
        id_detalle_receta INTEGER PRIMARY KEY,
        cantidad INTEGER NOT NULL CHECK (cantidad > 0),
        dosis TEXT NOT NULL,
        frecuencia TEXT NOT NULL,
        duracion_tratamiento TEXT NOT NULL,
        id_receta INTEGER NOT NULL REFERENCES RECETA_MEDICA(id_receta) ON DELETE CASCADE,
        id_medicamento INTEGER NOT NULL REFERENCES MEDICAMENTO(id_medicamento))"""


class VacunaDAO(BaseDAO):
    MODELO, TABLA = Vacuna, "VACUNA"
    DDL = """CREATE TABLE IF NOT EXISTS VACUNA (
        id_vacuna INTEGER PRIMARY KEY,
        tipo_vacuna TEXT NOT NULL,
        fecha_aplicacion TEXT NOT NULL,
        proxima_dosis TEXT NOT NULL,
        id_mascota INTEGER NOT NULL REFERENCES MASCOTA(id_mascota),
        id_veterinario INTEGER NOT NULL REFERENCES VETERINARIO(id_veterinario))"""


class AlergiaDAO(BaseDAO):
    MODELO, TABLA = Alergia, "ALERGIA"
    DDL = """CREATE TABLE IF NOT EXISTS ALERGIA (
        id_alergia INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        nivel_gravedad TEXT NOT NULL CHECK (nivel_gravedad IN ('Leve','Moderada','Grave')),
        id_mascota INTEGER NOT NULL REFERENCES MASCOTA(id_mascota))"""


class FacturaDAO(BaseDAO):  # una consulta genera 0..1 factura -> id_consulta UNIQUE
    MODELO, TABLA = Factura, "FACTURA"
    DDL = """CREATE TABLE IF NOT EXISTS FACTURA (
        id_factura INTEGER PRIMARY KEY,
        monto_total REAL NOT NULL CHECK (monto_total > 0),
        metodo_pago TEXT NOT NULL,
        fecha_emision TEXT NOT NULL,
        id_consulta INTEGER NOT NULL UNIQUE REFERENCES CONSULTA(id_consulta))"""


class ContraindicacionDAO:
    """Tabla intermedia de la relación muchos-a-muchos Alergia <-> Medicamento."""
    DDL = """CREATE TABLE IF NOT EXISTS ALERGIA_MEDICAMENTO (
        id_alergia INTEGER NOT NULL REFERENCES ALERGIA(id_alergia) ON DELETE CASCADE,
        id_medicamento INTEGER NOT NULL REFERENCES MEDICAMENTO(id_medicamento) ON DELETE CASCADE,
        PRIMARY KEY (id_alergia, id_medicamento))"""

    def __init__(self, conexion_db):
        self.db = conexion_db
        with traducir_errores_sql(), self.db.obtener_conexion() as conn:
            conn.execute(self.DDL)

    def agregar(self, id_alergia: int, id_medicamento: int):
        with traducir_errores_sql(), self.db.obtener_conexion() as conn:
            conn.execute("INSERT INTO ALERGIA_MEDICAMENTO (id_alergia, id_medicamento) VALUES (?, ?)",
                         (id_alergia, id_medicamento))

    def hay_contraindicacion(self, id_mascota: int, id_medicamento: int) -> bool:
        sql = """SELECT 1 FROM ALERGIA_MEDICAMENTO am
                 JOIN ALERGIA a ON a.id_alergia = am.id_alergia
                 WHERE a.id_mascota = ? AND am.id_medicamento = ? LIMIT 1"""
        with traducir_errores_sql(), self.db.obtener_conexion() as conn:
            return conn.execute(sql, (id_mascota, id_medicamento)).fetchone() is not None


def construir_daos(conexion_db) -> dict:
    """Crea todos los DAOs (y sus tablas) con una misma conexión."""
    return {
        "propietario": PropietarioDAO(conexion_db),
        "mascota": MascotaDAO(conexion_db),
        "veterinario": VeterinarioDAO(conexion_db),
        "medicamento": MedicamentoDAO(conexion_db),
        "consulta": ConsultaDAO(conexion_db),
        "detalle_consulta": DetalleConsultaDAO(conexion_db),
        "receta": RecetaMedicaDAO(conexion_db),
        "detalle_receta": DetalleRecetaDAO(conexion_db),
        "vacuna": VacunaDAO(conexion_db),
        "alergia": AlergiaDAO(conexion_db),
        "factura": FacturaDAO(conexion_db),
        "contraindicacion": ContraindicacionDAO(conexion_db),
    }
