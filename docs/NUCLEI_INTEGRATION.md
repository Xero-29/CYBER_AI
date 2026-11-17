# Nuclei: escaneo web autorizado

CYBER_AI integra Nuclei como escáner remoto explícito, no como adaptador local automático. El flujo es:

1. El operador aporta un destino IP literal y una autorización vigente que coincide exactamente con destino y acción `nuclei_scan`.
2. CYBER_AI selecciona plantillas HTTP locales y ejecuta Nuclei con concurrencia y tasa limitadas.
3. Se almacena el JSONL original, se valida que los hallazgos correspondan al origen autorizado y se registra el inicio/fin en el ledger.
4. `analyze_scan` agrupa hallazgos por plantilla y severidad y genera un informe resumido.
5. Los hallazgos son indicios; deben verificarse manualmente. Cero hallazgos no demuestra ausencia de vulnerabilidades.

## Instalar Nuclei y plantillas

Instala Nuclei desde el proyecto oficial de ProjectDiscovery y descarga sus plantillas:

```bash
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
nuclei -update-templates
```

Las plantillas son contenido ejecutable por un motor de escaneo y deben tratarse como código de terceros. Actualízalas desde el repositorio oficial, revísalas y conserva la verificación de firmas. CYBER_AI deshabilita plantillas sin firma y excluye etiquetas `dos`, `intrusive`, `fuzz`, `code` y `headless`; limita el protocolo a HTTP. No activa los motores de código, headless ni interacciones externas.

Por defecto se usa `$HOME/nuclei-templates/http`. Si están en otra ruta:

```bash
export CYBER_AI_NUCLEI_TEMPLATES="$HOME/nuclei-templates/http"
```

## Registrar autorización

Copia `config/authorized_targets.example.json` a un archivo privado administrado localmente. Cambia destino, ID, responsable, ticket y expiración. Ejemplo de destino local de laboratorio:

```json
{
  "authorizations": [
    {
      "id": "lab-web-001",
      "target": "http://127.0.0.1:8080",
      "actions": ["nuclei_scan"],
      "expires_at": "2099-12-31T23:59:59Z",
      "approved_by": "Responsable del laboratorio",
      "ticket": "LAB-001"
    }
  ]
}
```

Protege el archivo:

```bash
chmod 600 /ruta/privada/authorized_targets.json
export CYBER_AI_AUTHORIZATIONS_FILE="/ruta/privada/authorized_targets.json"
```

Se aceptan IP públicas, privadas y loopback solo cuando existe un permiso explícito que coincide con la URL. Los nombres DNS siguen bloqueados: la resolución no está fijada y podría sufrir DNS rebinding. No autorices direcciones o servicios que no controles.

## Ejecutar un escaneo

```bash
python cyber_ai.py --scan "http://127.0.0.1:8080" \
  --confirm-authorized \
  --authorization-id "lab-web-001" \
  --scan-timeout 300 \
  --scan-rate-limit 2 \
  --scan-concurrency 2
```

Opcionalmente puedes pasar `--nuclei-templates "/ruta/nuclei-templates/http"`, `--scan-severity "medium,high,critical"`, y ajustar timeout (5-3600 s), tasa (1-20 solicitudes/s) y concurrencia (1-10).

Los informes se guardan en `reports/`: uno con la evidencia JSONL estructurada y otro con el análisis agrupado. La persistencia en ledger es obligatoria en la CLI.

## Límites

- Solo HTTP/HTTPS y direcciones IP literales; no hay DNS fijado ni escaneo de redes/rangos.
- No se ejecutan plantillas de tipo code, headless, fuzz, DoS o intrusivas.
- Los límites de tasa y concurrencia reducen impacto, pero no garantizan que una plantilla no cause efectos secundarios.
- La validación comprueba estructura y correspondencia de origen, no explotabilidad ni veracidad.
- Nuclei no se dispara desde el plan multiagente: requiere invocación CLI y autorización del operador.
