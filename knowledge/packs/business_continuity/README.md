# Continuidad de negocio y recuperación ante desastres — Guía de dominio

**ID:** `business_continuity` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito
Mantiene servicios críticos durante interrupciones y recupera operaciones dentro de objetivos aprobados. La continuidad incluye personas, procesos, proveedores, instalaciones, datos y tecnología. Tener backups no equivale a poder recuperar un servicio.

## Competencias
- Realizar BIA y clasificar procesos críticos.
- Definir RTO, RPO, MTPD y dependencias.
- Diseñar DR por zona/región/proveedor.
- Proteger backups, claves, runbooks y comunicaciones.
- Ensayar failover, restauración y operación degradada.
- Gestionar proveedores, capacidad y recursos alternativos.
- Coordinar crisis, comunicaciones y toma de decisiones.

## Controles
- BIA actualizado y propietario por servicio.
- RTO/RPO aprobados y medidos.
- Backups cifrados, aislados y protegidos contra borrado.
- Copias de configuración, secretos y dependencias.
- Runbooks versionados y accesibles fuera del entorno principal.
- Canales alternos y suplencias.
- Capacidad reservada y pruebas de failover.
- Retención y restauración verificadas, no solo jobs exitosos.

## Metodología
1. Identificar procesos, clientes, impacto y obligaciones.
2. Mapear sistemas, personas y proveedores dependientes.
3. Definir BIA, RTO/RPO y escenarios.
4. Seleccionar estrategia: backup/restore, pilot light, warm/hot standby.
5. Preparar runbooks, contactos y criterios de activación.
6. Ensayar restauración con datos sintéticos.
7. Medir tiempo real, pérdida y errores.
8. Corregir brechas y repetir simulacro.
9. Reportar resultados y aceptar riesgo residual.

## Laboratorio
Servicio ficticio con base SQLite, almacenamiento de archivos y configuración. Crear backup, simular pérdida, restaurar en entorno alterno y medir RTO/RPO.

## Evaluación
Restauración reproducible, RTO/RPO demostrados, runbooks disponibles y responsabilidades claras.

## Referencias
ISO 22301, NIST SP 800-34, NIST SP 800-184, FFIEC business continuity y CISA resilience guidance.

## Instrucciones para agentes IA
No apagues servicios ni restaures producción. Los ejercicios usan copias y entornos aislados; la activación de DR requiere autoridad humana.