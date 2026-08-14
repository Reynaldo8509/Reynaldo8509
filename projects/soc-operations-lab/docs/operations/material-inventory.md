# Inventario y decisión de publicación

Este inventario clasifica el material revisado al preparar el repositorio. Los originales no se movieron ni se borraron.

| Fuente / conjunto | Categoría | Propósito | Utilidad pública | Sensibilidad / decisión |
|---|---|---|---|---|
| `ContextoIA/contexto_anterior.md` | I, D, E, F | Historial técnico extenso de cambios y troubleshooting. | Alta como fuente de conocimiento. | Puede contener material operativo; extraer conocimiento, no copiar. |
| `ContextoIA/transcripcion_completa.md`, `.txt`, `transcripcion_wazuh.txt` | I, L | Transcripciones completas de sesiones. | Baja en forma cruda. | No publicar; fuente privada de decisiones verificadas. |
| `ContextoIA/contexto_maestro.md` | H, J, K | Resumen de contextos de varias tareas. | Media. | Histórico y mezclado con material ajeno; usar solo para corroborar, no copiar. |
| `ContextoIA/WFP_PortScan_Detection_Final.md` | D, H | Informe técnico WFP. | Alta. | Transformado en `detection-rules/WFP_PortScan_Detection_Final.md`; revisar siempre antes de publicar. |
| `ContextoIA/Proyecto SOC WASU/.../events-*.csv` | G, L | Exportación de eventos. | Potencialmente alta. | No copiar hasta sanitizar campos, fechas e identificadores. |
| `ContextoIA/Proyecto SOC WASU/Capturas de pantalla/...` | G, L | 57 capturas históricas de instalación, Wazuh y Windows. | Potencialmente alta tras revisión individual. | Ocho copias sin modificar, de alto valor técnico, se publican en `evidence/screenshots/`; las 49 restantes no se copian por información sensible, falta de contexto o bajo valor documental. |
| `ContextoIA/*/MEMORY.md`, `raw_memories.md`, `memory_summary.md` | I, L | Memoria de agentes y resúmenes internos. | Baja. | Nunca publicar. |
| `ContextoIA/memories_root_backup.sqlite` | I, L | Copia de memoria interna. | Ninguna. | Nunca publicar. |
| Capturas históricas del repositorio (`fase1_repo_ready.png`, SHA-256 `3ae74ac…bf64cbf82`; `fase1_repo2_ready.png`, SHA-256 `a623425e…26662a25`) | G, L | Preparación inicial del repositorio. | Ninguna. | **UNSAFE_TO_PUBLISH**: la revisión visual mostró nombre de usuario/ruta local y pantalla de autenticación GitHub. Las dos copias originales fueron preservadas fuera del repositorio; sus duplicados exactos no se publican. |
| Placeholders `scenario-1-bruteforce/attack.png`, `wazuh-alert.png` y `logs.json` (0 bytes; SHA-256 `e3b0c442…b855`) | F, G, J, K | Estructura histórica vacía. | Ninguna. | Retirados del repositorio: no son evidencia ni contenido publicable. |
| 57 capturas bajo `ContextoIA/Proyecto SOC WASU/Capturas de pantalla/` | G, I, L | Instalación, operación y pruebas históricas. | Ocho son útiles como evidencia visual pública. | Revisión visual individual: ocho candidatos **PUBLISH_AS_IS** se copiaron a `evidence/screenshots/`; 49 permanecen **DO_NOT_PUBLISH** por pantallas de autenticación, prompts de contraseña, rutas o nombres personales, marcadores del navegador, direcciones públicas, comandos no necesarios o valor documental insuficiente. No se modificó ningún original. |
| `evidence/screenshots/` (8 archivos) | G, H | Evidencia visual curada de arquitectura, Wazuh, WFP y Sysmon. | Alta, con alcance explícito. | **PUBLISH_AS_IS**: revisión visual real, sin contraseñas, tokens, claves, cookies, códigos de autenticación, pantallas de login, direcciones públicas ni direcciones del rango privado excluido. Las IPs privadas de ATTACK/LAB y NAT se conservan como parte de la arquitectura documentada. |
| `evidence/scenario-1-bruteforce/` | F, K | Marcador documental de escenario inicial. | Baja. | Solo README; no debe usarse como prueba. |
| `detection-rules/WFP_PortScan_Detection_Final.md` | D, H | Detección WFP validada. | Alta. | Publicable: contiene resultados sanitizados, límites de cardinalidad y no incluye secretos. |

## Leyenda

- **D** detección, **E** troubleshooting, **F** pruebas, **G** evidencia, **H** documentación, **I** transcripción interna, **J** duplicado, **K** obsoleto/incompleto, **L** sensible o requiere revisión.

La fuente histórica permanece fuera del repositorio. La documentación pública expresa resultados validados y limitaciones, no conversaciones ni datos operativos crudos.
