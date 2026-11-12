# PETI-TALLER14

Repositorio del **Taller de laboratorio 14** del curso **SI-886 Planeamiento Estratégico de TI**
(Universidad Privada de Tacna): *Priorización multicriterio, hoja de ruta y presupuesto plurianual*.

**Autor** · Vargas Gutierrez, Angel · 2020066922
**Docente** · Dr. Oscar Juan Jimenez Flores
**Organización** · Distribuidora Andina del Sur S.A.C. — EMPRESA-06 del banco de casos del curso
(organización ficticia). Sus documentos están en `caso/EMPRESA-06/`.

## Resultado

- De **14 proyectos**, 2 son no negociables (protección de datos personales) y 12 compiten.
- El plan ejecuta **11 proyectos en tres olas** (2027–2029) y **deja fuera 3**, con su riesgo y su
  responsable: el cambio de ERP, la analítica de demanda y el canal de pedidos móvil.
- El presupuesto cuadra con el techo de S/ 222 000 los tres años: S/ 169 376, S/ 208 024 y S/ 203 516.
- El gasto operativo se multiplica por 6.7 en tres años y deja S/ 106 720 fijos al año desde 2030
  (48 % del techo).

La primera hoja de ruta respetaba dependencias y capacidad, pero excedía el techo en 2028 y 2029.
Las dos versiones están en el historial de commits.

## Contenido

| Archivo | Qué es |
|---|---|
| `07_portafolio/PF01_consolidacion.py`, `PF02_tco.py` | Insumos de la Semana 13: portafolio candidato y costo total de propiedad |
| `07_portafolio/PR01_no_negociables.py` → `PR01_portafolio_marcado.csv` | Separa los proyectos que impone una norma |
| `07_portafolio/PR02_pesos.md` | Pesos, umbrales, capacidad y techo, fijados antes de calcular |
| `07_portafolio/PR03_priorizacion.py` → `PR03_priorizado.csv` | Modelo multicriterio y matriz esfuerzo-impacto |
| `07_portafolio/PR04_hoja_ruta.py` | Niveles de dependencia, propuesta de olas y verificación de la hoja de ruta |
| `07_portafolio/PR05_hoja_ruta.csv`, `PR05_gantt.py`, `PR05_hoja_ruta.gan` | Hoja de ruta y su cronograma para GanttProject |
| `07_portafolio/PR06_presupuesto.py` → `PR06_presupuesto.csv` | Presupuesto plurianual y curva de gasto operativo |
| `07_portafolio/PR07_no_se_hara.csv` | Lo que no se hará, el riesgo asumido y quién lo acepta |
| `07_portafolio/PR08_validacion.py` | Las tres comprobaciones del Paso F y cuatro de coherencia |
| `07_portafolio/7.2-7.4_priorizacion_hoja_ruta_presupuesto.md` | **Secciones 7.2 a 7.4 del PETI** |
| `graficos/` | Matriz esfuerzo-impacto, hoja de ruta y presupuesto |
| `evidencias/S14/salidas/` | Salida literal de cada programa |
| `anexos/` | Anexos A a F del informe |
| `SI886-S14-TALLER-Grupo1.pdf` | Informe de laboratorio |

## Reproducir

```bash
cd 07_portafolio
python PF01_consolidacion.py && python PF02_tco.py
python PR01_no_negociables.py
python PR03_priorizacion.py
python PR04_hoja_ruta.py
python PR05_gantt.py
python PR06_presupuesto.py
python PR08_validacion.py
cd .. && python informe_build/build_taller14.py
```

Requiere Python 3.11 o superior con `pandas`, `matplotlib`, `networkx`, `openpyxl` y `python-docx`.

## Pendiente

- La Entrevista 3 con la gerencia, simulada con el docente, aún no se realizó: los pesos y el techo
  son la propuesta del equipo.
- `PR05_hoja_ruta.gan` se generó por programa. Falta abrirlo en GanttProject y guardar la captura
  en `evidencias/S14/`.
- Los costos son estimaciones del equipo, sin cotizaciones.
