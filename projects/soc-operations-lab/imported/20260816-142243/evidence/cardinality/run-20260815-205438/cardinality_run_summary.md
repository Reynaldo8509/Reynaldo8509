# Resumen — run 20260815-205438

## Objetivo y resultado

PASS operativo: WFP produjo 100501 en 10 puertos distintos y 100502 en 15;
Sysmon EID 3 real ATTACK/LAB fue detectado por la regla específica 100004.

## Pasos ejecutados

1. Verificación de ATTACK, GitHub/origin y backup con SHA-256.
2. Validación XML y `wazuh-analysisd -t`.
3. Parseo reproducible de los 34 eventos y replay Sysmon con `wazuh-logtest`.
4. Nmap autorizado, exportación tolerante a JSON incompleto y análisis de orden.

## Publicación

No se hizo push. `gh auth status` es válido, pero `git ls-remote origin
refs/heads/main` devolvió `Repository not found`; no se alteró la URL ni se
intentó crear repositorios. Para restaurarlo, verificar que
`Reynaldo8509/soc-operations-lab` exista y que el token tenga acceso a ese repo,
después ejecutar `git push origin HEAD:main` desde la rama aprobada.

## Próximo paso

Mantener las reglas actuales para detección operativa. Si se exige cardinalidad
matemáticamente exacta, aprobar la alternativa B (agregador SQLite) y ejecutar
su PoC y matriz de pruebas antes de instalarla.
