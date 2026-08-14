# Known limitations

## WFP Port Scan

- `100501` y `100502` son umbrales heurísticos de alta señal; no cuentan puertos únicos de forma exacta.
- `ignore=60` limita alertas repetidas, pero no representa una garantía de una sola alerta por atacante durante toda una campaña larga.
- La visibilidad final en Dashboard no fue probada mediante una consulta autenticada al índice durante la validación descrita; se comprobó salud del pipeline.

## Sysmon Network

- Falta evidencia EID 3 ATTACK real desde Kali hacia Windows.
- Las correlaciones existentes no tienen throttling y comparten una base, con riesgos de cardinalidad y competencia.
- Reglas oficiales más específicas pueden eclipsar subconjuntos de eventos.

## Otros detectores

- Brute force por IP para OpenSSH requiere campos fuente fiables.
- YARA no tiene un paquete de validación publicable seleccionado.
- FIM requiere una revalidación de extremo a extremo con evidencia sanitizada.
