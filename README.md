# pipemon-raspberry-server

Servidor auxiliar para coleta e visualização de dados via MQTT.

**Descrição**
- Reúne um subscriber MQTT (`mqtt_subscriber.py`), um gerador/agrupador de logs (`make_log.py`) e uma interface/visualizador (`dashboard.py`).

**Requisitos**
- Python 3.8+
- Dependências do projeto: instalar via `requirements.txt`.
- Um broker MQTT ativo (Mosquitto). Há scripts de suporte: [broker_setup.sh](broker_setup.sh) e [broker_kill.sh](broker_kill.sh).

**Estrutura principal**
- [`mqtt_subscriber.py`](mqtt_subscriber.py): inscreve-se nos tópicos MQTT e armazena dados.
- [`make_log.py`](make_log.py): processa dados e gera logs em `logs/`.
- [`dashboard.py`](dashboard.py): dashboard para visualizar os dados.
- `examples/`: exemplos de publisher/subscriber para testes.
- `sensors_data/`, `logs/`: arquivos e logs gerados.

**Instalação no Ubuntu 22.04**
1. Crie e ative um ambiente virtual (recomendado):

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Certifique-se de que o broker MQTT está rodando.

```bash
bash broker_setup.sh
```

**Como rodar (importante: rodar os três ao mesmo tempo)**

Escolha uma das opções abaixo para executar simultaneamente `mqtt_subscriber.py`, `make_log.py` e `dashboard.py`.

```bash
python3 mqtt_subscriber.py
python3 make_log.py
python3 dashboard.py
```

**Observações**:
- Sempre inicie primeiro o broker MQTT antes dos outros scripts.
- Os logs são gravados em `logs/`. Dados brutos ficam em `sensors_data/`.

**Testes e exemplos**
- Use os exemplos em [`examples/publisher.py`](examples/publisher.py) para enviar mensagens de teste.

**Problemas comuns**
- Se não receber dados, verifique se o broker está ativo e as configurações de tópico no `mqtt_subscriber.py`. Se os problemas persistirem, pare o broker e execute novamente.
- Verifique permissões de escrita nas pastas `logs/` e `sensors_data/`.
