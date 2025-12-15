from nicegui import ui, app
from pathlib import Path
import asyncio
import random

#-----------------------------------------------------------------------------------------------------------------

#==================================================================================================================
# ---------------------------------------------- VARIÁVEIS GLOBAIS -----------------------------------------------
#==================================================================================================================

#-----------------------------------------------------------------------------------------------------------------
# Caminho de arquivos e diretórios
BASE_DIR = Path(__file__).parent
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
                temp = ui.tab('Temperature')
                flow = ui.tab('Flow')

            # cria as abas de seleção interativa e através de uma ação faz o chaveamento de qual aba mostrar
            with ui.tab_panels(tabs, value=flow).classes('w-full p-4'):

                # aba "TEMPERATURE" mostrará o gráfico das temperaturas recebidas ao longo do tempo
                with ui.tab_panel(temp):
                    ui.label('Conteúdo da primeira aba - gráfico da temperatura')

                # aba "FLOW" mostrará o gráfico das vazões recebidas ao longo do tempo
                with ui.tab_panel(flow):
                    ui.label('Conteúdo da segunda aba - gráfico da vazão')

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
