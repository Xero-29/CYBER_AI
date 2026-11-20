# Investigación técnica: Telecomunicaciones y seguridad 5G

**ID:** telecom_5g · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Validación de red operador pendiente.

## Arquitectura
Modelar UE, SIM/eSIM, gNB, RAN, AMF, SMF, UPF, AUSF, UDM, PCF, NRF, NEF, SEPP, roaming, slice, MEC, OSS/BSS y core cloud-native. Diferenciar control plane/user plane, subscriber identity, roaming, interconnect y network slicing.

## Seguridad 5G
Estudiar authentication and key agreement, SUCI/SUPI privacy, home network control, mutual authentication, key hierarchy, NAS/AS security, security context, slice isolation, SEPP, inter-PLMN security, service-based architecture, OAuth2/TLS for APIs and NF authorization. Revisar release/versión exacta; especificaciones cambian por Release.

**Actualidad:** ETSI/3GPP publicó TS 33.501 Release 19 versión 19.7.0 en agosto de 2026. No usar un documento Release 15/16 como referencia actual sin identificar el alcance.

## Amenazas
Rogue base station, downgrade, IMSI/SUPI exposure, signaling abuse, API compromise, slice escape, NF impersonation, roaming interconnect risk, misconfigured cloud-native core, supply chain, DDoS y lawful intercept abuse. Evaluar privacidad y seguridad nacional/regulación.

## Controles
SIM/eSIM lifecycle, key protection, secure boot, mutual auth, NF identity, mTLS, service authorization, slice isolation, API gateway, rate limit, anomaly detection, secure orchestration, audit, software supply chain y incident response inter-operator.

## Laboratorios
5G core open-source en entorno aislado, UE simulator, gNB emulator, test SIM credentials, NF APIs mock, slice segmentation y roaming simulation. No transmitir RF fuera de bandas/condiciones autorizadas ni interferir redes comerciales.

## Fuentes
- 3GPP/ETSI TS 33.501 Release 19: https://portal.etsi.org/webapp/WorkProgram/Frame_WorkItemList.asp?SearchPage=TRUE+++&qTITLE=TS+33.501
- ETSI Publications: https://www.etsi.org/standards
- NIST CSF 2.0: https://doi.org/10.6028/NIST.CSWP.29

**Límite:** estándares 3GPP son extensos y versionados; revisar texto completo, release, corrigenda y normativa local de espectro.
