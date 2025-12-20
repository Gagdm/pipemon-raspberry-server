from nicegui import ui, app
from pathlib import Path
import asyncio
import random
import os

#-----------------------------------------------------------------------------------------------------------------

#==================================================================================================================
# ---------------------------------------------- GLOBAL VARIABLES -----------------------------------------------
#==================================================================================================================

#-----------------------------------------------------------------------------------------------------------------
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

# verifica se a pasta existe antes de tentar carregar durante o código
if not ASSETS_FOLDER.exists():
    print(f"ERRO: A pasta não foi encontrada em: {ASSETS_FOLDER}")
else:
    print(f"SUCESSO: Pasta assets encontrada em: {ASSETS_FOLDER}")
    app.add_static_files('/assets', str(ASSETS_FOLDER))
#-----------------------------------------------------------------------------------------------------------------

#==================================================================================================================
# -------------------------------------------- DEFINITION OF GRAPHICS ---------------------------------------------
#==================================================================================================================

#-----------------------------------------------------------------------------------------------------------------
# definição do gráfico do sensor de temperatura 1
@ui.refreshable
def define_and_update_graphic_temp1():

    CURRENT_TEMP_TIME, CURRENT_TEMPERATURE = get_current_data('temp')

    # pega as 20 últimas linhas do arquivo "temp_sensors_data.txt" para fazer o gráfico
    data_temp = get_all_data('temp')
    time_list = []
    values_list = []

    # a depender do estado em que está a medição, o gráfico será printado com cores diferentes
    # caso a temperatura medida esteja dentro do intervalo esperado
    if CURRENT_TEMPERATURE[0] >= MIN_TEMP and CURRENT_TEMPERATURE[0] <= MAX_TEMP:
        CHART_SENSOR_TEMP1 = ui.echart({
                'title': {
                    'text': 'Leituras do Sensor de Temperatura 1',
                    'textStyle': {'color': "#FFFFFF"},
                    'left': 'center',
                    'top': '10' 
                },
                'tooltip': {'trigger': 'axis'},
                'xAxis': {
                    'name': 'Data/Hora',
                    'textStyle': {'color': "#FFFFFF"},
                    'type': 'category', 
                    'data': [], 
                    'axisLabel': {'color': "#FFFFFF", 'rotate': 45},
                    'color': '#CBD5E1',
                    'axisLine': {
                        'lineStyle': {'color': "#FFFFFF"}
                    }
                },
                'yAxis': {
                    'type': 'value', 
                    'name': 'Temperatura (°C)',
                    'nameTextStyle': {'color': "#FFFFFF"},
                    'min': -127,
                    'max': 50,
                    'axisLabel': {'color': '#FFFFFF'}, 
                    'axisLine': {
                        'show': True, 
                        'lineStyle': {'color': '#FFFFFF'} 
                    },
                    'splitLine': {
                        'show': True,
                        'lineStyle': {
                            'color': "#FFFFFF", 
                            'type': 'dashed'   
                        }
                    }
                },
                'series': [{
                    'name': 'Sensor 1',
                    'type': 'line',
                    'smooth': True,
                    'data': [],
                    'lineStyle': {'color': "#2FBE5F", 'width': 3},
                    'areaStyle': {'opacity': 0.4, 'color': "#A8F3A5"},
                    'symbol': 'circle', 
                    'symbolSize': 8,    
                    'itemStyle': {
                        'color': "#104600",      
                        'borderColor': "#D3E7CC", 
                        'borderWidth': 2          
                    }
                }],
                 
            }).classes('w-full h-96')

    # caso a temperatura medida esteja acima do normal esperado   
    elif CURRENT_TEMPERATURE[0] > MAX_TEMP:
        CHART_SENSOR_TEMP1 = ui.echart({
                'title': {
                    'text': 'Leituras do Sensor de Temperatura 1',
                    'textStyle': {'color': "#FFFFFF"},
                    'left': 'center',
                    'top': '10' 
                },
                'tooltip': {'trigger': 'axis'},
                'xAxis': {
                    'name': 'Data/Hora',
                    'textStyle': {'color': "#FFFFFF"},
                    'type': 'category', 
                    'data': [], 
                    'axisLabel': {'color': "#FFFFFF", 'rotate': 45},
                    'color': '#CBD5E1',
                    'axisLine': {
                        'lineStyle': {'color': "#EB8B5F"}
                    }
                },
                'yAxis': {
                    'type': 'value', 
                    'name': 'Temperatura (°C)',
                    'nameTextStyle': {'color': "#FFFFFF"},
                    'min': -127,
                    'max': 50,
                    'axisLabel': {'color': '#FFFFFF'}, 
                    'axisLine': {
                        'show': True, 
                        'lineStyle': {'color': '#FFFFFF'} 
                    },
                    'splitLine': {
                        'show': True,
                        'lineStyle': {
                            'color': "#DB977C", 
                            'type': 'dashed'   
                        }
                    }
                },
                'series': [{
                    'name': 'Sensor 1',
                    'type': 'line',
                    'smooth': True,
                    'data': [],
                    'lineStyle': {'color': "#FF5E00", 'width': 3},
                    'areaStyle': {'opacity': 0.4, 'color': "#F3BBA5"},
                    'symbol': 'circle', 
                    'symbolSize': 8,    
                    'itemStyle': {
                        'color': '#FACC15',      
                        'borderColor': '#FFFFFF', 
                        'borderWidth': 2          
                    }
                }],
                 
            }).classes('w-full h-96')
    
    # caso o sensor de temperatura esteja desconectado
    elif CURRENT_TEMPERATURE[0] == DISC_TEMP:
        CHART_SENSOR_TEMP1 = ui.echart({
                'title': {
                    'text': 'Leituras do Sensor de Temperatura 1',
                    'left': 'center',
                    'top': '10' 
                },
                'tooltip': {'trigger': 'axis'},
                'xAxis': {
                    'name': 'Data/Hora',
                    'textStyle': {'color': "#554F4F"},
                    'type': 'category', 
                    'data': [], 
                    'axisLabel': {'color': "#776F6F", 'rotate': 45},
                    'color': "#515355",
                    'axisLine': {
                        'lineStyle': {'color': "#807D7B"}
                    }
                },
                'yAxis': {
                    'type': 'value', 
                    'name': 'Temperatura (°C)',
                    'nameTextStyle': {'color': "#807979"},
                    'min': -127,
                    'max': 50,
                    'axisLabel': {'color': "#928D8D"}, 
                    'axisLine': {
                        'show': True, 
                        'lineStyle': {'color': "#615B5B"} 
                    },
                    'splitLine': {
                        'show': True,
                        'lineStyle': {
                            'color': "#999593", 
                            'type': 'dashed'    
                        }
                    }
                },
                'series': [{
                    'name': 'Sensor 1',
                    'type': 'line',
                    'smooth': True,
                    'data': [],
                    'lineStyle': {'color': "#770000", 'width': 3},
                    'areaStyle': {'opacity': 0.4, 'color': "#AC7575"},
                    'symbol': 'circle', 
                    'symbolSize': 8,    
                    'itemStyle': {
                        'color': "#302F2C",      
                        'borderColor': '#FFFFFF', 
                        'borderWidth': 2          
                    }
                }],
                 
            }).classes('w-full h-96')
    
    # caso a temperatura medida seja mais baixa que o normal esperado
    else:
        CHART_SENSOR_TEMP1 = ui.echart({
                'title': {
                    'text': 'Leituras do Sensor de Temperatura 1',
                    'textStyle': {'color': "#FFFFFF"},
                    'left': 'center',
                    'top': '10' 
                },
                'tooltip': {'trigger': 'axis'},
                'xAxis': {
                    'name': 'Data/Hora',
                    'textStyle': {'color': "#FFFFFF"},
                    'type': 'category', 
                    'data': [], 
                    'axisLabel': {'color': "#FFFFFF", 'rotate': 45},
                    'color': '#CBD5E1',
                    'axisLine': {
                        'lineStyle': {'color': "#98DADA"}
                    }
                },
                'yAxis': {
                    'type': 'value', 
                    'name': 'Temperatura (°C)',
                    'nameTextStyle': {'color': "#FFFFFF"},
                    'min': -127,
                    'max': 50,
                    'axisLabel': {'color': '#FFFFFF'}, 
                    'axisLine': {
                        'show': True, 
                        'lineStyle': {'color': '#FFFFFF'} 
                    },
                    'splitLine': {
                        'show': True,
                        'lineStyle': {
                            'color': "#98BDC4", 
                            'type': 'dashed'   
                        }
                    }
                },
                'series': [{
                    'name': 'Sensor 1',
                    'type': 'line',
                    'smooth': True,
                    'data': [],
                    'lineStyle': {'color': "#62B3FF", 'width': 3},
                    'areaStyle': {'opacity': 0.4, 'color': "#8CC6CA"},
                    'symbol': 'circle', 
                    'symbolSize': 8,    
                    'itemStyle': {
                        'color': "#00DDFA",      
                        'borderColor': '#FFFFFF', 
                        'borderWidth': 2          
                    }
                }],
                 
            }).classes('w-full h-96')

    # checa se a linha está completa, separa os tipos de dados e atualiza o gráfico para os novos valores
    for row in data_temp:
        if len(row) == 3:
            time_list.append(row[0])
            values_list.append(float(row[1]))

    CHART_SENSOR_TEMP1.options['xAxis']['data'] = time_list
    CHART_SENSOR_TEMP1.options['series'][0]['data'] = values_list
    CHART_SENSOR_TEMP1.update()
#-----------------------------------------------------------------------------------------------------------------
# definição do gráfico do sensor de temperatura 2
@ui.refreshable
def define_and_update_graphic_temp2():

    CURRENT_TEMP_TIME, CURRENT_TEMPERATURE = get_current_data('temp')

    # pega as 20 últimas linhas do arquivo "temp_sensors_data.txt" para fazer o gráfico
    data_temp = get_all_data('temp')
    time_list = []
    values_list = []

    # a depender do estado em que está a medição, o gráfico será printado com cores diferentes
    # caso a temperatura medida esteja dentro do intervalo esperado
    if CURRENT_TEMPERATURE[1] >= MIN_TEMP and CURRENT_TEMPERATURE[1] <= MAX_TEMP:
        CHART_SENSOR_TEMP2 = ui.echart({
                'title': {
                    'text': 'Leituras do Sensor de Temperatura 2',
                    'textStyle': {'color': "#FFFFFF"},
                    'left': 'center',
                    'top': '10' 
                },
                'tooltip': {'trigger': 'axis'},
                'xAxis': {
                    'name': 'Data/Hora',
                    'textStyle': {'color': "#FFFFFF"},
                    'type': 'category', 
                    'data': [], 
                    'axisLabel': {'color': "#FFFFFF", 'rotate': 45},
                    'color': '#CBD5E1',
                    'axisLine': {
                        'lineStyle': {'color': "#FFFFFF"}
                    }
                },
                'yAxis': {
                    'type': 'value', 
                    'name': 'Temperatura (°C)',
                    'nameTextStyle': {'color': "#FFFFFF"},
                    'min': -127,
                    'max': 50,
                    'axisLabel': {'color': '#FFFFFF'}, 
                    'axisLine': {
                        'show': True, 
                        'lineStyle': {'color': '#FFFFFF'} 
                    },
                    'splitLine': {
                        'show': True,
                        'lineStyle': {
                            'color': "#FFFFFF", 
                            'type': 'dashed'   
                        }
                    }
                },
                'series': [{
                    'name': 'Sensor 1',
                    'type': 'line',
                    'smooth': True,
                    'data': [],
                    'lineStyle': {'color': "#2FBE5F", 'width': 3},
                    'areaStyle': {'opacity': 0.4, 'color': "#A8F3A5"},
                    'symbol': 'circle', 
                    'symbolSize': 8,    
                    'itemStyle': {
                        'color': "#104600",      
                        'borderColor': "#D3E7CC", 
                        'borderWidth': 2          
                    }
                }],
                 
            }).classes('w-full h-96')

    # caso a temperatura medida esteja acima do normal esperado      
    elif CURRENT_TEMPERATURE[1] > MAX_TEMP:
        CHART_SENSOR_TEMP2 = ui.echart({
                'title': {
                    'text': 'Leituras do Sensor de Temperatura 2',
                    'textStyle': {'color': "#FFFFFF"},
                    'left': 'center',
                    'top': '10' 
                },
                'tooltip': {'trigger': 'axis'},
                'xAxis': {
                    'name': 'Data/Hora',
                    'textStyle': {'color': "#FFFFFF"},
                    'type': 'category', 
                    'data': [], 
                    'axisLabel': {'color': "#FFFFFF", 'rotate': 45},
                    'color': '#CBD5E1',
                    'axisLine': {
                        'lineStyle': {'color': "#EB8B5F"}
                    }
                },
                'yAxis': {
                    'type': 'value', 
                    'name': 'Temperatura (°C)',
                    'nameTextStyle': {'color': "#FFFFFF"},
                    'min': -127,
                    'max': 50,
                    'axisLabel': {'color': '#FFFFFF'}, 
                    'axisLine': {
                        'show': True, 
                        'lineStyle': {'color': '#FFFFFF'} 
                    },
                    'splitLine': {
                        'show': True,
                        'lineStyle': {
                            'color': "#DB977C", 
                            'type': 'dashed'    
                        }
                    }
                },
                'series': [{
                    'name': 'Sensor 1',
                    'type': 'line',
                    'smooth': True,
                    'data': [],
                    'lineStyle': {'color': "#FF5E00", 'width': 3},
                    'areaStyle': {'opacity': 0.4, 'color': "#F3BBA5"},
                    'symbol': 'circle', 
                    'symbolSize': 8,    
                    'itemStyle': {
                        'color': '#FACC15',      
                        'borderColor': '#FFFFFF', 
                        'borderWidth': 2          
                    }
                }],
                 
            }).classes('w-full h-96')
        
    # caso o sensor de temperatura esteja desconectado
    elif CURRENT_TEMPERATURE[1] == DISC_TEMP:
        CHART_SENSOR_TEMP2 = ui.echart({
                'title': {
                    'text': 'Leituras do Sensor de Temperatura 2',
                    'left': 'center',
                    'top': '10' 
                },
                'tooltip': {'trigger': 'axis'},
                'xAxis': {
                    'name': 'Data/Hora',
                    'textStyle': {'color': "#554F4F"},
                    'type': 'category', 
                    'data': [], 
                    'axisLabel': {'color': "#776F6F", 'rotate': 45},
                    'color': "#515355",
                    'axisLine': {
                        'lineStyle': {'color': "#807D7B"}
                    }
                },
                'yAxis': {
                    'type': 'value', 
                    'name': 'Temperatura (°C)',
                    'nameTextStyle': {'color': "#807979"},
                    'min': -127,
                    'max': 50,
                    'axisLabel': {'color': "#928D8D"}, 
                    'axisLine': {
                        'show': True, 
                        'lineStyle': {'color': "#615B5B"} 
                    },
                    'splitLine': {
                        'show': True,
                        'lineStyle': {
                            'color': "#999593", 
                            'type': 'dashed'    
                        }
                    }
                },
                'series': [{
                    'name': 'Sensor 1',
                    'type': 'line',
                    'smooth': True,
                    'data': [],
                    'lineStyle': {'color': "#770000", 'width': 3},
                    'areaStyle': {'opacity': 0.4, 'color': "#AC7575"},
                    'symbol': 'circle', 
                    'symbolSize': 8,    
                    'itemStyle': {
                        'color': "#302F2C",      
                        'borderColor': '#FFFFFF', 
                        'borderWidth': 2          
                    }
                }],
                 
            }).classes('w-full h-96')
    
    # caso a temperatura medida seja mais baixa que o normal esperado
    else:
        CHART_SENSOR_TEMP2 = ui.echart({
                'title': {
                    'text': 'Leituras do Sensor de Temperatura 2',
                    'textStyle': {'color': "#FFFFFF"},
                    'left': 'center',
                    'top': '10' 
                },
                'tooltip': {'trigger': 'axis'},
                'xAxis': {
                    'name': 'Data/Hora',
                    'textStyle': {'color': "#FFFFFF"},
                    'type': 'category', 
                    'data': [], 
                    'axisLabel': {'color': "#FFFFFF", 'rotate': 45},
                    'color': '#CBD5E1',
                    'axisLine': {
                        'lineStyle': {'color': "#98DADA"}
                    }
                },
                'yAxis': {
                    'type': 'value', 
                    'name': 'Temperatura (°C)',
                    'nameTextStyle': {'color': "#FFFFFF"},
                    'min': -127,
                    'max': 50,
                    'axisLabel': {'color': '#FFFFFF'}, 
                    'axisLine': {
                        'show': True, 
                        'lineStyle': {'color': '#FFFFFF'} 
                    },
                    'splitLine': {
                        'show': True,
                        'lineStyle': {
                            'color': "#98BDC4", 
                            'type': 'dashed'   
                        }
                    }
                },
                'series': [{
                    'name': 'Sensor 1',
                    'type': 'line',
                    'smooth': True,
                    'data': [],
                    'lineStyle': {'color': "#62B3FF", 'width': 3},
                    'areaStyle': {'opacity': 0.4, 'color': "#8CC6CA"},
                    'symbol': 'circle', 
                    'symbolSize': 8,    
                    'itemStyle': {
                        'color': "#00DDFA",      
                        'borderColor': '#FFFFFF', 
                        'borderWidth': 2          
                    }
                }],
                 
            }).classes('w-full h-96')

    # checa se a linha está completa, separa os tipos de dados e atualiza o gráfico para os novos valores
    for row in data_temp:       
        if len(row) == 3:
            time_list.append(row[0])
            values_list.append(float(row[2]))

    CHART_SENSOR_TEMP2.options['xAxis']['data'] = time_list
    CHART_SENSOR_TEMP2.options['series'][0]['data'] = values_list
    CHART_SENSOR_TEMP2.update()
#-----------------------------------------------------------------------------------------------------------------
# definição do gráfico do trecho 1
@ui.refreshable
def define_and_update_graphic_flow():

    # pega os valores atuais e calcula a diferença para saber o estado do trecho
    CURRENT_FLOW_TIME, CURRENT_FLOW = get_current_data('flow')
    dif_current_flow = CURRENT_FLOW[0] - CURRENT_FLOW[1]

    # pega as últimas 20 linhas do "flow_difference.txt" para geraro gráfico
    data_temp = get_all_data('flow')
    time_list = []
    values_list = []

    # caso algum sensor de vazão esteja disconectado
    if CURRENT_FLOW[0] == DISC_FLOW or CURRENT_FLOW[1] == DISC_FLOW:
        CHART_SENSOR_FLOW = ui.echart({
                'title': {
                    'text': 'Diferença de Vazão no Trecho 1',
                    'left': 'center',
                    'top': '10' 
                },
                'tooltip': {'trigger': 'axis'},
                'xAxis': {
                    'name': 'Data/Hora',
                    'textStyle': {'color': "#554F4F"},
                    'type': 'category', 
                    'data': [], 
                    'axisLabel': {'color': "#776F6F", 'rotate': 45},
                    'color': "#515355",
                    'axisLine': {
                        'lineStyle': {'color': "#807D7B"}
                    }
                },
                'yAxis': {
                    'type': 'value', 
                    'name': 'Diferença de Vazão (L/s)',
                    'nameTextStyle': {'color': "#807979"},
                    'min': -10,
                    'max': 10,
                    'axisLabel': {'color': "#928D8D"}, 
                    'axisLine': {
                        'show': True, 
                        'lineStyle': {'color': "#615B5B"} 
                    },
                    'splitLine': {
                        'show': True,
                        'lineStyle': {
                            'color': "#999593", 
                            'type': 'dashed'    
                        }
                    }
                },
                'series': [{
                    'name': 'Sensor 1',
                    'type': 'line',
                    'smooth': True,
                    'data': [],
                    'lineStyle': {'color': "#770000", 'width': 3},
                    'areaStyle': {'opacity': 0.4, 'color': "#AC7575"},
                    'symbol': 'circle', 
                    'symbolSize': 8,    
                    'itemStyle': {
                        'color': "#302F2C",      
                        'borderColor': '#FFFFFF', 
                        'borderWidth': 2          
                    }
                }],
                 
            }).classes('w-full h-96')
    
    # caso a diferença de vazão esteja com uma diferença aceitável
    elif dif_current_flow <= DIF_ACCEPT_FLOW:
        CHART_SENSOR_FLOW = ui.echart({
                'title': {
                    'text': 'Diferença de Vazão no Trecho 1',
                    'textStyle': {'color': "#FFFFFF"},
                    'left': 'center',
                    'top': '10' 
                },
                'tooltip': {'trigger': 'axis'},
                'xAxis': {
                    'name': 'Data/Hora',
                    'textStyle': {'color': "#FFFFFF"},
                    'type': 'category', 
                    'data': [], 
                    'axisLabel': {'color': "#FFFFFF", 'rotate': 45},
                    'color': '#CBD5E1',
                    'axisLine': {
                        'lineStyle': {'color': "#FFFFFF"}
                    }
                },
                'yAxis': {
                    'type': 'value', 
                    'name': 'Diferença de Vazão (L/s)',
                    'nameTextStyle': {'color': "#FFFFFF"},
                    'min': -10,
                    'max': 10,
                    'axisLabel': {'color': '#FFFFFF'}, 
                    'axisLine': {
                        'show': True, 
                        'lineStyle': {'color': '#FFFFFF'} 
                    },
                    'splitLine': {
                        'show': True,
                        'lineStyle': {
                            'color': "#FFFFFF", 
                            'type': 'dashed'    
                        }
                    }
                },
                'series': [{
                    'name': 'Sensor 1',
                    'type': 'line',
                    'smooth': True,
                    'data': [],
                    'lineStyle': {'color': "#2FBE5F", 'width': 3},
                    'areaStyle': {'opacity': 0.4, 'color': "#A8F3A5"},
                    'symbol': 'circle', 
                    'symbolSize': 8,    
                    'itemStyle': {
                        'color': "#104600",      
                        'borderColor': "#D3E7CC", 
                        'borderWidth': 2          
                    }
                }],
                 
            }).classes('w-full h-96')
    
    # caso a diferença de vazão notifique algum vazamento ou algo de errado com o trecho
    else:
        CHART_SENSOR_FLOW = ui.echart({
                'title': {
                    'text': 'Diferença de Vazão no Trecho 1',
                    'textStyle': {'color': "#FFFFFF"},
                    'left': 'center',
                    'top': '10' 
                },
                'tooltip': {'trigger': 'axis'},
                'xAxis': {
                    'name': 'Data/Hora',
                    'textStyle': {'color': "#FFFFFF"},
                    'type': 'category', 
                    'data': [], 
                    'axisLabel': {'color': "#FFFFFF", 'rotate': 45},
                    'color': '#CBD5E1',
                    'axisLine': {
                        'lineStyle': {'color': "#EB8B5F"}
                    }
                },
                'yAxis': {
                    'type': 'value', 
                    'name': 'Diferença de Vazão (L/s)',
                    'nameTextStyle': {'color': "#FFFFFF"},
                    'min': -10,
                    'max': 10,
                    'axisLabel': {'color': '#FFFFFF'}, 
                    'axisLine': {
                        'show': True, 
                        'lineStyle': {'color': '#FFFFFF'} 
                    },
                    'splitLine': {
                        'show': True,
                        'lineStyle': {
                            'color': "#DB977C", 
                            'type': 'dashed'   
                        }
                    }
                },
                'series': [{
                    'name': 'Sensor 1',
                    'type': 'line',
                    'smooth': True,
                    'data': [],
                    'lineStyle': {'color': "#FF5E00", 'width': 3},
                    'areaStyle': {'opacity': 0.4, 'color': "#F3BBA5"},
                    'symbol': 'circle', 
                    'symbolSize': 8,    
                    'itemStyle': {
                        'color': '#FACC15',      
                        'borderColor': '#FFFFFF', 
                        'borderWidth': 2          
                    }
                }],

            }).classes('w-full h-96')

    # checa se a linha está completa, separa os tipos de dados e atualiza o gráfico para os novos valores
    for row in data_temp:
        if len(row) == 2:
            time_list.append(row[1])
            values_list.append(float(row[0]))

    CHART_SENSOR_FLOW.options['xAxis']['data'] = time_list
    CHART_SENSOR_FLOW.options['series'][0]['data'] = values_list
    CHART_SENSOR_FLOW.update()
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
        ui.notify('Redirecionando para página inicial...', type='ongoing')
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

    elif new_page == 'history' and current_page == 'dashboard':

        # gera uma notificação
        ui.notify('Abrindo o histórico...', type='ongoing')
        # simula tempo de boot
        await asyncio.sleep(2.0) 
        # direciona para a página history
        ui.navigate.to('/history')

    elif new_page == 'dashboard' and current_page == 'history':

        # gera uma notificação
        ui.notify('Fechando histórico...', type='ongoing')
        await asyncio.sleep(1.2) 
        ui.notify('Atualizando sistema...', type='ongoing')
        await asyncio.sleep(2.0) 
        # direciona para a página history
        ui.navigate.to('/dashboard')

    elif new_page == 'home' and current_page == 'history':

        # gera notificações e simula o tempo de boot
        ui.notify('Fechando histórico...', type='ongoing')
        await asyncio.sleep(1.2) 
        ui.notify('Redirecionando para página inicial...', type='ongoing')
        await asyncio.sleep(1.5) 
        # direciona para a Home
        ui.navigate.to('/')
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

    # pega a última linha e separa os dados pela ','
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
# função utilizada para pegar os dados para fazer os gŕaficos, ou seja, pega as últimas 20 linhas do arquivo escolhido
def get_all_data(arc):

    linhas = [] 
    dados = []
    arch = ""

    # define o arquivo que quero acessar
    if arc == 'temp':
        arch = TEMP_SENSORS_DATA_FILE
    elif arc == "flow":
        arch = FLOW_DIFFERENCE_FILE
    else:
        return dados

    # tenta ler o arquivo, caso haja algum erro, cria uma excessão
    try:
        # caso o arquivo não exista
        if not os.path.exists(arch):
            print("Arquivo não existe!")
            return dados

        # abre o arquivo apenas para leitura
        with open(arch, 'r') as f:
            linhas = f.readlines()
        
    except Exception as e:
        print(f"Erro ao ler: {e}")
        return dados

    # proteção contra arquivo vazio
    if len(linhas) == 0:
        return dados

    # pega as últimas 20 linhas e separa os dados pela ','
    ultimas_linhas = linhas[-20:] 
    for linha in ultimas_linhas:
        partes = linha.strip().split(',')
        dados.append(partes)

    return dados
#-----------------------------------------------------------------------------------------------------------------
# função utilizada para pegar as 10 últimas linhas do "debug_data.txt" para gerar os alertas recentes na dashboard
def get_debug_data():
     
    linhas = [] 
    dados = []

    # tenta ler o arquivo, caso haja algum erro, cria uma excessão
    try:
        # caso o arquivo não exista
        if not os.path.exists(DEBUG_FILE):
            print("Arquivo não existe!")
            return dados

        # abre o arquivo apenas para leitura
        with open(DEBUG_FILE, 'r') as f:
            linhas = f.readlines()
        
    except Exception as e:
        print(f"Erro ao ler: {e}")
        return dados

    # proteção contra arquivo vazio
    if len(linhas) == 0:
        return dados

    # pega as últimas 10 linhas e separa os dados pela ','
    ultimas_linhas = linhas[-10:] 
    for linha in ultimas_linhas:
        partes = linha.strip().split(',')
        dados.append(partes)

    return dados
#-----------------------------------------------------------------------------------------------------------------
# para um desenvolvimento futuro, fazer um merge entre essa função e as de cima é possível
# função responsável para pegar as últimas 150 para a construção da aba de histórico
def get_all_debug_data():
     
    linhas = [] 
    dados = []

    # tenta ler o arquivo, caso haja algum erro, cria uma excessão
    try:
        # caso o arquivo não exista
        if not os.path.exists(DEBUG_FILE):
            print("Arquivo não existe!")
            return dados

        # abre o arquivo apenas para leitura
        with open(DEBUG_FILE, 'r') as f:
            linhas = f.readlines()
        
    except Exception as e:
        print(f"Erro ao ler: {e}")
        return dados

    # proteção contra arquivo vazio
    if len(linhas) == 0:
        return dados

    # pega as últimas 150 linhas e separa os dados pela ','
    ultimas_linhas = linhas[-150:] 
    for linha in ultimas_linhas:
        partes = linha.strip().split(',')
        dados.append(partes)

    return dados
#-----------------------------------------------------------------------------------------------------------------
# função que atualiza o histórico dos alertas recentes da aba dashboard
@ui.refreshable
def update_history():

    # pega as últimas 10 linhas do arquivo e inverte, para que a última escritaa passe a ser a primeira na lista
    debug_data = get_debug_data()
    debug_data.reverse()
    count = 0

    # cria as notificações no 'timeline' de avisos reentes
    for row in debug_data:
        if len(row) == 2:
           
            with ui.timeline(side='right').classes('w-full max-w-md'):  

                # caso seja a primeira, será plotada com uma cor vermelha mais viva e um icon distindo
                if count == 0:
                    ui.timeline_entry(
                        title=f"{row[0]}",
                        subtitle=f"{row[1]}",
                        icon = 'notifications_active',
                    ).classes('text-xl font-bold text-red-600') \
                     .props('color=red-600')

                # caso contrário, um vermelho mais escuro
                else:
                    ui.timeline_entry(
                        title=f"{row[0]}",
                        subtitle=f"{row[1]}",
                        icon = 'notifications',
                    ).classes('text-xl font-bold text-black') \
                     .props('color=red-900')
                    
            # atualiza o contador
            count = count+1  
    count = 0
#-----------------------------------------------------------------------------------------------------------------
# função para utilizar no timer e recarregar a página das temperaturas
@ui.refreshable
def temp_expansions():

    # pega as últimas temperaturas 
    CURRENT_TEMP_TIME, CURRENT_TEMPERATURE = get_current_data('temp')

    # cria uma expansão, uma para cada sensor no sistema
    for i in range(NUM_SENSORS):

        # verifica se a temperatura está dentro do esperado, caso contrário, haverá avisos!
        if CURRENT_TEMPERATURE[i] >= MIN_TEMP and CURRENT_TEMPERATURE[i] <= MAX_TEMP:
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
                
                # chama a função de criação dos gráficos
                if i == 0:
                    define_and_update_graphic_temp1()
                elif i == 1:
                    define_and_update_graphic_temp2()

                # faz chamar essas funções de 30 em 30 segundos
                ui.timer(30, define_and_update_graphic_temp1.refresh)
                ui.timer(30, define_and_update_graphic_temp2.refresh)
        
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

                # chama a função de criação dos gráficos
                if i == 0:
                    define_and_update_graphic_temp1()
                elif i == 1:
                    define_and_update_graphic_temp2()

                # faz chamar essas funções de 30 em 30 segundos
                ui.timer(30, define_and_update_graphic_temp1.refresh)
                ui.timer(30, define_and_update_graphic_temp2.refresh)

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

                # chama a função de criação dos gráficos
                if i == 0:
                    define_and_update_graphic_temp1()
                elif i == 1:
                    define_and_update_graphic_temp2()

                # faz chamar essas funções de 30 em 30 segundos
                ui.timer(30, define_and_update_graphic_temp1.refresh)
                ui.timer(30, define_and_update_graphic_temp2.refresh)
        
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

                # chama a função de criação dos gráficos
                if i == 0:
                    define_and_update_graphic_temp1()
                elif i == 1:
                    define_and_update_graphic_temp2()

                # faz chamar essas funções de 30 em 30 segundos
                ui.timer(30, define_and_update_graphic_temp1.refresh)
                ui.timer(30, define_and_update_graphic_temp2.refresh)
#-----------------------------------------------------------------------------------------------------------------
# função para utilizar no timer e recarregar a página das vazões
@ui.refreshable
def flow_expansions():
    # pega as últimas vazões 
    CURRENT_FLOW_TIME, CURRENT_FLOW = get_current_data('flow')

    # cria uma expansão, uma para cada sensor no sistema
    for i in range(NUM_SENSORS):

        # caso em que o sensor está disconectado
        if CURRENT_FLOW[i] == DISC_FLOW:
            with ui.expansion(f'Sensor de Vazão {i+1}', icon='sensors_off') \
                .classes('w-full bg-slate-800 text-gray-500 rounded-xl mb-2 border-2 border-red-700 shadow-lg'):
        
                # o que aparecerá quando abrir a expansão
                with ui.row().classes('w-full items-center justify-between p-2'):
                    
                    with ui.column():
                        ui.label('Leitura Atual').classes('text-xs text-gray-400 uppercase tracking-wider')
                        ui.label(f'0.00L/s').classes('text-4xl font-mono text-gray-900 font-bold')

                    # mostrará o status do sensor
                    with ui.column().classes('items-end'):
                        ui.label('Status: Disconectado').classes('text-sm text-red-400')
                        ui.label(f'Última atualização: 00:00:00').classes('text-xs text-gray-500')

        # caso em que o sensor está conectado
        else: 
            with ui.expansion(f'Sensor de Vazão {i+1}', icon='waves') \
                .classes('w-full bg-slate-800 text-white rounded-xl mb-2 border border-slate-700 shadow-lg'):
        
                # o que aparecerá quando abrir a expansão
                with ui.row().classes('w-full items-center justify-between p-2'):
                    
                    # mostrará o último valor lido do sensor de vazão
                    with ui.column():
                        ui.label('Leitura Atual').classes('text-xs text-gray-400 uppercase tracking-wider')
                        ui.label(f'{CURRENT_FLOW[i]:.2f}L/s').classes('text-4xl font-mono text-emerald-400 font-bold')

                    # mostrará o status do sensor
                    with ui.column().classes('items-end'):
                        ui.label('Status: Ativo').classes('text-sm text-green-400')
                        ui.label(f'Última atualização: {CURRENT_FLOW_TIME}').classes('text-xs text-gray-500')
#-----------------------------------------------------------------------------------------------------------------
# função para utilizar no timer e recarregar a página das vazões
@ui.refreshable
def stretch_expansions():
    
    CURRENT_FLOW_TIME, CURRENT_FLOW = get_current_data('flow')

    # cria uma expansão a cada 2 sensores no sistema
    for i in range(NUM_SENSORS-1):
        # calcula a diferença entre as vazões lidas
        dif_current_flow = CURRENT_FLOW[i] - CURRENT_FLOW[i+1]

        # caso em que algum sensor está disconetado
        if CURRENT_FLOW[i] == DISC_FLOW or CURRENT_FLOW[i+1] == DISC_FLOW:
            with ui.expansion(f'Trecho {i+1}', icon='sensors_off') \
                .classes('w-full bg-slate-800 text-gray-500 rounded-xl mb-2 border-2 border-red-700 shadow-lg'):
        
                # o que aparecerá quando abrir a expansão
                with ui.row().classes('w-full items-center justify-between p-2'):
                    
                    with ui.column():
                        ui.label('Diferença atual entre as vazões').classes('text-xs text-gray-400 uppercase tracking-wider')
                        ui.label(f'0.00L/s').classes('text-4xl font-mono text-gray-900 font-bold')

                    # mostrará o status do sensor
                    with ui.column().classes('items-end'):
                        ui.label('Última atualização: 00:00:00').classes('text-sm text-red-400')
                        ui.label(f'Trecho monitorado pelos sensores {i+1} e {i+2}').classes('text-xs text-gray-500')

                # chama a função de criação dos gráficos
                if i == 0:
                    define_and_update_graphic_flow()
                
                # faz chamar essa função de 30 em 30 segundos
                ui.timer(30, define_and_update_graphic_flow.refresh)

        # caso em que a vazão está normal
        elif CURRENT_FLOW[i] - CURRENT_FLOW[i+1] <= DIF_ACCEPT_FLOW:
            with ui.expansion(f'Trecho {i+1}', icon='linear_scale') \
                .classes('w-full bg-slate-800 text-white rounded-xl mb-2 border border-slate-700 shadow-lg'):
        
                # o que aparecerá quando abrir a expansão
                with ui.row().classes('w-full items-center justify-between p-2'):
                    
                    # mostrará o último valor lido do sensor de temperatura
                    with ui.column():
                        ui.label('Diferença atual entre as vazões').classes('text-xs text-gray-400 uppercase tracking-wider')
                        ui.label(f'{dif_current_flow:.2f}L/s').classes('text-4xl font-mono text-emerald-400 font-bold')

                    # mostrará o status do sensor
                    with ui.column().classes('items-end'):
                        ui.label(f'Última atualização: {CURRENT_FLOW_TIME}').classes('text-sm text-green-400')
                        ui.label(f'Trecho monitorado pelos sensores {i+1} e {i+2}').classes('text-xs text-gray-500')

                # chama a função de criação dos gráficos
                if i == 0:
                    define_and_update_graphic_flow()
                
                # faz chamar essa função de 30 em 30 segundos
                ui.timer(30, define_and_update_graphic_flow.refresh)
        
        # caso em que a diferença de vazão é maior que 1
        else: 
            with ui.expansion(f'Trecho {i+1}', icon='water_drop') \
                .classes('w-full bg-red-800 text-white rounded-xl mb-2 border border-red-700 shadow-lg'):
        
                # o que aparecerá quando abrir a expansão
                with ui.row().classes('w-full items-center justify-between p-2'):
                    
                    # mostrará o último valor lido do sensor de temperatura
                    with ui.column():
                        ui.label('Diferença atual entre as vazões').classes('text-xs text-red-400 uppercase tracking-wider')
                        ui.label(f'{dif_current_flow:.2f}L/s').classes('text-4xl font-mono text-white font-bold')

                    # mostrará o status do sensor
                    with ui.column().classes('items-end'):
                        ui.label(f'Última atualização: {CURRENT_FLOW_TIME}').classes('text-sm text-white')
                        ui.label(f'Trecho monitorado pelos sensores {i+1} e {i+2}').classes('text-xs text-gray-300')
                
                # chama a função de criação dos gráficos
                if i == 0:
                    define_and_update_graphic_flow()
                
                # faz chamar essa função de 30 em 30 segundos
                ui.timer(30, define_and_update_graphic_flow.refresh)
#-----------------------------------------------------------------------------------------------------------------
# faz a bolinha com 3 barrinhas do menu abrir e fechar, mostrando outros botões
def toggle_menu():
    # inverte o estado do menu
    MENU_STATE['aberto'] = not MENU_STATE['aberto']
#-----------------------------------------------------------------------------------------------------------------
# cria o bloco/cartão para ser plotado no histórico de cada notificação
def make_block_notification(item):
    # checa se a linha está completa e cria o bloco
    if len(item) == 2:
        with ui.card().classes('w-full p-2 bg-slate-100 shadow-sm border border-slate-200'):
            with ui.row().classes('items-center gap-2'):
                ui.icon('notifications', color='red').classes('text-xl')
                ui.label(f"#{item[0]}").classes('font-bold text-slate-700')
                ui.label(f"{item[1]}").classes('text-xs text-gray-500')
#-----------------------------------------------------------------------------------------------------------------
# faz o gerenciamento do histórico, do que mostrar em cada aba e a parte do mecanismo de passar as páginas
@ui.refreshable
def update_notifications(pagina_atual):

    # pega as últimas 150 linhas do arquivo "debug_data.txt" e inverte a lista
    debug_data = get_all_debug_data()
    debug_data.reverse()

    # conta que gerencia a paginação
    items_por_pagina = 30
    inicio = (pagina_atual - 1) * items_por_pagina
    fim = inicio + items_por_pagina
    
    # Pega apenas os 30 itens dessa página dentro da lista de 150 itens
    dados_pagina = debug_data[inicio:fim]
    
    # Separa 15 para o lado esquerdo da tela e 15 para o direito
    lado_esquerdo = dados_pagina[:15]
    lado_direito = dados_pagina[15:]

    # configuração das colunas e separação delas por uma linha vertical
    # usamos grid com 3 colunas: [Conteúdo Esquerda] [Linha] [Conteúdo Direita]
    with ui.grid().classes('grid-cols-[1fr_auto_1fr] w-full gap-4'):
        
        # cria as notificações do lado esquerdo
        with ui.column().classes('w-full gap-3'):
            for item in lado_esquerdo:
                make_block_notification(item)
        
        # Uma linha fina cinza que ocupa toda a altura da página
        ui.element('div').classes('w-[2px] bg-slate-300 h-full mx-auto rounded')

        # cria as notificações do lado direito
        with ui.column().classes('w-full gap-3'):
            for item in lado_direito:
                make_block_notification(item)
#-----------------------------------------------------------------------------------------------------------------

#==================================================================================================================
# -------------------------------------------------- HISTORY ---------------------------------------------------
#==================================================================================================================

#----------------------------------------------------------------------------------------------------------------- 
# definição da página do histórico
@ui.page('/history')
def history_page():
    
    # definição dos botões interativos do menu
    with ui.column().classes('fixed bottom-5 right-5 z-100 gap-3 items-center'):

        # declaração do botão de histórico
        ui.button(icon='bar_chart', on_click=lambda: go_to_page('dashboard','history')) \
            .classes('rounded-full w-12 h-12 !bg-indigo-900 !hover:bg-indigo-600 shadow-xl text-white') \
            .bind_visibility_from(MENU_STATE, 'aberto') # só aparece se 'aberto' for True

        # declaração do botão da página inicial
        ui.button(icon='home', on_click=lambda: go_to_page('home', 'history')) \
            .classes('rounded-full w-12 h-12 !bg-blue-900 !hover:bg-blue-600 shadow-xl text-white') \
            .bind_visibility_from(MENU_STATE, 'aberto') # só aparece se 'aberto' for True

        # declaração do botão de controle desse "menu"
        ui.button(on_click=toggle_menu) \
            .classes('rounded-full w-16 h-16 !bg-slate-800 !hover:bg-slate-700 shadow-2xl text-white text-xl border-2 border-slate-600') \
            .bind_icon_from(MENU_STATE, 'aberto', 
                    backward=lambda x: 'close' if x else 'menu') # muda o icon se tiver aberto ou fechado
        
    # o icon no começo da página acima de 'HISTÓRICO"
    ui.icon('manage_history', color='blue-800', size='3em')
    
    with ui.column().classes('gap-0'):
        # o título 
        ui.label('HISTÓRICO') \
            .classes('fonte-titulo text-4xl text-blue-800 tracking-wide')
        
        # o subtítulo
        ui.label('Registro de Atividades') \
            .classes('text-sm text-gray-500 font-bold uppercase tracking-widest')

    # área que será atualizada
    update_notifications(1)

    # espaçador para empurrar a paginação para baixo (opcional)
    ui.space()

    # container centralizado (items-center)
    with ui.column().classes('w-full items-center mt-2'):
        # o componente de paginação
        paginacao = ui.pagination(1, 5, direction_links=True) \
            .classes('shadow-lg bg-white rounded-lg')
        
        # quando mudar o valor, atualiza a função lá em cima
        paginacao.on_value_change(lambda: update_notifications.refresh(paginacao.value))

        ui.timer(30, lambda: update_notifications.refresh(paginacao.value))

ui.run()
#-----------------------------------------------------------------------------------------------------------------

#==================================================================================================================
# ------------------------------------------------- DASHBOARD --------------------------------------------------
#==================================================================================================================

#----------------------------------------------------------------------------------------------------------------- 
# definição da tela dashboard
@ui.page('/dashboard')
def dashboard_page():
    with ui.row().classes('w-full h-screen gap-0 no-wrap'):
        
        # definição da coluna que fica do lado esquerdo da tela e ocupa 1/5 da sua largura
        with ui.column().classes('w-1/5 bg-gray-100 p-4 border-r border-slate-300'):

            with ui.column().classes('w-full items-center mb-5'):
                
                # título e subtítulo da coluna
                ui.label('Monitoramento') \
                    .classes('text-red-500 text-sm uppercase tracking-widest')
                
                ui.label('Alertas Recentes') \
                    .classes('text-3xl font-bold')
                
                # atualiza os alertas recentes de 30 em 30 segs
                update_history()
                ui.timer(30, update_history.refresh)

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
                    ui.timer(30, temp_expansions.refresh)
                    
                # aba "FLOW" mostrará o gráfico das vazões recebidas ao longo do tempo
                with ui.tab_panel(flow):
                    # carrega a página e faz o reload a cada 60 segs
                    flow_expansions()
                    ui.separator()
                    stretch_expansions()
                    ui.timer(30, flow_expansions.refresh)
                    ui.timer(30, stretch_expansions.refresh)

        # difinição no menu interativo
        with ui.column().classes('fixed bottom-5 right-5 z-100 gap-3 items-center'):

            # declaração do botão de histórico
            ui.button(icon='history', on_click=lambda: go_to_page('history','dashboard')) \
                .classes('rounded-full w-12 h-12 !bg-indigo-900 !hover:bg-indigo-600 shadow-xl text-white') \
                .bind_visibility_from(MENU_STATE, 'aberto') # só aparece se 'aberto' for True

            # declaração do botão da página inicial
            ui.button(icon='home', on_click=lambda: go_to_page('home', 'dashboard')) \
                .classes('rounded-full w-12 h-12 !bg-blue-900 !hover:bg-blue-600 shadow-xl text-white') \
                .bind_visibility_from(MENU_STATE, 'aberto') # só aparece se 'aberto' for True

            # declaração do botão de controle desse "menu"
            ui.button(on_click=toggle_menu) \
                .classes('rounded-full w-16 h-16 !bg-slate-800 !hover:bg-slate-700 shadow-2xl text-white text-xl border-2 border-slate-600') \
                .bind_icon_from(MENU_STATE, 'aberto', 
                        backward=lambda x: 'close' if x else 'menu')
            
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
if __name__ == "__main__":
    ui.run(title='Sensor App')
#----------------------------------------------------------------------------------------------------------------- 