# Investigación de cardinalidad Wazuh

La evidencia final y la propuesta técnica están en
[`evidence/cardinality/report.md`](../evidence/cardinality/report.md). La
corrección mínima aplicada hace directa la admisión de Sysmon Event ID 3 para
ATTACK/LAB, conservando exclusiones de NAT y Management. Para cardinalidad
auditada exacta se recomienda el agregador SQLite descrito en la propuesta.
