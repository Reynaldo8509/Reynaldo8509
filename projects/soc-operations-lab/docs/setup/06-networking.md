# 06 — Networking

| Network | CIDR | Kali | Ubuntu/Wazuh | Windows | Uso |
|---|---|---:|---:|---:|---|
| MANAGEMENT | `192.168.57.0/24` | `192.168.57.1` | `192.168.57.10` | `192.168.57.20` | Administración y transferencias. |
| ATTACK/LAB | `192.168.56.0/24` | `192.168.56.1` | `192.168.56.10` | `192.168.56.20` | Simulaciones y validación de detecciones. |
| NAT/INTERNET | `10.0.2.0/24` | — | `10.0.2.3` | `10.0.2.15` | Actualizaciones y servicios externos. |

## Alcance de la evidencia

La tabla describe el diseño operativo final documentado. Las capturas revisadas muestran direcciones ATTACK/LAB y NAT en el endpoint y una prueba de conectividad puntual, pero no recuperan comandos de creación de adaptadores, rutas ni una captura final de los tres planos a la vez. Por tanto, la segmentación está **documentada y parcialmente evidenciada**, no es un procedimiento de VirtualBox reproducible paso a paso.

### Regla operativa

Las pruebas de detección de ataque se limitan a ATTACK/LAB. MANAGEMENT y NAT deben conservar telemetría; no son fuentes elegibles para el detector WFP de port scan.

Consulta los comandos confirmados y las brechas de historial en la [referencia de comandos](08-command-reference.md).
