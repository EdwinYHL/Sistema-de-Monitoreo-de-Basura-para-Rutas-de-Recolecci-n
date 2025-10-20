#!/usr/bin/env python3
import json
import time
import subprocess
import paho.mqtt.client as mqtt

# CONFIGURACIÓN - Usa tu IP de EC2
MQTT_BROKER = "3.85.201.184"
MQTT_PORT = 1883
MQTT_TOPIC = "ciudad/basura/contenedores"

client = mqtt.Client()
print("🔌 Conectando a MQTT...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

print("🚀 Sistema de Monitoreo de Basura Iniciado")
print("📍 Enviando datos de 3 contenedores...")

while True:
    try:
        # Ejecutar simulador por 35 segundos
        result = subprocess.run(
            ["python3", "sensor_basura_simulator.py"],
            capture_output=True, 
            text=True,
            timeout=35
        )
        
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if line and line.startswith('{'):
                    try:
                        data = json.loads(line)
                        client.publish(MQTT_TOPIC, json.dumps(data))
                        
                        # Mostrar estado con colores
                        if data["porcentaje_lleno"] > 90:
                            emoji = "🔴"
                        elif data["porcentaje_lleno"] > 60:
                            emoji = "🟡"
                        else:
                            emoji = "🟢"
                            
                        print(f"{emoji} {data['contenedor_id']}: {data['porcentaje_lleno']}% lleno - {data['temperatura']}°C")
                        
                    except json.JSONDecodeError:
                        continue
            
    except subprocess.TimeoutExpired:
        print("⏰ Ciclo de simulación completado")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    time.sleep(5)  # Breve pausa antes del siguiente ciclo
