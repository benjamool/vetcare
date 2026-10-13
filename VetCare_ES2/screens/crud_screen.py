from services.crud_service import CrudService
from utils.consola import (limpiar_pantalla, pausar, pedir_valor, formatear, ejecutar_seguro)


def _titulo(texto: str):
    limpiar_pantalla()
    print("\n" + "=" * 55)
    print(f" VETCARE — {texto}")
    print("=" * 55)


def _pedir_id(campos) -> int:
    return pedir_valor(campos[0][1], "int")


def _listar(servicio: CrudService, modelo, campos):
    registros = servicio.listar()
    if not registros:
        print("\n[!] No hay registros.")
    for r in registros:
        print(" | ".join(f"{k}={formatear(v)}" for k, v in r.a_diccionario().items()))


def _consultar(servicio, modelo, campos):
    registro = servicio.obtener(_pedir_id(campos))
    print()
    for (param, etiqueta, _), valor in zip(campos, registro.a_diccionario().values()):
        print(f"{etiqueta:<35}: {formatear(valor)}")


def _registrar(servicio, modelo, campos):
    datos = {param: pedir_valor(etiqueta, tipo) for param, etiqueta, tipo in campos}
    servicio.registrar(modelo(**datos))  # el constructor valida; el DAO persiste
    print("\n[✓] Registro guardado.")


def _actualizar(servicio, modelo, campos):
    existente = servicio.obtener(_pedir_id(campos))
    print("\n(ENTER conserva el valor actual)")
    datos = {campos[0][0]: getattr(existente, campos[0][0])}  # el ID no se modifica
    for param, etiqueta, tipo in campos[1:]:
        datos[param] = pedir_valor(etiqueta, tipo, actual=getattr(existente, param))
    servicio.actualizar(modelo(**datos))  # se reconstruye el objeto: se revalidan TODAS las reglas
    print("\n[✓] Registro actualizado.")


def _eliminar(servicio, modelo, campos):
    identificador = _pedir_id(campos)
    servicio.obtener(identificador)  # falla si no existe
    if input("¿Confirma la eliminación? (s/n): ").strip().lower() == "s":
        servicio.eliminar(identificador)
        print("\n[✓] Registro eliminado.")
    else:
        print("\nOperación cancelada.")


def ejecutar_submenu_crud(servicio: CrudService, titulo: str, modelo, campos):
    acciones = {"1": _listar, "2": _consultar, "3": _registrar, "4": _actualizar, "5": _eliminar}
    while True:
        _titulo(titulo)
        print("1. Listar\n2. Consultar por ID\n3. Registrar\n4. Actualizar\n5. Eliminar\n6. Volver")
        opcion = input("\nSeleccione una opción: ").strip()
        if opcion == "6":
            return
        if opcion in acciones:
            ejecutar_seguro(acciones[opcion], servicio, modelo, campos)
        else:
            print(" [!] Opción no válida.")
            pausar()
