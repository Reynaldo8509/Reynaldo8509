# Comandos reproducibles del HomeLab

Estos comandos documentan la verificación y pruebas controladas. No contienen
contraseñas, tokens, llaves privadas ni rutas de perfiles personales.

```bash
# Integridad y estado del repositorio
git -C <LOCAL_HOME>/soc-operations-lab fsck --full
git -C <LOCAL_HOME>/soc-operations-lab status --porcelain
git -C <LOCAL_HOME>/soc-operations-lab ls-remote origin refs/heads/main

# Validación del ruleset en el manager (requiere privilegios ya configurados)
ssh wazuh 'sudo /var/ossec/bin/wazuh-analysisd -t'
ssh wazuh "sudo sh -c '{ printf \"<ruleset>\\n\"; cat /var/ossec/etc/rules/local_rules.xml; printf \"\\n</ruleset>\\n\"; } | xmllint --noout -'"

# Reconstrucción de cardinalidad desde el CSV exportado
python3 tools/parse_cardinality.py INPUT.csv \
  --output evidence/cardinality/run-STAMP/cardinality \
  --limit 34 --source 192.168.56.1 --destination 192.168.56.20

# Replay de Sysmon en el manager, usando un fixture generado en ATTACK/LAB
python3 tools/generate_logtest_events.py --kind sysmon --ports 21,22,23,24,25,26,27,28,29,30
ssh wazuh 'sudo /var/ossec/bin/wazuh-logtest -v < /tmp/fixture.jsonl'

# Escaneo autorizado desde ATTACK/LAB hacia el endpoint del laboratorio
nmap -Pn -sS --min-rate 100 --max-retries 0 -T4 -p 1-20 192.168.56.20
nmap -Pn -sT --max-retries 0 -T4 -p 22 192.168.56.20

# Exportación tolerante a una línea JSON aún en escritura
sudo tail -n 5000 /var/ossec/logs/alerts/alerts.json | jq -Rc 'fromjson? | select(.)'
```

`xmllint` puede requerir un wrapper temporal cuando `local_rules.xml` contiene
varios fragmentos `<group>` raíz; el wrapper se valida sin sustituir el archivo
activo. Los resultados y hashes de cada ejecución están en `evidence/`.
