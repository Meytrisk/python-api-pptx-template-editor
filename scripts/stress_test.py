import asyncio
import aiohttp
import time
import os
import sys
import statistics
from dataclasses import dataclass
from typing import List

# Configuración
BASE_URL = os.getenv("API_URL", "http://localhost:8000")
API_TOKEN = os.getenv("API_TOKEN", "changeme_in_production")
CONCURRENCY = 50  # Número de usuarios simultáneos
TOTAL_REQUESTS = 200

@dataclass
class Result:
    status: int
    latency: float
    error: str = None

async def make_request(session, url, method="GET", data=None) -> Result:
    start = time.time()
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        async with session.request(method, url, headers=headers, data=data) as response:
            await response.read()  # Leer cuerpo para completar la request
            latency = (time.time() - start) * 1000  # ms
            return Result(response.status, latency)
    except Exception as e:
        latency = (time.time() - start) * 1000
        return Result(0, latency, str(e))

async def run_load_test(endpoint: str, name: str, method="GET", data=None):
    print(f"\n🚀 Iniciando prueba: {name}")
    print(f"   URL: {BASE_URL}{endpoint}")
    print(f"   Concurrency: {CONCURRENCY} | Total: {TOTAL_REQUESTS}")
    
    url = f"{BASE_URL}{endpoint}"
    tasks = []
    results: List[Result] = []
    
    start_total = time.time()
    
    async with aiohttp.ClientSession() as session:
        # Crear lote de tareas
        for _ in range(TOTAL_REQUESTS):
            tasks.append(make_request(session, url, method, data))
            
            # Control simple de concurrencia por lotes si fuera necesario, 
            # pero aiohttp maneja bien pool de conexiones.
            # Para mas precision usariamos asyncio.Semaphore
        
        results = await asyncio.gather(*tasks)
    
    duration = time.time() - start_total
    
    # Análisis
    statuses = [r.status for r in results]
    latencies = [r.latency for r in results]
    errors = [r for r in results if r.status >= 500 or r.status == 0]
    success = [r for r in results if 200 <= r.status < 300]
    
    print("\n📊 Resultados:")
    print(f"   Tiempo Total: {duration:.2f}s")
    print(f"   RPS (Req/s):  {TOTAL_REQUESTS / duration:.2f}")
    if latencies:
        print(f"   Latencia AVG: {statistics.mean(latencies):.2f}ms")
        print(f"   Latencia P95: {statistics.quantiles(latencies, n=20)[18]:.2f}ms") # approx P95
        print(f"   Latencia MIN: {min(latencies):.2f}ms")
        print(f"   Latencia MAX: {max(latencies):.2f}ms")
    
    print(f"   Éxitos (2xx): {len(success)}")
    print(f"   Fallos (5xx/Err): {len(errors)}")
    
    if errors:
        print(f"   ⚠️ Primer error: {errors[0].error or errors[0].status}")

async def main():
    # 0. Check dependencies
    try:
        import aiohttp
    except ImportError:
        print("❌ Error: Necesitas instalar aiohttp. Ejecuta: pip install aiohttp")
        return

    print(f"⚡ Stress Test Tool - PPTX API")
    print(f"   Target: {BASE_URL}")
    print(f"   Token:  {API_TOKEN[:5]}***")
    
    # 1. Prueba de Salud (Sin Auth y Con Auth si aplicara, pero health es publico)
    # Probaremos Listar Templates que SI requiere Auth
    await run_load_test("/api/v1/templates/", "Listar Templates (Lectura)")
    
    # 2. Prueba de Creación (Escritura - Si hay templates)
    # Primero obtenemos un ID de template válido
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        async with session.get(f"{BASE_URL}/api/v1/templates/", headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                templates = data.get("templates", [])
                if templates:
                    template_id = templates[0]["template_id"]
                    print(f"\n📝 Usando Template ID: {template_id} para prueba de escritura")
                    
                    # Prueba de Creación
                    global TOTAL_REQUESTS
                    old_req = TOTAL_REQUESTS
                    TOTAL_REQUESTS = 50 
                    await run_load_test("/api/v1/presentations/create", "Crear Presentación", "POST", {"template_id": template_id})
                    
                    # Prueba de Reemplazo (Text e Imagen)
                    # Necesitamos un presentation_id. Creamos uno para la prueba.
                    async with session.post(f"{BASE_URL}/api/v1/presentations/create", 
                                          headers=headers, 
                                          json={"template_id": template_id}) as c_resp:
                        if c_resp.status == 201:
                            c_data = await c_resp.json()
                            pres_id = c_data["presentation_id"]
                            print(f"\n🚀 Probando reemplazos en Presentation: {pres_id}")
                            
                            # Stress de Texto
                            await run_load_test(f"/api/v1/presentations/{pres_id}/text", 
                                               "Reemplazo Texto", "POST", 
                                               {"variable_name": "mes", "text": "Stress Test"})
                            
                            # Stress de Imagen (Multipart)
                            # Nota: aiohttp maneja multipart con FormData
                            print(f"\n🖼️ Iniciando prueba: Reemplazo Imagen (Concurrente)")
                            img_tasks = []
                            img_url = f"{BASE_URL}/api/v1/presentations/{pres_id}/image"
                            img_path = "c:/Users/Admin/Documents/Proyectos/pptx/test-data/grafico.png"
                            
                            async with aiohttp.ClientSession() as img_session:
                                start_img = time.time()
                                for _ in range(30): # Menos request para imagen por ser pesado
                                    data = aiohttp.FormData()
                                    data.add_field("variable_name", "grafico")
                                    data.add_field("image", open(img_path, "rb"), filename="grafico.png")
                                    img_tasks.append(make_request(img_session, img_url, "POST", data))
                                
                                img_results = await asyncio.gather(*img_tasks)
                                img_duration = time.time() - start_img
                                print(f"   Completado: {len(img_results)} peticiones en {img_duration:.2f}s ({len(img_results)/img_duration:.2f} RPS)")
                            
                        else:
                            print(f"❌ No se pudo crear presentación para prueba de carga: {c_resp.status}")
                    
                    TOTAL_REQUESTS = old_req
                else:
                    print("\n⚠️ No se encontraron templates para probar la creación.")
            else:
                print(f"\n❌ Error obteniendo templates: {resp.status}")

if __name__ == "__main__":
    asyncio.run(main())
