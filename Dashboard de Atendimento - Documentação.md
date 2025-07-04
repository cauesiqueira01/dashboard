# Dashboard de Atendimento - Documentação

## Visão Geral

O Dashboard de Atendimento é um sistema web interativo desenvolvido para visualizar e analisar métricas de atendimento ao cliente. O sistema permite acompanhar indicadores chave de performance (KPIs), analisar tendências históricas e filtrar dados por diferentes critérios.

## Funcionalidades Principais

### 1. Indicadores Chave de Performance (KPIs)
O dashboard apresenta cinco KPIs principais na parte superior:

- **Total de Chamados Entrantes**: Número total de chamados que entraram no sistema
- **Total de Chamados Fechados**: Número total de chamados que foram resolvidos/fechados
- **TIT Dentro do Prazo**: Percentual de chamados com Tempo de Interação Total dentro do prazo estabelecido
- **SLA Dentro do Prazo**: Percentual de chamados que atenderam ao Service Level Agreement
- **Reaberturas**: Percentual de chamados que foram reabertos

### 2. Análise por Dimensão
Esta seção apresenta dois gráficos de barras:

- **Total de Chamados por Empresa**: Compara o volume de chamados entrantes e fechados para cada empresa (Memora e Seduc)
- **Status TIT e SLA**: Mostra a distribuição dos status "DENTRO" e "FORA" do prazo para TIT e SLA

### 3. Visão Histórica
Gráfico de linha que mostra a tendência de chamados entrantes e fechados ao longo do tempo, permitindo identificar padrões sazonais e tendências de crescimento ou declínio.

### 4. Filtros e Detalhes
Seção interativa que inclui:

- **Filtros**: Por empresa, status TIT e status SLA
- **Tabela de Detalhes**: Lista detalhada dos chamados com informações como ID, empresa, datas de abertura e encerramento, status TIT, SLA e reaberturas

## Estrutura dos Dados

O sistema foi projetado para trabalhar com dados de planilhas Excel contendo duas guias principais:

### Base de Entrantes
- **Coluna**: Data/hora abertura
- **Coluna**: Empresa (AV)

### Base de Fechamento
- **Coluna**: Data/hora encerramento
- **Coluna**: Empresa (AX - Guia Gestor)
- **Coluna**: TIT (BA) - Status: "DENTRO" ou "FORA"
- **Coluna**: SLA 2 (BA) - Status: "DENTRO" ou "FORA"
- **Coluna**: Reabertos (BC) - Status: "SIM" ou "NÃO"

## Tecnologias Utilizadas

- **Python 3.11**: Linguagem de programação principal
- **Dash**: Framework para criação de aplicações web interativas
- **Plotly**: Biblioteca para criação de gráficos interativos
- **Pandas**: Biblioteca para manipulação e análise de dados
- **OpenPyXL**: Biblioteca para leitura de arquivos Excel

## Instalação e Execução

### Pré-requisitos
- Python 3.11 ou superior
- Pip (gerenciador de pacotes Python)

### Instalação das Dependências
```bash
pip install dash plotly pandas openpyxl
```

### Execução do Dashboard
```bash
python dashboard_atendimento_corrigido.py
```

O dashboard estará disponível em: `http://localhost:8051`

## Estrutura do Código

### Principais Componentes

1. **Geração de Dados Simulados**: Função `gerar_dados_simulados()` que cria dados de exemplo baseados na estrutura real da planilha
2. **Cálculo de KPIs**: Função `calcular_kpis()` que processa os dados e calcula as métricas principais
3. **Layout do Dashboard**: Definição da estrutura visual usando componentes Dash
4. **Callbacks Interativos**: Funções que atualizam os gráficos e tabelas baseadas nas interações do usuário

### Callbacks Principais

- `atualizar_grafico_empresa()`: Atualiza o gráfico de chamados por empresa
- `atualizar_grafico_status()`: Atualiza o gráfico de status TIT e SLA
- `atualizar_tendencia_chamados()`: Atualiza o gráfico de tendência histórica
- `atualizar_tabela_detalhes()`: Atualiza a tabela de detalhes baseada nos filtros selecionados

## Personalização

### Adaptação para Dados Reais
Para usar o dashboard com dados reais de uma planilha Excel:

1. Substitua a função `gerar_dados_simulados()` por uma função que leia os dados da planilha real
2. Ajuste os nomes das colunas conforme a estrutura da sua planilha
3. Modifique os filtros e KPIs conforme necessário

### Exemplo de Leitura de Planilha Real
```python
import pandas as pd

def ler_dados_planilha(caminho_arquivo):
    # Ler guia de entrantes
    df_entrantes = pd.read_excel(caminho_arquivo, sheet_name='base de entrantes')
    
    # Ler guia de fechamento
    df_fechados = pd.read_excel(caminho_arquivo, sheet_name='BASE DE FECHAMENTO')
    
    return df_entrantes, df_fechados
```

## Manutenção e Suporte

### Atualizações de Dados
O dashboard pode ser configurado para atualizar automaticamente os dados em intervalos regulares ou mediante upload manual de novas planilhas.

### Monitoramento
Recomenda-se monitorar o desempenho do dashboard e ajustar os filtros e visualizações conforme o crescimento do volume de dados.

### Backup
Mantenha backups regulares dos dados e do código do dashboard para garantir a continuidade do serviço.

## Conclusão

O Dashboard de Atendimento fornece uma visão abrangente e interativa das métricas de atendimento, permitindo análises do macro ao micro através de KPIs, gráficos de tendência e filtros detalhados. A arquitetura modular facilita futuras expansões e personalizações conforme as necessidades específicas da organização.

