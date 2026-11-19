# Foundations labs — ejecución reproducible

## Alcance y seguridad
Los siete laboratorios son simulaciones deterministas con datos sintéticos. No escanean redes, no se conectan a IdP/KMS/SIEM reales, no usan credenciales ni modifican servicios externos.

Desde la raíz del repositorio:

```bash
python -m knowledge.deep_modules.foundations.labs.runner
python -m unittest tests.test_foundations_labs -v
```

Semilla fija: `20261119`. El runner imprime JSON. Los resultados de referencia están en `results.json`.

| Laboratorio | Qué valida | Qué no valida |
|---|---|---|
| LAB-FND-01A | Invalidación de caché y denegación por defecto | Consistencia distribuida real |
| LAB-FND-02A | Claves estables frente a colisiones de hostname | Calidad de fuentes reales |
| LAB-FND-03A | Cobertura de rutas de ataque modeladas | Explotabilidad o exhaustividad |
| LAB-FND-04A | Issuer, audience, expiry, scope y revocación simulados | Firma JWT u OAuth/OIDC real |
| LAB-FND-05A | HMAC-SHA-256, integridad/autenticidad y alteración | Cifrado, AES, KMS o validación FIPS |
| LAB-FND-06A | Ordenamiento, deduplicación y completitud | Detección o atribución real |
| LAB-FND-07A | Evidencia caducada/contradictoria no cierra controles | Auditoría organizacional real |

Un test que pasa demuestra solo el comportamiento del harness bajo sus supuestos. No extrapolar resultados sintéticos a producción.
