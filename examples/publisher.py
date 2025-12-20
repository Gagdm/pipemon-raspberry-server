import paho.mqtt.client as mqtt
import time
import json # <--- Importamos a biblioteca JSON

# 1. Configurações do Broker (Mosquitto Local)
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "teste/paho/sensor"

# 2. Funções de Callback (Opcional, mas recomendado para debugging)
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT com sucesso!")
    else:
        print(f"Falha na conexão, código de retorno: {rc}")

def on_publish(client, userdata, mid):
    """Função chamada quando a mensagem foi publicada (confirmada pelo broker)."""
    # Nota: Este callback é chamado após a confirmação do QoS 1 ou 2 pelo broker.
    # mid é o ID da mensagem.
    print(f"Mensagem publicada com sucesso (mid: {mid})")


# 3. Criação e Configuração do Cliente
client_id = "Publisher_JSON_Exemplo"
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)
client.on_connect = on_connect
client.on_publish = on_publish # Atribui o callback de publicação

# Conecta-se ao broker
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start() # Inicia um thread em segundo plano para processar a rede
except Exception as e:
    print(f"Erro ao conectar: {e}")
    exit(1)

# 4. Publicação das Mensagens
print("Iniciando publicação de 5 mensagens JSON...")

for i in range(1, 6):
    temperatura = 20.0 + i/2
    umidade = 60 + i
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    # Cria o objeto de dados (dicionário Python)
    payload_data = {
        "device_id": client_id,
        "leitura_id": i,
        "temperatura_c": f"{temperatura:.1f}",
        "umidade_pct": umidade,
        "timestamp": timestamp
    }
    
    # Converte o dicionário Python para uma string JSON
    # 'json_message' é a string que será enviada pelo MQTT
    json_message = json.dumps(payload_data)
    
    # Publica a mensagem: (tópico, mensagem, QoS=1)
    result = client.publish(MQTT_TOPIC, json_message, qos=1)
    
    # O método 'wait_for_publish' espera que a confirmação de QoS 1 ou 2 seja recebida.
    result.wait_for_publish() 
    
    print(f"[{i}/5] Enviado: {json_message}")
    time.sleep(1)

# 5. Finaliza
client.loop_stop() # Para o thread de processamento de rede
client.disconnect()
print("Publicação concluída e desconectado.")