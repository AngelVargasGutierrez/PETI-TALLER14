# 07_portafolio/PR08_validacion.py
# Paso F del taller: las tres comprobaciones, más la coherencia entre los archivos entregados.
import sys
import pandas as pd
from comun import DEP, PRESUPUESTO_ANUAL, leer_pesos, leer_hoja_ruta
sys.stdout.reconfigure(encoding="utf-8")
fallas = []


def comprobar(titulo, ok, detalle):
    print(f"[{'OK' if ok else 'FALLA'}] {titulo}\n       {detalle}")
    if not ok:
        fallas.append(titulo)


print("=== PASO F · VALIDACIÓN ===\n")
pesos = leer_pesos()
suma = round(sum(p for _, _, p, _ in pesos), 6)
sin_just = [n for _, n, _, j in pesos if len(j) < 40]
social = dict((k, p) for k, _, p, _ in pesos)["social_ambiental"]
comprobar("1. Los pesos suman uno y cada peso tiene su justificación en el diagnóstico",
          suma == 1.0 and not sin_just and social >= 0.10,
          f"suma = {suma:.2f} · {len(pesos)} criterios · sin justificación: {len(sin_just)} · impacto social y ambiental = {social:.2f} (mínimo 0.10)")

hr = leer_hoja_ruta()
ini, fin = hr.set_index("codigo").m_ini.to_dict(), hr.set_index("codigo").m_fin.to_dict()
rotas = [f"{b} antes que {a}" for b, a in DEP if b in ini and (a not in fin or ini[b] <= fin[a])]
revisadas = [(b, a) for b, a in DEP if b in ini]
comprobar("2. Ningún proyecto está programado antes que aquel del que depende",
          not rotas, f"{len(revisadas)} dependencias revisadas ({', '.join(f'{a}→{b}' for b, a in revisadas)}) · rotas: {len(rotas)} {rotas or ''}")

pr = pd.read_csv("PR06_presupuesto.csv")
excede = pr[pr.total > PRESUPUESTO_ANUAL]
comprobar("3. El presupuesto por año cuadra con la capacidad real de gasto",
          excede.empty, " · ".join(f"{x.año}: S/ {x.total:,.0f} de S/ {PRESUPUESTO_ANUAL:,.0f}" for x in pr.itertuples())
          + f" · años que exceden: {len(excede)}")

print()
marc = pd.read_csv("PR01_portafolio_marcado.csv")
prio = pd.read_csv("PR03_priorizado.csv")
nsh = pd.read_csv("PR07_no_se_hara.csv")
nsh["codigo"] = nsh.Proyecto.str.extract(r"(PR-\d+)")
fuera = set(marc.codigo) - set(hr.codigo)
comprobar("4. Todo proyecto del portafolio está en la hoja de ruta o en la tabla de lo que no se hará",
          fuera == set(nsh.codigo), f"en la hoja de ruta: {len(hr)} · no se harán: {sorted(nsh.codigo)} · sin destino: {sorted(fuera ^ set(nsh.codigo)) or 'ninguno'}")
c4 = set(prio[prio.cuadrante.str.startswith("④")].codigo)
comprobar("5. Los proyectos del cuadrante ④ están declarados como no ejecutados, con riesgo y responsable",
          c4 <= set(nsh.codigo) and nsh.iloc[:, 3:7].notna().all().all(),
          f"cuadrante ④: {sorted(c4)} · filas con riesgo, responsable y fecha de revisión: {len(nsh)} de {len(nsh)}")
nn = set(marc[marc.no_negociable].codigo)
comprobar("6. Los no negociables no fueron puntuados y sí están en la hoja de ruta",
          not (nn & set(prio.codigo)) and nn <= set(hr.codigo), f"no negociables: {sorted(nn)}")
comprobar("7. Las cifras del presupuesto se presentan con su rango de incertidumbre",
          {"total_min", "total_max"} <= set(pr.columns),
          " · ".join(f"{x.año}: S/ {x.total_min:,.0f} a S/ {x.total_max:,.0f}" for x in pr.itertuples()))

print(f"\nRESULTADO: {7 - len(fallas)} de 7 comprobaciones superadas." + ("" if not fallas else " Fallan: " + "; ".join(fallas)))
print("\nPendiente que la validación automática no puede cerrar:")
print(f"  · En el extremo alto del rango, {int((pr.total_max > PRESUPUESTO_ANUAL).sum())} de 3 años superan el techo. "
      "Se trata en el hito de decisión de cada ola.")
print("  · Los pesos y el techo son la propuesta para la Entrevista 3; falta el acta de la entrevista simulada.")
sys.exit(1 if fallas else 0)
