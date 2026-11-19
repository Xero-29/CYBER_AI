# Secciones de profundización — Seguridad cloud

## Modelo de amenazas
Distinguir responsabilidad del proveedor y cliente, organización/cuentas/proyectos/subscriptions, IAM, control plane, redes virtuales, workloads, datos, metadata services y servicios gestionados. Amenazas: exposición pública, roles excesivos, credenciales temporales robadas, abuso de APIs, supply chain de imágenes, secretos en pipelines, snapshots expuestos y control plane comprometido. Incluir terceros y regiones.

## Detección
Habilitar audit logs del control plane, IAM, cambios de políticas, actividad de red, acceso a objetos, KMS, workloads y posture management. Correlacionar principal, sesión, origen, recurso, región, API y resultado. Detectar creación de credenciales, cambios de trust policy, exposición pública, desactivación de logs y extracción masiva. Verificar cobertura multi-account y retención fuera del tenant comprometible.

## Respuesta a incidentes
Preservar logs de organización y proveedor, snapshots y metadatos; suspender o limitar identidades comprometidas; revocar sesiones/keys; bloquear egress y exposición; identificar recursos creados y persistencia IAM; rotar secretos y claves; reconstruir workloads desde artefactos firmados. No borrar cuentas ni recursos antes de preservar evidencia. Validar restore y controles de organización.

## Casos prácticos
Un bucket de laboratorio queda público tras cambio de política. Detectar el evento de control plane, enumerar objetos sintéticos expuestos, retirar acceso público, revisar copias/replicas y principal que ejecutó el cambio. Añadir policy-as-code y test preventivo. Otro caso simula token temporal filtrado en CI y evalúa alcance de permisos y revocación.

## Referencias
Consultar [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para NIST SP 800-53/800-207, CIS cloud benchmarks, documentación oficial del proveedor y CSA CCM. Indicar proveedor, servicio, región y fecha de la referencia.
