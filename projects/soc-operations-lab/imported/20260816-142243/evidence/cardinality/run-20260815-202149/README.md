# Run 20260815-202149

- [x] Backup activo y SHA-256 registrado.
- [x] XML envuelto validado con `xmllint`.
- [x] `wazuh-analysisd -t` limpio y RC 0.
- [x] Reinicio controlado; `wazuh-manager` activo.
- [x] Secuencia histórica de 34 eventos reconstruida.
- [x] Nmap ATTACK/LAB de 20 puertos produjo `100501` y `100502`.
- [x] EID 3 Sysmon real y exclusiones Management/NAT comprobados.
- [x] Informe y evidencia sanitizada generados.

El informe completo está en [cardinality_report.md](cardinality_report.md).
Los logs completos de `wazuh-logtest` permanecen locales; las salidas que se
versionen son fixtures y extractos no sensibles.
