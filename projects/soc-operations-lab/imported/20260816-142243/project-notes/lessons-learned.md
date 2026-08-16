# Lessons learned

1. Separar MANAGEMENT de ATTACK/LAB reduce falsos positivos sin perder telemetría administrativa.
2. NAT debe conservarse para investigación, aunque quede fuera de un detector concreto.
3. `wazuh-logtest` y Windows EventChannel no son equivalentes cuando cambia el decoder efectivo.
4. `archives.json` prueba ingesta; `alerts.json` prueba creación de alerta; Dashboard requiere verificación independiente.
5. Las reglas `frequency` y `different_field` de Wazuh no implementan `COUNT(DISTINCT)`.
6. La prioridad entre reglas hermanas puede impedir que una base custom reciba el evento real.
7. La telemetría estándar y el veredicto de detección son conceptos distintos: `60104` es WFP audit telemetry, no una alerta de port scan.
8. La ausencia de una señal Sysmon ATTACK debe tratarse como una brecha de validación, no como éxito o fracaso de la correlación.
9. Los límites y las pruebas negativas son parte de una detección profesional, no una nota secundaria.
