# 07_portafolio/PR01_no_negociables.py
# Programa del curso (SEMANA-14/RECURSOS-TALLER), editado con los datos de Distribuidora Andina del Sur S.A.C.
import sys
import pandas as pd
sys.stdout.reconfigure(encoding="utf-8")

p = pd.read_csv("PF01_portafolio_candidatos.csv")

# La norma ya está vigente: no concede un plazo nuevo. La fecha límite es la que el plan se compromete
# a no pasar ante la gerencia, y el proyecto debe terminar al menos un trimestre antes.
NO_NEGOCIABLES = {          # proyecto: (norma, plazo límite, fundamento)
 "PR-02": ("Ley 29733 y D. S. 016-2024-JUS", "2027-09-30",
           "Registro de actividades de tratamiento: obligación vigente y supervisada por la ANPD"),
 "PR-12": ("Ley 29733 art. 9 (principio de seguridad) y D. S. 016-2024-JUS", "2027-12-31",
           "Medidas de seguridad sobre datos personales: hoy la clave mínima es de seis caracteres y solo el correo tiene segundo factor"),
}
p["no_negociable"] = p.codigo.isin(NO_NEGOCIABLES)
p["norma"]         = p.codigo.map(lambda c: NO_NEGOCIABLES.get(c, (None,None,None))[0])
p["plazo_limite"]  = p.codigo.map(lambda c: NO_NEGOCIABLES.get(c, (None,None,None))[1])
p["fundamento_nn"] = p.codigo.map(lambda c: NO_NEGOCIABLES.get(c, (None,None,None))[2])

print("=== PROYECTOS NO NEGOCIABLES ===")
for r in p[p.no_negociable].itertuples():
    print(f"  {r.codigo}  {r.nombre}")
    print(f"         norma: {r.norma}")
    print(f"         plazo límite del plan: {r.plazo_limite}")
    print(f"         fundamento: {r.fundamento_nn}")
print("\n→ NO entran al modelo de priorización. Se ubican en la hoja de ruta por su plazo,")
print("  con al menos un trimestre de margen antes de la fecha límite.")
print(f"\nCandidatos: {len(p)} · no negociables: {int(p.no_negociable.sum())} · "
      f"compiten en el modelo: {(~p.no_negociable).sum()}")
print("Proyectos que sí compiten: " + ", ".join(p[~p.no_negociable].codigo))
p.to_csv("PR01_portafolio_marcado.csv", index=False)
