"""Pruebas del sistema completo sobre una BD temporal. Ejecutar desde la raíz:
    python -m tests.test_sistema
"""
import os
import tempfile
from datetime import date

from database.conexion import ConexionDB
from dao.entidades_dao import construir_daos
from services.clinica_service import ClinicaService
from models.propietario import Propietario
from models.mascota import Mascota
from models.veterinario import Veterinario
from models.medicamento import Medicamento
from models.enums import EspecieAnimal, EstadoConsulta
from exceptions.errores_clinica import (EntidadNoEncontradaError, ReglaNegocioError,
                                        RegistroDuplicadoError, ReferenciaIntegridadError,
                                        PersistenciaError, VetCareException)


def debe_fallar(excepcion, accion, descripcion):
    try:
        accion()
    except excepcion as error:
        print(f"  OK  {descripcion}  ->  {type(error).__name__}")
        return
    raise AssertionError(f"No lanzó {excepcion.__name__}: {descripcion}")


def main():
    with tempfile.TemporaryDirectory() as carpeta:
        db = ConexionDB(os.path.join(carpeta, "test.db"))
        daos = construir_daos(db)
        srv = ClinicaService(daos)
        crud = srv.crud

        print("\n[1] Validaciones del dominio (encapsulamiento)")
        debe_fallar(ValueError, lambda: Medicamento(1, "X", "Lab", -1, 100, "Oral", True), "stock negativo")
        debe_fallar(ValueError, lambda: Medicamento(1, "X", "Lab", 1, 0, "Oral", True), "precio 0")
        debe_fallar(TypeError, lambda: Medicamento("1", "X", "Lab", 1, 100, "Oral", True), "id no entero")
        debe_fallar(ValueError, lambda: Propietario(1, "Ana", "123", "Calle 1", "ana@mail.cl"), "teléfono corto")
        debe_fallar(ValueError, lambda: Propietario(1, "Ana", "+56912345678", "Calle 1", "sin-arroba"), "email inválido")
        debe_fallar(ValueError, lambda: Mascota(1, "Rex", "DRAGON", "x", "2020-01-01", "Macho", False, 1), "especie inválida")
        debe_fallar(ValueError, lambda: Mascota(1, "Rex", "PERRO", "x", "2999-01-01", "Macho", False, 1), "nacimiento futuro")

        print("\n[2] CRUD y relaciones")
        crud["propietario"].registrar(Propietario(1, "Ana Soto", "+56912345678", "Calle 1", "ana@mail.cl"))
        crud["mascota"].registrar(Mascota(1, "Rex", "perro", "Labrador", "2020-05-01", "macho", False, 1))
        crud["veterinario"].registrar(Veterinario(1, "Dr. Pérez", "Cirugía", "LIC-001"))
        masc = crud["mascota"].obtener(1)
        assert masc.especie is EspecieAnimal.PERRO and masc.esterilizado is False
        masc.nombre = "Rexi"
        crud["mascota"].actualizar(masc)
        assert crud["mascota"].obtener(1).nombre == "Rexi"
        print("  OK  registrar / obtener / actualizar")
        debe_fallar(RegistroDuplicadoError, lambda: crud["veterinario"].registrar(
            Veterinario(2, "Otro", "X", "LIC-001")), "licencia duplicada (UNIQUE)")
        debe_fallar(ReferenciaIntegridadError, lambda: crud["mascota"].registrar(
            Mascota(2, "Luna", "GATO", "x", "2021-01-01", "Hembra", True, 99)), "mascota con propietario inexistente (FK)")
        debe_fallar(ReferenciaIntegridadError, lambda: crud["propietario"].eliminar(1), "borrar propietario con mascotas")
        debe_fallar(EntidadNoEncontradaError, lambda: crud["mascota"].obtener(999), "ID inexistente")

        print("\n[3] Reglas de negocio")
        v = crud["veterinario"].obtener(1)
        consulta = v.atender_consulta(1, 1, "Control anual")
        assert consulta.estado is EstadoConsulta.EN_CURSO
        crud["consulta"].registrar(consulta)
        crud["detalle_consulta"].registrar(consulta.registrar_detalle(1, "Sano", "Ninguno", ""))
        receta = consulta.emitir_receta(1, "Con comida")
        crud["receta"].registrar(receta)
        crud["medicamento"].registrar(Medicamento(1, "Amoxicilina 250mg", "LabX", 10, 5500, "Oral", True))
        crud["medicamento"].registrar(Medicamento(2, "Ketoprofeno 10mg", "LabY", 5, 3200, "Oral", True))

        srv.agregar_medicamento_a_receta(1, 1, 1, 4, "1 comp", "c/12h", "7 días")
        assert crud["medicamento"].obtener(1).stock == 6
        print("  OK  agregar medicamento descuenta stock (10 -> 6)")
        debe_fallar(ReglaNegocioError, lambda: srv.agregar_medicamento_a_receta(
            2, 1, 1, 50, "1", "c/8h", "5 días"), "stock insuficiente")
        assert crud["medicamento"].obtener(1).stock == 6

        crud["alergia"].registrar(masc.registrar_alergia(1, "Penicilina", "grave"))
        srv.registrar_contraindicacion(1, 2)
        debe_fallar(ReglaNegocioError, lambda: srv.agregar_medicamento_a_receta(
            3, 1, 2, 1, "1", "c/8h", "5 días"), "medicamento contraindicado por alergia")

        debe_fallar(ReglaNegocioError, lambda: srv.facturar_consulta(
            1, 1, 20000, "Efectivo"), "facturar consulta no completada")
        debe_fallar(ReglaNegocioError, lambda: srv.cambiar_estado_consulta(
            1, EstadoConsulta.PROGRAMADA), "transición de estado inválida")
        srv.cambiar_estado_consulta(1, EstadoConsulta.COMPLETADA)
        srv.facturar_consulta(1, 1, 20000, "efectivo")
        debe_fallar(ReglaNegocioError, lambda: srv.facturar_consulta(
            2, 1, 20000, "Efectivo"), "facturar dos veces la misma consulta")
        assert len(srv.historial_consultas(1)) == 1
        print("  OK  historial de consultas")

        print("\n[4] Seguridad SQL Injection")
        assert len(srv.buscar_medicamentos("' OR '1'='1")) == 0
        assert len(srv.buscar_medicamentos("Amoxi")) == 1
        assert len(srv.buscar_medicamentos("'; DROP TABLE MEDICAMENTO; --")) == 0
        assert len(crud["medicamento"].listar()) == 2
        print("  OK  payloads de inyección no alteran la consulta; la tabla sigue intacta")

        print("\n[5] Integridad y errores de conexión")
        debe_fallar(ReferenciaIntegridadError, lambda: crud["consulta"].eliminar(1), "borrar consulta con receta/factura")
        archivo = os.path.join(carpeta, "archivo.txt")
        open(archivo, "w").close()
        debe_fallar(PersistenciaError, lambda: construir_daos(ConexionDB(os.path.join(archivo, "x.db"))),
                    "ruta de BD imposible")
        debe_fallar(VetCareException, lambda: crud["mascota"].obtener(999), "todas heredan de VetCareException")

    print("\n" + "=" * 55)
    print("TODAS LAS PRUEBAS APROBARON")
    print("=" * 55)


if __name__ == "__main__":
    main()
