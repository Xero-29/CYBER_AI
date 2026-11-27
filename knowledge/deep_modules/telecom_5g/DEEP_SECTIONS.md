# Secciones de profundización — Telecomunicaciones y 5G

## Modelo de amenazas
Modelar UE, SIM/eSIM, gNB, RAN, 5G core, AMF/SMF/UPF, slice, MEC, roaming, OSS/BSS y network functions virtualizadas. Amenazas: rogue base station, abuso de señalización, exposición de interfaces, compromiso de NF, slicing isolation failure, supply chain y ataques a disponibilidad. Incluir interconexión con redes heredadas.

## Detección
Correlacionar signaling, autenticación de abonado, cambios de configuración, NF telemetry, roaming, slices, interfaces de gestión y flujos de usuario. Detectar anomalías de registro, signaling storms, cambios de ruta, NF no autorizadas y degradación de slice. Proteger datos de abonados y limitar retención.

## Respuesta a incidentes
Aislar NF o interfaz comprometida mediante orquestación controlada, revocar certificados/credenciales, preservar trazas de signaling, coordinar con operador y proveedor y mantener continuidad del servicio. Validar impacto por slice y roaming antes de bloquear. Restaurar configuración conocida y verificar autenticación, routing y aislamiento.

## Casos prácticos
En testbed 5G, simular NF con certificado inválido y carga anómala de signaling. Detectar rechazo de identidad y saturación controlada, aislar función, renovar certificado y comprobar que otras slices continúan. Documentar límites del emulador frente a red comercial.

## Referencias
Consultar [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para 3GPP SA3, GSMA NESAS, NIST y ENISA 5G threat landscape. Registrar release 3GPP y perfiles implementados.
