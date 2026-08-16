# Informe final — cardinalidad WFP y Sysmon EID 3

Run: `20260815-195300`. No se publicaron claves, contraseñas ni transcripciones.

## Hallazgos confirmados

- Los 34 eventos reales del export CSV forman una sesión
  `192.168.56.1 -> 192.168.56.20`; hay **33 puertos únicos**. El evento 13 repite
  443.
- El evento 9 histórico es puerto 199 y deja cardinalidad 9; el evento 10 es
  puerto 256 y deja cardinalidad 10. Por ello la afirmación “evento 9 produjo
  100501 y evento 10 produjo 100502” no está respaldada por los datos.
- Las reglas activas tenían `100501 frequency=10` y `100502 frequency=14`, con
  `timeframe=60`, `same_field=sourceAddress` y
  `different_field=destPort`.
- En el test real de 20 puertos, `100501` apareció en el décimo puerto distinto
  observado (puerto 7) y `100502` en el decimoquinto (puerto 12). Ambos eventos
  fueron WFP 5152 ATTACK/LAB. La diferencia entre `frequency=14` y el evento 15
  es la semántica observable de esta versión; se documenta con evidencia, no se
  infiere como un conteo SQL.

## Cambio aplicado y validado

Se sustituyó en `100409` el dependencia de `<if_group>sysmon_event3</if_group>`
por predicados explícitos de proveedor Sysmon, canal, Event ID 3, TCP, origen
ATTACK/LAB y destino endpoint. Así no se relaja ninguna exclusión NAT o
Management. Se hicieron backups con SHA-256, wrapper XML válido y
`wazuh-analysisd -t` RC 0 sin WARNING/ERROR/CRITICAL antes del reinicio.

Un logtest de 15 eventos Sysmon distintos dispara `100420` en el décimo. Un
Sysmon EID 3 real fue generado por `nmap -sT -p 22 192.168.56.20` desde
ATTACK/LAB; llegó con `sourceIp=192.168.56.1`, destino `.56.20`, TCP e
`Initiated=false`. No se generaron diez conexiones exitosas distintas porque no
se modificó el endpoint fuera de las pruebas Nmap autorizadas.

## Cardinalidad exacta

`different_field` rechazó un duplicado consecutivo y uno no consecutivo en las
pruebas de logtest incluidas. Aun así, la regla nativa no ofrece un conjunto
persistido/auditable ni un contrato de `COUNT(DISTINCT)` independiente de la
versión. La propuesta A usa `session_id` enriquecido y conserva Wazuh; la B usa
SQLite y es la recomendada cuando “exacta” es un requisito de control, no solo de
alerta. Véase `proposal_cardinality.md`.

## Artefactos y reproducción

- Parser: `tools/parse_cardinality.py`.
- Fixtures: `tools/generate_logtest_events.py`.
- Builder validado: `tools/build_cardinality_candidate.py`.
- Secuencia: `run-20260815-195300/cardinality/sequence_unique_ports.csv`.
- Evidencia de producción: `run-20260815-195300/production_test/`.

```bash
python3 tools/parse_cardinality.py INPUT.csv --output evidence/cardinality/run-X/cardinality --limit 34
python3 tools/generate_logtest_events.py --kind sysmon --count 15 | ssh wazuh 'sudo /var/ossec/bin/wazuh-logtest'
nmap -Pn -sS --min-rate 100 --max-retries 0 -T4 -p 1-20 192.168.56.20
```

La rama/publicación se decidirá tras la revisión final de los artefactos curados;
no se incluye la salida raw que contenía atributos personales del endpoint.
