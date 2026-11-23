# Política de salida de investigación web

## Registro de dominios confiables

`config/trusted_sources.json` define los sufijos DNS autorizados. `load_sources()` lee el archivo con comprobación de tipo/identidad, rechaza symlinks y puntos de reanálisis, y rechaza hardlinks en POSIX; aplica un límite de 1 MB. Exige IDs únicos y dominios DNS canónicos con al menos dos etiquetas. Rechaza comodines, IP literales, IPv4 abreviado/numérico, hosts locales, etiquetas vacías, puertos, rutas y sintaxis ambigua. Los nombres IDN se normalizan a ASCII IDNA.

La coincidencia es por sufijo: registrar `example.org` también incluye sus subdominios. Registra únicamente dominios cuya jerarquía completa sea aceptable. No se incorpora una Public Suffix List; por tanto, la revisión humana del alcance del dominio sigue siendo obligatoria.

## URLs y redirecciones

Solo se consultan URLs HTTPS cuyo host coincida con un dominio registrado. Se rechazan userinfo, autoridades ambiguas, puertos inválidos, IPs y hosts que no sean DNS canónico. Cada redirección vuelve a comprobarse contra el mismo registro. Los resultados fuera del registro solo pueden incluirse para descubrimiento con `include_untrusted=True`; no se descargan ni se consideran fuentes verificadas.

## Límites de entrada

Antes de cargar la política o contactar proveedores, la consulta debe ser texto no vacío, sin caracteres de control y de hasta 1.000 caracteres. `max_results` debe ser un entero estricto entre 1 y 20; los booleanos no se aceptan como enteros. `include_untrusted` exige un booleano real. Las URLs recibidas de los motores se rechazan si superan 4.096 caracteres o contienen controles. Estos límites reducen abuso de recursos y evitan que entradas malformadas lleguen al cliente de red.

## Gateway obligatorio

La búsqueda y descarga requieren `CYBER_AI_WEB_RESEARCH_EGRESS_PROXY`. El cliente no intenta resolver ni fijar DNS por sí mismo: la variable debe apuntar a un gateway administrado que aplique allowlist, DNS pinning, bloqueo de redes privadas/no autorizadas, límites de respuesta y trazabilidad. El código local valida la forma del proxy, pero no demuestra que el gateway esté configurado correctamente ni elimina TOCTOU de DNS.

- Un proxy HTTP solo se admite en loopback.
- Un proxy remoto debe usar HTTPS y no incluir credenciales en la URL.
- La búsqueda y la descarga de páginas usan el mismo proxy explícito.
- No habilites acceso directo a Internet como fallback si el gateway falla.

## Tratamiento de contenido

El contenido web y los resultados de búsqueda son datos no confiables, nunca instrucciones para agentes. La inclusión en un dominio registrado no demuestra la veracidad de una afirmación, la vigencia de una página, su licencia ni su calidad científica. Las fechas no detectadas permanecen sin confirmar y las afirmaciones importantes requieren fuentes independientes y revisión de evidencia.

## Validación pendiente

Las pruebas unitarias verifican normalización, rechazo de autoridades ambiguas y uso obligatorio del proxy. El despliegue aún debe demostrar en un gateway real el pinning DNS, el bloqueo de destinos privados, el comportamiento ante redirecciones, la política de certificados, los límites y la auditoría central.
