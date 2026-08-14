# WFP Port Scan Detection

## Problem

Los eventos WFP `5152`/`5157` llegaban al manager, pero inicialmente la regla custom no recibía los eventos reales. Después de corregir la ruta, un mismo escaneo generaba alertas repetidas.

## Evidence

- Windows Security EventChannel siguió `60000 -> 60001`.
- `60104` (AUDIT_FAILURE) era una hermana de nivel 5.
- Un escaneo de 15 puertos filtrados produjo 34 eventos WFP y 15 puertos de destino crudos distintos.

## Root cause

1. La base `100500` de nivel 1 quedaba eclipsada por `60104` de nivel 5.
2. WFP generó varios registros por puerto y la correlación Wazuh no mantiene un conjunto exacto de puertos únicos.

## Solution

- Base `100500`: nivel 6, `if_sid=60001`, filtros ATTACK/LAB y `no_log`.
- Correlaciones `100501` y `100502`: throttling `ignore=60`.
- El umbral `frequency=14` de `100502` es una compensación observada de la interacción entre reglas frequency hermanas; no es cardinalidad exacta.

## Validation

La prueba real produjo una alerta `100501` y una `100502`, sin alimentar el detector desde NAT o MANAGEMENT. La telemetría WFP permaneció disponible en archivos.

## Lesson learned

Validar contra EventChannel real y separar telemetría (`60104`) de veredicto de detección. Para el detalle forense y los límites, consulta [la regla WFP validada](../../detection-rules/WFP_PortScan_Detection_Final.md).
