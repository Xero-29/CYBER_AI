import urllib.request
import json
import os

class CyberAIEngine:
    def __init__(self):
        print("[CYBER_AI] Motor de Agentes y Traductor de Acciones Inicializado.")

    def translate_and_execute(self, agent_thought):
        """
        Toma el pensamiento en lenguaje natural del agente, 
        lo traduce y ejecuta la acción técnica correspondiente.
        """
        print(f"\n🤖 [Pensamiento del Agente]: \"{agent_thought}\"")
        
        thought_lower = agent_thought.lower()

        if "cabeceras" in thought_lower or "servidor" in thought_lower or "http" in thought_lower:
            return self.action_check_headers("https://example.com")
        elif "archivo" in thought_lower or "configuración" in thought_lower or "local" in thought_lower:
            return self.action_check_local_file("agent_core.py")
        else:
            return {
                "status": "error", 
                "message": "El agente generó un pensamiento que no tiene una herramienta asignada todavía."
            }

    def action_check_headers(self, url):
        print(f"⚙️ [Ejecutando Herramienta]: Consultando cabeceras HTTP de {url}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'CyberAI-Framework/1.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                headers = dict(response.headers)
                server_type = headers.get("Server", "No especificado")
                return {
                    "status": "success", 
                    "accion_realizada": "HTTP Header Inspection",
                    "servidor_detectado": server_type,
                    "total_cabeceras": len(headers)
                }
        except Exception as e:
            return {"status": "error", "error_msg": str(e)}

    def action_check_local_file(self, filepath):
        print(f"⚙️ [Ejecutando Herramienta]: Buscando archivo local '{filepath}'...")
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            return {
                "status": "success", 
                "accion_realizada": "Local File Check",
                "resultado": f"El archivo '{filepath}' existe y pesa {file_size} bytes."
            }
        else:
            return {
                "status": "success", 
                "accion_realizada": "Local File Check",
                "resultado": f"El archivo '{filepath}' no se encuentra en el directorio."
            }

if __name__ == "__main__":
    engine = CyberAIEngine()
    pensamientos_simulados = [
        "Necesito indagar qué tipo de servidor web y cabeceras tiene el objetivo.",
        "Quiero verificar si el archivo de configuración local está disponible en el entorno.",
        "Voy a inventar algo que no tiene sentido para ver cómo reacciona el sistema."
    ]

    for pensamiento in pensamientos_simulados:
        resultado = engine.translate_and_execute(pensamiento)
        print(f"📊 [Resultado devuelto al Agente]: {json.dumps(resultado, indent=2, ensure_ascii=False)}")
        print("-" * 60)
