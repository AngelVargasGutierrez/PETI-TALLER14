# -*- coding: utf-8 -*-
"""Parámetros y utilidades compartidos por los programas PR03 a PR08.
Los parámetros repiten lo fijado en PR02_pesos.md antes de calcular."""
import re
from pathlib import Path
import pandas as pd

AQUI = Path(__file__).parent
RAIZ = AQUI.parent
GRAFICOS = RAIZ / "graficos"

CLAVES = ["contribucion", "beneficio", "urgencia", "habilitacion",
          "riesgo_no_hacer", "facilidad", "aceptacion", "social_ambiental"]

UMBRAL_IMPACTO = 3.5
UMBRAL_ESFUERZO = 3.5
CAPACIDAD_SIMULTANEA = 2        # proyectos activos por trimestre · equipo de TI de 4 personas
PRESUPUESTO_ANUAL = 222_000     # S/ · 742 000 del presupuesto de TI menos 520 000 comprometidos en operación
CAMBIO_PCT = 0.10
CONTINGENCIA_PCT = 0.15
ANIO_BASE = 2027
HORIZONTE_MESES = 36
AREAS_INTERNAS = {"Sistemas"}   # un proyecto transversal solo puede coincidir con uno de estas áreas

DEP = [  # (proyecto, depende_de) — mapa de dependencias del portafolio (Sección 7.1.7)
    ("PR-03", "PR-04"),                     # el almacén necesita el maestro de productos y ubicaciones
    ("PR-07", "PR-04"), ("PR-07", "PR-03"), # el canal muestra stock y precios: maestro limpio e inventario conciliado
    ("PR-08", "PR-04"),                     # el ruteo necesita el maestro de clientes con dirección única
    ("PR-09", "PR-04"), ("PR-09", "PR-03"), # la analítica de demanda necesita ventas e inventario confiables
]

# Paleta (validada para daltonismo) y tinta
AZUL, NARANJA, AQUA, AMARILLO = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
CRITICO = "#d03b3b"
TINTA, TINTA2, MUDO, GRILLA, EJE, FONDO = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"


def leer_pesos():
    """Lee la tabla de pesos de PR02_pesos.md. Devuelve [(clave, criterio, peso, justificacion)]."""
    filas, en_tabla = [], False
    for linea in (AQUI / "PR02_pesos.md").read_text(encoding="utf-8").splitlines():
        if linea.startswith("## "):
            en_tabla = linea.strip() == "## Pesos"
            continue
        if not en_tabla or not linea.startswith("|"):
            continue
        c = [x.strip() for x in linea.strip().strip("|").split("|")]
        if len(c) >= 4 and re.fullmatch(r"\d\.\d+", c[1]):
            filas.append((c[0], float(c[1]), c[3]))
    if len(filas) != len(CLAVES):
        raise SystemExit(f"PR02_pesos.md debe tener {len(CLAVES)} criterios; tiene {len(filas)}")
    return [(k, n, p, j) for k, (n, p, j) in zip(CLAVES, filas)]


def mes(aaaamm):
    """'2027-04' -> 4 (mes 1 = enero del año base)."""
    a, m = str(aaaamm).split("-")[:2]
    return (int(a) - ANIO_BASE) * 12 + int(m)


def leer_hoja_ruta(ruta=None):
    hr = pd.read_csv(ruta or AQUI / "PR05_hoja_ruta.csv", dtype=str).fillna("")
    hr["codigo"] = hr["Proyecto"].str.extract(r"(PR-\d+)")
    hr["m_ini"] = hr["Inicio"].map(mes)
    hr["m_fin"] = hr["Fin"].map(mes)
    hr["ola"] = hr["Ola"].str[:5]
    hr["area"] = hr["Área usuaria afectada"]
    return hr


def estilo_ejes(ax):
    ax.set_facecolor(FONDO)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(EJE)
    ax.tick_params(colors=MUDO, labelsize=9)
    ax.grid(True, color=GRILLA, linewidth=0.8)
    ax.set_axisbelow(True)
