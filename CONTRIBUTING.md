# Contribuir de forma segura

Este laboratorio documenta configuraciones y pruebas reales. Antes de proponer un cambio:

1. Conserva los límites MANAGEMENT, ATTACK/LAB y NAT.
2. No declares una detección validada sin eventos reales y una prueba negativa relevante.
3. Valida reglas Wazuh con `wazuh-analysisd -t` antes de reiniciar un servicio.
4. Distingue ingesta (`archives.json`), creación de alerta (`alerts.json`) e indexación/visualización.
5. No añadas secretos, llaves privadas, respaldos de producción, transcripciones completas ni capturas sin revisión.

Las mejoras de detección deben explicar su evidencia, falsos positivos esperados, límites y plan de rollback. No se realizan commits ni pushes automáticos desde procedimientos de validación.
