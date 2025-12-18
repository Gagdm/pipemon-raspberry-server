from nicegui import ui, app
from pathlib import Path
import asyncio
import random
import os
from dashboard import *

if __name__ == "__main__":

    CURRENT_FLOW_TIME, CURRENT_FLOW = get_current_data('flow')
    CURRENT_TEMP_TIME, CURRENT_TEMPERATURE = get_current_data('temp')

    problems = False
    okays = 0

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
            debug_file.write(f"Sensor de temperatura {i+1} disconectado!,{CURRENT_TEMP_TIME}\n")
            problems = True
        
        # se o sensor de vazão estiver disconectado
        if CURRENT_FLOW[i] == DISC_FLOW:
            debug_file.write(f"Sensor de vazão {i+1} disconectado!,{CURRENT_TEMP_TIME}\n")
            problems = True

        # se o sentor de temperatura estiver apontando uma temperatura abaixo da esperada
        if CURRENT_TEMPERATURE[i] < MIN_TEMP:
            debug_file.write(f"Sensor de temperatura {i+1} inferiu uma temperatura mais baixa que o normal!,{CURRENT_TEMP_TIME}\n")
            problems = True

        # se o sentor de temperatura estiver apontando uma temperatura acima da esperada
        if CURRENT_TEMPERATURE[i] > MAX_TEMP:
            debug_file.write(f"Sensor de temperatura {i+1} inferiu uma temperatura mais alta que o normal!,{CURRENT_TEMP_TIME}\n")
            problems = True

    for i in range(NUM_SENSORS-1):

        # faz a diferença atual e escreve no arquivo
        dif_current_flow = CURRENT_FLOW[i] - CURRENT_FLOW[i+1]
        flow_file.write(f"{dif_current_flow},{CURRENT_FLOW_TIME}\n")

        # se a diferença da vazão lida nos sensores de vazão for maior que 1
        if dif_current_flow > DIF_ACCEPT_FLOW:
            debug_file.write(f"Vazamento detectado no trecho {i+1}!,{CURRENT_TEMP_TIME}\n")
            problems = True
            
    if problems == False:
        okays = okays+1
    
    if okays == 4:
        debug_file.write(f"Não houve relatos de problemas nos últimos 2 minutos :3")


    debug_file.close()
    flow_file.close()
            
