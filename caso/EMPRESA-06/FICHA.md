<div align="center">
  <img src="../../../Logos/logo_universidad.png" alt="Universidad Privada de Tacna" height="62">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="../../../Logos/logo_escuela_sistemas.jpeg" alt="Escuela Profesional de Ingeniería de Sistemas" height="62">
</div>

<p align="center">
  <strong>Universidad Privada de Tacna</strong><br>
  Facultad de Ingeniería · Escuela Profesional de Ingeniería de Sistemas
</p>

<h1 align="center">DISTRIBUIDORA ANDINA DEL SUR S.A.C.</h1>

<p align="center">
  Banco de casos · <strong>Empresa 06</strong> · Distribución mayorista de consumo masivo<br>
  <em>Organización ficticia. Cualquier parecido con una empresa real es coincidencia.</em>
</p>

---

## A. Ficha de la organización

| Campo | Contenido |
|---|---|
| **Razón social** | DISTRIBUIDORA ANDINA DEL SUR S.A.C. |
| **Sector** | Distribución mayorista de consumo masivo |
| **Domicilio fiscal** | Tacna, con almacenes en Tacna e Ilo |
| **RUC** | 20486XXXXX *(enmascarado; es una organización ficticia)* |
| **Años de operación** | 21 |
| **Personal en planilla** | 157 |
| **Personal adicional** | 34 en temporada alta |
| **Facturación / presupuesto anual** | S/ 68.4 millones |
| **Mercado o población atendida** | Tacna, Moquegua y frontera |
| **Naturaleza** | Empresa privada. |
| **Entidades que la regulan o supervisan** | SUNAT · INDECOPI · SUNAFIL · ANPD |

**Objetivo declarado para TI en el periodo.** Restablecer el control interno sobre el ciclo de compras y pagos y conciliar el inventario.

## B. Estructura y gobierno

| | |
|---|---|
| **Personal de TI** | 4 personas |
| **Responsable de TI** | Jefe de Sistemas, reporta a Gerencia de Administración y Finanzas |
| **Comité de TI o de gobierno digital** | Existe en el papel; no se ha reunido en el último año. |
| **Política de seguridad de la información** | Existe desde 2022, sin difusión ni revisión posterior. |
| **Presupuesto de TI del periodo** | S/ 742 000 · 1.08 % de la facturación |

> **Sin marco de gobierno digital obligatorio.** Al ser privada, las exigencias provienen de su regulador sectorial, de la Ley 29733 de protección de datos personales y de sus compromisos contractuales.

## C. Sistemas de información

| Sistema | Descripción | Dónde corre | Desde | ¿Tiene soporte vigente? |
|---|---|---|---|---|
| **ERP comercial** | Producto peruano con módulos de compras, ventas, almacén, tesorería y contabilidad | Servidor propio | 2015 | Sí |
| **Fuerza de ventas móvil** | App del proveedor del ERP | Nube del proveedor | 2020 | Sí |
| **Facturación electrónica** | OSE contratado | SaaS | 2018 | Sí |
| **Gestión de almacén** | Módulo del ERP más hojas de cálculo paralelas | Mixto | 2015 | Parcial |
| **Portal de pedidos para clientes** | Desarrollo propio | Hosting compartido | 2022 | No |

**El problema que la organización reconoce.** El módulo de almacén del ERP se dejó de usar para la gestión de ubicaciones y se sostiene en hojas de cálculo. El inventario contable y el físico difieren en promedio 4.7 %.

## D. Procesos de negocio

| N.º | Proceso | ¿Qué sistema lo soporta? |
|---|---|---|
| 1 | Compras a proveedores y reposición | ERP comercial |
| 2 | Almacenamiento y despacho | Gestión de almacén |
| 3 | Venta y distribución en ruta | Fuerza de ventas móvil |
| 4 | Cobranza y crédito a clientes | ERP comercial |
| 5 | Tesorería y pagos | ERP comercial |
| 6 | Contabilidad y cierre | ERP comercial |

## E. Instrumentos de planeamiento existentes

| Instrumento | ¿Existe? | Vigencia | Estado real |
|---|---|---|---|
| Plan estratégico o plan de negocio | Sí | 2023–2027 | Aprobado por resolución, se cumple parcialmente. |
| Plan operativo anual | Sí | 2025 | Se formula cada año para efectos presupuestales. |
| Plan Estratégico de Tecnologías de la Información (PETI) | **No** | — | **Nunca se ha formulado.** |
| Plan de transformación digital | No | — | No se ha formulado. |
| Política de seguridad de la información | Parcial | — | Existe desde 2022, sin difusión ni revisión posterior. |
| Plan de continuidad del negocio | No | — | No existe. El BIA de `datos/bia.csv` es un borrador incompleto elaborado por un practicante. |
| Catálogo de servicios de TI | No | — | Sin responsable asignado. |

## F. Situación de TI — hechos verificables para el diagnóstico

Son los hechos que la organización admite y que pueden darse por ciertos. Todo lo demás se pregunta en la entrevista.

| Aspecto | Situación verificada |
|---|---|
| **Registro de incidentes** | No se registra. Se resuelve y se olvida. |
| **Inventario de activos de TI** | Existe una hoja de cálculo actualizada por última vez hace dos años. |
| **Contraseñas** | No hay política escrita. La longitud mínima del sistema principal es de seis caracteres. |
| **Respaldos** | Se ejecutan a disco local y nunca se ha probado una restauración completa. |
| **Contratos con proveedores de TI** | Dos de los cinco contratos están vencidos y el servicio continúa. |
| **Segundo factor de autenticación** | Solo en el correo corporativo. |
| **Capacitación en seguridad** | Se hizo una charla de una hora en la inducción, hace tres años. |
| **Gestión de cambios** | Los cambios en producción se aplican directamente, sin registro ni aprobación. |

## G. El incidente del periodo

**Fraccionamiento de compras bajo el umbral de aprobación**

Una revisión interna detectó órdenes de compra fraccionadas sistemáticamente bajo el umbral de S/ 5 000 que exige aprobación de gerencia. El mismo usuario registraba y aprobaba. El ERP lo permitía por configuración de perfiles.

## H. Riesgos que la organización ya conoce y no ha tratado

| N.º | Riesgo conocido | ¿Tratado? |
|---|---|---|
| 1 | Segregación de funciones inexistente en compras y pagos | No |
| 2 | Inventario sin conciliación sistemática | No |
| 3 | Portal de clientes sin mantenimiento ni pruebas de seguridad | No |

## I. Datos entregados

Los siete archivos de `datos/` corresponden al periodo del 1 de enero al 31 de diciembre de 2025. Fueron generados con la semilla de esta empresa. **No coinciden con los de ningún otro equipo**.

| Archivo | Qué contiene | Registros |
|---|---|---|
| `pagos.csv` | Población de pagos del periodo — comprobante, fecha, proveedor, concepto, monto, quién registró y quién aprobó | 17 798 |
| `proveedores.csv` | Maestro de proveedores con su contacto y documento de identidad | 78 |
| `empleados.csv` | Planilla del periodo, con fechas de ingreso y cese | 157 |
| `usuarios_erp.csv` | Usuarios del ERP con su perfil, último acceso y estado | 114 |
| `bia.csv` | Análisis de impacto al negocio por proceso, con RTO, RPO y fecha de la última prueba | 6 |
| [`presupuesto_ti.csv`](presupuesto_ti.csv) | Presupuesto de TI del periodo por partida, planificado contra ejecutado | 7 |
| [`inversiones_cerradas.csv`](inversiones_cerradas.csv) | Tres inversiones cerradas con su beneficio declarado y si se midió | 3 |

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
