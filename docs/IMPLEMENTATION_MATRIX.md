# Matriz vigente de implementación y cierre — CYBER_AI

**Corte:** 2026-11-17  
**Rama:** `main`  
**Referencia de código y CI anterior a esta actualización documental:** `0767cd68d418f7bfbb69bbe336106a9e869de563`.  
**Regla:** los estados de CI solo validan el SHA indicado; los estados de catálogo, simulación y pruebas unitarias no equivalen a validación operacional.

## Definiciones de estado

- **Implementado:** existe código versionado para la función.
- **Integrado:** existe un consumidor real en el flujo del producto; una entrada de catálogo no basta.
- **CI aprobado:** el workflow pasó sobre el SHA exacto.
- **Validación operacional pendiente:** requiere binarios, proveedores, credenciales, datos, infraestructura o revisión independiente.
- **Bloqueado:** una política de seguridad o una dependencia no satisfecha impide ejecutar la capacidad.

## Resumen ejecutivo

| Subsistema | Estado comprobable | Límite principal |
|---|---|---|
| CLI y flujo de agentes | Implementado e integrado | Calidad semántica con modelos reales no evaluada |
| Proveedores LLM | Cuatro familias integradas más plugins | Pruebas reales de cuotas, latencia, coste, fallos y privacidad pendientes |
| Conocimiento | 48 paquetes offline y 48 perfiles de dominio | Profundidad no validada; no es corpus experto exhaustivo |
| Investigación | 48 agendas y 48 dossiers exploratorios M1 | No son revisiones sistemáticas ni investigación empírica |
| Recuperación | SQLite/FTS, embeddings y recuperación híbrida | Benchmark experto de relevancia y embeddings reales pendiente |
| Herramientas | 21 declaradas; 20 IDs TOOL_SPECS; Nuclei separado | Binarios/bases no garantizados; aislamiento host general pendiente |
| Memoria y Skills | Ledger, memoria verificada, Skillbook y auditoría | Firmante KMS/HSM, identidad y doble control pendientes |
| Pruebas automatizadas | 594 pruebas, 1 omitida en Python CI del SHA citado | No demuestran eficacia semántica ni seguridad operacional |
| Sandbox | YARA/TShark con Docker endurecido | Docker comparte kernel; no es una microVM |
| Operación institucional | Backups, preflight, SBOM y evidencia local implementados parcialmente | DR, WORM, RBAC/MFA, KMS/HSM, carga y revisión independiente pendientes |

## Flujo principal

| Capacidad | Estado | Evidencia y límite |
|---|---|---|
| `cyber_ai.py --ask` → DIRECTOR → especialista | Implementado e integrado | Enrutamiento y recuperación por defecto; selección semántica avanzada y calidad real no medidas |
| `cyber_ai.py --team` → planificador → orquestador | Implementado e integrado | Orquestación, supervisión, plan de capacidades y simulación determinista; simulación no prueba razonamiento real |
| Proveedor LLM intercambiable | Parcialmente integrado | Ollama, OpenAI-compatible, Anthropic y Gemini; otros proveedores requieren plugin compatible. Fallback actual es por capacidad/configuración, no reintento robusto de fallos transitorios |
| Recuperación de conocimiento y Skills | Integrada | Requiere configurar proveedor de embeddings e indexar; calidad de recuperación no validada con dataset experto |
| Herramientas → evidencia → validación → ledger | Parcialmente integrado | Ejecución opt-in; la salida de la herramienta es evidencia no confiable y la validación estructural no demuestra verdad del hallazgo |
| Escaneo remoto Nuclei | Runner independiente | Autorización explícita y ledger; DNS bloqueado hasta pinning y control de egress adecuados |

## Conocimiento e investigación

| Elemento | Estado | Criterio que falta |
|---|---|---|
| Paquetes offline | 48/48 presentes | Revisión técnica específica por subtema y actualización continua |
| Perfiles de dominio | 48/48 conectados al manifiesto | No prueban cobertura operativa |
| Módulos de profundización | 48/48 con estructura y compendio | Contenido específico, fuentes leídas y validación experta |
| Agendas de investigación | 48/48 | Ejecutar estudios y publicar resultados reproducibles |
| Dossiers bibliográficos | 48/48 exploratorios M1 | No elevar a revisión sistemática sin protocolo ejecutado |
| Matriz de cobertura global | 48 áreas y 61 familias de referencia mapeadas | La profundidad permanece `not_assessed_by_this_crosswalk` |
| Registro de fuentes de investigación | 138 fuentes observadas en el último preflight | 0 revisadas; 276 verificaciones pendientes según auditoría de procedencia de ese SHA; licencias y lectura integral sin aprobar |
| Recuperación semántica | Código implementado | Benchmark etiquetado por especialistas, métricas y umbrales por dominio |
| Extracción documental | Formatos soportados parcialmente | OCR y parsers aislados; fixtures reales PDF/Office y validación de documentos hostiles |

Los paquetes editoriales, agendas y fuentes catalogadas no deben presentarse como conocimiento experto exhaustivo. La descarga externa continúa deshabilitada hasta aprobar procedencia, licencia, integridad y política de egreso.

## Herramientas y aislamiento

| Grupo | Recuento/estado | Límite |
|---|---|---|
| Catálogo | 21 herramientas declaradas | Catálogo no significa instalación |
| Registro local | 20 IDs en `TOOL_SPECS` | Adaptador no significa ejecución lista |
| Adaptadores host | 17: 16 local/offline y Nmap scoped | No hay sandbox general de host |
| pip-audit | Registrado, bloqueado | Política de red específica pendiente |
| YARA/TShark | Runner Docker aislado | Docker comparte kernel; amenaza hostil requiere frontera más fuerte |
| Nuclei | Runner remoto separado | Egress allowlist y DNS pinning pendientes |
| OSV-Scanner/Grype | Adaptadores offline con preflight read-only obligatorio | OSV valida ZIP/ecosistemas pero frescura y esquema quedan desconocidos por límites del formato; Grype valida schemaVersion, built, ruta local y antigüedad máxima de 14 días (configurable) |
| Nmap | CIDR/IP allowlisted y escaneo TCP limitado | Aislamiento egress de sistema operativo no impuesto |
| Herramientas personalizadas | Registro declarativo | No se puede garantizar que no accedan a red; evidencia declara `network_access=not_enforced` |

## Memoria, Skills y evidencia

| Capacidad | Estado | Límite |
|---|---|---|
| Ledger de ejecuciones | Implementado | Checkpoints externos inmutables y restauración independiente pendientes |
| Memoria de lecciones | Verifica firma/evidencia contra ledger | Custodia y rotación de claves externas pendientes |
| Skillbook | Verifica historial append-only y snapshot vigente | Dataset real de regresión con juicios independientes pendiente |
| Promoción de Skills | Flujo controlado con aprobación HMAC | HMAC no ofrece identidad individual, KMS/HSM ni doble control |
| Auditoría del ciclo | Read-only, con diagnóstico de memoria, ledger y Skills | No sustituye monitorización continua ni revisión humana |

## Seguridad, resiliencia y gobierno

| Control | Estado | Cierre requerido |
|---|---|---|
| Autorización de herramientas | Parcial, opt-in y alcance explícito | Política común fail-closed e identidad/roles |
| Allowlist ejecutables | HMAC opcional por compatibilidad; modo obligatorio configurable | Enrolamiento confiable, rotación, revocación y mitigación TOCTOU |
| Aislamiento de ejecución | YARA/TShark en Docker | Runner común host, microVM/VM para cargas no confiables |
| Aislamiento de red | Docker network none para YARA/TShark | Firewall/namespace para Nmap y Nuclei, DNS pinning |
| Secretos | Variables externas y recomendaciones documentadas | Secret manager/KMS, rotación y revocación demostradas |
| Backups | Integridad y restauración local implementadas | Cifrado, off-host, DR y simulacro de pérdida |
| Identidad y acceso | No demostrado end-to-end | RBAC, IdP, MFA, segregación de funciones |
| Observabilidad | Logs/evidencia local | Métricas, trazas, alertas, retención y redacción |
| Resiliencia | Pruebas unitarias/transacciones parciales | Load, soak, concurrencia, disco lleno, pérdida de host y RPO/RTO |
| Gobernanza | Threat model y release gates documentados | Revisión independiente, protección de rama y aceptación formal de riesgos |

## Evidencia CI por SHA

| SHA | Workflow | Resultado | Qué demuestra |
|---|---|---|---|
| `0767cd68d418f7bfbb69bbe336106a9e869de563` | [Python tests #44181807943](https://github.com/Xero-29/CYBER_AI/actions/runs/44181807943) | Success; 594 pruebas, 1 omitida | Suite Python, preflight, verificaciones y artefacto SBOM del workflow |
| `0767cd68d418f7bfbb69bbe336106a9e869de563` | [Docker sandbox #44181807961](https://github.com/Xero-29/CYBER_AI/actions/runs/44181807961) | Success | Build/smoke del sandbox y artefacto de evidencia |
| `125f6a21fa08c38188b2d4ce8fe52ceb95fe7c05` | [Python #44179945373](https://github.com/Xero-29/CYBER_AI/actions/runs/44179945373) | Success | Suite del commit anterior |
| `125f6a21fa08c38188b2d4ce8fe52ceb95fe7c05` | [Docker #44179945273](https://github.com/Xero-29/CYBER_AI/actions/runs/44179945273) | Success | Sandbox del commit anterior |

## Próximas acciones

1. Corregir y mantener sincronizados README, estado del proyecto, inventario y matriz (Fase 0).
2. Extender la verificación OSV con procedencia de descarga/build cuando OSV publique metadatos verificables; el estado actual declara frescura/esquema desconocidos. Mantener Grype con preflight de metadatos y antigüedad fail-closed.
3. Diseñar runner común aislado y separar Nmap/Nuclei en perfiles de red con enforcement de firewall/egress.
4. Construir benchmark real de recuperación y selector de agentes; revisar contenido de los 48 dominios.
5. Añadir firma externa e identidad al ciclo de Skills.
6. Ejecutar validación operacional, DR, carga y revisión independiente antes de piloto.

## Regla de actualización

Cada cambio de estado debe enlazar al código, pruebas y SHA exacto. No se marca como validado por existir un archivo, una entrada de catálogo, un mock o una simulación. Los estados que dependen de infraestructura deben permanecer abiertos hasta adjuntar evidencia operacional.
