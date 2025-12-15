from nicegui import ui, app
from pathlib import Path
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
        ui.button('VISUALIZAR DADOS', icon='power_settings_new') \
            .classes('px-8 py-4 text-xl bg-green-600 hover:bg-green-500 rounded-full shadow-lg font-bold')
#----------------------------------------------------------------------------------------------------------------- 

#==================================================================================================================
# ---------------------------------------------------- MAIN -----------------------------------------------------
#==================================================================================================================

#----------------------------------------------------------------------------------------------------------------- 
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='Sensor App')
#----------------------------------------------------------------------------------------------------------------- 
