# PR02 · Pesos del modelo de priorización

**Organización** · Distribuidora Andina del Sur S.A.C. (EMPRESA-06 del banco de casos)
**Regla** · Los pesos, los umbrales y las restricciones de este archivo se fijan **antes** de calcular.
`PR03_priorizacion.py` lee los pesos de la tabla de abajo; no los tiene escritos en el código.
La prueba de que se fijaron antes es el historial de Git: este archivo se versionó en un commit
anterior al de `PR03_priorizado.csv`.

## Pesos

| Criterio | Peso | Escala 1–5 | Justificación (origen en el diagnóstico) |
|---|---|---|---|
| Contribución a los objetivos | 0.25 | 1 = tributa a un objetivo de bajo peso · 5 = tributa a dos o más objetivos de alto peso | El objetivo declarado de TI del periodo es restablecer el control interno en compras y pagos y conciliar el inventario (FICHA, sección A). El plan de negocio 2023–2027 «se cumple parcialmente» (sección E): lo que no tributa a un objetivo no se sostiene |
| Beneficio económico | 0.10 | Según el beneficio neto estimado a 5 años | Se reduce frente al 0.20 de referencia del curso. Las tres inversiones cerradas de 2025 declararon un beneficio y **en ninguna se midió** (expedientes de inversión): el beneficio estimado es hoy el dato menos confiable de la organización. Los 0.10 liberados pasan al criterio social y ambiental |
| Urgencia | 0.15 | 1 = sin plazo · 5 = plazo legal o técnico vencido o inminente | Hay un incidente abierto de fraccionamiento de compras (sección G), un portal de pedidos sin soporte (sección C) y dos de cinco contratos de TI vencidos (sección F) |
| Habilitación | 0.15 | Número de proyectos que desbloquea | Cuatro proyectos de valor dependen del dato maestro (ver dependencias en `comun.py`) |
| Riesgo de no hacerlo | 0.10 | Probabilidad × impacto del escenario de inacción | Tres riesgos conocidos y no tratados (sección H) y respaldos que nunca se han restaurado (sección F) |
| Facilidad de ejecución | 0.10 | 5 = bajo esfuerzo y capacidad interna disponible · 1 = alto esfuerzo, capacidad ausente | **Equipo de TI de 4 personas** (sección B). La partida «Proyectos nuevos» se ejecutó al 66 % en 2025 (`presupuesto_ti.csv`, PT06): la capacidad es la restricción real |
| Aceptación organizacional | 0.05 | Según el perfil cultural y los interesados | Los cambios en producción se aplican sin registro ni aprobación (sección F): la organización acepta poco control nuevo a la vez |
| Impacto social y ambiental | 0.10 | 5 = beneficia a clientes o trabajadores, o reduce combustible, papel o residuos · 1 = genera impacto negativo | **Criterio obligatorio, peso no menor al 10 %.** La empresa mueve mercadería por carretera en Tacna, Moquegua y la frontera, y atiende a bodegas pequeñas |

**Suma de pesos: 1.00**

## Umbrales de la matriz esfuerzo-impacto

Se usan los del programa del curso, sin cambios.

| Eje | Fórmula | Umbral |
|---|---|---|
| Impacto | 0.5 × contribución + 0.3 × beneficio + 0.2 × riesgo de no hacerlo | Alto si ≥ 3.5 |
| Esfuerzo | 6 − facilidad de ejecución | Alto si ≥ 3.5 |

## Restricciones de la hoja de ruta y del presupuesto

| Restricción | Valor | Fundamento |
|---|---|---|
| Capacidad simultánea | Máximo **2 proyectos** activos por trimestre | Equipo de 4 personas que además opera. El ejemplo del curso asigna 3 proyectos a un equipo de 5 |
| Absorción del cambio | Nunca dos proyectos sobre la **misma área usuaria** en el mismo trimestre. Un proyecto transversal solo puede coincidir con uno interno de Sistemas | Sección 2.4 y hechos de la sección F |
| Techo anual del portafolio | **S/ 222 000** por año | Presupuesto de TI de S/ 742 000 menos S/ 520 000 comprometidos en operación (cifra del caso en la sesión de teoría de la Semana 14) |
| Gestión del cambio | 10 % de la inversión | Rango de referencia 8–12 % |
| Contingencia | **15 %** del subtotal anual | Tope del rango 10–15 %: las tres inversiones de 2025 se desviaron +30.4 %, +20.5 % y +16.5 % |
| Rango de incertidumbre | El de cada proyecto en `PF02_tco.csv` (±15 % a ±50 %) | Estimaciones sin cotización |

## Lo que queda por confirmar en la Entrevista 3

Con el banco de casos, la Entrevista 3 con la gerencia es simulada con el docente. **Aún no existe
acta de esa entrevista**: estos pesos y el techo son la propuesta que el equipo lleva a ella. Lo
que este archivo sí garantiza es el orden, porque se versionó antes de calcular.

Preguntas que el equipo lleva a la entrevista, porque los documentos del caso no las responden:

1. **¿El techo es S/ 222 000 o es menor?** `presupuesto_ti.csv` muestra S/ 682 640 planificados
   en operación y solo S/ 59 360 en «Proyectos nuevos», de los que se ejecutaron S/ 39 242. Con
   esas cifras, S/ 222 000 al año exige que la gerencia reasigne presupuesto o lo amplíe.
2. **¿De qué partida salieron las tres inversiones de 2025?** Sumaron S/ 564 215 ejecutados, casi
   quince veces la partida «Proyectos nuevos» de ese año. Si existe un presupuesto de inversión
   aparte, el techo del portafolio debe fijarse sobre él.
3. **¿Quién firma la aceptación del riesgo de los proyectos que no se harán?** (`PR07_no_se_hara.csv`).

Si la entrevista cambia un peso o el techo, se edita esta tabla y se vuelven a ejecutar `PR03`,
`PR04`, `PR06` y `PR08`. Ningún otro archivo guarda los pesos.
