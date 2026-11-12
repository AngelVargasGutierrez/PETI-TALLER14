# -*- coding: utf-8 -*-
"""Construye el informe del Taller de laboratorio 14 (SI-886) sobre la plantilla oficial
SI886-PLANTILLA-TALLER.docx, conservando su carátula, encabezado, pie y estilos.
Las tablas se llenan desde los CSV del repositorio: el informe no repite cifras a mano."""
import os
import docx
import pandas as pd
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P7 = os.path.join(ROOT, "07_portafolio")
SAL = os.path.join(ROOT, "evidencias", "S14", "salidas")
TEMPLATE = os.path.join(ROOT, "SI886-PLANTILLA-TALLER.docx")
OUT = os.path.join(ROOT, "SI886-S14-TALLER-Grupo1.docx")
G = lambda n: os.path.join(ROOT, "graficos", n)

REPO = "https://github.com/AngelVargasGutierrez/PETI-TALLER14"
BASE = f"{REPO}/blob/taller-14"
TREE = f"{REPO}/tree/taller-14"
PR_URL = f"{REPO}/pull/1"
F7 = f"{BASE}/07_portafolio"
FS = f"{BASE}/evidencias/S14/salidas"
FONT = "Arial"


def miles(v):
    return f"{float(v):,.0f}".replace(",", " ")


def set_font(run, name=FONT, size=11, bold=False, italic=False, color=None):
    run.font.name = name; run.font.size = Pt(size); run.font.bold = bold; run.font.italic = italic
    if color:
        run.font.color.rgb = color
    rPr = run._element.get_or_add_rPr()
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rPr.append(rf)
    rf.set(qn("w:ascii"), name); rf.set(qn("w:hAnsi"), name)


def find(doc, exact=None, starts=None):
    for p in doc.paragraphs:
        if (exact is not None and p.text.strip() == exact) or (starts is not None and p.text.startswith(starts)):
            return p
    raise ValueError(f"No encontrado: {exact or starts}")


def set_text(par, text):
    if not par.runs:
        set_font(par.add_run(text)); return
    par.runs[0].text = text
    for r in par.runs[1:]:
        r.text = ""


def add_runs(par, text, size=11, italic=False):
    """Texto con **negritas** intercaladas."""
    for i, part in enumerate(text.split("**")):
        if part:
            set_font(par.add_run(part), FONT, size, bold=(i % 2 == 1), italic=italic)


def para(anchor, text="", style=None, size=11, italic=False, align=None, before=None, after=6, indent=None):
    el = OxmlElement("w:p"); anchor._p.addprevious(el)
    p = docx.text.paragraph.Paragraph(el, anchor._parent)
    if style:
        p.style = anchor.part.document.styles[style]
    if align is not None:
        p.alignment = align
    if before is not None:
        p.paragraph_format.space_before = Pt(before)
    if after is not None:
        p.paragraph_format.space_after = Pt(after)
    if indent is not None:
        p.paragraph_format.left_indent = Cm(indent)
    if text:
        if style and style.startswith("Heading"):
            p.add_run(text)
        else:
            add_runs(p, text, size, italic)
    return p


def bullets(anchor, items, numbered=False):
    for i, t in enumerate(items, 1):
        para(anchor, (f"{i}. " if numbered else "• ") + t, after=3, indent=0.6)


def code(anchor, text, size=7.5):
    p = para(anchor, "", before=2, after=8, indent=0.2)
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), "F2F2F2")
    p._p.get_or_add_pPr().append(shd)
    p.paragraph_format.line_spacing = 1.0
    lines = text.rstrip("\n").split("\n")
    for i, ln in enumerate(lines):
        if i:
            p.add_run().add_break()
        set_font(p.add_run(ln), "Consolas", size)


def table(anchor, headers, rows, widths=None, size=8.5):
    doc = anchor.part.document
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = TABLE_STYLE; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]; c.text = ""
        set_font(c.paragraphs[0].add_run(h), FONT, size, bold=True)
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            add_runs(cells[i].paragraphs[0], str(v), size)
    if widths:
        t.autofit = False
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
    anchor._p.addprevious(t._tbl)
    para(anchor, "", after=4)
    return t


def figure(anchor, n, title, path, note, width=15.5):
    para(anchor, f"**Figura {n}**", before=8, after=0)
    para(anchor, title, italic=True, after=4)
    p = para(anchor, "", align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    p.add_run().add_picture(path, width=Cm(width))
    para(anchor, note, size=9, italic=True, after=10)


def salida(nombre, desde=None, hasta=None, max_lineas=None):
    L = open(os.path.join(SAL, nombre), encoding="utf-8").read().rstrip("\n").split("\n")
    if desde:
        L = L[next(i for i, l in enumerate(L) if desde in l):]
    if hasta:
        L = L[:next(i for i, l in enumerate(L) if hasta in l)]
    while L and not L[-1].strip():
        L.pop()
    return "\n".join(L[:max_lineas] if max_lineas else L)


# ---------------------------------------------------------------- datos
marc = pd.read_csv(os.path.join(P7, "PR01_portafolio_marcado.csv"))
prio = pd.read_csv(os.path.join(P7, "PR03_priorizado.csv"))
hr = pd.read_csv(os.path.join(P7, "PR05_hoja_ruta.csv"), dtype=str).fillna("")
pres = pd.read_csv(os.path.join(P7, "PR06_presupuesto.csv"))
nsh = pd.read_csv(os.path.join(P7, "PR07_no_se_hara.csv"), dtype=str)
tco = pd.read_csv(os.path.join(P7, "PF02_tco.csv")).set_index("codigo")
nombre = marc.set_index("codigo").nombre.to_dict()

doc = Document(TEMPLATE)
TABLE_STYLE = doc.tables[0].style

# ---------------------------------------------------------------- carátula
set_text(find(doc, exact="TALLER"), "TALLER 14")
set_text(find(doc, exact="“…………………………………………….”"), "“Priorización multicriterio, hoja de ruta y presupuesto plurianual”")
set_text(find(doc, exact="“………………………….”"), "“Planeamiento Estratégico de TI”")
set_text(find(doc, starts="APELLIDOS Y NOMBRES"), "VARGAS GUTIERREZ, ANGEL · 2020066922")

# elimina la página «Cómo se usa esta plantilla»
start = find(doc, exact="Cómo se usa esta plantilla"); end = find(doc, exact="Borra esta página antes de entregar.")
body = doc.element.body; quitar = []; on = False
previo = start._p.getprevious()           # el salto de página que antecede a esa hoja
for el in list(body):
    if el is start._p or (el is previo and "w:br" in previo.xml and not "".join(previo.itertext()).strip()):
        on = True
    if on:
        quitar.append(el)
    if el is end._p:
        break
for el in quitar:
    body.remove(el)

t_rec, t_res = doc.tables[0], doc.tables[1]
a_rec = docx.text.paragraph.Paragraph(t_rec._tbl.getnext(), t_rec._parent)
a_res = docx.text.paragraph.Paragraph(t_res._tbl.getnext(), t_res._parent)

# ---------------------------------------------------------------- 1. información
a = find(doc, exact="1.2 Objetivos")
para(a, "Priorización del portafolio de proyectos de TI de **Distribuidora Andina del Sur S.A.C.** (EMPRESA-06 del banco "
        "de casos del curso): modelo multicriterio con pesos fijados antes de calcular, hoja de ruta en tres olas para "
        "2027–2029 y presupuesto plurianual con su curva de gasto operativo acumulado. El taller produce las secciones "
        "7.2, 7.3 y 7.4 del PETI de la organización.")
a = find(doc, exact="1.3 Tiempo de duración")
bullets(a, [
    "Separar del modelo los proyectos que impone una norma y ubicarlos por su fecha.",
    "Fijar con la gerencia los pesos del modelo antes de calcular, con el criterio de impacto social y ambiental en 10 %.",
    "Calcular el puntaje de los doce proyectos que compiten y ubicarlos en la matriz esfuerzo-impacto.",
    "Decir por escrito qué proyectos no se harán, qué riesgo asume la organización y quién lo acepta.",
    "Armar la hoja de ruta en tres olas sin romper dependencias, plazos, capacidad ni absorción del cambio.",
    "Calcular el presupuesto de tres años y mostrar cuánto gasto fijo deja el plan al terminar.",
    "Redactar las secciones 7.2, 7.3 y 7.4 del PETI.",
])
a = find(doc, exact="1.4 Resultados de aprendizaje")
para(a, "Sesión 2 de laboratorio de la Semana 14, más el trabajo de cierre fuera de aula para versionar la evidencia.")
a = find(doc, exact="1.5 Recursos")
bullets(a, [
    "Distingue un proyecto que se prioriza de uno que se programa por obligación.",
    "Explica por qué el orden del puntaje no es el orden del cronograma.",
    "Sustenta un presupuesto plurianual mostrando el gasto operativo que deja, no solo la inversión.",
    "Comunica a la gerencia lo que el plan deja fuera y el riesgo que eso implica.",
])
table(a_rec, ["Recurso", "Versión", "Para qué se usó"], [
    ["Documentos del caso EMPRESA-06", "Banco de casos del curso", "FICHA.md, presupuesto_ti.csv, inversiones_cerradas.csv y expedientes-de-inversion.md: de ahí salen los pesos, la capacidad y la contingencia"],
    ["Programas del curso PF01, PF02, PR01, PR03, PR04 y PR06", "RECURSOS-TALLER de las semanas 13 y 14", "Base de los programas del equipo, editados con los datos de la organización"],
    ["Python", "3.13.7", "Ejecución de los programas"],
    ["pandas", "2.3.3", "No negociables, modelo multicriterio, presupuesto y curva de gasto operativo"],
    ["networkx", "3.6", "Niveles de dependencia y verificación de precedencias"],
    ["matplotlib", "3.11.1", "Matriz esfuerzo-impacto, hoja de ruta y presupuesto en PNG"],
    ["GanttProject", "Formato .gan 3.2", "Cronograma con dependencias fin-inicio, hitos de decisión y plazos normativos (archivo generado por PR05_gantt.py)"],
    ["Git y GitHub", "—", "Versionado, Pull Request y etiquetas taller-14 y v0.14"],
], widths=[4.6, 3.6, 8.2])
t_rec._tbl.getparent().remove(t_rec._tbl)

set_text(find(doc, starts="Reglas de uso del laboratorio"),
         "1. El presupuesto es información Confidencial de la organización. Este informe y las secciones 7.2 a 7.4 llevan esa clasificación.")
a = find(doc, exact="2. Procedimiento o metodología")
for t in [
    "2. El criterio «Impacto social y ambiental» está en el modelo con peso 0.10 y se fijó antes de calcular, como los demás.",
    "3. Los pesos se versionaron en un commit anterior al del cálculo. El programa los lee de PR02_pesos.md; no los tiene escritos.",
    "4. Los proyectos descartados y el riesgo que la organización asume se declaran en una tabla propia, con el cargo que acepta el riesgo.",
    "5. Ninguna cifra de costo se presenta cerrada: cada total lleva su rango de incertidumbre.",
    "6. Las personas del caso se citan por cargo, nunca por nombre.",
]:
    para(a, t)

# ---------------------------------------------------------------- 2. procedimiento
set_text(find(doc, starts="Cada paso lleva su título"),
         "Organización de trabajo: Distribuidora Andina del Sur S.A.C., mayorista de consumo masivo con 157 trabajadores, "
         "4 personas en TI y un presupuesto de TI de S/ 742 000. Cada paso dice qué se buscaba, qué se ejecutó y dónde "
         f"quedó la evidencia en el repositorio del equipo: {REPO}. Todos los archivos están en la carpeta 07_portafolio/.")

# Paso A
a = find(doc, exact="Paso B")
set_text(find(doc, exact="Paso A"), "Paso A — Separar los no negociables y fijar los pesos")
para(a, "**Qué se buscaba.** Sacar del modelo los proyectos que impone una norma y dejar escritos los pesos antes de calcular nada.")
para(a, "**Insumos.** El equipo no tenía el portafolio de la Semana 13 en el repositorio. Se generó con los programas de esa "
        "semana (PF01_consolidacion.py y PF02_tco.py), editados con los hechos de la ficha del caso: 14 proyectos candidatos, "
        "cada uno con su fuente y su objetivo, y su costo total de propiedad. La inversión inicial suma S/ 514 000 y el costo "
        "a 5 años S/ 2 025 500, 3.9 veces más.")
para(a, "**Acción.** Se ejecutó PR01_no_negociables.py:")
code(a, "cd 07_portafolio && python PR01_no_negociables.py\n\n" + salida("PR01_no_negociables.txt"))
para(a, "La norma ya está vigente y no da un plazo nuevo. La fecha límite es la que el plan se compromete a no pasar, y cada "
        "proyecto termina al menos un trimestre antes.")
para(a, "**Pesos.** Se escribieron en PR02_pesos.md, cada uno con su razón en los documentos del caso:")
PES = [
    ["Contribución a los objetivos", "0.25", "El objetivo declarado de TI es restablecer el control interno en compras y pagos y conciliar el inventario (ficha, sección A)"],
    ["Beneficio económico", "0.10", "Baja del 0.20 de referencia: las tres inversiones de 2025 declararon un beneficio y en ninguna se midió (expedientes de inversión)"],
    ["Urgencia", "0.15", "Incidente abierto de fraccionamiento de compras, portal de pedidos sin soporte y dos de cinco contratos vencidos"],
    ["Habilitación", "0.15", "Cuatro proyectos de valor dependen del dato maestro"],
    ["Riesgo de no hacerlo", "0.10", "Tres riesgos conocidos sin tratar y respaldos que nunca se han restaurado"],
    ["Facilidad de ejecución", "0.10", "Equipo de TI de 4 personas; la partida «Proyectos nuevos» se ejecutó al 66 % en 2025"],
    ["Aceptación organizacional", "0.05", "Hoy los cambios en producción se aplican sin registro ni aprobación"],
    ["**Impacto social y ambiental**", "**0.10**", "Criterio obligatorio. La empresa distribuye por carretera y atiende a bodegas pequeñas"],
    ["**Suma**", "**1.00**", ""],
]
table(a, ["Criterio", "Peso", "Justificación acordada"], PES, widths=[4.4, 1.4, 10.6])
para(a, "También quedaron fijados ahí el techo anual (S/ 222 000: el presupuesto de TI de S/ 742 000 menos S/ 520 000 "
        "comprometidos en operación), la capacidad (2 proyectos por trimestre), la gestión del cambio (10 %) y la "
        "contingencia (15 %, el tope del rango, porque las inversiones de 2025 se desviaron +30.4 %, +20.5 % y +16.5 %).")
para(a, f"**Evidencia.** {F7}/PR01_portafolio_marcado.csv · {F7}/PR02_pesos.md. El commit de los pesos es anterior al del "
        f"cálculo: {REPO}/commits/taller-14")

# Paso B
a = find(doc, exact="Paso C")
set_text(find(doc, exact="Paso B"), "Paso B — Calcular la priorización")
para(a, "**Qué se buscaba.** El puntaje de los 12 proyectos que compiten y su lugar en la matriz esfuerzo-impacto.")
para(a, "**Acción.** Se editó PR03_priorizacion.py con las calificaciones de la organización. El programa lee los pesos de "
        "PR02_pesos.md y se detiene si no suman 1 o si el criterio social y ambiental pesa menos de 10 %.")
code(a, "python PR03_priorizacion.py\n\n" + salida("PR03_priorizacion.txt", desde="=== PORTAFOLIO PRIORIZADO"), size=6.8)
figure(a, 1, "Matriz esfuerzo-impacto del portafolio", G("PR_esfuerzo_impacto.png"),
       "Nota. Elaboración propia con PR03_priorizacion.py. Impacto = 0.5 × contribución + 0.3 × beneficio + 0.2 × riesgo de no "
       "hacerlo; esfuerzo = 6 − facilidad. Umbrales en 3.5.", width=13.5)
para(a, "**Lectura.** Los cuatro cuadrantes quedaron poblados. El primer puesto no es un sistema: es reactivar el comité de TI "
        "y medir beneficios (PR-11, 4.00), porque sin él nadie decide ni mide el resto. El cuadrante ④ tiene dos proyectos: "
        "la analítica de demanda (PR-09) y el cambio de ERP (PR-13).")
para(a, f"**Evidencia.** {F7}/PR03_priorizado.csv · {BASE}/graficos/PR_esfuerzo_impacto.png · {FS}/PR03_priorizacion.txt")

# Paso C
a = find(doc, exact="3. Resultados")
set_text(find(doc, exact="Paso C"), "Paso C — Construir la hoja de ruta")
para(a, "**Qué se buscaba.** Un cronograma que respete cuatro restricciones: dependencias, plazos, capacidad y absorción del cambio.")
para(a, "**Acción.** PR04_hoja_ruta.py calcula los niveles de dependencia con networkx y propone las olas:")
code(a, "python PR04_hoja_ruta.py\n\n" + salida("PR04_hoja_ruta.txt", hasta="=== PROPUESTA DE OLAS"))
para(a, "Con esa propuesta se registró a mano la hoja de ruta en PR05_hoja_ruta.csv:")
table(a, ["Proyecto", "Ola", "Inicio", "Fin", "Meses", "Depende de", "Hito", "Área usuaria"],
      [[r["Proyecto"], r["Ola"], r["Inicio"], r["Fin"], r["Duración (meses)"], r["Depende de"], r["Hito de decisión"],
        r["Área usuaria afectada"]] for _, r in hr.iterrows()], widths=[5.6, 2.0, 1.5, 1.5, 1.1, 1.4, 1.5, 2.2], size=7.5)
para(a, "El mismo programa verifica lo registrado:")
code(a, salida("PR04_hoja_ruta.txt", desde="=== VERIFICACIÓN"), size=6.8)
para(a, "**Dos proyectos rompen el orden del puntaje.** PR-03, el almacén, es el problema que la empresa reconoce y puntúa "
        "3.65, pero empieza en abril de 2028: necesita el maestro de productos y ubicaciones que entrega PR-04. Y PR-11, el "
        "primero del puntaje, arranca en abril de 2027 porque el primer trimestre ya tiene dos proyectos, uno de ellos legal.")
para(a, "**Cronograma.** PR05_gantt.py convierte la hoja de ruta en el archivo de GanttProject: un grupo por ola, una tarea por "
        "proyecto, 2 enlaces fin-inicio (PR-04 → PR-03 y PR-04 → PR-08), 3 hitos de decisión y 2 hitos rojos de plazo normativo.")
figure(a, 2, "Hoja de ruta en tres olas, 2027–2029", G("PR_hoja_ruta.png"),
       "Nota. Elaboración propia con PR05_gantt.py a partir de PR05_hoja_ruta.csv. Es la vista del mismo cronograma que "
       "contiene PR05_hoja_ruta.gan.", width=16)
para(a, f"**Evidencia.** {F7}/PR05_hoja_ruta.csv · {F7}/PR05_hoja_ruta.gan · {FS}/PR04_hoja_ruta.txt")

# Paso D
para(a, "Paso D — Presupuesto plurianual y curva de OPEX", style="Heading 2")
para(a, "**Qué se buscaba.** Saber si el plan cabe en lo que la organización puede gastar cada año, y cuánto gasto fijo deja.")
para(a, "**Acción.** Se ejecutó PR06_presupuesto.py. La inversión se reparte en los meses de ejecución y el gasto operativo "
        "empieza el mes siguiente a la entrega.")
para(a, "**Primera ejecución: no cuadró.** La primera hoja de ruta incluía el canal de pedidos (PR-07) en 2029 y el ruteo "
        "(PR-08) en 2028. Respetaba dependencias y capacidad, pero excedía el techo dos años:")
code(a, salida("PR06_presupuesto_v1_no_cuadra.txt", hasta="TOTAL DEL PLAN"))
para(a, "**Corrección.** Se retiró PR-07 del horizonte y se movieron PR-08 y PR-14 a 2029. Segunda ejecución:")
code(a, salida("PR06_presupuesto.txt", hasta="=== ESCENARIO ALTERNO"), size=7.2)
table(a, ["Año", "CAPEX", "OPEX", "Gestión del cambio", "Contingencia", "Total", "Holgura", "Rango de incertidumbre"],
      [[r["año"], miles(r.capex), miles(r.opex), miles(r.gestion_cambio), miles(r.contingencia), f"**{miles(r.total)}**",
        miles(r.holgura), f"{miles(r.total_min)} a {miles(r.total_max)}"] for _, r in pres.iterrows()]
      + [["**Total**", f"**{miles(pres.capex.sum())}**", f"**{miles(pres.opex.sum())}**", f"**{miles(pres.gestion_cambio.sum())}**",
          f"**{miles(pres.contingencia.sum())}**", f"**{miles(pres.total.sum())}**", "", ""]],
      widths=[2.3, 1.7, 1.7, 2.0, 2.0, 1.8, 1.7, 3.4])
figure(a, 3, "Presupuesto por año y gasto operativo acumulado", G("PR_presupuesto.png"),
       "Nota. Elaboración propia con PR06_presupuesto.py. Cifras en miles de soles.", width=16)
para(a, "**Interpretación de la curva.** El gasto operativo pasa de S/ 14 183 en 2027 a S/ 95 570 en 2029, 6.7 veces más. Desde "
        "2030, sin aprobar ningún proyecto nuevo, el plan deja S/ 106 720 de gasto fijo al año: el 48 % del techo. Por eso "
        "PR-07 no cabe: agregarlo en 2029 llevaría ese año a S/ 325 329, S/ 103 329 sobre el techo.")
para(a, "**Lo que limita cada año.** En 2027 sobran S/ 52 624 pero los cuatro trimestres ya tienen dos proyectos: limita la "
        "capacidad. En 2028 y 2029 hay capacidad libre y limita el presupuesto.")
para(a, f"**Evidencia.** {F7}/PR06_presupuesto.csv · {BASE}/graficos/PR_presupuesto.png · {FS}/PR06_presupuesto.txt · "
        f"{FS}/PR06_presupuesto_v1_no_cuadra.txt")

# Paso E
para(a, "Paso E — Declarar lo que no se hará y redactar", style="Heading 2")
para(a, "**Qué se buscaba.** Escribir qué queda fuera, qué objetivo se deja sin cumplir, qué riesgo se asume y quién lo acepta.")
table(a, ["Proyecto", "Puntaje", "Cuadrante", "Objetivo que queda sin cumplir", "Riesgo que la organización asume", "Acepta el riesgo", "Fecha de revisión"],
      [list(r) for r in nsh.iloc[:, :7].itertuples(index=False)], widths=[2.6, 1.2, 1.9, 2.4, 4.8, 1.7, 2.2], size=7.5)
para(a, "PR-07 no es un sumidero: es una apuesta mayor que la gerencia comercial pide. Queda fuera por el gasto operativo "
        "acumulado, y el plan lo dice con la cifra. El riesgo de seguridad del portal actual sí se trata, con PR-06.")
para(a, "**Redacción.** Las secciones 7.2, 7.3 y 7.4 del PETI se redactaron con las subsecciones que pide la guía (7.2.1 a "
        "7.2.5, 7.3.1 a 7.3.4 y 7.4.1 a 7.4.4).")
para(a, f"**Evidencia.** {F7}/PR07_no_se_hara.csv · {F7}/7.2-7.4_priorizacion_hoja_ruta_presupuesto.md")

# Paso F
para(a, "Paso F — Validar y corregir", style="Heading 2")
para(a, "**Acción.** PR08_validacion.py ejecuta las tres comprobaciones de la guía y cuatro de coherencia entre archivos:")
code(a, "python PR08_validacion.py\n\n" + salida("PR08_validacion.txt"), size=6.6)
table(a, ["Comprobación", "Qué falló", "Qué se hizo"], [
    ["1. Pesos suman uno y están justificados", "Nada", "Suma 1.00; ocho criterios con su razón en los documentos del caso"],
    ["2. Ningún proyecto antes que su habilitador", "Nada", "0 dependencias rotas en la primera y en la segunda versión"],
    ["3. El presupuesto cuadra con la capacidad de gasto", "**Falló en la primera versión**: 2028 excedía el techo en S/ 85 498 y 2029 en S/ 22 542",
     "**Corregido**: PR-07 sale del horizonte y PR-08 y PR-14 pasan a 2029. Las dos versiones están en el historial de Git"],
], widths=[4.6, 5.4, 6.4])
para(a, f"**Evidencia.** {FS}/PR08_validacion.txt")

# Paso G
para(a, "Paso G — Registrar la evidencia y cerrar", style="Heading 2")
para(a, f"Se versionó el trabajo en la rama taller-14, paso por paso, y se fusionó a main con el Pull Request #1 ({PR_URL}). "
        f"Se crearon las etiquetas taller-14 ({TREE}) y v0.14 ({REPO}/tree/v0.14).")
code(a, 'git add . && git commit -m "S14: priorizacion, hoja de ruta y presupuesto — secciones 7.2 a 7.4"\n'
        'git tag -a v0.14 -m "PETI v0.14 — plan ejecutable"\n'
        'git tag -a taller-14 -m "Taller 14 · SI886"\ngit push origin taller-14 v0.14', size=8)
para(a, "La pregunta de transferencia se responde en la sección 5.")

# ---------------------------------------------------------------- 3. resultados
RES = [
    ["1", "Proyectos no negociables separados del modelo, con su norma y plazo", "Sí — 2 (PR-02 y PR-12)", f"{F7}/PR01_portafolio_marcado.csv"],
    ["2", "Pesos del modelo con justificación acordada con la gerencia, sumando 1", "Parcial — suman 1.00 y están justificados; falta el acta de la Entrevista 3", f"{F7}/PR02_pesos.md"],
    ["3", "Priorización calculada para todos los proyectos que compiten", "Sí — 12 proyectos", f"{F7}/PR03_priorizado.csv"],
    ["4", "Matriz esfuerzo-impacto con los cuatro cuadrantes poblados", "Sí — 4, 3, 3 y 2 proyectos", f"{BASE}/graficos/PR_esfuerzo_impacto.png"],
    ["5", "Proyectos del cuadrante ④ identificados como candidatos a no ejecutar", "Sí — PR-09 y PR-13", f"{FS}/PR03_priorizacion.txt"],
    ["6", "Niveles de dependencia calculados; cero dependencias rotas", "Sí — 3 niveles, 0 rotas", f"{FS}/PR04_hoja_ruta.txt"],
    ["7", "Hoja de ruta en tres olas con su fundamento", "Sí — 11 proyectos", f"{F7}/PR05_hoja_ruta.csv"],
    ["8", "Capacidad simultánea respetada en todos los trimestres", "Sí — máximo 2 en los 12 trimestres", f"{FS}/PR04_hoja_ruta.txt"],
    ["9", "Cronograma en GanttProject con dependencias, hitos de decisión y plazos normativos", "Parcial — archivo .gan generado y validado como XML; falta abrirlo en GanttProject y capturarlo", f"{F7}/PR05_hoja_ruta.gan"],
    ["10", "Presupuesto plurianual con CAPEX, OPEX, gestión del cambio y contingencia", "Sí — cuadra los tres años", f"{F7}/PR06_presupuesto.csv"],
    ["11", "Curva de OPEX acumulado graficada e interpretada", "Sí", f"{BASE}/graficos/PR_presupuesto.png"],
    ["12", "Tabla de lo que no se hará, con el riesgo asumido y su responsable", "Sí — 3 proyectos", f"{F7}/PR07_no_se_hara.csv"],
    ["13", "Secciones 7.2 a 7.4 redactadas · etiqueta v0.14", "Sí", f"{F7}/7.2-7.4_priorizacion_hoja_ruta_presupuesto.md · {REPO}/tree/v0.14"],
]
table(a_res, ["#", "Resultado esperado", "¿Se logró?", "Evidencia (GitHub)"], RES, widths=[0.8, 4.6, 3.6, 7.4], size=8)
t_res._tbl.getparent().remove(t_res._tbl)
a = find(doc, starts="Si algo no se logró")
set_text(a, f"Todo se verifica en la etiqueta del taller: {TREE} · Pull Request: {PR_URL}")
a4 = find(doc, exact="4. Conclusiones")
para(a4, "Problemas y mejoras", style="Heading 2")
bullets(a4, [
    "**Entrevista 3.** Con el banco de casos es simulada con el docente y todavía no se realizó. Los pesos y el techo de "
    "S/ 222 000 son la propuesta que el equipo lleva. Si cambian, se edita PR02_pesos.md y se vuelven a ejecutar los programas.",
    "**El techo frente a los documentos del caso.** presupuesto_ti.csv registra S/ 682 640 planificados en operación y solo "
    "S/ 59 360 en proyectos nuevos, de los que se ejecutaron S/ 39 242. Las tres inversiones de 2025 sumaron S/ 564 215, "
    "casi quince veces esa partida. Los documentos no dicen de dónde salieron: es la primera pregunta para la entrevista.",
    "**Cronograma en GanttProject.** El archivo .gan lo genera PR05_gantt.py y se comprobó que es XML bien formado, pero "
    "GanttProject no está instalado en el equipo donde se trabajó. Falta abrirlo, revisar que cargue como se espera y "
    "guardar la captura en evidencias/S14/.",
    "**Extremo alto del rango.** Con la incertidumbre de cada proyecto, 2028 puede llegar a S/ 255 398 y 2029 a S/ 233 875, "
    "sobre el techo. Se revisa en los hitos H1 y H2; la primera medida sería retirar PR-14 y desplazar PR-08.",
    "**Costos.** El portafolio y su costo se armaron en este taller con los programas de la Semana 13. Son estimaciones "
    "del equipo, sin cotizaciones.",
], numbered=True)

# ---------------------------------------------------------------- 4. conclusiones
set_text(find(doc, starts="Mínimo tres. Una conclusión"),
         "1. Priorizar fue decidir qué no se hace. De 14 proyectos quedaron fuera tres, y el más difícil de dejar fue el canal "
         "de pedidos móvil, que no es un sumidero. Decirlo con su cifra (S/ 103 329 sobre el techo) es lo que permite que la "
         "gerencia lo discuta en vez de descubrirlo en 2029.")
a = find(doc, exact="5. Cuestionario")
for t in [
    "2. El puntaje no dio el cronograma. El almacén puntúa 3.65 y es el problema que la empresa reconoce, pero empieza quince "
    "meses después porque depende del dato maestro. El proyecto de mayor puntaje arranca en el cuarto mes porque la capacidad "
    "del primer trimestre ya estaba tomada por una obligación legal.",
    "3. La primera hoja de ruta cumplía dependencias y capacidad y aun así no se podía pagar: 2028 excedía el techo en "
    "S/ 85 498. El error estaba en mirar solo la inversión. El gasto operativo acumulado es lo que más pesa al final: llega al "
    "43 % del techo en 2029 y deja el 48 % comprometido desde 2030.",
    "4. El historial de la organización cambió dos parámetros del modelo. Como ninguna inversión de 2025 midió su beneficio, "
    "el beneficio económico bajó a 0.10. Como las tres se desviaron entre +16.5 % y +30.4 %, la contingencia subió a 15 %.",
    "5. El límite no fue el mismo cada año. En 2027 sobra presupuesto y falta capacidad; en 2028 y 2029 sobra capacidad y "
    "falta presupuesto. Un plan que mire solo una de las dos restricciones falla en la otra.",
]:
    para(a, t)

# ---------------------------------------------------------------- 5. cuestionario
set_text(find(doc, starts="Copia cada pregunta"),
         "¿Qué riesgo correría una organización real si esto se hiciera mal?")
a = find(doc, exact="6. Referencias bibliográficas")
para(a, "Aprobaría el plan mirando solo la inversión y descubriría en el tercer año que el gasto operativo acumulado ya "
        "consume la mitad de su presupuesto, sin margen para lo que falta. Y si convirtiera el orden del puntaje en "
        "cronograma, construiría el almacén y el ruteo sobre un dato maestro que no cuadra, con sistemas entregados que nadie "
        "puede usar.")

# ---------------------------------------------------------------- 6. referencias
REFS = [
    "Project Management Institute. (2017). The Standard for Portfolio Management (4.ª ed.). PMI. https://www.pmi.org/",
    "International Organization for Standardization. (2021). ISO 21500:2021 Project, programme and portfolio management — Context and concepts. https://www.iso.org/standard/75704.html",
    "ISACA. (2018). COBIT 2019 Framework: Governance and Management Objectives (EDM02, APO05 y APO06). https://www.isaca.org/resources/cobit",
    "ISACA. (2008). Enterprise Value: Governance of IT Investments. The Val IT Framework 2.0. https://www.isaca.org/",
    "Congreso de la República del Perú. (2011). Ley 29733, Ley de Protección de Datos Personales.",
    "Ministerio de Justicia y Derechos Humanos. (2024). Decreto Supremo 016-2024-JUS, Reglamento de la Ley 29733.",
    "Rodríguez Bermúdez, J. R. (2015). Planificación y dirección estratégica de sistemas de información. Editorial UOC. https://elibro.net/es/lc/bibliotecaupt/titulos/57875",
    "González Millán, J. (2020). Manual práctico de planeación estratégica. Ediciones Díaz de Santos. https://elibro.net/es/lc/bibliotecaupt/titulos/129291",
    "Kotter, J. P. (2012). Leading change. Harvard Business Review Press.",
    "GanttProject. (s. f.). GanttProject user guide. https://www.ganttproject.biz/",
    "Jimenez Flores, O. J. (2026). SI-886 Planeamiento Estratégico de TI: Semana 14, banco de casos, EMPRESA-06. Universidad Privada de Tacna. https://github.com/OscarJimenezFlores/PETI",
]
set_text(find(doc, starts="Normas técnicas, marcos profesionales"), REFS[0])
a = find(doc, exact="7. Anexos")
for r in REFS[1:]:
    p = para(a, r, size=10.5)
    p.paragraph_format.left_indent = Cm(1.0); p.paragraph_format.first_line_indent = Cm(-1.0)

# ---------------------------------------------------------------- 7. anexos
AX = f"{BASE}/anexos"
ANEX = [
    f"Anexo A — Priorización completa, con las ocho calificaciones por proyecto. {AX}/anexo_A_priorizacion.xlsx",
    f"Anexo B — Matriz esfuerzo-impacto. {AX}/anexo_B_esfuerzo_impacto.png",
    f"Anexo C — Hoja de ruta: archivo de GanttProject y su vista. {AX}/anexo_C_hoja_ruta.gan · {AX}/anexo_C_hoja_ruta.png",
    f"Anexo D — Presupuesto plurianual, costo total de propiedad y hoja de ruta. {AX}/anexo_D_presupuesto.xlsx",
    f"Anexo E — Curva de gasto operativo acumulado. {AX}/anexo_E_curva_opex.png",
    f"Anexo F — Lo que no se hará. {AX}/anexo_F_no_se_hara.csv",
    f"Anexo G — Secciones 7.2 a 7.4 del PETI. {F7}/7.2-7.4_priorizacion_hoja_ruta_presupuesto.md",
    f"Anexo H — Documentos del caso EMPRESA-06 usados. {TREE}/caso/EMPRESA-06",
]
a7 = find(doc, starts="Capturas completas, archivos de configuración")
set_text(a7, ANEX[0])
last = a7
for t in ANEX[1:]:
    el = OxmlElement("w:p"); last._p.addnext(el)
    np_ = docx.text.paragraph.Paragraph(el, last._parent)
    set_font(np_.add_run(t), FONT, 11); last = np_

doc.save(OUT)
print("Guardado:", OUT)
