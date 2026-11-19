# Foundations labs — ejecución reproducible

## Alcance y seguridad
Los siete laboratorios usan datos sintéticos y prototipos locales deterministas; no escanean redes ni se conectan a IdP/KMS/SIEM reales, no usan credenciales externas ni modifican servicios. Se incorporaron dos mecanismos ejecutables de referencia con primitivas reales de Python: verificación JWS HS256 y cadena de auditoría HMAC.

Desde la raíz del repositorio:

```bash
python -m knowledge.deep_modules.foundations.labs.runner
python -m unittest discover -s tests -p test_foundations_labs.py -v
```

Semilla fija: `20261119`. El runner imprime JSON. Los resultados de referencia están en `results.json`.

| Laboratorio | Qué valida | Qué no valida |
|---|---|---|
| LAB-FND-01A | Invalidación de caché y denegación por defecto | Consistencia distribuida real |
| LAB-FND-02A | Claves estables frente a colisiones de hostname | Calidad de fuentes reales |
| LAB-FND-03A | Cobertura de rutas de ataque modeladas | Explotabilidad o exhaustividad |
| LAB-FND-04A | Verificación JWS HS256, alg/type/header allowlist estrictos, base64url canónico, issuer, audience, exp, nbf, scope, jti/revocación y JSON duplicado | JWKS/rotación, firmas asimétricas, discovery OIDC, servidor OAuth, TLS o integración IdP |
| LAB-FND-05A | HMAC-SHA-256, integridad/autenticidad y alteración | Cifrado, AES, KMS o validación FIPS |
| LAB-FND-06A | Ordenamiento/deduplicación más cadena HMAC encadenada con detección de alteración/reordenamiento | Ingesta SIEM, timestamps confiables, atribución o no repudio |
| LAB-FND-07A | Evidencia caducada/contradictoria no cierra controles | Auditoría organizacional real |

Un test que pasa demuestra solo el comportamiento del harness bajo sus supuestos. No extrapolar resultados sintéticos a producción.

## Reproducción limpia y límites

La suite de Foundations usa exclusivamente la biblioteca estándar de Python. El job dedicado ejecuta la suite en runners limpios para Python 3.11, 3.12 y 3.13 y compara el resultado calculado con `results.json`. Esto prueba consistencia entre versiones del runtime bajo CI, pero **no equivale a reproducción por un operador externo** ni a interoperabilidad con un proveedor real.

`LAB-FND-04A` implementa verificación JWS HS256 de referencia: firma antes de claims, algoritmo/tipo permitidos, issuer/audience, expiración, not-before, scope, revocación por jti y rechazo de miembros JSON duplicados. No debe usarse como biblioteca JWT de producción: no incluye JWKS, rotación, algoritmos asimétricos, discovery, gestión de claves, OAuth server ni OIDC completo.

`LAB-FND-06A` implementa cadena de eventos HMAC con secuencia y MAC anterior. Detecta alteración y reordenamiento dentro de la cadena; no proporciona no repudio, protección si la clave se compromete, ni garantía de tiempo/ingesta.
