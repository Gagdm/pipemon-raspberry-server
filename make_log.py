from nicegui import ui, app
from pathlib import Path
import asyncio
import random
import os
import time

# variáveis para auxiliar ajustes, caso necessário
NUM_SENSORS = 2
MAX_TEMP = 27
MIN_TEMP = 20
DISC_TEMP = -127
CURRENT_TEMPERATURE = [0.0] * NUM_SENSORS
CURRENT_TEMP_TIME = ''
CURRENT_FLOW_TIME = ''
CURRENT_FLOW = [0.0] * NUM_SENSORS
DIF_ACCEPT_FLOW = 1
DISC_FLOW = -127
MENU_STATE = {'aberto': False}
MENU_ICON = ''

#-----------------------------------------------------------------------------------------------------------------
# Caminho de arquivos e diretórios
BASE_DIR = Path(__file__).parent
DEBUG_FILE = BASE_DIR / 'logs' / 'debug_sensors.txt'
FLOW_DIFFERENCE_FILE = BASE_DIR / 'logs' / 'flow_difference.txt'
TEMP_SENSORS_DATA_FILE = BASE_DIR / 'sensors_data' / 'temp_sensors_data.txt'
FLOW_SENSORS_DATA_FILE = BASE_DIR / 'sensors_data' / 'flow_sensors_data.txt'
ASSETS_FOLDER = BASE_DIR / 'assets'
#-----------------------------------------------------------------------------------------------------------------

# verifica se a pasta existe antes de tentar carregar durante o código
if not ASSETS_FOLDER.exists():
    print(f"ERRO: A pasta não foi encontrada em: {ASSETS_FOLDER}")
else:
    print(f"SUCESSO: Pasta assets encontrada em: {ASSETS_FOLDER}")
    app.add_static_files('/assets', str(ASSETS_FOLDER))

# pega a última linha do arquivo escolhido
def get_current_data(arc):

    linhas = [] 
    arch = ""

    # define o arquivo que quero acessar
    if arc == 'temp':
        arch = TEMP_SENSORS_DATA_FILE
    elif arc == "flow":
        arch = FLOW_SENSORS_DATA_FILE
    else:
        return ('00:00:00', [])

    # tenta ler o arquivo, caso haja algum erro, cria uma excessão
    try:
        # caso o arquivo não exista
        if not os.path.exists(arch):
            print("Arquivo não existe!")
            return ('00:00:00', [])

        # abre o arquivo apenas para leitura
        with open(arch, 'r') as f:
            linhas = f.readlines()
        
    except Exception as e:
        print(f"Erro ao ler: {e}")
        return ('00:00:00', [])

    # proteção contra arquivo vazio
    if len(linhas) == 0:
        return ('00:00:00', [])

    # pega a última linha e separa os dados
    ultima_linha = linhas[-1] 
    partes = ultima_linha.strip().split(',')
    
    # verifica se tem o tamanho certo (Hora + N Sensores)
    if len(partes) == (NUM_SENSORS + 1):

        # se for cabeçalho, retorna zeros
        if partes[0] == "Hora":
            # cria lista de zeros do tamanho certo
            zeros = [0.0] * NUM_SENSORS 
            return ('00:00:00', zeros)
        
        else:
            # pega os valores
            time = partes[0] 
            values = []
            for i in range(NUM_SENSORS):
                try:
                    val = float(partes[i+1])
                    values.append(val)
                except:
                    values.append(0.0) 
            return (time, values)

    # se a linha estiver quebrada/incompleta
    return ('00:00:00', [])

if __name__ == "__main__":

    while(1):

        CURRENT_FLOW_TIME, CURRENT_FLOW = get_current_data('flow')
        CURRENT_TEMP_TIME, CURRENT_TEMPERATURE = get_current_data('temp')

        try:
            # caso o arquivo não exista
            if not os.path.exists(DEBUG_FILE):
                print("Arquivo não existe!")

            # abre o arquivo apenas para leitura
            debug_file = open(DEBUG_FILE, "a")
                
        except Exception as e:
            print(f"Erro ao ler: {e}")

        try:
            # caso o arquivo não exista
            if not os.path.exists(FLOW_DIFFERENCE_FILE):
                print("Arquivo não existe!")

            # abre o arquivo apenas para leitura
            flow_file = open(FLOW_DIFFERENCE_FILE, "a")

        except Exception as e:
            print(f"Erro ao ler: {e}")

        for i in range(NUM_SENSORS):

            # se o sensor de temperatura estiver disconectado
            if CURRENT_TEMPERATURE[i] == DISC_TEMP:
                debug_file.write(f"SENSOR DE TEMPERATURA {i+1} DISCONECTADO!,{CURRENT_TEMP_TIME}\n")
            
            # se o sensor de vazão estiver disconectado
            if CURRENT_FLOW[i] == DISC_FLOW:
                debug_file.write(f"SENSOR DE VAZÃO {i+1} DISCONECTADO!,{CURRENT_TEMP_TIME}\n")

            # se o sentor de temperatura estiver apontando uma temperatura abaixo da esperada
            if CURRENT_TEMPERATURE[i] < MIN_TEMP:
                debug_file.write(f"SENSOR DE TEMPERATURA {i+1} inferiu uma temperatura MAIS BAIXA que o normal!,{CURRENT_TEMP_TIME}\n")

            # se o sentor de temperatura estiver apontando uma temperatura acima da esperada
            if CURRENT_TEMPERATURE[i] > MAX_TEMP:
                debug_file.write(f"SENSOR DE TEMPERATURA {i+1} inferiu uma temperatura MAIS ALTA que o normal!,{CURRENT_TEMP_TIME}\n")

        for i in range(NUM_SENSORS-1):

            # faz a diferença atual e escreve no arquivo
            dif_current_flow = CURRENT_FLOW[i] - CURRENT_FLOW[i+1]
            flow_file.write(f"{dif_current_flow},{CURRENT_FLOW_TIME}\n")

            # se a diferença da vazão lida nos sensores de vazão for maior que 1
            if dif_current_flow > DIF_ACCEPT_FLOW:
                debug_file.write(f"VAZAMENTO detectado no TRECHO {i+1}!,{CURRENT_TEMP_TIME}\n")

        debug_file.close()
        flow_file.close()

        time.sleep(30)