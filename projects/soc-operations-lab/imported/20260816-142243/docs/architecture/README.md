# Arquitectura del SOC HomeLab

## Objetivo de diseño

El laboratorio separa la administración, los escenarios controlados y la conectividad externa. Esa separación permite interpretar el origen de la telemetría antes de aplicar una detección.

## Componentes virtualizados

| Componente | Función |
|---|---|
| Kali Linux | Administración desde MANAGEMENT y ejecución de escenarios controlados desde ATTACK/LAB. |
| Ubuntu / Wazuh Manager 4.14.7 | Recepción de eventos, análisis, correlación, almacenamiento local de archivos y envío al pipeline de visualización. |
| Windows 11 endpoint | Endpoint monitorizado con Wazuh Agent, Windows Security EventChannel y Sysmon. |
| VirtualBox | Plataforma de virtualización y segmentación de adaptadores del laboratorio. |

## Planos de red

| Plano | CIDR | Direcciones | Uso permitido |
|---|---|---|---|
| Administration Plane | `192.168.57.0/24` | Kali `.1`, Ubuntu `.10`, Windows `.20` | SSH, SCP/SFTP, WinRM, mantenimiento y transferencia de archivos. |
| Attack Plane | `192.168.56.0/24` | Kali `.1`, Ubuntu `.10`, Windows `.20` | Reconnaissance y pruebas controladas contra el endpoint del laboratorio. |
| Internet/NAT Plane | `10.0.2.0/24` | Ubuntu `.3`, Windows `.15` | Actualizaciones, repositorios y conexiones externas normales. |

El plano MANAGEMENT no participa en el detector WFP de port scan. NAT conserva telemetría, pero tampoco participa. Solo ATTACK/LAB es elegible para ese caso de uso.

## Flujo de telemetría

```text
Windows 11
  ├─ Windows Security: WFP 5152/5157
  ├─ Sysmon Operational: Event ID 3 y otras fuentes
  └─ Wazuh Agent
          |
          v
Ubuntu / Wazuh Manager
  ├─ archives.json: evidencia de ingesta
  ├─ ruleset: clasificación y correlación
  └─ alerts.json: alertas creadas
          |
          v
Filebeat -> Wazuh Indexer -> Wazuh Dashboard
```

El estado de Filebeat o del servicio Indexer no sustituye una consulta autenticada al índice o una búsqueda visible en Dashboard.

## Decisiones de seguridad

- La actividad administrativa es telemetría legítima, no actividad de ataque por defecto.
- La telemetría NAT se retiene para investigación, en lugar de silenciarla globalmente.
- Las reglas de detección se validan primero contra el evento Windows EventChannel real, no solo con `wazuh-logtest`.
- Los artefactos públicos contienen procedimientos y evidencias sanitizadas, nunca claves privadas o secretos.
