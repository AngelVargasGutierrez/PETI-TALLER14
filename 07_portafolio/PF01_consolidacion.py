# 07_portafolio/PF01_consolidacion.py
# Programa del curso (SEMANA-13/RECURSOS-TALLER), editado con los datos de la organización del equipo:
# Distribuidora Andina del Sur S.A.C. (EMPRESA-06). Insumo del Taller 14.
import sys
import pandas as pd
sys.stdout.reconfigure(encoding="utf-8")

CANDIDATOS = pd.DataFrame([
 # codigo, nombre, fuente, seccion_origen, objetivo, categoria, area_usuaria
 ("C-01","Segregación de funciones y flujo de aprobación en compras y pagos","Brecha de capacidad","FICHA G (incidente) y H-1","OD-01","Operar","Administración y Finanzas"),
 ("C-02","Registro de actividades de tratamiento de datos personales","Obligación normativa","Sección 4.1.5 · Sección 3.5 E-08","OD-04","Operar","Comercial"),
 ("C-03","Reactivación del módulo de almacén y conciliación del inventario","Brecha de capacidad","FICHA C (problema reconocido) y H-2","OD-02","Transformar","Almacén"),
 ("C-04","Gobierno del dato maestro (productos, proveedores y clientes)","Estrategia FODA","Sección 3.5 E-05","OD-01, OD-02","Transformar","Compras"),
 ("C-05","Restauración probada de respaldos y plan de continuidad","Brecha de capacidad","FICHA E y F (respaldos) · Sección 3.5 E-09","OD-03","Operar","Sistemas"),
 ("C-06","Remediación de seguridad del portal de pedidos","Brecha de capacidad","FICHA C (sin soporte) y H-3","OD-03","Operar","Sistemas"),
 ("C-07","Rediseño móvil del canal de pedidos de la bodega","Estrategia FODA","Sección 3.5 E-06","OD-05","Crecer","Comercial"),
 ("C-08","Planificación de rutas y trazabilidad de despacho","Estrategia FODA","Sección 3.5 E-02","OD-05","Crecer","Distribución"),
 ("C-09","Analítica de demanda y tablero comercial","Estrategia FODA","Sección 3.5 E-01","OD-05","Crecer","Gerencia"),
 ("C-10","Mesa de servicio con registro de incidentes y de cambios","Brecha de línea base","FICHA F (incidentes y cambios)","OD-03, OD-06","Operar","Sistemas"),
 ("C-11","Reactivación del comité de TI y medición de beneficios","Brecha de capacidad","FICHA B (comité) · expedientes de inversión","OD-06","Operar","Gerencia"),
 ("C-12","Medidas de seguridad sobre datos personales (contraseñas, segundo factor, capacitación)","Obligación normativa","Sección 4.1.5 · FICHA F","OD-04","Operar","Transversal"),
 ("C-13","Cambio del ERP por una versión en nube","Estrategia FODA","Sección 3.5 E-04","OD-03","Transformar","Transversal"),
 ("C-14","Autoservicio de trabajadores (boletas y vacaciones)","Brecha de servicio digital","Pedido de Recursos Humanos","OD-06","Crecer","Recursos Humanos"),
], columns=["codigo","nombre","fuente","seccion_origen","objetivo","categoria","area_usuaria"])

FUENTES_VALIDAS = {"Obligación normativa","Brecha de arquitectura","Brecha de capacidad",
                   "Estrategia FODA","Brecha de servicio digital","Brecha de línea base"}

print("=== CONTROL DE ADMISIÓN ===")
inv = CANDIDATOS[~CANDIDATOS.fuente.isin(FUENTES_VALIDAS)]
print(f"Candidatos sin fuente admisible: {len(inv)} → se retiran: {list(inv.codigo)}")
sin_obj = CANDIDATOS[CANDIDATOS.objetivo.isna() | (CANDIDATOS.objetivo.astype(str).str.strip()=="")]
print(f"Candidatos sin objetivo asociado: {len(sin_obj)} → se retiran o se justifican")

p = CANDIDATOS[CANDIDATOS.fuente.isin(FUENTES_VALIDAS) & CANDIDATOS.objetivo.notna()].copy()
p["codigo"] = ["PR-%02d" % (i+1) for i in range(len(p))]
p.to_csv("PF01_portafolio_candidatos.csv", index=False)

print(f"\nProyectos admitidos: {len(p)}")
print("\nPor fuente:\n", p.fuente.value_counts().to_string())
print("\nPor categoría:\n", p.categoria.value_counts().to_string())
print("\n=== COBERTURA DE OBJETIVOS ===")
obj = p.objetivo.str.split(", ").explode().value_counts()
print(obj.sort_index().to_string())
print("""
OD-01 Restablecer el control interno en compras y pagos
OD-02 Conciliar el inventario contable con el físico (diferencia actual 4.7 %)
OD-03 Asegurar la continuidad y la seguridad de la operación
OD-04 Cumplir el marco legal de datos personales (ANPD)
OD-05 Crecer en el canal digital y reducir el costo de despacho
OD-06 Gobernar la inversión de TI con beneficios medidos""")
