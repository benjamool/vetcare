# VetCare — ES2 (TI3021 Programación Orientada a Objeto Seguro)

CRUD en Python orientado a objetos, con SQLite (`sqlite3`, librería oficial), implementado desde el diagrama de clases UML de VetCare.

## Ejecutar
Requiere Python 3.10+ (sin librerías externas). Desde esta carpeta:

    python main.py                  # menú de consola (crea database/clinica_vetcare.db)
    python -m tests.test_sistema    # pruebas automáticas (usan una BD temporal)

## Arquitectura (por capas, igual que la S9 P2)
    screens/    -> menús de consola (pide datos, muestra resultados, atrapa errores)
    services/   -> reglas de negocio (stock, alergias, estados, facturación)
    dao/        -> SQL parametrizado; CRUD genérico en base_dao.py
    database/   -> ConexionDB (commit / rollback / cierre automático, claves foráneas ON)
    models/     -> clases del UML con encapsulamiento y validaciones
    exceptions/ -> errores propios (VetCareException y derivadas)
    utils/      -> validaciones y utilidades de consola

## UML -> Python
| UML | Python |
|---|---|
| Clase con atributos `-x` | Clase en `models/` con atributo protegido `_x` + `property` que valida |
| Enumeración | `Enum` en `models/enums.py` (`EspecieAnimal`, `EstadoConsulta`) |
| Atributos `idX` (llaves foráneas) | Atributo entero en el modelo + `FOREIGN KEY` en la tabla |
| Composición `*--` (Consulta→DetalleConsulta, Receta→DetalleReceta) | FK con `ON DELETE CASCADE` |
| Agregación `o--` y asociaciones `-->` | FK sin cascada (la BD impide borrar al padre con hijos) |
| `0..1` (Consulta→Receta, Consulta→Factura) | columna `id_consulta` `UNIQUE` |
| `0..*` ↔ `0..*` (Alergia ↔ Medicamento) | tabla intermedia `ALERGIA_MEDICAMENTO` |
| Métodos del UML que crean objetos (`registrarMascota`, `emitirReceta`...) | métodos del modelo que devuelven el objeto nuevo |
| Métodos del UML que necesitan la BD (`obtenerHistorialConsultas`) | `ClinicaService` |

Los IDs se ingresan manualmente (como en el ejemplo del profesor), por eso algunos métodos reciben un `id_...` extra respecto al UML.

## Principios aplicados
- **Encapsulamiento:** `propiedad_validada` (models/base.py) obliga a que todo valor pase por su validador, también dentro del constructor.
- **Herencia / reutilización:** todos los modelos heredan de `EntidadBase`; todos los DAO heredan el CRUD de `BaseDAO`; las pantallas CRUD son una sola función configurada en `entidades_config.py`.
- **Seguridad:** todas las consultas usan parámetros `?` (sin concatenar texto del usuario); `PRAGMA foreign_keys = ON`; `CHECK` en la BD además de las validaciones en Python.
- **Errores:** `sqlite3.Error` se traduce a `PersistenciaError`, `RegistroDuplicadoError`, `ReferenciaIntegridadError`; las pantallas atrapan todo y el programa no se cae.

## Reglas de negocio (ClinicaService)
- Una consulta solo cambia de estado por transiciones válidas (PROGRAMADA → EN_CURSO → COMPLETADA; CANCELADA desde los dos primeros).
- Al agregar un medicamento a una receta: se descuenta stock, se rechaza si no alcanza y si la mascota tiene una alergia contraindicada con ese medicamento.
- Solo se facturan consultas COMPLETADAS, y una sola factura por consulta.
