import urllib.request
import json
import os
import time
import tracemalloc

class CyberAIBenchmark:
    def __init__(self):
        print("[CYBER_AI BENCHMARK] Inicializando monitor de rendimiento local...")

    def run_task_with_stats(self, task_name, task_func, *args):
        # Iniciar medición de memoria en RAM
        tracemalloc.start()
        start_time = time.perf_counter()

        # Ejecutar la tarea real
        try:
            result = task_func(*args)
            success = True
        except Exception as e:
            result = {"status": "error", "error_msg": str(e)}
            success = False

        # Detener medición
        end_time = time.perf_counter()
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        elapsed_ms = (end_time - start_time) * 1000

        stats = {
            "tarea": task_name,
            "tiempo_ms": round(elapsed_ms, 2),
            "memoria_pico_bytes": peak_mem,
            "exito": success,
            "detalle_resultado": result
        }
        return stats

    def action_check_headers(self, url):
        req = urllib.request.Request(url, headers={'User-Agent': 'CyberAI-Benchmark/1.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            headers = dict(response.headers)
            return {"servidor": headers.get("Server", "No especificado"), "total_headers": len(headers)}

    def action_check_local_file(self, filepath):
        if os.path.exists(filepath):
            return {"peso_bytes": os.path.getsize(filepath), "estado": "Encontrado"}
        return {"estado": "No encontrado"}

if __name__ == "__main__":
    bench = CyberAIBenchmark()

    print("\n" + "="*60)
    print("📊 DIAGNÓSTICO DE RENDIMIENTO EN TIEMPO REAL (THINKPAD E440)")
    print("="*60)

    # Definir tareas de prueba
    tareas = [
        ("Inspección HTTP (Red Externa)", bench.action_check_headers, "https://example.com"),
        ("Lectura de Archivo Local (Disco)", bench.action_check_local_file, "agent_core.py")
    ]

    for nombre, func, argumento in tareas:
        print(f"\n⚙️ Ejecutando: {nombre}...")
        stat = bench.run_task_with_stats(nombre, func, argumento)
        
        print(f"  ⏱️  Tiempo de ejecución: {stat['tiempo_ms']} ms")
        print(f"  💾 Memoria RAM pico:    {stat['memoria_pico_bytes']} bytes")
        print(f"  📦 Resultado obtenido:  {json.dumps(stat['detalle_resultado'], ensure_ascii=False)}")
        print("-" * 60)

    print("\n✅ ¡Diagnóstico finalizado con éxito sin saturar el sistema!")
