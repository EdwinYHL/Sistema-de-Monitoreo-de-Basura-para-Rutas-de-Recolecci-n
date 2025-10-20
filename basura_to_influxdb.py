#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision

# CONFIGURACIÓN - REEMPLAZA CON TU TOKEN
MQTT_BROKER = "localhost"
MQTT_TOPIC = "ciudad/basura/contenedores"

INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "TU-TOKEN-AQUI" 
INFLUXDB_ORG = "IoTOrg"
INFLUXDB_BUCKET = "basura-data"

# Clientes
influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = influx_client.write_api()

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado a MQTT - Sistema de Basura")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Escuchando: {MQTT_TOPIC}")
    else:
        print(f"❌ Error MQTT: {rc}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        
        # Determinar emoji para log
        if data["porcentaje_lleno"] > 90:
            emoji = "🔴"
        elif data["porcentaje_lleno"] > 60:
            emoji = "🟡"
        else:
            emoji = "🟢"
        
        point = (
            Point("contenedores_basura")
            .tag("contenedor_id", data["contenedor_id"])
            .tag("ubicacion", data["ubicacion"])
            .tag("estado", data["estado"])
            .field("nivel_actual", int(data["nivel_actual"]))
            .field("porcentaje_lleno", float(data["porcentaje_lleno"]))
            .field("temperatura", float(data["temperatura"]))
            .field("capacidad_max", int(data["capacidad_max"]))
            .field("lat", float(data["lat"]))
            .field("lon", float(data["lon"]))
            .time(datetime.utcnow(), WritePrecision.NS)
        )
        
        write_api.write(bucket=INFLUXDB_BUCKET, record=point)
        print(f"{emoji} {data['contenedor_id']}: {data['porcentaje_lleno']}% - {data['temperatura']}°C")
        
    except Exception as e:
        print(f"❌ Error procesando: {e}")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

print("🚀 Iniciando Sistema de Monitoreo de Basura...")
try:
    mqtt_client.connect(MQTT_BROKER, 1883, 60)
    mqtt_client.loop_forever()
except KeyboardInterrupt:
    print("🛑 Deteniendo sistema...")
    mqtt_client.disconnect()
    influx_client.close()
except Exception as e:
    print(f"💥 Error crítico: {e}")
