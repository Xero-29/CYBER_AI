# Autorización central de ejecución de red

## Objetivo

Las herramientas de red deben aplicar una política independiente del agente que solicita la acción. La selección de una capacidad nunca concede permiso para ejecutarla.

La política actual es **deny-by-default**: si no hay un permiso local válido, específico y vigente, no se inicia ninguna conexión ni escaneo.

## Requisitos de un permiso

Cada entrada de `authorizations` debe declarar:

- `id`: identificador único que se pasa al ejecutar.
- `target`: URL exacta autorizada, con IP literal.
- `actions`: acciones permitidas, por ejemplo `nuclei_scan` o `inspect_http_headers`.
- `approved_by`: responsable que aprobó el alcance.
- `ticket`: referencia de autorización/cambio.
- `expires_at`: expiración ISO-8601 con zona horaria.

No se admiten dominios en esta versión: hasta disponer de transporte con DNS fijado contra DNS rebinding, solo se aceptan IP literales. Se permiten IP públicas globales y, únicamente mediante un permiso exacto y vigente, rangos RFC1918, ULA IPv6 y loopback para laboratorios/redes internas. Se rechazan link-local, multicast, no especificadas y reservadas. Los destinos deben coincidir exactamente con el permiso. Las comprobaciones HTTP no siguen redirecciones y no usan proxies ambientales; Nuclei se ejecuta con redirecciones deshabilitadas.

## Configuración

1. Copia `config/authorized_targets.json` a una ubicación local fuera del repositorio.
2. Añade solo permisos aprobados para el entorno concreto. No uses la IP de ejemplo como objetivo de escaneo.
3. Restringe el archivo al propietario del servicio:
   ```bash
   chmod 600 /ruta/segura/authorized_targets.json
   ```
4. Configura la variable:
   ```bash
   export CYBER_AI_AUTHORIZATIONS_FILE=/ruta/segura/authorized_targets.json
   ```
5. No guardes permisos reales, tickets sensibles ni datos de clientes en Git.

Ejemplo de estructura (reemplaza todos los valores de ejemplo por un alcance real aprobado):

```json
{
  "authorizations": [
    {
      "id": "CHG-2026-0001",
      "target": "https://203.0.113.10",
      "actions": ["nuclei_scan", "inspect_http_headers"],
      "approved_by": "responsable-de-seguridad",
      "ticket": "CHG-2026-0001",
      "expires_at": "2026-12-01T23:59:59Z"
    }
  ]
}
```

La dirección reservada del ejemplo anterior es documental y será rechazada por el motor. Sustitúyela por una IP pública global realmente incluida en el alcance autorizado.

## Integridad del archivo de política

El cargador valida la política antes de considerar cualquier permiso:

- solo acepta JSON UTF-8 con el esquema exacto `authorizations`;
- rechaza claves JSON duplicadas, IDs repetidos, acciones que no sean listas de identificadores y campos desconocidos;
- limita el archivo a 1 MiB y a 500 autorizaciones;
- rechaza symlinks, puntos de reanálisis y archivos que no sean regulares; compara la identidad del archivo abierto con la ruta para detectar sustituciones durante la apertura;
- en POSIX, los directorios padre y todos sus ancestros deben pertenecer a `root` o al usuario efectivo; no pueden ser modificables por grupo u otros, salvo directorios sticky propiedad de `root` como `/tmp`;
- cuando existen permisos, exige modo POSIX `0600`; la verificación de ACL NTFS debe realizarse en el sistema operativo;
- rechaza destinos con dominios, credenciales, query, fragmentos, rutas ambiguas/escapadas y puertos fuera de rango. Solo admite IP literales globales o privadas expresamente incluidas en el permiso; nunca link-local, multicast, no especificadas ni reservadas.

Una política vacía no concede permisos y puede permanecer como plantilla versionada. No agregues permisos reales a ese archivo dentro del repositorio: crea una copia local privada y configura `CYBER_AI_AUTHORIZATIONS_FILE`.

## Integridad del escáner Nuclei

Los dos puntos de entrada activos (`nuclei_scanner.py` y `task_runner.py`) exigen una entrada HMAC firmada para el identificador `nuclei`; si falta la política, el binario no coincide o el archivo no puede verificarse, el proceso no inicia. También exigen una entrada `nuclei_template_*` por cada plantilla seleccionada, ligada a su ruta relativa y SHA-256 exacto. Una plantilla sin aprobación, modificada o revocada bloquea el lanzamiento o descarta los resultados. La comprobación se repite antes de aceptar hallazgos. El opt-out general de allowlist no omite esta barrera de Nuclei.

La allowlist general puede seguir en modo de compatibilidad para herramientas locales, pero Nuclei —por realizar conexiones activas— no admite ese modo. Consulta [la guía de allowlist firmada](TOOL_ALLOWLIST.md) para enrolar el binario fuera del repositorio. La clave HMAC y el manifiesto real deben permanecer fuera de Git.

El escáner `nuclei_scanner.py` revalida el permiso inmediatamente antes de lanzar el proceso, en cada ciclo de supervisión y antes de aceptar los resultados; si el permiso expira o se revoca, termina el grupo POSIX y descarta los hallazgos. `task_runner.py` revalida antes del lanzamiento y al terminar; su ejecución síncrona no puede interrumpir el proceso en el instante de la revocación, por lo que descarta el resultado al finalizar si el permiso ya no está vigente.

## Ejecución

```bash
python cyber_ai.py --scan https://IP_AUTORIZADA \
  --confirm-authorized --authorization-id CHG-2026-0001

python task_runner.py --task "revisión de cabeceras" \
  --target https://IP_AUTORIZADA --execute \
  --confirm-authorized --authorization-id CHG-2026-0001
```

La confirmación del operador es una bandera explícita de CLI; no abre un diálogo interactivo y no sustituye al permiso local. El ID no concede acceso por sí solo: destino, acción, responsable, ticket y expiración deben coincidir. Los destinos se canonizan antes de mostrarse o registrarse; se rechazan query, fragmentos, credenciales, nombres DNS y patrones sensibles en la ruta.

## Límites conocidos y trabajo pendiente

- `approved_by` y `ticket` son metadatos declarativos en un archivo local. Esta versión no autentica criptográficamente la identidad del aprobador ni verifica el ticket contra un sistema externo.
- La seguridad del permiso depende de la protección del archivo y del sistema operativo. Para un despliegue institucional debe integrarse un servicio de autorización con identidad corporativa, aprobación firmada, revocación, auditoría inmutable y separación entre quien solicita y quien aprueba.
- Se bloquean nombres DNS hasta implementar resolución y conexión con IP fijada, validación de cada redirección y protección contra DNS rebinding.
- La autorización actual no es un sandbox. El runner POSIX crea y termina un grupo de procesos, pero un descendiente puede escapar si crea otra sesión/grupo (setsid/setpgid); por tanto, no equivale a contención completa del árbol. Los trabajos hostiles requieren cgroups/namespace o contenedor reforzado; para Windows siguen pendientes Job Objects.
- El runner de procesos no impone aislamiento de red. Los adaptadores host pueden alcanzar la red salvo que una política externa de egress lo impida.
- No se deben habilitar escaneos externos hasta que la organización configure y revise su archivo de permisos.
