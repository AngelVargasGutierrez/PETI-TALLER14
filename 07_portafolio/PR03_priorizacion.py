# 07_portafolio/PR03_priorizacion.py
# Programa del curso (SEMANA-14/RECURSOS-TALLER), editado con los datos de Distribuidora Andina del Sur S.A.C.
# Cambios frente al original: (1) los pesos no están en el código, se leen de PR02_pesos.md;
# (2) se agrega el criterio obligatorio de impacto social y ambiental; (3) el gráfico no depende solo del color.
import sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from comun import (GRAFICOS, CLAVES, UMBRAL_IMPACTO, UMBRAL_ESFUERZO, leer_pesos, estilo_ejes,
                   AZUL, NARANJA, AQUA, AMARILLO, TINTA, TINTA2, MUDO, EJE, FONDO)
sys.stdout.reconfigure(encoding="utf-8")

pesos = leer_pesos()
PESOS = {k: p for k, _, p, _ in pesos}
print("=== PESOS LEÍDOS DE PR02_pesos.md ===")
for k, nombre, p, _ in pesos:
    print(f"  {nombre:<30} {p:.2f}")
print(f"  {'SUMA':<30} {sum(PESOS.values()):.2f}")
assert abs(sum(PESOS.values()) - 1) < 1e-9, "Los pesos no suman 1: corregir PR02_pesos.md"
assert PESOS["social_ambiental"] >= 0.10, "El criterio social y ambiental debe pesar al menos 10 %"

CALIF = pd.DataFrame([
 # codigo, contribucion, beneficio, urgencia, habilitacion, riesgo_no_hacer, facilidad, aceptacion, social_ambiental
 ("PR-01", 5, 3, 5, 2, 5, 4, 2, 3),   # segregación de funciones — hay un incidente abierto; quita la autoaprobación
 ("PR-03", 5, 5, 4, 2, 4, 2, 2, 3),   # almacén — diferencia de inventario de 4.7 %; cambia el trabajo diario del almacén
 ("PR-04", 5, 2, 3, 5, 4, 3, 3, 2),   # dato maestro — habilitador de cuatro proyectos
 ("PR-05", 4, 2, 4, 2, 5, 5, 4, 2),   # restauración probada — el respaldo de 2025 nunca se restauró
 ("PR-06", 3, 2, 4, 2, 4, 4, 4, 3),   # seguridad del portal — sin soporte ni pruebas de seguridad
 ("PR-07", 4, 5, 2, 1, 2, 2, 4, 4),   # canal de pedidos móvil
 ("PR-08", 4, 5, 2, 1, 3, 2, 3, 5),   # ruteo — menos kilómetros y combustible
 ("PR-09", 3, 4, 1, 1, 2, 2, 3, 2),   # analítica de demanda
 ("PR-10", 3, 2, 3, 3, 3, 5, 4, 2),   # mesa de servicio — da la línea base de incidentes y cambios
 ("PR-11", 5, 2, 4, 4, 4, 5, 3, 3),   # comité de TI — el que decide y mide el resto del portafolio
 ("PR-13", 3, 2, 1, 1, 2, 1, 1, 1),   # cambio de ERP — el ERP tiene soporte vigente; el problema es de uso
 ("PR-14", 2, 2, 1, 1, 1, 4, 5, 4),   # autoservicio de trabajadores
], columns=["codigo"] + CLAVES)

marc = pd.read_csv("PR01_portafolio_marcado.csv")
compiten = set(marc[~marc.no_negociable].codigo)
assert set(CALIF.codigo) == compiten, f"Calificados y competidores no coinciden: {set(CALIF.codigo) ^ compiten}"

CALIF["puntaje"] = sum(CALIF[c]*w for c, w in PESOS.items()).round(3)
CALIF = CALIF.sort_values(["puntaje", "codigo"], ascending=[False, True])

tco = pd.read_csv("PF02_tco.csv")[["codigo","tco_5","inv_inicial","meses"]]
r = CALIF.merge(tco, on="codigo", how="left").merge(marc[["codigo","nombre"]], on="codigo")

# --- Matriz esfuerzo-impacto (fórmulas del programa del curso) ---
r["impacto"]  = (r.contribucion*.5 + r.beneficio*.3 + r.riesgo_no_hacer*.2).round(2)
r["esfuerzo"] = (6 - r.facilidad).round(2)
r["cuadrante"] = [
  "① Ganancia rápida" if i >= UMBRAL_IMPACTO and e < UMBRAL_ESFUERZO else
  "② Apuesta mayor"   if i >= UMBRAL_IMPACTO and e >= UMBRAL_ESFUERZO else
  "③ Relleno"         if i < UMBRAL_IMPACTO and e < UMBRAL_ESFUERZO else
  "④ Sumidero"
  for i, e in zip(r.impacto, r.esfuerzo)]
r.insert(0, "puesto", range(1, len(r) + 1))
r.to_csv("PR03_priorizado.csv", index=False)

print("\n=== PORTAFOLIO PRIORIZADO (sin los no negociables) ===")
print(r[["puesto","codigo"] + CLAVES + ["puntaje","tco_5"]].rename(columns={
    "contribucion":"contr","beneficio":"benef","urgencia":"urg","habilitacion":"habil",
    "riesgo_no_hacer":"riesgo","facilidad":"facil","aceptacion":"acept","social_ambiental":"social"}).to_string(index=False))
print("\nNo negociables, fuera del modelo:", ", ".join(marc[marc.no_negociable].codigo))

CUAD = ["① Ganancia rápida","② Apuesta mayor","③ Relleno","④ Sumidero"]
print("\n=== MATRIZ ESFUERZO-IMPACTO ===")
for c in CUAD:
    sub = r[r.cuadrante == c]
    print(f"{c}: {list(sub.codigo)}")
print(f"Cuadrantes poblados: {r.cuadrante.nunique()} de 4")
print("\n=== CANDIDATOS A NO EJECUTAR (cuadrante ④) ===")
for x in r[r.cuadrante == "④ Sumidero"].itertuples():
    print(f"  {x.codigo}  puntaje {x.puntaje:.2f} · impacto {x.impacto:.2f} · esfuerzo {x.esfuerzo:.0f} · "
          f"TCO a 5 años S/ {x.tco_5:,.0f} · {x.nombre}")
print("→ Deben declararse explícitamente en el plan, con el riesgo que la organización asume.")

# --- Gráfico ---
COL = dict(zip(CUAD, [AQUA, AZUL, AMARILLO, NARANJA]))
MARCA = dict(zip(CUAD, ["o", "s", "^", "D"]))
ROT = dict(zip(CUAD, ["① Ganancias rápidas · hacer primero", "② Apuestas mayores · planificar bien",
                      "③ Relleno · si sobra capacidad", "④ Sumideros · no hacer"]))
fig, ax = plt.subplots(figsize=(9.2, 6.4), dpi=160)
fig.patch.set_facecolor(FONDO); estilo_ejes(ax)
ax.set_xlim(0.5, 5.5); ax.set_ylim(1.4, 5.1)
ax.axhline(UMBRAL_IMPACTO, color=EJE, lw=1.2, ls=(0, (4, 3))); ax.axvline(UMBRAL_ESFUERZO, color=EJE, lw=1.2, ls=(0, (4, 3)))
for c in CUAD:
    g = r[r.cuadrante == c]
    ax.scatter(g.esfuerzo, g.impacto, s=110, color=COL[c], marker=MARCA[c], edgecolor=FONDO, linewidth=2, label=ROT[c], zorder=3)
vistos = {}
for x in r.sort_values("impacto", ascending=False).itertuples():   # etiquetas apiladas cuando comparten esfuerzo
    k = (x.esfuerzo, round(x.impacto, 1)); n = vistos.get(k, 0); vistos[k] = n + 1
    ax.annotate(f"{x.codigo} · {x.puntaje:.2f}", (x.esfuerzo, x.impacto), xytext=(9, -3 - 11 * n),
                textcoords="offset points", fontsize=8.5, color=TINTA)
ax.text(5.45, 5.05, "ALTO IMPACTO", ha="right", va="top", fontsize=8, color=MUDO)
ax.text(5.45, 1.45, "BAJO IMPACTO", ha="right", va="bottom", fontsize=8, color=MUDO)
ax.set_xticks([1, 2, 3, 4, 5])
ax.set_xlabel("Esfuerzo  (6 − facilidad de ejecución)  →", color=TINTA2, fontsize=10)
ax.set_ylabel("Impacto  (contribución, beneficio y riesgo de no hacerlo)  →", color=TINTA2, fontsize=10)
ax.set_title("Matriz esfuerzo-impacto del portafolio · Distribuidora Andina del Sur\n"
             "Junto a cada proyecto, su puntaje multicriterio", color=TINTA, fontsize=11.5, loc="left", pad=46)
ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, frameon=False, fontsize=8.5, labelcolor=TINTA2)
fig.tight_layout(); GRAFICOS.mkdir(exist_ok=True)
fig.savefig(GRAFICOS / "PR_esfuerzo_impacto.png", facecolor=FONDO)
print("\nArchivos creados: PR03_priorizado.csv · ../graficos/PR_esfuerzo_impacto.png")
