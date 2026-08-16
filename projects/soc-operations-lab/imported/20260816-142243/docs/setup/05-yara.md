# 05 — YARA

## Estado

**PENDING VALIDATION**.

El material histórico menciona trabajo de YARA y detección de malware, pero no existe en este repositorio una regla, configuración de despliegue y evidencia sanitizada que permitan afirmar que el flujo funciona de extremo a extremo.

Antes de publicar una implementación YARA deben existir, como mínimo:

1. Regla YARA segura para compartir y su licencia/origen.
2. Método de ejecución y recolección por Wazuh documentado.
3. Muestra de evento en `archives.json` y alerta correspondiente en `alerts.json`.
4. Prueba negativa y estrategia de actualización.
