from models.enums import EstadoConsulta
from services.clinica_service import ClinicaService
from utils.consola import limpiar_pantalla, pausar, pedir_valor, formatear, ejecutar_seguro


def _historial(service: ClinicaService):
    id_mascota = pedir_valor("ID de la mascota", "int")
    consultas = service.historial_consultas(id_mascota)
    if not consultas:
        print("\n[!] La mascota no tiene consultas.")
    for c in consultas:
        print(f"#{c.id_consulta} | {c.fecha} | {c.estado.name} | {c.motivo}")


def _cambiar_estado(service: ClinicaService):
    id_consulta = pedir_valor("ID de la consulta", "int")
    nuevo = pedir_valor("Nuevo estado", EstadoConsulta)
    consulta = service.cambiar_estado_consulta(id_consulta, nuevo)
    print(f"\n[✓] Consulta #{consulta.id_consulta} ahora está {consulta.estado.name}.")


def _agregar_medicamento(service: ClinicaService):
    detalle = service.agregar_medicamento_a_receta(
        pedir_valor("ID del nuevo detalle de receta", "int"),
        pedir_valor("ID de la receta", "int"),
        pedir_valor("ID del medicamento", "int"),
        pedir_valor("Cantidad", "int"),
        pedir_valor("Dosis", "texto"),
        pedir_valor("Frecuencia", "texto"),
        pedir_valor("Duración del tratamiento", "texto"))
    print(f"\n[✓] Medicamento agregado (detalle #{detalle.id_detalle_receta}) y stock descontado.")


def _facturar(service: ClinicaService):
    factura = service.facturar_consulta(
        pedir_valor("ID de la nueva factura", "int"),
        pedir_valor("ID de la consulta", "int"),
        pedir_valor("Monto total", "float"),
        pedir_valor("Método de pago (Efectivo/Débito/Crédito/Transferencia)", "texto"))
    print(f"\n[✓] Factura #{factura.id_factura} generada por ${factura.monto_total:,.0f}.")


def _buscar(service: ClinicaService):
    termino = pedir_valor("Texto a buscar en el nombre", "texto")
    resultados = service.buscar_medicamentos(termino)
    if not resultados:
        print("\n[!] Sin coincidencias.")
    for m in resultados:
        print(f"#{m.id_medicamento} | {m.nombre} | {m.laboratorio} | stock {m.stock} | ${m.precio_unitario:,.0f}")


def _contraindicacion(service: ClinicaService):
    service.registrar_contraindicacion(pedir_valor("ID de la alergia", "int"),
                                       pedir_valor("ID del medicamento contraindicado", "int"))
    print("\n[✓] Contraindicación registrada.")


def ejecutar_submenu_operaciones(service: ClinicaService):
    acciones = {"1": _historial, "2": _cambiar_estado, "3": _agregar_medicamento,
                "4": _facturar, "5": _buscar, "6": _contraindicacion}
    while True:
        limpiar_pantalla()
        print("\n" + "=" * 55)
        print(" VETCARE — OPERACIONES CLÍNICAS")
        print("=" * 55)
        print("1. Historial de consultas de una mascota")
        print("2. Cambiar estado de una consulta")
        print("3. Agregar medicamento a una receta (valida alergias y stock)")
        print("4. Facturar una consulta completada")
        print("5. Buscar medicamento por nombre")
        print("6. Registrar contraindicación (alergia ↔ medicamento)")
        print("7. Volver")
        opcion = input("\nSeleccione una opción: ").strip()
        if opcion == "7":
            return
        if opcion in acciones:
            ejecutar_seguro(acciones[opcion], service)
        else:
            print(" [!] Opción no válida.")
            pausar()
