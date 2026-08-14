# Scenario 1 — Brute Force (legacy marker)

Este directorio conserva un export sanitizado de cinco eventos Windows Security `4625` ([CSV](events-2026-08-08T18_46_56.179Z.csv)) y el marcador documental del escenario histórico. Tres filas muestran fallos NTLM desde `192.168.56.1`; dos son fallos locales desde `127.0.0.1`. El archivo no contiene contraseñas, tokens ni direcciones públicas.

El CSV prueba telemetría individual y la regla histórica `60122`; no prueba una correlación custom, una alerta de brute force ni una prueba negativa. La futura evidencia deberá contener una prueba autorizada, campos sanitizados de ingesta/alerta y una descripción de la regla efectiva. Hasta entonces, el estado de brute force es **TELEMETRY OBSERVED / PENDING DETECTION VALIDATION**.
