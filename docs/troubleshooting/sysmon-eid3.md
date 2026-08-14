# Sysmon Event ID 3: brecha de validación

## Problem

Se configuró una cadena custom para correlacionar Event ID 3 desde ATTACK/LAB hacia Windows, pero no existe en el archivo revisado un evento real de ese flujo.

## Evidence

- MANAGEMENT y NAT sí generaron EID 3 reales.
- La ruta oficial `60000 -> 60004 -> 61600 -> 61605` se confirmó.
- No apareció `192.168.56.1 -> 192.168.56.20` como EID 3 real durante la revisión.

## Root cause / current limit

El detector no dispone de señal ATTACK real para correlacionar. No está demostrado si la ausencia proviene de la semántica de conexiones bloqueadas, de filtros adicionales de Sysmon o de ambos factores.

## Solution status

No se aplicó ninguna corrección. La próxima fase debe generar un evento ATTACK autorizado y verificar primero la ruta de reglas real. Elevar niveles o copiar el diseño WFP sin esta evidencia podría eclipsar reglas oficiales Sysmon más específicas.

## Lesson learned

El hecho de que Sysmon esté habilitado no demuestra que emita la señal necesaria para un caso de uso concreto. Consulta [el informe de auditoría](../../detection-rules/sysmon-network.md).
