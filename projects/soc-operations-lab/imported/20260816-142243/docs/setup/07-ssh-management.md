# 07 — SSH Management

Las tareas de administración utilizan la red MANAGEMENT. El material público no contiene aliases SSH, claves privadas, archivos `known_hosts` ni configuraciones locales de usuario.

Prácticas documentadas:

- Usar autenticación por claves y `IdentitiesOnly` cuando corresponda.
- Mantener las claves fuera del repositorio.
- Confirmar que una conexión administrativa genere telemetría sin alimentar detectores diseñados para ATTACK/LAB.
- Transferir configuraciones mediante canales administrativos, nunca mediante la red de simulación de ataques.
