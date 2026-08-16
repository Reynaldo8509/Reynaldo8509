# Informe final de cardinalidad — run 20260815-202149

## Resultado ejecutivo

La configuración activa pasó la validación XML (mediante un wrapper, porque
`local_rules.xml` contiene varios fragmentos `<group>`) y
`wazuh-analysisd -t` terminó con RC 0 sin `WARNING`, `ERROR` ni `CRITICAL`.
El servicio `wazuh-manager` se reinició y quedó `active`.

La corrección mínima ya instalada para Sysmon EID 3 se conservó sin cambios:
la regla base `100409` identifica explícitamente proveedor Sysmon, canal,
EID 3, TCP, origen ATTACK y destino Windows. La candidata generada en este
run fue idéntica al archivo activo (SHA-256
`771b23f687cd2fad835da19d366947f72fcb784bfeefbcb313eabc91eaca4eca`), por lo
que no hubo una segunda sustitución innecesaria.

El escaneo autorizado de 20 puertos desde `192.168.56.1` hacia
`192.168.56.20` produjo 20 eventos WFP y alertas `100501` y `100502`. La
conexión TCP autorizada a SSH produjo un Sysmon EID 3 real y fue detectada por
la regla específica `100004`; esa regla es intencionadamente más específica
para ATTACK/LAB hacia el puerto 22.

## Reconstrucción de los 34 eventos históricos

Entrada: exportación CSV local `events-2026-08-13T17_25_14.105Z.csv`, filtrada
por origen `192.168.56.1`, destino `192.168.56.20`, ordenada por marca de
tiempo y limitada a 34 filas. La exportación no es un volcado de
`archives.json`; sus filas reportan la regla histórica `100509`. Por tanto no
prueba un `firedtimes` de los correladores actuales.

La secuencia fue:

```
143, 993, 110, 111, 995, 587, 21, 23, 199, 256, 554, 443,
443 (repetido), 25, 113, 53, 80, 889, 419, 485, 622, 268, 286,
321, 679, 226, 173, 184, 811, 773, 266, 436, 74, 787
```

Hay 33 puertos distintos. El evento 9 es `199`, con cardinalidad 9; el evento
10 es `256`, con cardinalidad 10. El evento 13 vuelve a usar `443`, por lo que
mantiene cardinalidad 12. Las filas completas y la clasificación por evento
están en [sequence_unique_ports.csv](cardinality/sequence_unique_ports.csv) y
[cardinality_report.txt](cardinality/cardinality_report.txt).

### Aclaración sobre «evento 9 → 100501; evento 10 → 100502»

Esa afirmación no está respaldada por los 34 datos exportados ni por las
reglas activas. Las filas 9 y 10 llevan `rule.id=100509`, no `100501` ni
`100502`. Además, el XML activo establece:

```xml
<rule id="100501" level="10" frequency="10" timeframe="60" ignore="60">
  <if_matched_sid>100500</if_matched_sid>
  <same_field>win.eventdata.sourceAddress</same_field>
  <different_field>win.eventdata.destPort</different_field>
</rule>
<rule id="100502" level="13" frequency="14" timeframe="60" ignore="60">
  <if_matched_sid>100500</if_matched_sid>
  <same_field>win.eventdata.sourceAddress</same_field>
  <different_field>win.eventdata.destPort</different_field>
</rule>
```

El replay y la prueba real demuestran que `different_field` descarta los
reintentos del mismo puerto en esta versión. Sin embargo, dos correladores
hermanos que comparten `if_matched_sid=100500` comparten efectos del estado de
correlación: el motor no ofrece un conjunto de puertos ni un contador de
cardinalidad auditable. Por eso `frequency=14` es una compensación observada
para la alerta número 15, no una garantía declarativa de `COUNT(DISTINCT)`.

En el escaneo de producción actual, `100501` se emitió en el décimo puerto
distinto (puerto 20) y `100502` en el decimoquinto (puerto 6). Véase
[current_attack_events_sanitized.jsonl](production_test/current_attack_events_sanitized.jsonl)
y [current_relevant_alerts_sanitized.jsonl](production_test/current_relevant_alerts_sanitized.jsonl).

## Sysmon EID 3 y exclusiones

La regla base `100409` conserva estas condiciones: proveedor
`Microsoft-Windows-Sysmon`, canal `Microsoft-Windows-Sysmon/Operational`, EID
`3`, `protocol=tcp`, origen `192.168.56.0/24` y destino `192.168.56.20`.

Un `nmap -sT -p 22` autorizado generó EID 3 real con origen ATTACK. El evento
final fue `100004`, regla directa para SSH desde Kali; su mayor especificidad
prevalece sobre la base silenciosa `100409`, pero conserva el alcance requerido
y confirma detección. El registro sanitizado está en
[sysmon_eid3_sanitized.jsonl](production_test/sysmon_eid3_sanitized.jsonl).

Los replays de una IP de Management (`192.168.57.1`) y una NAT (`10.0.2.2`) no
produjeron `100409`, `100420` ni `100421`; evidencia:
[logtest_sysmon_exclusion_hits.txt](logtest_sysmon_exclusion_hits.txt).

## Arquitectura para cardinalidad exacta

### A. Correlación Wazuh enriquecida

Un enriquecedor previo debe emitir un campo explícito y estable, por ejemplo
`session_id=source|destination|protocol|bucket_utc_60s`. La base sigue filtrando
ATTACK/LAB y ambos umbrales se acotan con ese campo:

```xml
<rule id="100500" level="1">
  <!-- WFP EID 5152/5157, TCP, source 192.168.56.0/24, dest .56.20 -->
  <options>no_log</options>
</rule>
<rule id="100501" level="10" frequency="10" timeframe="60">
  <if_matched_sid>100500</if_matched_sid>
  <same_field>session_id</same_field>
  <different_field>win.eventdata.destPort</different_field>
</rule>
```

Pros: permanece en Wazuh y limita NAT/Management desde la base. Contras: debe
validarse por versión que los dos umbrales no interfieran; el motor sigue sin
exponer el conjunto persistente. No se aplicó.

### B. Agregador SQLite local — recomendado

Consumir solamente eventos ya filtrados ATTACK/LAB e insertar en SQLite una
clave única `(bucket, source, destination, protocol, dest_port)`. El proceso
emite un evento Wazuh al cruzar 10 y 15, guardando `emitted_10` y `emitted_15`
por sesión. Así se implementa `COUNT(DISTINCT dest_port)` real y ambos umbrales
son independientes y auditables. Requiere un nuevo componente, monitoreo y
retención; no se instaló en este run.

## Comandos reproducibles

```bash
python3 tools/parse_cardinality.py INPUT.csv --output evidence/cardinality/run-STAMP/cardinality \
  --limit 34 --source 192.168.56.1 --destination 192.168.56.20
python3 tools/generate_logtest_events.py --kind sysmon --ports 21,22,23,24,25,26,27,28,29,30
# En el manager, con privilegios:
/var/ossec/bin/wazuh-logtest -v < fixture.jsonl
nmap -Pn -sS --min-rate 100 --max-retries 0 -T4 -p 1-20 192.168.56.20
```

## Artefactos y decisión

- Backup y hashes: [backup_ruleset.txt](backup_ruleset.txt).
- Bitácora: [actions.log](actions.log).
- Reglas extraídas: [rules_relevant.xml](rules_relevant.xml).
- Validaciones: [xmllint_candidate.txt](xmllint_candidate.txt) y
  [analysisd_candidate_test.txt](analysisd_candidate_test.txt).
- Prueba WFP: [nmap_1-20.txt](production_test/nmap_1-20.txt).

La corrección Sysmon mínima y la detección WFP se validaron positivamente. No
conviene optimizar más reglas hermanas para afirmar cardinalidad exacta: la
alternativa B es la vía segura si se necesita esa propiedad formal.

## Publicación

El commit local de este run pasó la revisión de secretos. La publicación no se
completó porque `origin` respondió `Repository not found` al consultar
`origin/main`. No se modificó la URL remota ni se hizo push a otro destino; la
salida está en [git_ls_remote.txt](git_ls_remote.txt).
