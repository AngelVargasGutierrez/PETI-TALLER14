# 07_portafolio/PR05_gantt.py
# Convierte PR05_hoja_ruta.csv en el archivo de GanttProject (PR05_hoja_ruta.gan) y en su vista PNG.
# El .gan lleva un grupo por ola, una tarea por proyecto con su duración, las dependencias como enlaces
# fin-inicio, un hito de decisión al cierre de cada ola y los plazos normativos como hitos rojos.
import sys
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from xml.sax.saxutils import quoteattr
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from comun import (AQUI, GRAFICOS, ANIO_BASE, DEP, leer_hoja_ruta, estilo_ejes,
                   AZUL, AQUA, AMARILLO, CRITICO, TINTA, TINTA2, EJE, FONDO)
sys.stdout.reconfigure(encoding="utf-8")

hr = leer_hoja_ruta()
marc = pd.read_csv("PR01_portafolio_marcado.csv")
COLOR_OLA = {"Ola 1": AZUL, "Ola 2": AQUA, "Ola 3": AMARILLO}
HITO = {"Ola 1": 12, "Ola 2": 24, "Ola 3": 36}        # mes de cierre de cada ola
en_ruta = set(hr.codigo)
sucesores = {}
for b, a in DEP:                                       # b depende de a
    if a in en_ruta and b in en_ruta:
        sucesores.setdefault(a, []).append(b)
plazos = [(x.codigo, x.plazo_limite) for x in marc[marc.no_negociable].itertuples() if x.codigo in en_ruta]


def habil(d):
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d


def inicio_mes(m):
    return date(ANIO_BASE + (m - 1) // 12, (m - 1) % 12 + 1, 1)


def fin_mes(m):
    return inicio_mes(m + 1) - timedelta(days=1)


def dias(i, f):
    return int(np.busday_count(i, f + timedelta(days=1)))


# ------------------ archivo .gan ------------------
ids, nid = {}, 1
olas = list(dict.fromkeys(hr.ola))
for ola in olas:
    ids[ola] = nid; nid += 1
    for x in hr[hr.ola == ola].itertuples():
        ids[x.codigo] = nid; nid += 1
    ids["H" + ola] = nid; nid += 1
T = []
for ola in olas:
    g = hr[hr.ola == ola]
    i, f = habil(inicio_mes(g.m_ini.min())), fin_mes(g.m_fin.max())
    nombre_ola = g.Ola.iloc[0]
    T.append(f'    <task id="{ids[ola]}" name={quoteattr(nombre_ola)} color="{COLOR_OLA[ola]}" meeting="false" '
             f'start="{i}" duration="{dias(i, f)}" complete="0" expand="true">')
    for x in g.itertuples():
        i, f = habil(inicio_mes(x.m_ini)), fin_mes(x.m_fin)
        dep = "".join(f'<depend id="{ids[s]}" type="2" difference="0" hardness="Rubber"/>' for s in sucesores.get(x.codigo, []))
        T.append(f'      <task id="{ids[x.codigo]}" name={quoteattr(x.Proyecto)} color="{COLOR_OLA[ola]}" meeting="false" '
                 f'start="{i}" duration="{dias(i, f)}" complete="0" expand="true">'
                 f'<notes><![CDATA[Área usuaria afectada: {x.area}. Duración: {x.m_fin - x.m_ini + 1} meses.]]></notes>{dep}</task>')
    h = habil(fin_mes(HITO[ola]))
    T.append(f'      <task id="{ids["H" + ola]}" name={quoteattr(f"HITO DE DECISIÓN H{ola[-1]} · cierre de {nombre_ola} · continuar, ajustar o detener")} '
             f'color="#52514e" meeting="true" start="{h}" duration="0" complete="0" expand="true"/>')
    T.append("    </task>")
for c, plazo in plazos:
    T.append(f'    <task id="{nid}" name={quoteattr(f"PLAZO NORMATIVO · {c} · {plazo}")} color="#d03b3b" meeting="true" '
             f'start="{habil(date.fromisoformat(plazo))}" duration="0" complete="0" expand="true"/>')
    nid += 1
NL = "\n"
gan = f'''<?xml version="1.0" encoding="UTF-8"?>
<project name="PETI Distribuidora Andina del Sur · Hoja de ruta 2027-2029" company="Distribuidora Andina del Sur S.A.C." webLink="" view-date="{ANIO_BASE}-01-01" view-index="0" gantt-divider-location="460" resource-divider-location="300" version="3.2.3247" locale="es">
  <description><![CDATA[Hoja de ruta del portafolio del PETI en tres olas. Generado por PR05_gantt.py a partir de PR05_hoja_ruta.csv.]]></description>
  <view zooming-state="default:2" id="gantt-chart">
    <field id="tpd3" name="Nombre" width="340" order="0"/>
    <field id="tpd4" name="Fecha de inicio" width="80" order="1"/>
    <field id="tpd5" name="Fecha de fin" width="80" order="2"/>
  </view>
  <view id="resource-table">
    <field id="0" name="Nombre" width="210" order="0"/>
    <field id="1" name="Función" width="86" order="1"/>
  </view>
  <calendars>
    <day-types>
      <day-type id="0"/>
      <day-type id="1"/>
      <default-week id="1" name="default" sun="1" mon="0" tue="0" wed="0" thu="0" fri="0" sat="1"/>
      <only-show-weekends value="false"/>
      <overriden-day-types/>
      <days/>
    </day-types>
  </calendars>
  <tasks empty-milestones="true">
    <taskproperties>
      <taskproperty id="tpd0" name="type" type="default" valuetype="icon"/>
      <taskproperty id="tpd1" name="priority" type="default" valuetype="icon"/>
      <taskproperty id="tpd2" name="info" type="default" valuetype="icon"/>
      <taskproperty id="tpd3" name="name" type="default" valuetype="text"/>
      <taskproperty id="tpd4" name="begindate" type="default" valuetype="date"/>
      <taskproperty id="tpd5" name="enddate" type="default" valuetype="date"/>
      <taskproperty id="tpd6" name="duration" type="default" valuetype="int"/>
      <taskproperty id="tpd7" name="completion" type="default" valuetype="int"/>
      <taskproperty id="tpd8" name="coordinator" type="default" valuetype="text"/>
      <taskproperty id="tpd9" name="predecessorsr" type="default" valuetype="text"/>
    </taskproperties>
{NL.join(T)}
  </tasks>
  <resources/>
  <allocations/>
  <vacations/>
  <previous/>
  <roles roles-name="Default"/>
</project>
'''
(AQUI / "PR05_hoja_ruta.gan").write_text(gan, encoding="utf-8")
raiz = ET.fromstring(gan.encode("utf-8"))
tareas = raiz.findall(".//task")
print("=== CRONOGRAMA PARA GANTTPROJECT ===")
print(f"PR05_hoja_ruta.gan · XML bien formado · {len(olas)} grupos (olas) · {len(hr)} proyectos · "
      f"{len(raiz.findall('.//depend'))} dependencias fin-inicio · {len(olas)} hitos de decisión · "
      f"{len(plazos)} hitos rojos de plazo normativo · {len(tareas)} tareas en total")
for a, ss in sucesores.items():
    print(f"  Enlace fin-inicio: {a} → {', '.join(ss)}")
for c, plazo in plazos:
    print(f"  Hito rojo: {c} · plazo {plazo}")

# ------------------ vista PNG ------------------
orden = hr.sort_values(["m_ini", "m_fin"]).reset_index(drop=True)
y = {x.codigo: len(orden) - 1 - i for i, x in enumerate(orden.itertuples())}
ini, fin = orden.set_index("codigo").m_ini, orden.set_index("codigo").m_fin
fig, ax = plt.subplots(figsize=(12, 6.6), dpi=160)
fig.patch.set_facecolor(FONDO); estilo_ejes(ax); ax.grid(axis="y", visible=False)
for x in orden.itertuples():
    ax.barh(y[x.codigo], x.m_fin - x.m_ini + 1, left=x.m_ini - 1, height=0.52, color=COLOR_OLA[x.ola],
            edgecolor=FONDO, linewidth=2, zorder=3)
    ax.text((x.m_ini - 1 + x.m_fin) / 2, y[x.codigo], f"{x.m_fin - x.m_ini + 1} m", va="center", ha="center", fontsize=8,
            color=TINTA if x.ola == "Ola 3" else "#ffffff", zorder=4)
for a, ss in sucesores.items():
    for s in ss:
        ax.annotate("", xy=(ini[s] - 1, y[s]), xytext=(fin[a] - 0.4, y[a] - 0.28), zorder=5,
                    arrowprops=dict(arrowstyle="-|>", color=TINTA2, lw=1, connectionstyle="angle,angleA=-90,angleB=0,rad=3"))
for k in (12, 24, 36):
    ax.axvline(k, color=EJE, lw=1, ls=(0, (4, 3)), zorder=1)
    ax.plot([k], [len(orden) - 0.3], marker="D", ms=8, color=TINTA2, mec=FONDO, mew=1.5, zorder=5, clip_on=False)
    ax.text(k - 0.7, len(orden) - 0.3, f"H{k // 12} · decisión", ha="right", va="center", fontsize=8, color=TINTA2)
for c, plazo in plazos:
    d = date.fromisoformat(plazo); xm = (d.year - ANIO_BASE) * 12 + d.month
    ax.plot([xm], [y[c]], marker="D", ms=8, color=CRITICO, mec=FONDO, mew=1.5, zorder=6)
    ax.text(xm + 0.8, y[c], f"plazo {d.strftime('%d/%m/%Y')}", fontsize=8, color=TINTA2, va="center")
ax.set_yticks([y[x.codigo] for x in orden.itertuples()])
ax.set_yticklabels([x.Proyecto if len(x.Proyecto) < 58 else x.Proyecto[:56] + "…" for x in orden.itertuples()], fontsize=8.5, color=TINTA)
ax.set_xticks(range(0, 37, 6))
ax.set_xticklabels(["ene 2027", "jul 2027", "ene 2028", "jul 2028", "ene 2029", "jul 2029", "dic 2029"])
ax.set_xlim(0, 38.5); ax.set_ylim(-0.6, len(orden) + 0.2)
ley = [Patch(color=AZUL, label="Ola 1 · Fundacional"), Patch(color=AQUA, label="Ola 2 · Habilitación"),
       Patch(color=AMARILLO, label="Ola 3 · Explotación"),
       Line2D([], [], marker="D", ls="", color=CRITICO, label="Plazo normativo"),
       Line2D([], [], marker="D", ls="", color=TINTA2, label="Hito de decisión"),
       Line2D([], [], color=TINTA2, lw=1, label="Dependencia fin-inicio")]
fig.legend(handles=ley, loc="upper left", bbox_to_anchor=(0.02, 0.93), ncol=6, frameon=False, fontsize=8.5, labelcolor=TINTA2)
fig.suptitle("Hoja de ruta del PETI en tres olas · Distribuidora Andina del Sur, 2027–2029", x=0.025, ha="left",
             color=TINTA, fontsize=12)
fig.tight_layout(rect=(0, 0, 1, 0.9))
fig.savefig(GRAFICOS / "PR_hoja_ruta.png", facecolor=FONDO)
print("Archivos creados: PR05_hoja_ruta.gan · ../graficos/PR_hoja_ruta.png")
