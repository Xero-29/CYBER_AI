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

No se admiten dominios en esta versión: hasta disponer de transporte con DNS fijado contra DNS rebinding, solo se aceptan IP literales públicas globales. Se rechazan IP privadas, loopback, link-local y reservadas. Los destinos deben coincidir exactamente con el permiso. Las comprobaciones HTTP no siguen redirecciones y no usan proxies ambientales; Nuclei se ejecuta con redirecciones deshabilitadas.

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

## Ejecución

```bash
python cyber_ai.py --scan https://IP_AUTORIZADA \
  --confirm-authorized --authorization-id CHG-2026-0001

python task_runner.py --task "revisión de cabeceras" \
  --target https://IP_AUTORIZADA --execute \
  --confirm-authorized --authorization-id CHG-2026-0001
```

La confirmación del operador es una barrera adicional; no sustituye al permiso local. El ID no concede acceso por sí solo: destino, acción, responsable, ticket y expiración deben coincidir.

## Límites conocidos y trabajo pendiente

- `approved_by` y `ticket` son metadatos declarativos en un archivo local. Esta versión no autentica criptográficamente la identidad del aprobador ni verifica el ticket contra un sistema externo.
- La seguridad del permiso depende de la protección del archivo y del sistema operativo. Para un despliegue institucional debe integrarse un servicio de autorización con identidad corporativa, aprobación firmada, revocación, auditoría inmutable y separación entre quien solicita y quien aprueba.
- Se bloquean nombres DNS hasta implementar resolución y conexión con IP fijada, validación de cada redirección y protección contra DNS rebinding.
- La autorización actual no es un sandbox. Los procesos Nuclei siguen necesitando aislamiento del sistema operativo, límites de recursos y políticas de egreso de red.
- No se deben habilitar escaneos externos hasta que la organización configure y revise su archivo de permisos.
