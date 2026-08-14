# Windows Brute Force

> **Status: PENDING CONTROLLED VALIDATION**

## Señales disponibles

- Windows Security `4625` registra fallos de autenticación.
- La regla oficial `60122` proporciona visibilidad de fallos individuales.
- El historial del laboratorio incluye correlación custom para patrones repetidos, pero una parte de los eventos OpenSSH dejó `win.eventdata.ipAddress` como `-`.
- El canal `OpenSSH/Operational` conservó la IP en el payload, pero la extracción automática hacia un campo correlacionable no quedó validada como solución final.
- Una exportación sanitizada contiene cinco eventos `4625` históricos: tres fallos NTLM desde `192.168.56.1` y dos fallos locales `127.0.0.1`, todos con la regla individual `60122`. Es evidencia de telemetría, no de una correlación de brute force.

## Implicación

No se debe afirmar todavía que el laboratorio tiene una detección de brute force por IP validada para OpenSSH. La telemetría de fallos existe; la correlación depende de un campo fuente fiable para el tipo de autenticación evaluado.

## Próxima validación requerida

1. Seleccionar un escenario autorizado de autenticación fallida.
2. Confirmar campos reales en `archives.json` para Security y OpenSSH/Operational.
3. Verificar la regla final en `alerts.json`.
4. Registrar una prueba negativa y los límites conocidos.

No se incluyen reglas activas en este documento hasta contar con una exportación revisada y evidencia reproducible.

La exportación disponible está en [evidence/scenario-1-bruteforce](../evidence/scenario-1-bruteforce/events-2026-08-08T18_46_56.179Z.csv). Su campo `rule.mitre.id` refleja la regla histórica de Wazuh y no debe reinterpretarse como la asignación final del caso de uso; la intención de detección se mapea a [T1110 — Brute Force](https://attack.mitre.org/techniques/T1110/) una vez que exista una correlación validada.
