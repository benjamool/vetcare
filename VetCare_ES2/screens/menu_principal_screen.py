import sys

from services.clinica_service import ClinicaService
from screens.entidades_config import ENTIDADES
from screens.crud_screen import ejecutar_submenu_crud
from screens.operaciones_screen import ejecutar_submenu_operaciones
from utils.consola import limpiar_pantalla, pausar


def iniciar_menu_principal(service: ClinicaService):
    salir = len(ENTIDADES) + 2
    while True:
        limpiar_pantalla()
        print("\n" + "=" * 55)
        print("            SISTEMA CLÍNICA VETCARE")
        print("=" * 55)
        for i, (_, titulo, _, _) in enumerate(ENTIDADES, start=1):
            print(f"{i:>2}. {titulo}")
        print(f"{len(ENTIDADES) + 1:>2}. Operaciones clínicas")
        print(f"{salir:>2}. Salir")
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == str(salir):
            print("\nSaliendo del sistema...")
            sys.exit(0)
        elif opcion == str(len(ENTIDADES) + 1):
            ejecutar_submenu_operaciones(service)
        elif opcion.isdigit() and 1 <= int(opcion) <= len(ENTIDADES):
            clave, titulo, modelo, campos = ENTIDADES[int(opcion) - 1]
            ejecutar_submenu_crud(service.crud[clave], titulo, modelo, campos)
        else:
            print(" [!] Opción no válida.")
            pausar()
