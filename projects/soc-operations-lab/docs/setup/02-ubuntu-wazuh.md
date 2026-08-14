# 02 — Ubuntu y Wazuh Manager

## Estado comprobado

- Wazuh Manager: `4.14.7`.
- Rol: recepción de telemetría Windows EventChannel, análisis, correlación y generación de alertas.
- Red MANAGEMENT: `192.168.57.10`.
- Red ATTACK/LAB: `192.168.56.10`.
- Red NAT/INTERNET: `10.0.2.3`.

## Procedimiento verificable

Una modificación de ruleset debe seguir este orden:

```bash
# Validar un fragmento local_rules.xml sin alterar su estructura fragmentada
{ printf '%s\n' '<ruleset>'; sudo cat /var/ossec/etc/rules/local_rules.xml; printf '%s\n' '</ruleset>'; } > /tmp/local_rules.xml.xmllint-wrapper
xmllint --noout /tmp/local_rules.xml.xmllint-wrapper
sudo /var/ossec/bin/wazuh-analysisd -t
```

Después de una modificación autorizada y validada, se verifica el servicio y los logs. No se publica `ossec.conf`, respaldos del manager ni archivos que puedan contener secretos sin una revisión específica.

## Límite de reproducibilidad

La instalación exacta, dependencias del Indexer y certificados no se exportaron como configuración pública sanitizada. Esta sección describe el proceso de validación, no un instalador completo.
