# Future improvements

1. Validar Sysmon Event ID 3 con una señal ATTACK autorizada antes de modificar sus reglas.
2. Implementar, fuera del rules engine nativo, una normalización stateful si se requiere `COUNT(DISTINCT destinationPort)` exacto.
3. Publicar configuraciones Wazuh/Sysmon/YARA solo después de sanitizarlas y crear pruebas de validación.
4. Ejecutar una consulta autenticada al Wazuh Indexer y una verificación de Dashboard para cerrar la cadena de visualización.
5. Crear evidencia reproducible y sanitizada para FIM, YARA y brute force.
6. Reemplazar los placeholders vacíos de evidencia de brute force mediante una prueba controlada, o retirarlos en una futura limpieza autorizada.
