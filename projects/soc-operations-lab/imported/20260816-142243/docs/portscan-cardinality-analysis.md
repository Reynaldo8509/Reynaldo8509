# Análisis de cardinalidad: Port Scan WFP / Sysmon EID 3

Fecha de inventario: 2026-08-15. Alcance: solo laboratorio local. No se modificó `/var/ossec`, no se reinició Wazuh y no se hizo commit ni push.

## Estado verificable

| Comprobación | Resultado |
|---|---|
| Repositorio | `main`, HEAD `e8af044 docs: add curated SOC lab evidence screenshots` |
| Backups Git | Los tres backups pasan `git fsck --no-reflogs` (exit 0) |
| Manager SSH | **FAIL**: `No route to host` a `192.168.57.10:22`; no se intentó ruta, host ni red alternativos |
| XML, `analysisd -t`, `ossec.log`, reglas y `archives.json` | No verificables/exportables por el fallo SSH |

Las salidas completas se preservan en `evidence/sysmon-eid3-test/`, incluidos los cuatro intentos SSH.

## Fuente y secuencia reconstruida

La ruta indicada `/mnt/data/events-2026-08-13T17_25_14.105Z.csv` no existe. Se encontró una exportación homónima recuperable en `/home/reyam/.local/share/Trash/files/`; contiene 10.000 filas, no 34. Se seleccionaron los primeros 34 eventos cronológicos WFP de `192.168.56.1` a `192.168.56.20` con puerto destino. No se afirma que sean una exportación de `archives.json`.

Ventana: `2026-08-12T22:54:47.865` a `22:54:48.438` (573 ms). Son 34 eventos y 33 puertos únicos. Todos salvo el evento 13 (Event ID `5157`) son `5152`; el 13 repite el puerto `443`.

| Evento | Puerto(s) | Nuevo | Cardinalidad |
|---:|---|:---:|---:|
| 1–8 | 143, 993, 110, 111, 995, 587, 21, 23 | sí | 1–8 |
| 9 | 199 | sí | 9 |
| 10 | 256 | sí | 10 |
| 11–12 | 554, 443 | sí | 11–12 |
| 13 | 443 (5157) | no | 12 |
| 14–16 | 25, 113, 53 | sí | 13–15 |
| 17–34 | 80, 889, 419, 485, 622, 268, 286, 321, 679, 226, 173, 184, 811, 773, 266, 436, 74, 787 | sí | 16–33 |

El décimo puerto único es `256`, en el evento 10. El detalle está en `evidence/sysmon-eid3-test/29-selected-34-summary.txt`. `artifacts/events-34.json` conserva la selección como `NOT_ARCHIVE_RAW`; `raw_event` es `null` hasta exportar los originales del manager.

## Contador compartido y cardinalidad

El historial local describe `100500` como base WFP y `100501`/`100502` como correladores de umbral que comparten `if_matched_sid=100500`. Las pruebas históricas dicen: 10 puertos ATTACK disparan `100501`; 15 disparan `100501` pero no `100502`; aislando `100502`, este sí dispara. El primer correlador consume/reinicia el estado compartido.

`frequency` cuenta coincidencias en un `timeframe`; el evento que completa el umbral también cuenta. Una traza puede mostrar nueve antecedentes y la alerta en el décimo evento entrante. Esto no demuestra `COUNT(DISTINCT destPort)`: el evento 13 repite `443` y prueba que eventos y puertos distintos no son equivalentes.

No fue posible confirmar el supuesto “100501 en el evento 9 / 100502 en el 10” con el XML activo. El historial disponible describe 10/15, no 9/10; la diferencia es compatible con “antecedentes previos + evento actual”, pero requiere `wazuh-logtest -v` con reglas activas antes de cambiar nada. El extracto está en `evidence/sysmon-eid3-test/27-counter-history-extracts.txt`; no hay `firedtimes` ni `ossec.log` actuales por el fallo SSH.

## Arquitectura final propuesta

No conviene optimizar más la correlación nativa si el requisito es cardinalidad exacta. Mantenerla como heurística es razonable, pero no debe llamarse “puertos únicos”.

1. Mantener reglas de admisión WFP y Sysmon EID 3 separadas, nivel 1 y `no_log`, solo TCP `^192\\.168\\.56\\.` hacia `192.168.56.20`; excluir explícitamente `192.168.57.` y `10.0.2.`.
2. Usar un correlador local con estado: clave `(telemetría, agente, sourceIp, destinationIp, protocol)`, TTL de 60 s y conjunto de `destPort`.
3. Emitir marcas independientes al cruzar exactamente 10 y 15 (`emitted_10`, `emitted_15`); Wazuh las decodifica y alerta como `100501` y `100502`.
4. Conservar la alerta por sonda solo para forense. Dos helper rules `no_log` separan contadores, pero siguen siendo heurística y no deduplican puertos de forma demostrable.

## Plan seguro y pruebas reproducibles

1. Recuperar únicamente la conectividad a `192.168.57.10`; releer XML y validar con `xmllint` y `wazuh-analysisd -t`, sin reiniciar.
2. Exportar 34 líneas raw de `archives.json` y reemplazar el artefacto provisional.
3. Validar 9, 10, 14 y 15 puertos únicos, repetición de puerto, NAT y Management con el replay.
4. Implementar el correlador con backup, validación, prueba negativa y rollback; después, bajo aprobación, probar un Nmap one-shot solo desde ATTACK/LAB.

```bash
# En el manager, después de exportar raw_event reales; no ejecutado en esta fase.
bash ./scripts/replay_events.sh | grep -E '100500|100501|100502|Phase 3'

# Desde Kali ATTACK/LAB, solo en la siguiente fase autorizada.
nmap -Pn -sS -p 21,23,25,53,80,110,111,143,199,256 192.168.56.20
```

El script rechaza el artefacto actual por no tener `raw_event`; no se ejecutó.

## Capturas y artefactos a revisar

`docs/images_index.json` cataloga 53 imágenes. Cuatro se marcan publicables porque su SHA-256 coincide con capturas ya curadas en el repositorio; las otras 49 se marcan `no` y requieren anonimización o revisión visual. No se subió ninguna imagen.

Para una futura subida: este documento, índice sin imágenes, script de replay, logs de `evidence/sysmon-eid3-test/` y una exportación minimizada/redactada de 34 `raw_event` reales. Excluir transcripciones completas, secretos, logs completos y la exportación CSV de 10.000 filas.
