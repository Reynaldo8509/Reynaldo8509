# Cardinalidad WFP y Sysmon — run 20260815-205438

## Decisión

**PASS operativo.** El ruleset activo validó con `xmllint` (wrapper temporal)
y `wazuh-analysisd -t`; el escaneo autorizado ATTACK/LAB produjo `100501` en
el décimo puerto distinto y `100502` en el decimoquinto. No se modificó el
ruleset durante este run: la candidata/corrección Sysmon ya activa se preservó.

## Reconstrucción histórica

El fixture CSV de 34 eventos, filtrado por `192.168.56.1 → 192.168.56.20`,
contiene 33 puertos únicos. El orden y los conteos se encuentran en
[sequence_unique_ports.csv](cardinality/sequence_unique_ports.csv).

| Evento | Puerto | Puertos únicos acumulados | Regla del CSV |
|---:|---:|---:|---:|
| 9 | 199 | 9 | 100509 |
| 10 | 256 | 10 | 100509 |
| 13 | 443 (repetido) | 12 | 100509 |

Las filas históricas tienen `rule.id=100509`, no `100501`/`100502`; por ello
no prueban que “evento 9 produjo 100501” ni que “evento 10 produjo 100502”.
Prueban cardinalidad 9 y 10, respectivamente. El detalle reproducible está en
[cardinality_report.txt](cardinality/cardinality_report.txt).

## Prueba real ATTACK/LAB

Se ejecutó `nmap -Pn -sS --min-rate 100 --max-retries 0 -T4 -p 1-20
192.168.56.20` desde la interfaz local `192.168.56.1`. Los 20 WFP EID 5152
fueron exportados sanitizados. El orden real fue:

| Evento | Puerto | Cardinalidad | Regla final |
|---:|---:|---:|---:|
| 9 | 2 | 9 | 100500 |
| 10 | 15 | 10 | 100501 |
| 14 | 6 | 14 | 100500 |
| 15 | 1 | 15 | 100502 |

Evidencia: [current_event_order.txt](current_event_order.txt),
[current_attack_events_sanitized.jsonl](current_attack_events_sanitized.jsonl)
y [current_alerts_sanitized.jsonl](current_alerts_sanitized.jsonl).

`100501` usa `frequency=10`, `timeframe=60`, `if_matched_sid=100500`,
`same_field=sourceAddress` y `different_field=destPort`. `100502` comparte el
antecedente y usa `frequency=14`; en esta versión el evento actual completa el
cruce observado de 15. El campo `firedtimes=2` que aparece en las alertas es
el número acumulado de emisiones de esa regla, no la cardinalidad del lote
actual.

## Sysmon y límites de la correlación

El replay local de 15 puertos Sysmon alcanzó `100420` en el décimo puerto.
La conexión TCP autorizada ATTACK→SSH generó Sysmon EID 3 real y fue detectada
por `100004`, regla directa y más específica para puerto 22. La corrección de
`100409` continúa filtrando proveedor Sysmon, canal operativo, EID 3, TCP,
origen `192.168.56.0/24` y destino `192.168.56.20`.

La configuración actual ofrece el comportamiento operativo validado, pero no
expone un conjunto persistente de puertos. Dos reglas hermanas con el mismo
`if_matched_sid` no constituyen una garantía formal de `COUNT(DISTINCT)`. La
propuesta para exactitud se documenta en [proposal_cardinality.md](proposal_cardinality.md).

## Validación y seguridad

- Backup remoto/local SHA-256: [backup_ruleset.txt](backup_ruleset.txt).
- XML: [xmllint_candidate.txt](xmllint_candidate.txt).
- Análisis: [analysisd_candidate_test.txt](analysisd_candidate_test.txt).
- Nmap: [nmap_1-20.txt](nmap_1-20.txt).
- Acciones y comandos sanitizados: [actions.log](actions.log).

Las IPs mostradas son exclusivamente del laboratorio autorizado; no se
incluyeron contraseñas, llaves ni artefactos privados.
