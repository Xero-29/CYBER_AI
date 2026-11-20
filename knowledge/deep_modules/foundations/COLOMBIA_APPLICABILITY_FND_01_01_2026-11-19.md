# Aplicabilidad normativa colombiana — análisis de alcance para FND-01.01

**Fecha de consulta:** 2026-11-19.  
**Naturaleza:** mapeo preliminar de fuentes oficiales y condiciones de aplicabilidad; no es concepto jurídico, certificación sanitaria ni análisis de conformidad.  
**Caso de referencia:** sistema hipotético de dosificación y supervisión remota. La aplicabilidad depende del servicio real, actor, datos tratados, ubicación, población y actividad regulada.

## 1. Protección de datos personales

### Fuente primaria

**Ley Estatutaria 1581 de 2012**, texto consultado en el Normograma/compilación jurídica oficial de Cancillería:
https://cancilleria.gov.co/normograma/compilacion/docs/ley_1581_2012.htm

Se inspeccionaron:
- Artículos 1–3: objeto, ámbito y definiciones. La norma alcanza datos personales en bases de datos susceptibles de tratamiento por entidades públicas o privadas; define dato personal como información vinculada o asociable a personas naturales determinadas o determinables y tratamiento como operaciones como recolección, almacenamiento, uso, circulación o supresión.
- Artículo 4: principios rectores, incluyendo legalidad, finalidad, libertad, calidad y transparencia.
- Artículos 8–10: derechos de titulares, autorización y excepciones.
- Artículo 6: reglas sobre datos sensibles.

**Aplicación condicionada:** si los registros OT, telemetría, bitácoras de acceso, video, turnos o datos de mantenimiento identifican o hacen identificable a una persona y están sometidos a tratamiento dentro del ámbito territorial/material de la ley, la arquitectura debe contemplar finalidad, legitimidad, minimización, acceso, retención, seguridad, derechos del titular y responsabilidades. No todo dato de proceso es dato personal; no se debe declarar aplicabilidad sin examinar identificabilidad, contexto y actor responsable/encargado.

**Implicación de diseño:** separar métricas de proceso de identificadores personales cuando sea posible; evitar cuentas compartidas; documentar finalidad de cada campo; limitar retención según necesidad y obligaciones; restringir acceso; definir respuesta a solicitudes de titulares y gestión de incidentes conforme al marco aplicable. El cifrado no sustituye estas obligaciones.

## 2. Calidad del agua para consumo humano: solo si el sistema cae en ese ámbito

### Decreto 1575 de 2007

Fuente oficial consultada:
https://cancilleria.gov.co/normograma/compilacion/docs/decreto_1575_2007.htm

El artículo 1 define el objeto como el sistema de protección y control de la calidad del agua para consumo humano y delimita su aplicación a prestadores que suministran o distribuyen agua para consumo humano, además de autoridades y usuarios. El artículo 2 contiene definiciones pertinentes, entre ellas agua para consumo humano, análisis de vulnerabilidad, calidad del agua y certificación/concepto sanitario.

### Resolución 2115 de 2007

Fuente oficial consultada:
https://cancilleria.gov.co/sites/default/files/Normograma/docs/resolucion_minproteccion_2115_2007.htm

Se inspeccionaron artículos 1–5 y tablas iniciales: define análisis básicos y complementarios, cloro residual, tiempo de contacto y potabilización; establece características físicas y químicas y valores aceptables para agua de consumo humano.

**Aplicación condicionada:** estos instrumentos son pertinentes si el sistema es parte de la producción, tratamiento, suministro o distribución de agua para consumo humano dentro de su campo de aplicación. No se deben aplicar automáticamente a cualquier dosificador industrial, piscina, proceso cerrado, agua envasada o instalación no destinada al consumo humano. El Decreto 1575 excluye expresamente el agua envasada de su objeto; ese caso exige identificar su régimen propio.

**Implicación de diseño:** cuando aplique, la arquitectura de control no puede sustituir el control sanitario del agua ni el muestreo/ensayo requerido. Los límites de proceso, variables, frecuencias, mapa de riesgo, responsabilidades y aceptación deben provenir de la regulación aplicable y de ingeniería sanitaria competente. Los ejemplos hipotéticos de este dossier no contienen consignas químicas ni valores operacionales y no sirven para operar una planta.

## 3. Lo que estas fuentes NO resuelven

- No constituyen una norma general de seguridad funcional de maquinaria, proceso industrial o sistemas OT.
- No identifican qué norma técnica sectorial de safety corresponde a una planta concreta.
- No sustituyen normas técnicas obligatorias, permisos, requisitos de autoridad sanitaria/ambiental ni obligaciones contractuales.
- No resuelven la aplicabilidad de reglas de infraestructura crítica, servicios públicos, salud, transporte, alimentos u otros sectores.
- No acreditan que el texto consultado incorpore todas las modificaciones, decisiones jurisprudenciales y reglas especiales relevantes para un caso real.

## 4. Árbol de decisión de aplicabilidad

1. **¿Se tratan datos vinculados o asociables a personas naturales?** Si sí, analizar Ley 1581/2012, responsables/encargados, ámbito territorial, finalidades, excepciones y reglas especiales. Si no, documentar por qué los datos no son personales; no presumirlo solo porque el sistema sea OT.
2. **¿El agua se suministra/distribuye para consumo humano?** Si sí, verificar el ámbito del Decreto 1575/2007 y Resolución 2115/2007, prestador, autoridad, actividad y modificaciones. Si no, identificar el régimen sectorial real; no extrapolar esas normas.
3. **¿El proceso puede causar daño físico, químico o ambiental?** Si sí, identificar el sector y autoridad, normas de seguridad funcional, proceso, salud ocupacional, ambiente y gestión de emergencias que correspondan. La selección requiere ingeniería sectorial y validación legal.
4. **¿La instalación es crítica o presta servicio público?** Si sí, identificar obligaciones adicionales de continuidad, reporte, seguridad, vigilancia y gestión del riesgo aplicables al actor y sector.

## 5. Registro de incertidumbre y cierre

- Ley 1581/2012: texto oficial consultado en artículos seleccionados; no se realizó dictamen jurídico ni análisis jurisprudencial completo.
- Decreto 1575/2007 y Resolución 2115/2007: artículos iniciales y ámbito/definiciones consultados; no se hizo análisis completo de modificaciones, régimen de vigilancia, excepciones y normativa técnica conexa.
- Normas sectoriales de seguridad funcional: no seleccionadas porque el caso es genérico y no identifica sector, proceso, equipos ni jurisdicción técnica concreta.
- No se asignan límites de concentración, dosificación, tiempos de contacto ni consignas de control.
- La revisión por abogado/autoridad competente e ingenieros de proceso/safety sigue pendiente.

**Resultado de auditoría:** NC-FND-01.01-02 se reduce parcialmente: existe un primer mapa de aplicabilidad colombiano para privacidad y, condicionalmente, agua para consumo humano. Permanece abierta para seguridad funcional y otras obligaciones sectoriales, además de la validación jurídica independiente. FND-01.01 continúa T0/O0 y no aprobado.
