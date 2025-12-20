import paho.mqtt.client as mqtt
import json
import time

# --- CONFIGURAÇÃO ---
# O Mosquitto está rodando na própria Pi (localhost)
MQTT_BROKER = "localhost" 
MQTT_PORT = 1883
# Tópico que o script irá ESCUTAR (assinante)
MQTT_TOPIC = "teste/paho/sensor" 

# --- CALLBACKS MQTT ---

def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao Broker MQTT com código de resultado: {rc}")
    # Assina o tópico assim que conectar
    client.subscribe(MQTT_TOPIC)
    print(f"Assinado ao tópico: {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    try:
        # Decodifica a mensagem de bytes para string
        payload_str = msg.payload.decode('utf-8')
        
        # Converte a string JSON para um dicionário Python
        data = json.loads(payload_str)
        
        # --- EXTRAÇÃO DE DADOS (AJUSTADA PARA O FORMATO DO PUBLISHER) ---
        
        # Usamos .get() para evitar erros caso o campo não exista
        device_id = data.get('device_id', 'N/A')
        temp_c = data.get('temperatura_c', 'N/A')
        umidade_pct = data.get('umidade_pct', 'N/A')
        timestamp = data.get('timestamp', 'N/A')
        
        print("\n--- NOVO PACOTE RECEBIDO ---")
        print(f"Timestamp do dado: {timestamp}")
        print(f"Dispositivo: {device_id} | Tópico: {msg.topic}")
        print(f"Temperatura: {temp_c}°C | Umidade: {umidade_pct}%")
        
        # --- AQUI VOCÊ ADICIONA A LÓGICA DE SALVAR NO BANCO DE DADOS ---
        # Exemplo:
        # save_to_database(device_id, temp_c, umidade_pct, timestamp)
        
    except json.JSONDecodeError:
        print(f"[{time.strftime('%H:%M:%S')}] Erro ao decodificar JSON: Mensagem inválida.")
        print(f"Conteúdo recebido: {msg.payload}")
    except Exception as e:
        print(f"Erro no processamento: {e}")

# --- INICIALIZAÇÃO ---
# Usando CallbackAPIVersion.VERSION1 para consistência com o Publisher
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message

print(f"Tentando conectar ao Broker em {MQTT_BROKER}:{MQTT_PORT}...")
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
except Exception as e:
    print(f"Não foi possível conectar ao broker. Certifique-se que o Mosquitto está rodando. Erro: {e}")
    exit(1)

# Mantém o script rodando e escutando mensagens
print("Cliente Subscriber iniciado e aguardando mensagens...")
client.loop_forever()