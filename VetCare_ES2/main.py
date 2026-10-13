import sys

from database.conexion import ConexionDB
from dao.entidades_dao import construir_daos
from services.clinica_service import ClinicaService
from screens.menu_principal_screen import iniciar_menu_principal
from exceptions.errores_clinica import PersistenciaError


def main():
    try:
        conexion = ConexionDB()                      # Infraestructura
        daos = construir_daos(conexion)              # Acceso a datos (crea las tablas)
    except PersistenciaError as error:
        print(f"[X] No se pudo iniciar la base de datos: {error}")
        sys.exit(1)

    servicio = ClinicaService(daos)                  # Lógica de negocio
    try:
        iniciar_menu_principal(servicio)             # Presentación
    except (KeyboardInterrupt, EOFError):
        print("\n\nSistema cerrado por el usuario.")


if __name__ == "__main__":
    main()
