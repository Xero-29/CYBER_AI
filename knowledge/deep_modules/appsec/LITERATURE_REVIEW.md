# Revisión de literatura inicial — Seguridad de aplicaciones y API

**Corte:** 2026-11-17  
**Madurez:** M1 (fuentes primarias identificadas y páginas oficiales revisadas); no M3/M4.  
**Alcance:** verificación de controles web/API, autorización, autenticación, gestión de datos y pruebas.  
**Limitación:** revisión exploratoria dirigida, no revisión sistemática ni lectura íntegra de todos los estándares.

## Síntesis y pregunta

¿Cómo convertir estándares y taxonomías de riesgo web/API en requisitos verificables que detecten fallos de autorización y exposición de datos sin confundir cobertura de checklist con seguridad efectiva?

La evidencia consultada apunta a separar tres capas: (1) requisitos verificables de controles (OWASP ASVS), (2) taxonomía de riesgos API (OWASP API Security Top 10 2023) y (3) pruebas específicas de la implementación y su contexto. ASVS 5.0.0 es la versión estable publicada el 30-05-2025 y declara como propósito normalizar requisitos para diseñar, desarrollar y probar aplicaciones web y servicios. API Top 10 2023 incluye riesgos diferenciados de autorización a nivel de objeto, propiedad y función; el listado también incorpora consumo ilimitado, flujos de negocio sensibles, SSRF, inventario deficiente y consumo inseguro de APIs.

**Conclusión técnica:** ASVS debe servir como catálogo versionado de requisitos de verificación; API Top 10, como mapa de riesgos; ninguno sustituye el modelado de amenazas, la revisión del código, las pruebas negativas por identidad/objeto/propiedad ni la validación del comportamiento en el entorno real. Los identificadores de requisitos deben llevar versión, ya que pueden cambiar entre releases.

## Fuentes primarias revisadas

| ID | Fuente | Estado de revisión | Uso y límite |
|---|---|---|---|
| OWASP-ASVS-5.0 | https://asvs.owasp.org/ | Página oficial de proyecto, versión y objetivos revisados; el estándar completo no se declara leído | Base de requisitos de verificación; fijar versión 5.0.0 |
| OWASP-API-TOP10-2023 | https://owasp.org/www-project-api-security/ | Página oficial y categorías revisadas | Taxonomía de riesgos, no prevalencia universal ni checklist exhaustivo |
| OWASP-API1-BOLA | https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/ | Página de riesgo revisada | Justifica pruebas de autorización por cada acceso a objetos identificados por el cliente |

## Taxonomía operacional

1. **Identidad y sesión:** autenticación, recuperación, rotación/revocación, expiración, MFA cuando aplique.
2. **Autorización:** objeto (BOLA), propiedad (BOPLA), función (BFLA), tenant y relaciones entre sujetos/recursos.
3. **Datos:** clasificación, minimización, filtrado de salida, protección en tránsito/reposo y secretos.
4. **Entrada y ejecución:** validación contextual, inyección, SSRF, deserialización, parser diferencial.
5. **Disponibilidad y abuso:** límites por usuario/tenant, cuotas, concurrencia, coste de operaciones y flujos de negocio.
6. **Ciclo de vida API:** inventario, versiones, endpoints obsoletos, dependencias y confianza en APIs de terceros.
7. **Verificación:** SAST/SCA/DAST, pruebas manuales, pruebas de contrato, regresión y observabilidad.

## Hipótesis investigables

- H1: pruebas de autorización con matriz sujeto–objeto–acción–tenant encuentran más defectos de control de acceso que pruebas de endpoints sin matriz explícita.
- H0: no existe diferencia medible bajo el protocolo definido.
- H2: mapear cada requisito ASVS a prueba automatizada o evidencia manual mejora trazabilidad, pero no necesariamente reduce por sí solo la tasa de defectos escapados.

## Protocolo experimental propuesto (no ejecutado)

- **Banco:** aplicación deliberadamente vulnerable local, dos roles y dos tenants con datos sintéticos; sin conexión a objetivos externos.
- **Comparadores:** (A) pruebas funcionales convencionales; (B) pruebas con matriz de autorización; (C) matriz más requisitos ASVS seleccionados.
- **Muestras:** mismos endpoints, casos, versión de aplicación y datos; orden aleatorizado de ejecución cuando sea viable.
- **Variables:** independiente = método de prueba; dependientes = defectos sembrados detectados, falsos positivos, tiempo, cobertura de combinaciones y defectos escapados.
- **Métricas:** recall sobre defectos sembrados, precision, F1, tiempo por hallazgo, cobertura sujeto/objeto/acción/tenant, severidad y reproducibilidad.
- **Control:** congelar commit, configuración, dataset, versiones y semillas; repetir al menos 3 veces; documentar desviaciones.
- **Criterio:** no afirmar superioridad sin intervalos de incertidumbre y análisis de validez.

## Brechas y trabajo siguiente

- Descargar y revisar el texto completo de ASVS 5.0.0 y archivar CSV/JSON con licencia, versión y SHA-256.
- Incorporar documentación específica de OAuth/OIDC, sesiones, GraphQL, gRPC y autorización multi-tenant.
- Añadir estudios revisados por pares y comparar herramientas con un benchmark público y reproducible.
- Ejecutar el laboratorio y publicar casos, resultados brutos saneados y análisis.
- Revisión técnica independiente antes de elevar a M4.

## Referencias

- OWASP Foundation, *Application Security Verification Standard 5.0.0*, estable 2025-05-30. https://asvs.owasp.org/
- OWASP Foundation, *API Security Top 10 2023*. https://owasp.org/www-project-api-security/
- OWASP Foundation, *API1:2023 Broken Object Level Authorization*. https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/


## Identificadores del registro de fuentes

- `OWASP-ASVS-5.0.0`
- `OWASP-API-TOP10-2023`
- `OWASP-API1-BOLA-2023`
