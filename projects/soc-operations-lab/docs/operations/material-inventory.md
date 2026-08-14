# Inventory and Publication Decision

This inventory classifies the material reviewed while preparing the repository. Originals were neither moved nor deleted.

| Source / Set | Category | Purpose | Public Value | Sensitivity / Decision |
|---|---|---|---|---|
| `ContextoIA/contexto_anterior.md` | I, D, E, F | Extensive technical history of changes and troubleshooting. | High as a knowledge source. | May contain operational material; extract knowledge, do not copy. |
| `ContextoIA/transcripcion_completa.md`, `.txt`, `transcripcion_wazuh.txt` | I, L | Full session transcripts. | Low in raw form. | Do not publish; private source of verified decisions. |
| `ContextoIA/contexto_maestro.md` | H, J, K | Summary of contexts from multiple tasks. | Medium. | Historical and mixed with unrelated material; use only for corroboration, do not copy. |
| `ContextoIA/WFP_PortScan_Detection_Final.md` | D, H | WFP technical report. | High. | Transformed into `detection-rules/WFP_PortScan_Detection_Final.md`; always review before publishing. |
| `ContextoIA/Proyecto SOC WASU/.../events-*.csv` | G, L | Event export. | Potentially high. | Do not copy until fields, dates, and identifiers are sanitized. |
| `/mnt/DATOS/REY/Ciberseguridad/Proyecto SOC WASU/Capturas de pantalla/Ubuntu/...` | G, L | 53 currently available installation, Wazuh, and Windows screenshots. | Potentially high after individual review. | Eight curated artifacts are published in `evidence/screenshots/`; some are safe crops rather than byte-for-byte copies. The rest remain outside the repository because of sensitivity, lack of context, contradiction with the final status, or low documentary value. See `evidence/image-catalog.md`. |
| `ContextoIA/*/MEMORY.md`, `raw_memories.md`, `memory_summary.md` | I, L | Agent memory and internal summaries. | Low. | Never publish. |
| `ContextoIA/memories_root_backup.sqlite` | I, L | Internal memory copy. | None. | Never publish. |
| Historical repository screenshots (`fase1_repo_ready.png`, SHA-256 `3ae74ac…bf64cbf82`; `fase1_repo2_ready.png`, SHA-256 `a623425e…26662a25`) | G, L | Initial repository preparation. | None. | **UNSAFE_TO_PUBLISH**: visual review showed a local username/path and GitHub authentication screen. Both original copies were preserved outside the repository; their exact duplicates are not published. |
| Placeholders `scenario-1-bruteforce/attack.png`, `wazuh-alert.png`, and `logs.json` (0 bytes; SHA-256 `e3b0c442…b855`) | F, G, J, K | Empty historical structure. | None. | Removed from the repository: they are neither evidence nor publishable content. |
| 53 screenshots under the identified source directory | G, I, L | Historical installation, operations, and tests. | Eight are useful as public visual evidence. | Individual review: eight curated artifacts are published; the catalog classifies the remaining ones as **B**, **C**, or **D**. Originals were not modified. |
| `evidence/screenshots/` (8 files) | G, H | Curated visual evidence of architecture, Wazuh, WFP, and Sysmon. | High, with explicit scope. | **PUBLISH_AS_IS**: real visual review, with no passwords, tokens, keys, cookies, authentication codes, login screens, public addresses, or addresses from the excluded private range. ATTACK/LAB and NAT private IPs are retained as part of the documented architecture. |
| `evidence/scenario-1-bruteforce/` | F, K | Initial-scenario documentation marker. | Low. | README only; must not be used as proof. |
| `detection-rules/WFP_PortScan_Detection_Final.md` | D, H | Validated WFP detection. | High. | Publishable: contains sanitized results and cardinality limitations, and includes no secrets. |

## Legend

- **D** detection, **E** troubleshooting, **F** tests, **G** evidence, **H** documentation, **I** internal transcript, **J** duplicate, **K** obsolete/incomplete, **L** sensitive or requires review.

The historical source remains outside the repository. Public documentation presents validated results and limitations, not conversations or raw operational data.
