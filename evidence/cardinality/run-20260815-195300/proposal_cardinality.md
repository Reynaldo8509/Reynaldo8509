# Propuesta para cardinalidad de puertos

## A. Correlación Wazuh enriquecida

Antes de la regla base, un enriquecedor debe añadir `session_id` estable, por
ejemplo `sourceIp|destinationIp|protocol|bucket_utc_60s`. Un decoder por sí solo
no concatena de forma fiable esos campos; el enriquecedor debe producir un campo
explícito para que Wazuh lo decodifique.

```xml
<rule id="100409" level="1">
  <field name="win.system.eventID">^3$</field>
  <field name="win.eventdata.sourceIp">^192\.168\.56\.</field>
  <field name="win.eventdata.destinationIp">^192\.168\.56\.20$</field>
  <options>no_log</options>
</rule>
<rule id="100420" level="10" frequency="10" timeframe="60">
  <if_matched_sid>100409</if_matched_sid>
  <same_field>session_id</same_field>
  <different_field>win.eventdata.destinationPort</different_field>
</rule>
```

Pros: conserva el motor Wazuh y los límites ATTACK/LAB; NAT y Management quedan
fuera por los filtros de base. Contras: el estado de `frequency`/`different_field`
es implícito, la semántica de dos umbrales debe probarse por versión y Wazuh no
expone un conjunto de puertos auditable.

Validación candidata segura:

```bash
cp -p /var/ossec/etc/rules/local_rules.xml /tmp/local_rules.xml.candidate
python3 /opt/soc/build_candidate.py /tmp/local_rules.xml.candidate
{ printf '<ruleset>\n'; cat /tmp/local_rules.xml.candidate; printf '\n</ruleset>\n'; } | xmllint --noout -
# Solo después: instalar temporalmente, ejecutar wazuh-analysisd -t y restaurar ante cualquier error.
```

## B. Agregador local con SQLite (recomendado para exactitud)

Un proceso local consume solo eventos ya filtrados ATTACK/LAB, inserta
`(bucket, source_ip, destination_ip, protocol, dest_port)` en SQLite con una
restricción `UNIQUE`, y emite un evento JSON cuando `COUNT(*)` cruza 10 o 15.
Las marcas `emitted_10` y `emitted_15` se guardan por sesión para que ambos
umbrales sean independientes y auditables.

Pros: `COUNT(DISTINCT dest_port)` real, explicación reproducible del conjunto,
dos umbrales independientes. Contras: proceso, base SQLite, monitoreo y retención
adicionales. Nunca debe recibir `192.168.57.0/24` ni `10.0.2.0/24`: la admisión
debe exigir origen `192.168.56.0/24`, destino `192.168.56.20` y TCP antes de
escribir en SQLite.

Implementar B requiere aprobación separada: añade un componente persistente y no
se instaló en esta ejecución.
