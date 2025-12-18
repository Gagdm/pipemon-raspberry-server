from nicegui import ui, app
from pathlib import Path
import asyncio
import random
import os

#-----------------------------------------------------------------------------------------------------------------

#==================================================================================================================
# ---------------------------------------------- VARIÁVEIS GLOBAIS -----------------------------------------------
#==================================================================================================================

#-----------------------------------------------------------------------------------------------------------------
# variáveis para auxiliar ajustes, caso necessário
NUM_SENSORS = 2
MAX_TEMP = 27
MIM_TEMP = 20
DISC_TEMP = -127
CURRENT_TEMPERATURE = [0.0] * NUM_SENSORS
CURRENT_TEMP_TIME = ''
CURRENT_FLOW_TIME = ''
CURRENT_FLOW = [0.0] * NUM_SENSORS
DIF_ACCEPT_FLOW = 1
#-----------------------------------------------------------------------------------------------------------------
# Caminho de arquivos e diretórios
BASE_DIR = Path(__file__).parent
TEMP_SENSORS_DATA_FILE = BASE_DIR / 'sensors_data' / 'temp_sensors_data.txt'
FLOW_SENSORS_DATA_FILE = BASE_DIR / 'sensors_data' / 'flow_sensors_data.txt'
ASSETS_FOLDER = BASE_DIR / 'assets'

# verifica se a pasta existe antes de tentar carregar durante o código
if not ASSETS_FOLDER.exists():
    print(f"ERRO: A pasta não foi encontrada em: {ASSETS_FOLDER}")
else:
    print(f"SUCESSO: Pasta assets encontrada em: {ASSETS_FOLDER}")
    app.add_static_files('/assets', str(ASSETS_FOLDER))
#-----------------------------------------------------------------------------------------------------------------

#==================================================================================================================
# ------------------------------------------------- UTILITIES --------------------------------------------------
#==================================================================================================================

#-----------------------------------------------------------------------------------------------------------------
# seleciona a imagem para a tela principal
def select_image_randomly(): 
    random_number = random.randint(0, 100)
    image_path = ''

    # muda o caminho da imagem a depender do número aleatório ser par ou ímpar
    if random_number % 2 == 0:
        image_path = '/assets/line_statistics.png'
    else:
        image_path = '/assets/block_statistics.png'

    return image_path
#-----------------------------------------------------------------------------------------------------------------
# muda a imagem que está sendo exibida em 'image'
def change_image(image):

    new_image = select_image_randomly()
    image.set_source(new_image)
#-----------------------------------------------------------------------------------------------------------------
# coloca um delay para simular um carregamento e direciona para a próxima aba
async def go_to_page(new_page, current_page):

    if new_page == 'home' and current_page == 'dashboard':

        # gera notificações e simula o tempo de boot
        ui.notify('Fechando arquivos...', type='ongoing')
        await asyncio.sleep(1.2) 
        ui.notify('Redirecionando para Home...', type='ongoing')
        await asyncio.sleep(1.5) 
        # direciona para a Home
        ui.navigate.to('/')

    elif new_page == 'dashboard' and current_page == 'home':

        # gera uma notificação
        ui.notify('Iniciando sistema...', type='ongoing')
        # simula tempo de boot
        await asyncio.sleep(2.0) 
        # direciona para a página dashboard
        ui.navigate.to('/dashboard')
#-----------------------------------------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------------------------------------
# função para utilizar no timer e recarregar a página das temperaturas
@ui.refreshable
def temp_expansions():

    # pega as últimas temperaturas 
    CURRENT_TEMP_TIME, CURRENT_TEMPERATURE = get_current_data('temp')

    # cria uma expansão, uma para cada sensor no sistema
    for i in range(NUM_SENSORS):

        # verifica se a temperatura está dentro do esperado, caso contrário, haverá avisos!
        if CURRENT_TEMPERATURE[i] > MIM_TEMP and CURRENT_TEMPERATURE[i] < MAX_TEMP:
            with ui.expansion(f'Sensor de Temperatura {i+1}', icon='device_thermostat') \
                .classes('w-full bg-slate-800 text-white rounded-xl mb-2 border border-slate-700 shadow-lg'):
        
                # o que aparecerá quando abrir a expansão
                with ui.row().classes('w-full items-center justify-between p-2'):
                    
                    # mostrará o último valor lido do sensor de temperatura
                    with ui.column():
                        ui.label('Leitura Atual').classes('text-xs text-gray-400 uppercase tracking-wider')
                        ui.label(f'{CURRENT_TEMPERATURE[i]:.1f}°C').classes('text-4xl font-mono text-emerald-400 font-bold')

                    # mostrará o status do sensor
                    with ui.column().classes('items-end'):
                        ui.label('Status: Ativo').classes('text-sm text-green-400')
                        ui.label(f'Última atualização: {CURRENT_TEMP_TIME}').classes('text-xs text-gray-500')
        
        # caso a temperatura esteja acima do esperado
        elif CURRENT_TEMPERATURE[i] > MAX_TEMP:
            with ui.expansion(f'Sensor de Temperatura {i+1}', icon='whatshot') \
                .classes('w-full bg-red-800 text-white rounded-xl mb-2 border border-red-700 shadow-lg'):
        
                # o que aparecerá quando abrir a expansão
                with ui.row().classes('w-full items-center justify-between p-2'):
                    
                    # mostrará o último valor lido do sensor de temperatura
                    with ui.column():
                        ui.label('Leitura Atual').classes('text-xs text-red-400 uppercase tracking-wider')
                        ui.label(f'{CURRENT_TEMPERATURE[i]:.1f}°C').classes('text-4xl font-mono text-white font-bold')

                    # mostrará o status do sensor
                    with ui.column().classes('items-end'):
                        ui.label('Status: Ativo').classes('text-sm text-white')
                        ui.label(f'Última atualização: {CURRENT_TEMP_TIME}').classes('text-xs text-gray-300')

        # caso o sensor esteja desconectado
        elif CURRENT_TEMPERATURE[i] == DISC_TEMP:
            with ui.expansion(f'Sensor de Temperatura {i+1}', icon='sensors_off') \
                .classes('w-full bg-slate-800 text-gray-500 rounded-xl mb-2 border-2 border-red-700 shadow-lg'):
        
                # o que aparecerá quando abrir a expansão
                with ui.row().classes('w-full items-center justify-between p-2'):
                    
                    # mostrará o último valor lido do sensor de temperatura
                    with ui.column():
                        ui.label('Leitura Atual').classes('text-xs text-gray-400 uppercase tracking-wider')
                        ui.label(f'0.0°C').classes('text-4xl font-mono text-gray-900 font-bold')

                    # mostrará o status do sensor
                    with ui.column().classes('items-end'):
                        ui.label('Status: Disconectado').classes('text-sm text-red-400')
                        ui.label(f'Última atualização: 00:00:00').classes('text-xs text-gray-500')
        
        #caso a temperatura esteja baixa
        else:
            with ui.expansion(f'Sensor de Temperatura {i+1}', icon='ac_unit') \
                .classes('w-full bg-blue-900 text-white rounded-xl mb-2 border border-blue-700 shadow-lg'):
        
                # o que aparecerá quando abrir a expansão
                with ui.row().classes('w-full items-center justify-between p-2'):
                    
                    # mostrará o último valor lido do sensor de temperatura
                    with ui.column():
                        ui.label('Leitura Atual').classes('text-xs text-blue-400 uppercase tracking-wider')
                        ui.label(f'{CURRENT_TEMPERATURE[i]:.1f}°C').classes('text-4xl font-mono text-white font-bold')

                    # mostrará o status do sensor
                    with ui.column().classes('items-end'):
                        ui.label('Status: Ativo').classes('text-sm text-white')
                        ui.label(f'Última atualização: {CURRENT_TEMP_TIME}').classes('text-xs text-gray-300')
#-----------------------------------------------------------------------------------------------------------------
# função para utilizar no timer e recarregar a página das vazões
@ui.refreshable
def flow_expansions():
    # pega as últimas vazões 
    CURRENT_FLOW_TIME, CURRENT_FLOW = get_current_data('flow')

    # cria uma expansão, uma para cada sensor no sistema
    for i in range(NUM_SENSORS):

        # verifica se os sensores estão conectados, caso contrário, haverá avisos!
        if CURRENT_FLOW[i] == 0.00:
            with ui.expansion(f'Sensor de Vazão {i+1}', icon='sensors_off') \
                .classes('w-full bg-slate-800 text-gray-500 rounded-xl mb-2 border-2 border-red-700 shadow-lg'):
        
                # o que aparecerá quando abrir a expansão
                with ui.row().classes('w-full items-center justify-between p-2'):
                    
                    # mostrará o último valor lido do sensor de temperatura
                    with ui.column():
                        ui.label('Leitura Atual').classes('text-xs text-gray-400 uppercase tracking-wider')
                        ui.label(f'0.00L/s').classes('text-4xl font-mono text-gray-900 font-bold')

                    # mostrará o status do sensor
                    with ui.column().classes('items-end'):
                        ui.label('Status: Disconectado').classes('text-sm text-red-400')
                        ui.label(f'Última atualização: 00:00:00').classes('text-xs text-gray-500')

        # caso em que os sensores estão conectados
        else: 
            with ui.expansion(f'Sensor de Vazão {i+1}', icon='waves') \
                .classes('w-full bg-slate-800 text-white rounded-xl mb-2 border border-slate-700 shadow-lg'):
        
                # o que aparecerá quando abrir a expansão
                with ui.row().classes('w-full items-center justify-between p-2'):
                    
                    # mostrará o último valor lido do sensor de temperatura
                    with ui.column():
                        ui.label('Leitura Atual').classes('text-xs text-gray-400 uppercase tracking-wider')
                        ui.label(f'{CURRENT_FLOW[i]:.2f}L/s').classes('text-4xl font-mono text-emerald-400 font-bold')

                    # mostrará o status do sensor
                    with ui.column().classes('items-end'):
                        ui.label('Status: Ativo').classes('text-sm text-green-400')
                        ui.label(f'Última atualização: {CURRENT_FLOW_TIME}').classes('text-xs text-gray-500')
#-----------------------------------------------------------------------------------------------------------------

#==================================================================================================================
# ------------------------------------------------- DASHBOARD --------------------------------------------------
#==================================================================================================================

#----------------------------------------------------------------------------------------------------------------- 
# definição da tela dashboard
@ui.page('/dashboard')
def dashboard_page():
    with ui.row().classes('w-full h-screen gap-0 no-wrap'):

        # botão Home no canto inferior direito
        ui.button(icon='home', on_click=lambda: go_to_page('home','dashboard')) \
            .classes('fixed bottom-5 right-5 z-50 rounded-full shadow-2xl w-14 h-14 bg-blue-600 hover:bg-blue-500 text-white')
        
        # definição da coluna que fica do lado esquerdo da tela e ocupa 1/5 da sua largura
        with ui.column().classes('w-1/5 bg-slate-100 p-4 border-r border-slate-300'):
            ui.label('Histórico')

        # definição da coluna que fica do lado direito da tela e ocupa 4/5 de sua largura
        with ui.column().classes('w-4/5 bg-white p-6'):

            # ajustes visuais nas abas de seleção interativa
            with ui.tabs().classes('w-full').props('align="justify"') as tabs:
                temp = ui.tab('Temperatura')
                flow = ui.tab('Vazão')

            # cria as abas de seleção interativa e, através de uma ação, faz o chaveamento de qual aba mostrar
            with ui.tab_panels(tabs, value=flow).classes('w-full p-4'):

                # aba "TEMPERATURE" mostrará o gráfico das temperaturas recebidas ao longo do tempo
                with ui.tab_panel(temp):
                    # carrega a página e faz o reload a cada 60 segs
                    temp_expansions()
                    ui.separator()
                    ui.timer(60, temp_expansions.refresh)
                    
                # aba "FLOW" mostrará o gráfico das vazões recebidas ao longo do tempo
                with ui.tab_panel(flow):
                    # carrega a página e faz o reload a cada 60 segs
                    flow_expansions()
                    ui.separator()
                    ui.timer(60, flow_expansions.refresh)

ui.run()
#----------------------------------------------------------------------------------------------------------------- 

#==================================================================================================================
# ----------------------------------------------- PÁGINA INICIAL ------------------------------------------------
#==================================================================================================================

#-----------------------------------------------------------------------------------------------------------------
# definição da tela inicial
@ui.page('/')
def initial_page():
    with ui.column().classes('w-full h-screen items-center justify-center bg-slate-900 text-white'):

        # exibe a imagem principal da tela inicial
        principal_image = ui.image(select_image_randomly()).classes('w-[600px] h-[400px] object-cover rounded-xl mb-8 opacity-80')
        # a cada 2segs e meio é realizada uma nova seleção de imagem
        ui.timer(2.5, lambda: change_image(principal_image))

        # título, subtítulo e legendas
        ui.label('PipeMon').classes('text-5xl font-bold mb-1')
        ui.label('Sistema de Monitoramento de Tubulações Subterrâneas e comunicação via LoRa').classes('text-2xl font-mono')
        ui.label('IF474 - Tópicos Avançados em Redes de Computadores - Gabriel Alves <gagm> e Lucas Emanuel <lessl>').classes('text-1xl font-mono mb-8')

        # botão que encaminha para a página de tabelas
        ui.button('VISUALIZAR DADOS', icon='power_settings_new', on_click=lambda: go_to_page('dashboard','home')) \
            .classes('px-8 py-4 text-xl bg-green-600 hover:bg-green-500 rounded-full shadow-lg font-bold')
#----------------------------------------------------------------------------------------------------------------- 

#==================================================================================================================
# ---------------------------------------------------- MAIN -----------------------------------------------------
#==================================================================================================================

#----------------------------------------------------------------------------------------------------------------- 
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='Sensor App')
#----------------------------------------------------------------------------------------------------------------- 
