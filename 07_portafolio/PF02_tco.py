# 07_portafolio/PF02_tco.py
# Programa del curso (SEMANA-13/RECURSOS-TALLER), editado con los datos de la organización del equipo:
# Distribuidora Andina del Sur S.A.C. (EMPRESA-06). Insumo del Taller 14.
# Las cifras son estimaciones de orden de magnitud del equipo, sin cotizaciones: cada una lleva su incertidumbre.
import sys
import pandas as pd
sys.stdout.reconfigure(encoding="utf-8")

PROYECTOS = pd.DataFrame([
 # codigo, inversion_inicial, licencias_anual, infraestructura_anual, soporte_pct,
 # personal_anual, capacitacion_inicial, migracion, integracion, meses, incertidumbre
 ("PR-01", 14000,     0,     0, .10,  3000, 3000,      0,     0, 3, "±20 %"),
 ("PR-02", 22000,     0,     0, .10,  6000, 4000,      0,     0, 5, "±20 %"),
 ("PR-03", 48000,  3600,  2400, .15,  9000, 9000,   8000,  6000, 8, "±35 %"),
 ("PR-04", 30000,  2400,     0, .12,  9000, 5000,   9000,     0, 6, "±30 %"),
 ("PR-05", 12000,     0,  3600, .10,  3000, 2000,      0,     0, 3, "±20 %"),
 ("PR-06", 16000,     0,  2400, .12,  3000,    0,   4000,     0, 3, "±30 %"),
 ("PR-07", 62000,  6000,  4800, .15, 12000, 8000,   5000, 14000, 9, "±40 %"),
 ("PR-08", 40000,  7200,  1200, .15,  6000, 6000,      0,  9000, 6, "±35 %"),
 ("PR-09", 34000,  6000,  2400, .12,  9000, 5000,      0,  7000, 5, "±35 %"),
 ("PR-10",  8000,     0,  1200, .10,  3000, 3000,      0,     0, 3, "±20 %"),
 ("PR-11",  6000,     0,     0, .00,  3000, 2000,      0,     0, 2, "±15 %"),
 ("PR-12", 18000,  4800,     0, .10,  3000, 5000,      0,     0, 3, "±25 %"),
 ("PR-13",190000, 30000, 12000, .18, 24000,20000,  40000, 30000,12, "±50 %"),
 ("PR-14", 14000,  2400,     0, .10,     0, 2000,      0,  3000, 3, "±25 %"),
], columns=["codigo","inv_inicial","licencias","infra","soporte_pct","personal",
            "capacitacion","migracion","integracion","meses","incertidumbre"])

AÑOS = 5
P = PROYECTOS.copy()
P["soporte_anual"] = (P.inv_inicial * P.soporte_pct).round(0)
P["costo_anual"]   = P.licencias + P.infra + P.soporte_anual + P.personal
P["costo_unico"]   = P.inv_inicial + P.capacitacion + P.migracion + P.integracion
P["tco_5"]         = P.costo_unico + P.costo_anual * AÑOS
P["pct_operativo"] = ((P.costo_anual * AÑOS) / P.tco_5 * 100).round(1)

P = P.sort_values("tco_5", ascending=False)
P.to_csv("PF02_tco.csv", index=False)

print("=== COSTO TOTAL DE PROPIEDAD A 5 AÑOS ===")
print(P[["codigo","inv_inicial","costo_unico","costo_anual","tco_5","pct_operativo","incertidumbre"]]
      .to_string(index=False))
print(f"\nInversión inicial total : S/ {P.inv_inicial.sum():,.0f}")
print(f"TCO total a 5 años      : S/ {P.tco_5.sum():,.0f}")
print(f"Factor TCO/inversión    : {P.tco_5.sum()/P.inv_inicial.sum():.2f}×")
print("\n→ El TCO es {:.1f} veces la inversión inicial. Presentar solo la inversión".format(
      P.tco_5.sum()/P.inv_inicial.sum()))
print("  inicial ante la gerencia subestima el compromiso en S/ {:,.0f}.".format(
      P.tco_5.sum()-P.inv_inicial.sum()))
