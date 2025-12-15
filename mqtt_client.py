import paho.mqtt.client as mqtt
import json
import time

# --- CONFIGURAÇÃO ---
# O Mosquitto está rodando na própria Pi (localhost)
MQTT_BROKER = "localhost" 
MQTT_PORT = 1883
# Tópico que o script irá ESCUTAR (assinante)
MQTT_TOPIC = "gateway/+/data" 

# --- CALLBACKS MQTT ---

def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao Broker MQTT com código de resultado: {rc}")
    # Assina o tópico assim que conectar
    client.subscribe(MQTT_TOPIC)
    print(f"Assinado ao tópico: {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    try:
        # Decodifica e converte a string JSON para um dicionário Python
        payload_str = msg.payload.decode('utf-8')
        data = json.loads(payload_str)
        
        # Extração de dados
        gateway_id = data.get('gateway_id', 'N/A')
        temp_remoto = data.get('temp_remoto')
        flow_remoto = data.get('flow_remoto')
        
        print("\n--- NOVO PACOTE RECEBIDO ---")
        print(f"Hora: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        print(f"Gateway: {gateway_id} | Tópico: {msg.topic}")
        print(f"Dados: Temp Entrada={temp_remoto}°C | Vazão Entrada={flow_remoto}")
        
        # --- AQUI VOCÊ ADICIONA A LÓGICA DE SALVAR NO BANCO DE DADOS ---
        
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON: Mensagem inválida.")
    except Exception as e:
        print(f"Erro no processamento: {e}")

# --- INICIALIZAÇÃO ---
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print(f"Tentando conectar ao Broker em {MQTT_BROKER}:{MQTT_PORT}...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Mantém o script rodando e escutando mensagens
client.loop_forever()