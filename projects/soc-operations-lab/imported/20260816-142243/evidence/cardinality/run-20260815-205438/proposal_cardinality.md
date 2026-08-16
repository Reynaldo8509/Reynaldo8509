# Propuesta: cardinalidad exacta de puertos

## Limitación observada

`frequency` con `different_field` fue útil para detectar el cruce 10/15 en
las pruebas, pero el estado es interno a Wazuh y los umbrales comparten el
antecedente `100500`. No existe un conjunto de puertos, sesión ni contador
auditable que permita afirmar `COUNT(DISTINCT destPort)` bajo todos los
reintentos y solapamientos.

## Alternativa A: enriquecimiento y correlación Wazuh

Un enriquecedor añade `session_id=source|destination|protocol|bucket_60s` antes
de Wazuh. Las reglas conservan el filtro ATTACK (`192.168.56.0/24`) y destino
`.56.20`, por lo que NAT/Management nunca entran al estado.

```xml
<rule id="100501" level="10" frequency="10" timeframe="60">
  <if_matched_sid>100500</if_matched_sid>
  <same_field>session_id</same_field>
  <different_field>win.eventdata.destPort</different_field>
</rule>
```

Ventaja: sin base externa. Riesgo: validar por versión que umbrales hermanos no
interfieran; no aporta evidencia persistente del conjunto. No instalar sin una
matriz de reintentos, solapamientos y sesiones concurrentes.

## Alternativa B: agregador SQLite local (recomendada)

Un proceso local consume únicamente eventos ya filtrados ATTACK/LAB y usa una
tabla con clave única:

```sql
CREATE TABLE ports (
  bucket TEXT, source_ip TEXT, destination_ip TEXT, protocol TEXT,
  dest_port INTEGER,
  PRIMARY KEY (bucket, source_ip, destination_ip, protocol, dest_port)
);
CREATE TABLE emissions (
  bucket TEXT, source_ip TEXT, destination_ip TEXT, protocol TEXT,
  emitted_10 INTEGER DEFAULT 0, emitted_15 INTEGER DEFAULT 0,
  PRIMARY KEY (bucket, source_ip, destination_ip, protocol)
);
```

PoC segura (no instalada):

1. Filtrar en la entrada: TCP, origen `192.168.56.0/24`, destino
   `192.168.56.20`; descartar `192.168.57.0/24` y `10.0.2.0/24` antes de SQLite.
2. `INSERT OR IGNORE` para cada `(sesión, puerto)`.
3. Calcular `COUNT(*)`; al primer cruce de 10 o 15 insertar la marca en
   `emissions` y emitir JSON normalizado para una regla Wazuh final.
4. Probar 9, 10, 14, 15, repetidos, puertos fuera de orden y dos sesiones.
5. Añadir retención por buckets, health-check, rotación y backup de SQLite.

Coste estimado: 1–2 días de PoC y matriz de pruebas; 2–4 días con servicio,
monitorización, retención y documentación. Requiere aprobación separada porque
añade un componente persistente.
