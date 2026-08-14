# SOC Operations HomeLab
<img width="1536" height="1024" alt="Home_Labs" src="https://github.com/user-attachments/assets/ef245809-4454-4a8b-8e96-f416abdef349" />

Repositorio de un laboratorio SOC reproducible construido con VirtualBox, Kali Linux, Ubuntu/Wazuh y un endpoint Windows 11. El proyecto prioriza ingeniería de detección verificable: separar telemetría de veredictos, reproducir escenarios controlados y documentar límites del motor antes de declarar una detección válida.

## What This Lab Demonstrates

- Detection engineering with Wazuh custom rules and event correlation
- Windows Security EventChannel and Sysmon endpoint telemetry
- Network-plane separation between administration, attack testing and NAT/internet
- False-positive reduction without globally silencing legitimate telemetry
- Production-event validation instead of relying on synthetic logtest results alone
- Evidence handling, investigation workflow and explicit documentation of engine limitations

## Estado de detecciones

| Detección | Estado | Evidencia disponible |
|---|---|---|
| WFP Port Scan | **VALIDATED** | Eventos WFP reales, `archives.json`, `alerts.json` y pruebas negativas de NAT/MANAGEMENT. |
| Sysmon Network / Event ID 3 | **AUDITED / PENDING VALIDATION** | EID 3 confirmado en MANAGEMENT y NAT; falta una señal ATTACK real que permita validar el detector. |
| Windows brute force | **PENDING CONTROLLED VALIDATION** | Telemetría 4625 y reglas históricas documentadas; la correlación depende de que Windows proporcione una IP fuente utilizable. |
| FIM | **CONFIGURED / REVALIDATION PENDING** | Historial de ajuste de ruido de rutas de prueba; falta un paquete público de evidencias reproducibles. |
| YARA | **PENDING VALIDATION** | No hay configuración ni evidencia sanitizada suficiente para hacer una afirmación operativa. |

## Detection Coverage Matrix

| Use case | Telemetry | Main rules | Status | Evidence |
|---|---|---|---|---|
| WFP Port Scan | Windows Security 5152/5157 | `100500–100502` | **VALIDATED** | Production WFP events + negative NAT/MANAGEMENT tests |
| Sysmon Network | Sysmon Event ID 3 | `100409–100421` | **AUDITED / PENDING** | Real EID 3 telemetry in MANAGEMENT/NAT |
| Windows Brute Force | Windows Security 4625 | `100210–100212` | **PENDING** | Rule design + Windows telemetry |
| File Integrity | Wazuh syscheck/FIM | FIM rules | **REVALIDATION PENDING** | Historical FIM tests |
| YARA | YARA scan results | `111111–111114` | **PENDING** | Sanitized evidence not yet sufficient |

Detailed rule documents are indexed in the [Detection Engineering directory](detection-rules/README.md).

## Arquitectura
<img width="1536" height="1024" alt="Arquitectura" src="https://github.com/user-attachments/assets/241fb358-1f68-417c-9aa2-630d762b8aa1" />

```text
                           Administration Plane
  Kali 192.168.57.1 ───────────────┬─────────────── Ubuntu/Wazuh 192.168.57.10
                                   │ SSH / SCP / WinRM
                                   └─────────────── Windows 11 192.168.57.20

                              Attack/Lab Plane
  Kali 192.168.56.1 ───────────────┬─────────────── Ubuntu/Wazuh 192.168.56.10
                                   │ controlled reconnaissance
                                   └─────────────── Windows 11 192.168.56.20

                              Internet/NAT Plane
             Ubuntu/Wazuh 10.0.2.3 ──────────────── Windows 11 10.0.2.15
```

| Network | CIDR | Kali | Ubuntu/Wazuh | Windows 11 | Purpose |
|---|---|---:|---:|---:|---|
| MANAGEMENT | `192.168.57.0/24` | `.1` | `.10` | `.20` | Administración: SSH, SCP/SFTP, WinRM y mantenimiento. |
| ATTACK/LAB | `192.168.56.0/24` | `.1` | `.10` | `.20` | Escenarios controlados de reconnaissance y detección. |
| NAT/INTERNET | `10.0.2.0/24` | — | `.3` | `.15` | Actualizaciones y telemetría externa normal. |

La separación evita que tráfico administrativo o NAT se clasifique como actividad del laboratorio. Más detalle: [arquitectura](docs/architecture/README.md).

## SOC Workflow

```text
01  Generate controlled activity
02  Collect endpoint telemetry
03  Decode / normalize the event path
04  Apply base tracking rule
05  Correlate and evaluate thresholds
06  Validate against production evidence
07  Investigate false positives / negatives
08  Document result and limitations
```

## Flujo de datos

```text
Windows Security / Sysmon
        -> Wazuh Agent
        -> Wazuh Manager 4.14.7
        -> archives.json (ingesta)
        -> ruleset / correlación
        -> alerts.json (alertas)
        -> Filebeat / Indexer / Dashboard
```

`archives.json` demuestra que un evento ingresó; `alerts.json` demuestra que una regla creó una alerta. La visualización en Dashboard requiere una comprobación independiente de indexación.

## Detection Case Study — WFP Port Scan

### Objective

Detect controlled inbound TCP reconnaissance against Windows 11 from the ATTACK/LAB network while retaining normal MANAGEMENT and NAT telemetry.

### Telemetry path

```text
Kali 192.168.56.1
      |
      | controlled TCP reconnaissance
      v
Windows 11 192.168.56.20
      |
      | WFP 5152 / 5157
      v
Wazuh Agent
      |
      v
Wazuh Manager 4.14.7
      |
      | 100500 -> 100501 / 100502
      v
alerts.json -> Filebeat -> Indexer -> Dashboard
```

### Observed result

- **34** WFP records were produced by the validated 15-port scan.
- **15** raw destination-port values were observed.
- The Wazuh correlation rules generated exactly one visible alert for each threshold in the observed scan.
- MANAGEMENT and NAT negative tests remained outside the WFP detector.

The correlation is intentionally documented as a **heuristic signal**, not exact `COUNT(DISTINCT destinationPort)` logic. The full forensic sequence and cardinality analysis are documented in [WFP Port Scan Detection](detection-rules/WFP_PortScan_Detection_Final.md).

## False-Positive Reduction

The detector uses the network architecture itself as part of the detection design:

```text
MANAGEMENT 192.168.57.0/24
    -> telemetry retained
    -> excluded from WFP correlation

NAT/INTERNET 10.0.2.0/24
    -> telemetry retained
    -> excluded from WFP correlation

ATTACK/LAB 192.168.56.0/24
    -> controlled reconnaissance
    -> eligible for WFP port-scan detection
```

This keeps legitimate telemetry available for investigation without allowing administration or ordinary external traffic to become a port-scan verdict.

## Caso destacado: WFP Port Scan

La detección WFP utiliza eventos Windows Security `5152`/`5157` inbound TCP, limitados a `192.168.56.0/24 -> 192.168.56.20`.

- `100500`: base de tracking silenciosa, nivel 6, anclada a la rama Security EventChannel.
- `100501`: correlación de señal alta nivel 10.
- `100502`: correlación de señal alta nivel 13.

Una prueba real produjo 34 eventos WFP sobre 15 puertos de destino crudos distintos y exactamente una alerta visible de cada umbral. Estos umbrales son **heurísticas de correlación**, no `COUNT(DISTINCT destinationPort)`. Consulta la [documentación WFP validada](detection-rules/WFP_PortScan_Detection_Final.md).

## Evidencia visual curada

El repositorio incluye capturas técnicas revisadas de arquitectura, Wazuh, WFP y Sysmon. Las capturas conservan únicamente las direcciones privadas relevantes del HomeLab; no contienen secretos ni pantallas de autenticación. La evidencia WFP ilustra telemetría ATTACK/LAB y acompaña una detección **VALIDATED** de naturaleza heurística. La captura de Sysmon prueba la preparación del endpoint, pero Sysmon EID 3 continúa **AUDITED / PENDING VALIDATION**.

[Ver el inventario de evidencia →](evidence/README.md)

## Problemas técnicos reales resueltos

- Una regla oficial WFP `60104` de nivel 5 eclipsaba la base custom de nivel 1. La base validada quedó en nivel 6.
- Un escaneo generó múltiples eventos `5152`/`5157` por puerto. `ignore="60"` limita el flooding sin eliminar telemetría.
- `wazuh-logtest` con JSON archivado puede usar un decoder distinto de `windows_eventchannel`; la validación definitiva se hizo con eventos de producción.

## Engineering Lessons

1. Un evento válido no equivale automáticamente a una detección válida.
2. Mayor volumen de eventos no implica necesariamente actividad maliciosa.
3. Separar planos de red reduce presión de falsos positivos sin eliminar telemetría.
4. La validación con eventos Windows EventChannel reales es más representativa que una prueba sintética aislada.
5. Los límites del rules engine deben documentarse antes de interpretar un contador de correlación como cardinalidad exacta.

## Tecnologías

- VirtualBox
- Kali Linux
- Ubuntu con Wazuh Manager 4.14.7
- Windows 11 con Wazuh Agent y Sysmon
- Windows Filtering Platform, Windows EventChannel, `jq`, Filebeat y Wazuh Indexer/Dashboard

## Reproducibilidad y comandos

La [guía de setup](docs/setup/README.md) separa arquitectura, roles y validación. El [Command Reference](docs/setup/08-command-reference.md) reúne los comandos públicos usados para verificar interfaces, conectividad, Sysmon, reglas Wazuh, `xmllint`, `wazuh-analysisd`, `jq` y reproducir la prueba Nmap validada.

La instalación histórica completa no se declara reproducible todavía: los transcripts originales de instalación se mantienen fuera del repositorio público hasta poder sanitizarlos. No se inventan comandos de instalación que no estén respaldados por la evidencia conservada.

## Navegación

- [Arquitectura](docs/architecture/README.md)
- [Guía de setup reproducible](docs/setup/README.md)
- [Comandos de operación y reproducción](docs/setup/08-command-reference.md)
- [Operación y validación](docs/operations/validation-workflow.md)
- [Detección e ingeniería de reglas](detection-rules/README.md)
- [Troubleshooting](docs/troubleshooting/)
- [Cronología técnica](docs/timeline/project-history.md)
- [Lecciones y limitaciones](project-notes/)
- [Inventario de evidencia](evidence/README.md)

## Principios del proyecto

1. No declarar una detección validada sin evidencia real.
2. Mantener telemetría legítima aunque quede fuera de un detector.
3. Documentar límites del rules engine y de la observabilidad.
4. No publicar claves, contraseñas, tokens, transcripciones internas ni configuraciones con secretos.

## Licencia

Este proyecto se publica bajo [MIT](LICENSE).
