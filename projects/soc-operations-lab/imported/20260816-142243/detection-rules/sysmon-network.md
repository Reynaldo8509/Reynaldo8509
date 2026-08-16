# Sysmon Network / Event ID 3

> **Status: AUDITED / PENDING VALIDATION**

Esta página documenta una auditoría de la cadena Sysmon EID 3. No declara un detector de port scan operativo.

## Ruta oficial observada

```text
windows_eventchannel
  -> 60000
     -> 60004  (Microsoft-Windows-Sysmon/Operational)
        -> 61600  (INFORMATION)
           -> 61605  (Event ID 3, group sysmon_event3)
```

## Reglas custom auditadas

```text
100409  level 1, if_group sysmon_event3, TCP,
        sourceIp 192.168.56.0/24, destinationIp 192.168.56.20, no_log

100420  level 10, frequency 10 / timeframe 60,
        if_matched_sid 100409, same sourceIp, different destinationPort

100421  level 13, frequency 15 / timeframe 60,
        if_matched_sid 100409, same sourceIp, different destinationPort
```

`100409` está correctamente anclada a `sysmon_event3` y es silenciosa por diseño. Solo resulta elegible para TCP desde ATTACK/LAB hacia el endpoint Windows de ATTACK/LAB.

## Evidencia de auditoría

| Contexto | Resultado |
|---|---|
| MANAGEMENT | EID 3 real confirmado para `192.168.57.1 -> 192.168.57.20:22`; la telemetría no alimentó `100409`. |
| NAT/INTERNET | EID 3 real confirmado desde `10.0.2.15` hacia servicios externos; no alimentó `100409`. |
| ATTACK/LAB | No se encontró EID 3 real `192.168.56.1 -> 192.168.56.20` en el archivo revisado. |

La ausencia ATTACK es la brecha principal: sin evento fuente real no es posible validar que `100409`, `100420` o `100421` funcionen en producción.

## Riesgos técnicos identificados

1. **Cardinalidad heurística.** `frequency`, `timeframe` y `different_field` no son un `COUNT(DISTINCT destinationPort)` nativo. La misma limitación documentada para WFP se aplica al motor de correlación de esta cadena.
2. **Reglas frequency hermanas.** `100420` y `100421` comparten `if_matched_sid=100409`; pueden competir por eventos de la misma ventana.
3. **Sin throttling.** Ninguna regla de correlación tiene `ignore="60"`, por lo que un flujo que llegue a correlacionar podría repetir alertas.
4. **Eclipses potenciales.** Reglas oficiales más específicas `92104`, `92105`, `92107` y `92110`, y la regla local `100004` nivel 12 para `192.168.56.1 -> :22`, pueden ganar para subconjuntos de eventos. Es una consideración estructural; no fue demostrada con un EID 3 ATTACK real.

## Decisión actual

WFP sigue siendo la fuente validada para port scans de puertos bloqueados. Antes de cambiar la cadena Sysmon se requiere una prueba controlada futura que produzca y archive un EID 3 ATTACK real. Entonces deberán verificarse la ruta final de regla, la posible competencia con reglas oficiales, repetición de alertas y pruebas negativas de MANAGEMENT/NAT.

No elevar el nivel de `100409` por intuición: podría eclipsar reglas oficiales más específicas.
