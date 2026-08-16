# Publish summary — 20260815-210501

## Resultado

La preparación pública pasó los controles locales. El push queda bloqueado:
el remoto configurado responde `Repository not found`, por lo que no se creó
PR, tag, release ni se modificó ningún repositorio remoto.

## Inventario y backups

- HEAD inicial auditado: `c8bace2`.
- `git fsck --full`: correcto, sin salida de errores.
- Comparación con `origin/main`: no verificable por indisponibilidad del remoto.
- Bundle local de recuperación: `soc-operations-lab-20260815-210501.bundle`;
  SHA-256 `36d1e4267188d79d3a4a1c2924fac5bef6ab1b529e5569cb52afd8ba9fcc4799`.
- Originales de imágenes: backup privado `images-20260815-210501/`.

## Controles de publicación

| Control | Resultado |
|---|---|
| Emails en texto rastreado publicable | 0 |
| CSV `evidence/csvs/4625.csv` | No presente; no se generó copia sanitizada |
| Enlaces Markdown locales | 71 comprobados, 0 rotos |
| Imágenes de origen | 53 |
| Imágenes publicadas | 45 |
| Imágenes excluidas | 8, por términos OCR asociados a credenciales |
| Metadata de imágenes | Eliminada antes de publicación |
| Optimización web | 18,314,492 → 16,917,854 bytes; 43 archivos reducidos |

Las rutas de origen, el texto OCR y las imágenes excluidas permanecen fuera del
repositorio. El [índice de imágenes](images/README.md) contiene únicamente
rutas relativas y hashes de los activos publicados.

## Cambios preparados

- `README.md`: Sysmon EID 3 actualizado a **VALIDATED** y enlaces a evidencia.
- `docs/images/`: 45 capturas normalizadas, sin metadata e indexadas.
- `docs/commands_used.md`: comandos reproducibles sin secretos.
- `docs/publish_summary.md`: este registro.

## Comandos principales

```bash
git -C /home/reyam/soc-operations-lab fsck --full
git -C /home/reyam/soc-operations-lab ls-remote origin refs/heads/main
git -C /home/reyam/soc-operations-lab bundle create BACKUP.bundle --all
python3 tools/parse_cardinality.py INPUT.csv --output evidence/cardinality/run-STAMP/cardinality --limit 34
nmap -Pn -sS --min-rate 100 --max-retries 0 -T4 -p 1-20 192.168.56.20
```

La lista reproducible completa está en [commands_used.md](commands_used.md).

## Publicación pendiente

Salida del gate remoto:

```text
remote: Repository not found.
fatal: repository 'https://github.com/Reynaldo8509/soc-operations-lab.git/' not found
```

Para publicar, confirmar que ese repositorio existe y que la cuenta autenticada
tiene acceso; después ejecutar `git push origin HEAD:main` o publicar la rama
de revisión `publish/finalize-evidence-20260815-210501`. Esta rama parte del
estado validado de cardinalidad, no de `main`, porque esos commits aún no están
en el remoto. No se debe cambiar la URL del remoto sin confirmar el destino
correcto.
