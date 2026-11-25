# CYBER_AI — MVP comercial y despliegue inicial

**Estado:** diseño de implementación; no es una declaración de que la plataforma comercial esté implementada ni lista para producción.  
**Capital máximo inicial:** USD 300, sin contar impuestos, comisiones ni variaciones de precio.  
**GPU elegida:** NVIDIA L40S de 48 GB bajo demanda.  
**Modelo comercial:** créditos prepago + membresías con cuota incluida.  
**Objetivo:** obtener los primeros usuarios e ingresos sin comprometer el capital en GPU ociosa.

## 1. Decisión ejecutiva

Lanzar una versión comercial pequeña y limitada, separada de los ejecutores internos de CYBER_AI:

- Sitio público estático en Cloudflare Pages.
- API comercial y PostgreSQL en un VPS pequeño independiente.
- Inferencia en una L40S alquilada bajo demanda.
- Ollama como primer servidor compatible con API OpenAI, reutilizando los adaptadores existentes.
- Enrutador multi-modelo de CYBER_AI, pero con una sola carga conversacional activa inicialmente.
- Wompi como primera opción de cobro en Colombia, sujeto a aprobación de cuenta y pruebas de desembolso.
- Créditos prepago y membresías con cupos finitos; nunca ofrecer uso ilimitado en esta fase.

No desplegar directamente `cyber_ai.py --team`, `tool_executor.py`, escáneres ni adaptadores host en el servicio público. La primera versión comercial solo ofrece tareas de análisis no destructivo, consulta de conocimiento y generación de informes con herramientas deshabilitadas.

## 2. Lo que ya existe y lo que falta

El repositorio ya incluye configuración de roles en `config/model_roles.json`, DIRECTOR, agentes, adaptadores de proveedores, biblioteca e indexación, memoria/Skills, ledger y pruebas. La política de recursos actual declara `max_chat_models_loaded: 1`, lo que coincide con la estrategia inicial de carga secuencial.

Brechas que bloquean producción comercial:

1. No hay evidencia suficiente de aislamiento multi-tenant de extremo a extremo para exponer memoria, historial, documentos o Skills de distintos clientes.
2. Falta una API comercial con autenticación, cuentas, saldo, cuotas, límites y conciliación de pagos.
3. Falta una integración de pagos con webhooks verificados e idempotencia.
4. Falta control global de concurrencia, límites de tokens/tiempo y apagado automático de GPU.
5. Falta despliegue reproducible, monitorización, alertas, backups y procedimiento de incidentes.
6. Las pruebas de AI Red Team recientes son parciales; el modelo Qwen 3.5 2B no debe anunciarse como validado.
7. El repositorio declara que no es una versión certificada para producción. El lanzamiento debe describirse como beta limitada.

## 3. Arquitectura de despliegue

```text
Internet
  |
  +-- Cloudflare DNS / TLS / WAF básico
  |
  +-- Cloudflare Pages (frontend React/Vite)
  |
  +-- api.cyber-ai... (VPS, HTTPS)
        |
        +-- Auth + API comercial
        +-- PostgreSQL
        +-- Ledger de pagos y uso
        +-- Cola simple / límite de concurrencia
        |
        +-- HTTPS autenticado --> RunPod L40S (Ollama)
                                  |
                                  +-- modelos de chat
                                  +-- modelo de embeddings
                                  +-- API compatible OpenAI
```

### Componentes

- **Frontend:** React + Vite, desplegado como estático. Páginas: Inicio, Laboratorio, Capacidades verificadas, Precios, Registro, Acceso, Panel, Historial y Estado del servicio.
- **API comercial:** servicio Python independiente (FastAPI) en el VPS. No importar ni ejecutar comandos arbitrarios desde el navegador.
- **Datos:** PostgreSQL en el VPS para cuentas, productos, pagos, libro de créditos y agregados de uso. Backups diarios cifrados y restauración probada.
- **GPU:** RunPod L40S 48 GB. Instancia bajo demanda, no reservada. Ollama inicialmente por compatibilidad con el endpoint OpenAI que ya usa el proyecto.
- **Conexión API-GPU:** endpoint privado o protegido con TLS y token rotatorio; no publicar el puerto de Ollama sin autenticación. El frontend nunca recibe la URL ni la clave de GPU.
- **Sitio y DNS:** Cloudflare Pages/ DNS; no alojar el frontend en la GPU.
- **Secretos:** variables de entorno del VPS y secretos del proveedor; nunca en Git, imágenes Docker, frontend o logs.

## 4. Selección multi-modelo inicial

Usar los roles existentes como candidatos, sujetos a benchmark real en L40S:

| Rol | Modelo candidato | Uso |
|---|---|---|
| NEXO | qwen3.5:4b-q4_K_M | Coordinación y análisis general |
| INVESTIGADOR | qwen3.5:2b-q4_K_M | Investigación ligera |
| FORJA | qwen2.5-coder:3b | Código y pruebas de laboratorio |
| FILTRO | qwen2.5:1.5b | Revisión crítica |
| VERITAS | granite3.3:2b | Revisión de evidencia |
| FARO | qwen3.5:0.8b | Supervisión ligera |
| ECO | qwen3-embedding:0.6b | Embeddings |

No activar todos los roles comercialmente desde el primer día. Comenzar con NEXO, VERITAS y ECO; habilitar FORJA solo en un entorno aislado y con tareas acotadas. Los demás roles se habilitan tras pruebas.

La L40S tiene 48 GB, pero no implica que todos los modelos deban quedar residentes. Mantener una carga conversacional activa, cambio controlado de modelo, cola pequeña y límites de concurrencia. Separar el proceso de embeddings si las mediciones muestran contención de VRAM.

Antes de anunciar una capacidad, registrar: modelo exacto y cuantización, tokens/s, tiempo hasta primer token, duración, VRAM máxima, errores, coste GPU imputado y puntuación de evaluación. No afirmar calidad experta por tamaño del modelo o por el número de agentes.

## 5. Presupuesto de USD 300

Presupuesto de control, no cotización garantizada:

| Partida | Tope |
|---|---:|
| L40S para pruebas y primeras sesiones | USD 70 |
| VPS API + PostgreSQL (primer periodo) | USD 20 |
| Dominio/DNS y gastos de publicación | USD 15 |
| Campaña inicial de adquisición | USD 100 |
| Materiales/edición básica | USD 15 |
| Reserva de operación y GPU | USD 80 |
| **Total** | **USD 300** |

La tarifa consultada de RunPod para L40S en Pods es aproximadamente USD 1.09/h. USD 70 equivalen a unas 64 horas antes de almacenamiento, impuestos u otros cargos. La tarifa y disponibilidad deben confirmarse al crear el Pod. Serverless L40S aparece desde aproximadamente USD 1.89/h; no usarlo sin recalcular el coste por tarea.

**Reglas de gasto:**
- No activar una GPU 24/7.
- Primera autorización de gasto GPU: máximo USD 15 para despliegue y benchmark.
- Segundo tramo: hasta USD 25 para demos y pruebas con usuarios invitados.
- Liberar el resto del presupuesto GPU solo si hay usuarios activos, coste por tarea medido y saldo suficiente.
- Configurar alertas de gasto y apagar el Pod al terminar cada sesión.
- No financiar anuncios con la reserva de operación.

## 6. Monetización: créditos + membresías

### Créditos prepago
- Paquetes de compra pequeños y claros (por ejemplo USD 5, USD 10 y USD 25).
- Los créditos se descuentan por consumo medido, no por número arbitrario de mensajes.
- El coste debe incluir tokens de entrada/salida, tiempo GPU, embeddings, almacenamiento y comisiones.
- Mostrar antes de ejecutar una estimación de consumo; mostrar después el consumo real.
- No permitir saldo negativo. Aplicar límites diarios y máximos por solicitud.

### Membresías
- Plan mensual de entrada y plan profesional, cada uno con una cuota mensual finita de créditos.
- La suscripción no incluye uso ilimitado.
- Los créditos incluidos vencen o se acumulan según condiciones visibles y legalmente revisadas.
- Las compras de créditos adicionales se mantienen separadas de la renovación mensual.
- Cancelación sencilla y aviso de renovación/precio.

No fijar la cantidad de créditos incluida en cada plan hasta medir al menos 50 tareas representativas en L40S. Definir el precio con margen sobre el coste variable real y revisar la tasa de reembolso.

### Wompi
Wompi publica para su Plan Avanzado una tarifa de 2,65 % + COP 700 + IVA por transacción exitosa. Su ayuda indica que para persona natural el primer desembolso ocurre 30 días después de la primera transacción; los siguientes, al siguiente día hábil. Confirmar elegibilidad, documentos, límites y calendario antes de depender de esos fondos para pagar la GPU. No asumir que el pago del cliente queda disponible inmediatamente.

### Integridad de pagos
- Crear una orden pendiente en la API antes de enviar al checkout.
- Confirmar el pago exclusivamente mediante webhook verificado; no confiar en el redirect del navegador.
- Validar firma, monto, moneda, referencia, estado y destinatario.
- Procesar webhooks idempotentemente usando el identificador del proveedor.
- Registrar eventos append-only; no permitir que un cliente modifique su saldo.
- Conciliar diariamente órdenes, transacciones, devoluciones y créditos.
- Emitir recibo/confirmación y conservar política de reembolso visible.

## 7. Datos, privacidad y aprendizaje

En la beta:
- No usar prompts, documentos o resultados de clientes para entrenar modelos por defecto.
- No almacenar contenido de conversaciones salvo que sea necesario y esté informado.
- Registrar métricas operativas minimizadas: modelo, tokens, duración, coste, estado, códigos de error y consumo.
- Separar telemetría de contenido y de datos de entrenamiento.
- Solicitar consentimiento explícito separado para aportar ejemplos al programa de mejora.
- Permitir retirar el consentimiento y definir retención/borrado.
- No recopilar credenciales, secretos, datos personales innecesarios ni muestras de redes reales.
- No publicar logs, direcciones IP, correos, nombres ni prompts de usuarios en vídeos.
- Revisar obligaciones colombianas de protección de datos (Ley 1581 y normas aplicables), términos de servicio, privacidad, facturación e impuestos antes de cobrar.

Los datos autorizados para mejora deben pasar por redacción, clasificación, deduplicación, evaluación y aprobación humana. Una interacción exitosa no se convierte automáticamente en una Skill ni en conocimiento validado.

## 8. Seguridad mínima de la beta

- Deshabilitar herramientas, ejecución de código, escaneo de red y acciones externas para usuarios públicos.
- No aceptar objetivos de terceros ni permitir escaneo remoto.
- No habilitar subida de archivos en la primera versión; añadirla solo después de validar aislamiento y análisis seguro.
- API con autenticación, autorización por cuenta, límites por IP/cuenta, CSRF cuando aplique, CORS restrictivo y validación de entrada.
- Contraseñas con hash moderno; sesiones seguras; MFA para operador.
- Separar cuentas de operador y cliente.
- Secretos fuera de Git; rotación y privilegios mínimos.
- Timeouts, tamaño máximo de prompt/respuesta, límite de tokens, rate limiting y circuit breaker.
- Cuotas por usuario y globales; bloqueo automático si coste o GPU supera el presupuesto.
- Registro de auditoría de pagos y operaciones administrativas.
- Escaneo de dependencias e imágenes; actualizaciones controladas.
- Política de incidentes, backups y prueba de restauración antes de aceptar pagos.

## 9. Orden de implementación

### Fase A — inventario y puerta de seguridad
1. Congelar el commit de partida y crear rama de despliegue.
2. Ejecutar tests, preflight, auditoría de capacidades y revisar configuración de modelos.
3. Identificar la interfaz mínima reutilizable; no reescribir el núcleo.
4. Mantener las herramientas públicas deshabilitadas.
5. Cerrar el diseño de datos, amenazas y límites de coste.

**Salida:** inventario reproducible y lista de bloqueos.

### Fase B — servicio comercial
1. Crear paquete independiente `commercial_api/`.
2. Implementar registro/login, sesión, roles cliente/operador.
3. Implementar PostgreSQL y migraciones.
4. Implementar catálogo, créditos, membresías y libro de transacciones.
5. Implementar órdenes y webhook Wompi con firma e idempotencia.
6. Implementar cuotas, límites de tokens, rate limit y métricas.
7. Implementar endpoint de inferencia que invoque solo roles permitidos.

**Salida:** tests unitarios e integración de pagos simulados; ningún pago real en pruebas.

### Fase C — GPU
1. Crear Pod L40S bajo demanda.
2. Instalar Ollama y modelos aprobados; no descargar toda la biblioteca de modelos.
3. Exponer endpoint solo al backend mediante conexión autenticada.
4. Ejecutar benchmark por modelo y tarea.
5. Implementar healthcheck, timeout, cola y cierre de sesión.
6. Confirmar que apagar la GPU no afecta la web ni el sistema de pagos.

**Salida:** informe de coste, rendimiento, calidad y errores por modelo.

### Fase D — web y beta cerrada
1. Publicar frontend en Cloudflare Pages.
2. Conectar dominio y TLS.
3. Publicar API en VPS con HTTPS.
4. Probar registro, pago sandbox, webhook duplicado, reembolso simulado, crédito agotado y caída de GPU.
5. Invitar a 5–10 usuarios de confianza con límites bajos.
6. Corregir errores antes de anuncios pagados.

**Salida:** beta limitada y monitoreada.

### Fase E — adquisición y cobro
1. Publicar vídeos reales del laboratorio con etiqueta de pruebas controladas.
2. CTA hacia registro y lista de acceso.
3. Empezar con USD 20–30 de publicidad; medir registro, primera tarea, conversión y coste por usuario.
4. Liberar el resto de publicidad solo si el coste de adquisición y el margen son razonables.
5. Activar cobros reales después de validar checkout, webhook, reembolsos y condiciones.
6. Publicar reporte de avance e ingresos agregados, sin exponer datos de usuarios.

## 10. Criterios de aceptación antes de cobrar

- [ ] La web permanece disponible con GPU apagada.
- [ ] Ningún puerto interno de Ollama queda abierto públicamente.
- [ ] Cliente A no puede leer ni modificar cuenta, saldo, historial o pagos de B.
- [ ] Los webhooks falsos, repetidos, fuera de orden o con importe incorrecto no generan créditos.
- [ ] Cada consumo genera un débito único e idempotente.
- [ ] Un usuario sin saldo no puede invocar inferencia.
- [ ] Límites por cuenta y globales impiden gasto ilimitado.
- [ ] Apagado de GPU y alertas de presupuesto comprobados.
- [ ] No se ejecutan herramientas ni escáneres desde la API pública.
- [ ] Backup y restauración de PostgreSQL probados.
- [ ] Política de privacidad, términos, precio, renovación y reembolso publicados.
- [ ] El estado beta y las capacidades no validadas están claramente indicados.
- [ ] Se han probado errores de modelo, respuestas vacías, timeout y caída del proveedor.

**No aceptar pagos hasta que todos los controles de pagos, aislamiento, límites de gasto y recuperación estén aprobados.**

## 11. Métricas de negocio

Medir diariamente:
- visitantes únicos y fuente de adquisición;
- registros y usuarios activados;
- usuarios que completan primera tarea;
- conversión a primer pago;
- ingresos brutos, comisiones, devoluciones y saldo disponible;
- coste GPU por solicitud y por 1.000 tokens;
- margen bruto por plan;
- uso por modelo, errores, latencia y disponibilidad;
- coste de adquisición por cliente pagador;
- retención y cancelación.

La métrica decisiva no es el número de seguidores: es el margen de contribución por usuario pagador después de inferencia, pagos y costes variables.

## 12. Fuentes operativas consultadas

- RunPod GPU pricing: https://www.runpod.io/pricing
- RunPod Serverless: https://www.runpod.io/product/serverless
- Cloudflare Pages limits: https://developers.cloudflare.com/pages/platform/limits/
- Wompi tarifas Colombia: https://wompi.com/es/co/planes-tarifas/
- Wompi requisitos y desembolsos: https://wompi.com/es/co/ayuda/como-crear-cuenta

---

**Conclusión:** la primera versión no debe vender “toda la plataforma CYBER_AI”. Debe vender una beta limitada, con capacidades demostrables, consumo medido y riesgo financiero acotado. La L40S es el motor de inferencia; el backend comercial controla identidad, dinero y permisos; la web atrae usuarios. El sistema interno de agentes y herramientas permanece detrás de una frontera de seguridad hasta superar pruebas de aislamiento y operación.
