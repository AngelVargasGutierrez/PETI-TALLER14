# 07_portafolio/PR06_presupuesto.py
# Programa del curso (SEMANA-14/RECURSOS-TALLER), editado con los datos de Distribuidora Andina del Sur S.A.C.
# Cambios frente al original: (1) la inversión se reparte por los meses de ejecución y el gasto operativo
# empieza el mes siguiente a la entrega, en vez de cargarse por año completo; (2) compara cada año con el techo
# acordado; (3) calcula el rango de incertidumbre de PF02; (4) el gráfico usa dos paneles, no dos ejes.
import sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from comun import (GRAFICOS, PRESUPUESTO_ANUAL, CAMBIO_PCT, CONTINGENCIA_PCT, ANIO_BASE, HORIZONTE_MESES,
                   leer_hoja_ruta, estilo_ejes, AZUL, NARANJA, AQUA, AMARILLO, CRITICO, TINTA, TINTA2, FONDO)
sys.stdout.reconfigure(encoding="utf-8")

tco = pd.read_csv("PF02_tco.csv").set_index("codigo")
tco["inc"] = tco.incertidumbre.str.extract(r"(\d+)").astype(float) / 100
hr = leer_hoja_ruta()
MESES = range(1, HORIZONTE_MESES + 1)
ANIO = [f"Año {(m - 1) // 12 + 1} ({ANIO_BASE + (m - 1) // 12})" for m in MESES]


def presupuesto(plan):
    """plan: lista de (codigo, mes_inicio, mes_fin). Devuelve (tabla por año, OPEX mensual)."""
    capex = pd.Series(0.0, index=MESES); opex = capex.copy(); cmin = capex.copy(); cmax = capex.copy()
    for c, m1, m2 in plan:
        n = m2 - m1 + 1
        capex.loc[m1:m2] += tco.loc[c, "costo_unico"] / n
        cmin.loc[m1:m2] += tco.loc[c, "costo_unico"] * (1 - tco.loc[c, "inc"]) / n
        cmax.loc[m1:m2] += tco.loc[c, "costo_unico"] * (1 + tco.loc[c, "inc"]) / n
        opex.loc[m2 + 1:] += tco.loc[c, "costo_anual"] / 12
    t = pd.DataFrame({"capex": capex.groupby(ANIO).sum(), "opex": opex.groupby(ANIO).sum()})
    t["gestion_cambio"] = t.capex * CAMBIO_PCT
    t["subtotal"] = t.capex + t.opex + t.gestion_cambio
    t["contingencia"] = t.subtotal * CONTINGENCIA_PCT
    t["total"] = t.subtotal + t.contingencia
    t["techo"] = PRESUPUESTO_ANUAL
    t["holgura"] = t.techo - t.total
    t["opex_acumulado"] = t.opex.cumsum()
    for nombre, serie in (("total_min", cmin), ("total_max", cmax)):
        cx = serie.groupby(ANIO).sum()
        t[nombre] = (cx * (1 + CAMBIO_PCT) + t.opex) * (1 + CONTINGENCIA_PCT)
    t.index.name = "año"
    return t.round(0), opex


def mostrar(t):
    print(f"  {'':<13}{'CAPEX':>9}{'OPEX':>9}{'G.cambio':>9}{'Conting.':>9}{'TOTAL':>9}{'Techo':>9}{'Holgura':>9}  ¿Cuadra?")
    for a, x in t.iterrows():
        print(f"  {a:<13}{x.capex:>9,.0f}{x.opex:>9,.0f}{x.gestion_cambio:>9,.0f}{x.contingencia:>9,.0f}"
              f"{x.total:>9,.0f}{x.techo:>9,.0f}{x.holgura:>9,.0f}  {'SÍ' if x.holgura >= 0 else 'NO · excede el techo'}")
    print(f"  {'Total 3 años':<13}{t.capex.sum():>9,.0f}{t.opex.sum():>9,.0f}{t.gestion_cambio.sum():>9,.0f}"
          f"{t.contingencia.sum():>9,.0f}{t.total.sum():>9,.0f}")


plan = [(x.codigo, x.m_ini, x.m_fin) for x in hr.itertuples()]
pr, opex_m = presupuesto(plan)
pr.to_csv("PR06_presupuesto.csv")
cuadra = bool((pr.holgura >= 0).all())

print("=== PRESUPUESTO PLURIANUAL (S/) ===")
print("Plan de PR05_hoja_ruta.csv: " + ", ".join(p[0] for p in plan))
mostrar(pr)
print(f"\nTOTAL DEL PLAN (3 años): S/ {pr.total.sum():,.0f}")
print(f"  CAPEX: S/ {pr.capex.sum():,.0f}  ({pr.capex.sum()/pr.total.sum():.0%})")
print(f"  OPEX : S/ {pr.opex.sum():,.0f}  ({pr.opex.sum()/pr.total.sum():.0%})")

print("\n=== RANGO DE INCERTIDUMBRE (según la incertidumbre de cada proyecto en PF02_tco.csv) ===")
for a, x in pr.iterrows():
    nota = "dentro del techo aun en el extremo alto" if x.total_max <= PRESUPUESTO_ANUAL else \
        f"el extremo alto supera el techo en S/ {x.total_max - PRESUPUESTO_ANUAL:,.0f}"
    print(f"  {a}: S/ {x.total_min:,.0f} a S/ {x.total_max:,.0f} · {nota}")

regimen = sum(tco.loc[p[0], "costo_anual"] for p in plan)
print("\n=== CURVA DE GASTO OPERATIVO (OPEX) ACUMULADO ===")
for a, x in pr.iterrows():
    print(f"  {a}: OPEX del año S/ {x.opex:>8,.0f} ({x.opex/PRESUPUESTO_ANUAL:5.1%} del techo) · acumulado S/ {x.opex_acumulado:>8,.0f}")
print(f"  Desde {ANIO_BASE + 3}, sin ningún proyecto nuevo: S/ {regimen:,.0f} por año ({regimen/PRESUPUESTO_ANUAL:.1%} del techo).")
print(f"  OPEX del año 3 ÷ OPEX del año 1: ×{pr.opex.iloc[-1]/max(pr.opex.iloc[0], 1):.1f}")
print("→ El OPEX NO BAJA: cada proyecto entregado lo incrementa de forma permanente.")
print("  Este es el compromiso real que la gerencia asume al aprobar el plan.")

if "PR-07" not in [p[0] for p in plan]:           # costo de oportunidad del proyecto que la gerencia más pide
    alt, _ = presupuesto(plan + [("PR-07", 25, 33)])
    print("\n=== ESCENARIO ALTERNO: agregar PR-07 (canal de pedidos móvil) en el año 3 ===")
    mostrar(alt)
    for a, x in alt[alt.holgura < 0].iterrows():
        print(f"→ {a} excedería el techo en S/ {-x.holgura:,.0f}: PR-07 no cabe sin retirar otro proyecto.")

print("\nRESULTADO: el presupuesto cuadra con el techo anual en los tres años." if cuadra else
      "\nRESULTADO: el presupuesto NO cuadra con el techo. Reprogramar PR05_hoja_ruta.csv y volver a ejecutar.")

# ------------------ gráfico: dos paneles, un eje cada uno ------------------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 5.4), dpi=160, gridspec_kw={"width_ratios": [1, 1.15]})
fig.patch.set_facecolor(FONDO)
series = [("capex", "Inversión (CAPEX)", AZUL), ("opex", "Gasto operativo (OPEX)", NARANJA),
          ("gestion_cambio", "Gestión del cambio", AQUA), ("contingencia", "Contingencia", AMARILLO)]
estilo_ejes(a1); a1.grid(axis="x", visible=False)
etq = [a.replace(" (", "\n(") for a in pr.index]
base = pd.Series(0.0, index=pr.index)
for col, nombre, color in series:
    a1.bar(etq, pr[col] / 1000, bottom=base / 1000, width=0.5, color=color, edgecolor=FONDO, linewidth=2, label=nombre)
    base += pr[col]
tope = max(PRESUPUESTO_ANUAL, pr.total.max()) / 1000
for x, tot in zip(etq, pr.total):
    a1.text(x, tope + 5, f"S/ {tot / 1000:,.0f} mil", ha="center", va="bottom", fontsize=9, color=TINTA)
a1.axhline(PRESUPUESTO_ANUAL / 1000, color=CRITICO, lw=1.6, ls=(0, (5, 3)), label=f"Techo anual · S/ {PRESUPUESTO_ANUAL / 1000:,.0f} mil")
a1.set_ylim(0, tope * 1.2)
a1.set_ylabel("Miles de S/", color=TINTA2, fontsize=10)
a1.set_title("Presupuesto del portafolio por año", color=TINTA, fontsize=11.5, loc="left", pad=58)
a1.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, frameon=False, fontsize=8.5, labelcolor=TINTA2)

estilo_ejes(a2)
acum = opex_m.cumsum() / 1000
a2.plot(acum.index, acum.values, color=NARANJA, lw=2)
a2.fill_between(acum.index, acum.values, color=NARANJA, alpha=0.10, lw=0)
for m in sorted({p[2] for p in plan}):             # cada entrega aumenta la pendiente
    a2.plot([m], [acum.loc[m]], "o", ms=6, color=NARANJA, mec=FONDO, mew=1.5, zorder=3)
a2.annotate(f"S/ {acum.iloc[-1]:,.0f} mil acumulados a dic. {ANIO_BASE + 2}", (36, acum.iloc[-1]), xytext=(0, 9),
            textcoords="offset points", ha="right", va="bottom", fontsize=9, color=TINTA)
a2.set_xticks([1, 12, 24, 36]); a2.set_xticklabels(["ene 2027", "dic 2027", "dic 2028", "dic 2029"])
a2.set_xlim(0, 37); a2.set_ylim(0, acum.iloc[-1] * 1.25)
a2.set_ylabel("Miles de S/ acumulados", color=TINTA2, fontsize=10)
a2.set_title("Gasto operativo acumulado: crece con cada entrega y no baja", color=TINTA, fontsize=11.5, loc="left", pad=58)
a2.text(0, 1.05, f"Cada punto es una entrega. Desde {ANIO_BASE + 3}: S/ {regimen / 1000:,.0f} mil de gasto fijo al año "
        f"({regimen / PRESUPUESTO_ANUAL:.0%} del techo).", transform=a2.transAxes, fontsize=8.5, color=TINTA2)
fig.tight_layout()
fig.savefig(GRAFICOS / "PR_presupuesto.png", facecolor=FONDO)
print("Archivos creados: PR06_presupuesto.csv · ../graficos/PR_presupuesto.png")
sys.exit(0 if cuadra else 1)
