import time
import random
from nicegui import ui

# --- Configurações Iniciais ---
MAX_POINTS = 10  # Mantém o gráfico limpo com os últimos 10 pontos

def root():
    
    # 1. Componente para exibir a última leitura (Opcional)
    last_reading_label = ui.label('Aguardando a primeira leitura...').classes('text-xl font-medium')
    
    # 2. Configuração do Gráfico ECharts
    chart = ui.echart({
        'title': {'text': 'Leitura de Temperatura Simulada'},
        'xAxis': {
            'type': 'time',
            'axisLabel': {'formatter': 'HH:mm:ss', 'hideOverlap': True},
            'splitLine': {'show': False}
        },
        'yAxis': {
            'type': 'value', 
            'name': 'Temperatura (°C)', 
            'min': 20, 
            'max': 35 # Faixa de valores simulada
        },
        'series': [{'type': 'line', 'data': [], 'smooth': True, 'name': 'Simulação'}],
        'tooltip': {
            'trigger': 'axis',
        },
    }).classes('w-full h-96')

    # 3. Função de Atualização (Substitui o 'update_chart' do seu código original)
    def update_chart(temperature: float):
        """Adiciona o novo ponto de temperatura ao gráfico e o atualiza."""
        
        # O ECharts usa milissegundos para o tipo 'time'
        current_time_ms = int(time.time() * 1000) 
        
        # Acessa os dados da série
        data = chart.options['series'][0]['data']
        
        # Adiciona o novo ponto [timestamp_ms, valor]
        data.append([current_time_ms, temperature])
        
        # Remove o ponto mais antigo se exceder o limite
        if len(data) > MAX_POINTS:
            data.pop(0)
            
        # Força a atualização do gráfico na interface
        chart.update()
        
        # Atualiza o label
        last_reading_label.set_text(f'Temperatura Atual: {temperature:.2f}°C')


    # 4. Função para Gerar Dados Aleatórios (Substitui o webhook da API)
    def generate_random_data():
        """Gera um valor aleatório e o envia para a função de atualização."""
        # Simula uma variação de temperatura entre 25.0 e 30.0
        new_temperature = random.uniform(25.0, 30.0)
        if (new_temperature > 27):
             ui.notify("AAAAAAAAAAAAAA")
        update_chart(new_temperature)
        
        
    # 5. O Timer: Agendamento da Geração de Dados
    # O timer executa a função 'generate_random_data' a cada 1.0 segundo.
    ui.timer(5.0, callback=generate_random_data)


# --- Inicializar a Aplicação ---
ui.run(root)