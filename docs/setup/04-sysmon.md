# 04 — Sysmon

Sysmon está presente en el endpoint y la telemetría Event ID 3 fue observada para conexiones MANAGEMENT y NAT. La ruta oficial de Wazuh es:

```text
60000 -> 60004 -> 61600 -> 61605 -> sysmon_event3
```

La configuración de red de Sysmon está habilitada, pero no hay una muestra EID 3 ATTACK `192.168.56.1 -> 192.168.56.20` en los archivos revisados. Por ello, el detector Sysmon Network no se considera validado. Consulta [sysmon-network.md](../../detection-rules/sysmon-network.md).

No se publica el XML activo de Sysmon hasta disponer de una versión sanitizada, revisada y reproducible.
