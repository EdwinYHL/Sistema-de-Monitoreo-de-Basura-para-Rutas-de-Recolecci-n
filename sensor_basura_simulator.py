#!/usr/bin/env python3
import json
import time
import random
from datetime import datetime

def simular_contenedores():
    contenedores = [
        {"id": "cont-001", "ubicacion": "zona_centro", "capacidad_max": 100, "lat": 32.5149, "lon": -117.0382},
        {"id": "cont-002", "ubicacion": "zona_norte", "capacidad_max": 120, "lat": 32.5249, "lon": -117.0282},
        {"id": "cont-003", "ubicacion": "zona_sur", "capacidad_max": 80, "lat": 32.5049, "lon": -117.0482}
    ]
    
    while True:
        for contenedor in contenedores:
            # Simular crecimiento realista de basura
            base_nivel = random.randint(10, 80)
            # Aumentar probabilidad de llenado en horas pico
            hora_actual = datetime.now().hour
            if 8 <= hora_actual <= 10 or 17 <= hora_actual <= 19:
                base_nivel += random.randint(10, 30)
            
            nivel_actual = min(base_nivel, contenedor["capacidad_max"])
            porcentaje_lleno = (nivel_actual / contenedor["capacidad_max"]) * 100
            
            # Temperatura más alta si hay mucha basura orgánica
            temp_base = random.uniform(18.0, 35.0)
            if porcentaje_lleno > 70:
                temp_base += random.uniform(2.0, 8.0)
            
            data = {
                "contenedor_id": contenedor["id"],
                "ubicacion": contenedor["ubicacion"],
                "nivel_actual": nivel_actual,
                "porcentaje_lleno": round(porcentaje_lleno, 2),
                "temperatura": round(temp_base, 2),
                "capacidad_max": contenedor["capacidad_max"],
                "lat": contenedor["lat"],
                "lon": contenedor["lon"],
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "estado": "critico" if porcentaje_lleno > 90 else "medio" if porcentaje_lleno > 60 else "normal"
            }
            
            print(json.dumps(data))
            time.sleep(2)  # Pequeña pausa entre contenedores
        
        print("--- Ciclo completo de contenedores ---")
        time.sleep(30)  # Espera entre ciclos

if __name__ == "__main__":
    simular_contenedores()
