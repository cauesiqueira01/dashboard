# Dashboard de Atendimento

Dashboard interativo para análise de métricas de atendimento ao cliente, desenvolvido com Python Dash.

## Funcionalidades

- **KPIs Principais**: Total de chamados entrantes, fechados, TIT dentro do prazo, SLA dentro do prazo e reaberturas
- **Análise por Dimensão**: Gráficos comparativos por empresa e status
- **Visão Histórica**: Tendências de chamados ao longo do tempo
- **Filtros Interativos**: Por empresa, status TIT e SLA
- **Tabela Detalhada**: Lista completa de chamados com filtros aplicados

## Tecnologias

- Python 3.11
- Dash 3.1.1
- Plotly 6.2.0
- Pandas 2.3.0
- Gunicorn (para deployment)

## Instalação Local

1. Clone o repositório
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o aplicativo:
   ```bash
   python app.py
   ```
4. Acesse: http://localhost:8051

## Deployment no Render

Este projeto está configurado para deployment automático no Render. Basta conectar o repositório GitHub ao Render e o deployment será feito automaticamente.

## Estrutura dos Dados

O dashboard trabalha com dados simulados baseados na estrutura de planilhas Excel com:

- **Base de Entrantes**: Data/hora abertura, Empresa
- **Base de Fechamento**: Data/hora encerramento, TIT, SLA, Reaberturas, Empresa

Para usar dados reais, substitua a função `gerar_dados_simulados()` por uma função que leia dados de planilhas Excel.

