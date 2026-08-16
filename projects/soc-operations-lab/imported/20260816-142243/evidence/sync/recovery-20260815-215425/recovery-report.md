# Recuperación de sincronización — 2026-08-15

## Resultado

La referencia remota anterior, `Reynaldo8509/soc-operations-lab`, ya no existe.
El proyecto fue consolidado en
[`Reynaldo8509/Reynaldo8509`](https://github.com/Reynaldo8509/Reynaldo8509)
bajo `projects/soc-operations-lab/`. Por ello no había un ancestro Git común
entre el checkout histórico y el repositorio canónico.

La integración se realizó mediante la rama
`recovery/soc-operations-lab-20260815-215425` y el PR
[#1](https://github.com/Reynaldo8509/Reynaldo8509/pull/1), integrado en
`main` como `65284c07a6a8578443d9a2c0a62c5e39dc2f5c00`.

## Preservación de datos

- Bundle y archivo completo del árbol histórico: `GitBackup/sync-recovery-20260815-215425/`.
- Copia privada de los 13 artefactos antes de sustituir rutas locales:
  `GitBackup/sync-recovery-20260815-215425/private-pre-sanitization/`.
- Rama local histórica: `legacy-local-20260815-215425`.
- Ramas de respaldo de la comparación previa: `backup-local-20260815-214910`
  y `backup-remote-20260815-214910`.

Los 31 archivos que ya existían en cloud se conservaron como fuente
autoritativa. Se añadieron 129 artefactos exclusivamente locales que superaron
la validación; 27 elementos no requeridos permanecen únicamente en el checkout
histórico y en el snapshot.

## Evidencia publicada

- Investigación reproducible de cardinalidad WFP/Sysmon.
- Herramientas de parser, generación de fixtures y validación candidata.
- 45 imágenes técnicas con catálogo y cribado previo.
- Estado de Sysmon corregido a **validación parcial**: señal real ATTACK/LAB
  para la regla directa `100004`; umbral multipuerto validado por replay, no
  afirmado como resultado de un escaneo real.

## Validaciones

- `git fsck --full` sobre el checkout histórico y el canónico.
- `check-publication-safety.sh`: PASS.
- Auditoría de secretos/PII, correos y rutas locales: PASS tras redacción.
- `git diff --check`, enlaces Markdown, sintaxis Bash y compilación Python: PASS.
- El checkout canónico quedó alineado con `origin/main`.

## Uso futuro

Trabajar desde `$HOME/Reynaldo8509/projects/soc-operations-lab` y actualizarlo
con `git -C "$HOME/Reynaldo8509" pull --ff-only origin main`. El checkout
`soc-operations-lab` es histórico; su `origin` ahora apunta al repositorio de
perfil únicamente para que el remoto vuelva a ser resoluble.
