# 07_portafolio/PR04_hoja_ruta.py
# Programa del curso (SEMANA-14/RECURSOS-TALLER), editado con los datos de Distribuidora Andina del Sur S.A.C.
# Cambio frente al original: además de calcular los niveles y proponer las olas, VERIFICA la hoja de ruta
# registrada a mano en PR05_hoja_ruta.csv (dependencias, plazos, capacidad y absorción del cambio).
import sys
import pandas as pd, networkx as nx
from comun import AQUI, DEP, CAPACIDAD_SIMULTANEA, HORIZONTE_MESES, AREAS_INTERNAS, ANIO_BASE, leer_hoja_ruta, mes
sys.stdout.reconfigure(encoding="utf-8")

r  = pd.read_csv("PR03_priorizado.csv")
nn = pd.read_csv("PR01_portafolio_marcado.csv")
tco = pd.read_csv("PF02_tco.csv").set_index("codigo")
puntaje, cuadrante = r.set_index("codigo").puntaje.to_dict(), r.set_index("codigo").cuadrante.to_dict()
no_neg = nn[nn.no_negociable].set_index("codigo").plazo_limite.to_dict()

G = nx.DiGraph(); G.add_nodes_from(list(nn.codigo))
G.add_edges_from([(b, a) for a, b in DEP])          # arista de habilitador → dependiente
assert nx.is_directed_acyclic_graph(G), "Existe un ciclo de dependencias: revisar el modelo"
nivel = {n: 0 for n in G.nodes}
for n in nx.topological_sort(G):
    for s in G.successors(n):
        nivel[s] = max(nivel[s], nivel[n] + 1)

print("=== NIVELES DE DEPENDENCIA (0 = puede iniciar de inmediato) ===")
for lv in sorted(set(nivel.values())):
    print(f"  Nivel {lv}: {[n for n, v in nivel.items() if v == lv]}")
print("\n=== PROYECTOS HABILITADORES ===")
for n in sorted(G.nodes, key=lambda x: -len(nx.descendants(G, x))):
    if nx.descendants(G, n):
        print(f"  {n} desbloquea a {sorted(nx.descendants(G, n))}")

print("\n=== PROPUESTA DE OLAS (insumo para registrar PR05_hoja_ruta.csv a mano) ===")
for c in nn.codigo:
    if c in no_neg:
        prop = f"Ola 1 · no negociable, por su plazo ({no_neg[c]})"
    elif cuadrante[c].startswith("④"):
        prop = "FUERA · cuadrante ④, candidato a no ejecutar"
    elif nivel[c] == 0 and nx.descendants(G, c):
        prop = "Ola 2 · habilitador: lo antes posible"
    elif nivel[c] == 0:
        prop = "Ola 1 u Ola 2 · sin dependencias, según capacidad"
    else:
        prop = f"Ola {min(nivel[c] + 1, 3)} o posterior · espera a {sorted(G.predecessors(c))}"
    p = f"{puntaje[c]:.2f}" if c in puntaje else " n/a"
    print(f"  {c}  nivel {nivel[c]}  puntaje {p}  {tco.loc[c, 'meses']:>2} meses  →  {prop}")

if not (AQUI / "PR05_hoja_ruta.csv").exists():
    print("\nPR05_hoja_ruta.csv aún no existe: registrar la hoja de ruta y volver a ejecutar.")
    sys.exit(0)

# ------------------ verificación de la hoja de ruta registrada ------------------
hr = leer_hoja_ruta()
ini, fin = hr.set_index("codigo").m_ini.to_dict(), hr.set_index("codigo").m_fin.to_dict()
fallas = 0
print("\n=== VERIFICACIÓN DE PR05_hoja_ruta.csv ===")

rotas = []
for a, b in G.edges:                                  # a habilita a b
    if b in ini:
        if a not in fin:
            rotas.append(f"{b} depende de {a}, que no está en la hoja de ruta")
        elif ini[b] <= fin[a]:
            rotas.append(f"{b} inicia en el mes {ini[b]} y {a} termina en el mes {fin[a]}")
print(f"[1] Dependencias rotas: {len(rotas)}  {'OK' if not rotas else 'FALLA'}")
for x in rotas: print("     - " + x)
fallas += len(rotas)

mal = [f"{x.codigo}: {x.m_fin - x.m_ini + 1} meses en la hoja de ruta, {tco.loc[x.codigo, 'meses']} en PF02_tco.csv"
       for x in hr.itertuples() if x.m_fin - x.m_ini + 1 != tco.loc[x.codigo, "meses"]]
mal += [f"{x.codigo}: termina fuera del horizonte de {HORIZONTE_MESES} meses" for x in hr.itertuples() if x.m_fin > HORIZONTE_MESES]
print(f"[2] Duraciones inconsistentes o fuera del horizonte: {len(mal)}  {'OK' if not mal else 'FALLA'}")
for x in mal: print("     - " + x)
fallas += len(mal)

tarde = []
for c, plazo in no_neg.items():
    if c not in fin:
        tarde.append(f"{c} es no negociable y no está en la hoja de ruta")
    elif fin[c] > mes(plazo) - 3:
        tarde.append(f"{c} termina en el mes {fin[c]}; su plazo es {plazo} (mes {mes(plazo)}) y exige un trimestre de margen")
print(f"[3] No negociables fuera de plazo o sin un trimestre de margen: {len(tarde)}  {'OK' if not tarde else 'FALLA'}")
for x in tarde: print("     - " + x)
fallas += len(tarde)

print(f"[4] Capacidad simultánea (máximo {CAPACIDAD_SIMULTANEA} por trimestre) y [5] absorción del cambio por área usuaria:")
exceso = choque = 0
for t in range(HORIZONTE_MESES // 3):
    m1, m2 = t * 3 + 1, t * 3 + 3
    act = hr[(hr.m_ini <= m2) & (hr.m_fin >= m1)]
    areas = list(act.area)
    rep = sorted({a for a in areas if areas.count(a) > 1 and a not in AREAS_INTERNAS})
    if "Transversal" in areas and any(a not in AREAS_INTERNAS and a != "Transversal" for a in areas):
        rep.append("Transversal junto a otra área usuaria")
    estado = []
    if len(act) > CAPACIDAD_SIMULTANEA: estado.append("FALLA capacidad"); exceso += 1
    if rep: estado.append("FALLA área: " + ", ".join(rep)); choque += 1
    print(f"     {ANIO_BASE + t // 4}-T{t % 4 + 1}  {len(act)} activos  {', '.join(act.codigo) or '—':<14} "
          f"{' · '.join(sorted(set(areas))) or '—':<34} {' · '.join(estado) or 'OK'}")
print(f"    Trimestres que exceden la capacidad: {exceso}  {'OK' if not exceso else 'FALLA'}")
print(f"    Trimestres con choque de área usuaria: {choque}  {'OK' if not choque else 'FALLA'}")
fallas += exceso + choque

olas = sorted(hr.ola.unique())
colados = [c for c in hr.codigo if cuadrante.get(c, "").startswith("④")]
ok6 = len(olas) == 3 and not colados
print(f"[6] Olas registradas: {len(olas)} ({', '.join(olas)}) · proyectos del cuadrante ④ programados: {len(colados)}  {'OK' if ok6 else 'FALLA'}")
fallas += (len(olas) != 3) + len(colados)

fuera = [c for c in nn.codigo if c not in ini]
print(f"\nProyectos del portafolio que NO están en la hoja de ruta: {', '.join(fuera) or 'ninguno'}")
print("→ Cada uno debe aparecer en PR07_no_se_hara.csv con el riesgo que la organización asume.")
print("\nRESULTADO: la hoja de ruta es ejecutable." if fallas == 0
      else f"\nRESULTADO: {fallas} falla(s). Corregir PR05_hoja_ruta.csv y volver a ejecutar.")
sys.exit(1 if fallas else 0)
