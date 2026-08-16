# File Integrity Monitoring (FIM)

> **Status: CONFIGURED / REVALIDATION PENDING**

El historial del laboratorio muestra que FIM/syscheck está configurado y que se realizó un ajuste estrecho para reducir ruido de una ruta de pruebas. Ese ajuste buscó conservar visibilidad de FIM fuera de dicha ruta.

No existe todavía un paquete público sanitizado con configuración, rutas monitorizadas, evento de cambio y alerta final que permita declarar una validación completa de extremo a extremo. Por ello, esta página no publica XML ni rutas de usuario.

Para cerrar esta detección se requiere una prueba controlada de cambio de archivo, evidencia de `archives.json` y `alerts.json`, y una revisión de que la excepción limitada no oculte rutas fuera de su ámbito.
