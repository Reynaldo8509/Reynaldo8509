# Configuraciones publicables

Este directorio se reserva para configuraciones sanitizadas y reproducibles. Actualmente no se exportan archivos activos de Wazuh, Sysmon, YARA o Windows porque pueden contener rutas específicas, identificadores del entorno o material sensible.

Una futura configuración publicada debe incluir:

1. propósito y versión del componente;
2. variables o valores que el lector deba reemplazar;
3. validación reproducible;
4. revisión de secretos antes de añadirla al repositorio.

Las reglas WFP ya documentadas se mantienen en [detection-rules](../detection-rules/), no como copia de `local_rules.xml` activo.
