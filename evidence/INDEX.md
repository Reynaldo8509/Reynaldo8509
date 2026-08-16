# Índice de evidencia — investigación de cardinalidad

La ejecución principal es [`cardinality/run-20260815-195300/`](cardinality/run-20260815-195300/).
La verificación de continuidad y prueba de producción posterior es
[`cardinality/run-20260815-202149/`](cardinality/run-20260815-202149/).

| Artefacto | Contenido |
|---|---|
| `cardinality/report.md` | Hallazgos, corrección aplicada y recomendación |
| `cardinality/run-20260815-195300/cardinality/` | Secuencia reconstruida de 34 eventos y resumen de puertos únicos |
| `cardinality/run-20260815-195300/decoder_tests/` | Fixtures JSON no sensibles y pruebas `wazuh-logtest` |
| `cardinality/run-20260815-195300/production_test/` | Campos sanitizados de WFP/Sysmon y pruebas Nmap autorizadas |
| `cardinality/run-20260815-195300/proposal_cardinality.md` | Alternativas para cardinalidad exacta |
| `cardinality/run-20260815-202149/cardinality_report.md` | Reconstrucción final, validación de continuidad y decisión de arquitectura |
| `cardinality/run-20260815-202149/production_test/` | Evidencia sanitizada de WFP, Sysmon EID 3 y Nmap autorizado |

No se versionan logs raw que contengan atributos personales del endpoint, credenciales
ni claves. Los backups del manager permanecen fuera del repositorio, en
`/home/reyam/GitBackup/cardinality-backups/`.
