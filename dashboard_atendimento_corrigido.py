import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuração da aplicação Dash
app = dash.Dash(__name__)
app.title = "Dashboard de Atendimento"

# Função para gerar dados simulados baseados na estrutura da planilha Excel
def gerar_dados_simulados():
    """
    Gera dados simulados baseados na estrutura da planilha Excel do usuário
    """
    # Configurações
    num_registros = 500
    empresas = ['Memora', 'Seduc']
    status_tit = ['DENTRO', 'FORA']
    status_sla = ['DENTRO', 'FORA']
    status_reabertos = ['SIM', 'NÃO']
    
    # Data base para simulação (últimos 6 meses)
    data_fim = datetime.now()
    data_inicio = data_fim - timedelta(days=180)
    
    # Gerar dados para base de entrantes
    dados_entrantes = []
    for i in range(num_registros):
        data_abertura = data_inicio + timedelta(
            days=random.randint(0, 180),
            hours=random.randint(8, 18),
            minutes=random.randint(0, 59)
        )
        
        dados_entrantes.append({
            'Data/hora abertura': data_abertura,
            'Empresa': random.choice(empresas),
            'ID_Chamado': f'CH{i+1:04d}'
        })
    
    df_entrantes = pd.DataFrame(dados_entrantes)
    
    # Gerar dados para base de fechamento (80% dos chamados entrantes são fechados)
    num_fechados = int(num_registros * 0.8)
    dados_fechados = []
    
    for i in range(num_fechados):
        # Usar dados dos entrantes como base
        data_abertura = dados_entrantes[i]['Data/hora abertura']
        data_encerramento = data_abertura + timedelta(
            days=random.randint(1, 15),
            hours=random.randint(1, 8)
        )
        
        dados_fechados.append({
            'ID_Chamado': dados_entrantes[i]['ID_Chamado'],
            'Data/hora encerramento': data_encerramento,
            'Empresa': dados_entrantes[i]['Empresa'],
            'TIT': random.choice(status_tit),
            'SLA 2': random.choice(status_sla),
            'Reabertos': random.choice(status_reabertos)
        })
    
    df_fechados = pd.DataFrame(dados_fechados)
    
    return df_entrantes, df_fechados

# Gerar dados simulados
df_entrantes, df_fechados = gerar_dados_simulados()

# Função para calcular KPIs
def calcular_kpis(df_entrantes, df_fechados):
    """
    Calcula os KPIs principais do dashboard
    """
    total_entrantes = len(df_entrantes)
    total_fechados = len(df_fechados)
    
    # Percentuais de TIT, SLA e Reaberturas dentro do prazo
    tit_dentro_prazo = len(df_fechados[df_fechados['TIT'] == 'DENTRO']) / len(df_fechados) * 100 if len(df_fechados) > 0 else 0
    sla_dentro_prazo = len(df_fechados[df_fechados['SLA 2'] == 'DENTRO']) / len(df_fechados) * 100 if len(df_fechados) > 0 else 0
    reaberturas = len(df_fechados[df_fechados['Reabertos'] == 'SIM']) / len(df_fechados) * 100 if len(df_fechados) > 0 else 0
    
    return {
        'total_entrantes': total_entrantes,
        'total_fechados': total_fechados,
        'tit_dentro_prazo': tit_dentro_prazo,
        'sla_dentro_prazo': sla_dentro_prazo,
        'reaberturas': reaberturas
    }

# Calcular KPIs
kpis = calcular_kpis(df_entrantes, df_fechados)

# Layout do Dashboard
app.layout = html.Div([
    # Cabeçalho
    html.Div([
        html.H1("Dashboard de Atendimento", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'})
    ]),
    
    # Seção de KPIs (Visão Macro)
    html.Div([
        html.H2("Indicadores Chave de Performance (KPIs)", 
                style={'color': '#34495e', 'marginBottom': '20px'}),
        
        html.Div([
            # Total de Chamados Entrantes
            html.Div([
                html.H3(f"{kpis['total_entrantes']}", 
                        style={'fontSize': '48px', 'color': '#3498db', 'margin': '0'}),
                html.P("Total de Chamados Entrantes", 
                       style={'fontSize': '16px', 'color': '#7f8c8d', 'margin': '0'})
            ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#ecf0f1', 
                     'borderRadius': '10px', 'margin': '10px'}),
            
            # Total de Chamados Fechados
            html.Div([
                html.H3(f"{kpis['total_fechados']}", 
                        style={'fontSize': '48px', 'color': '#27ae60', 'margin': '0'}),
                html.P("Total de Chamados Fechados", 
                       style={'fontSize': '16px', 'color': '#7f8c8d', 'margin': '0'})
            ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#ecf0f1', 
                     'borderRadius': '10px', 'margin': '10px'}),
            
            # TIT Dentro do Prazo
            html.Div([
                html.H3(f"{kpis['tit_dentro_prazo']:.1f}%", 
                        style={'fontSize': '48px', 'color': '#e74c3c', 'margin': '0'}),
                html.P("TIT Dentro do Prazo", 
                       style={'fontSize': '16px', 'color': '#7f8c8d', 'margin': '0'})
            ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#ecf0f1', 
                     'borderRadius': '10px', 'margin': '10px'}),
            
            # SLA Dentro do Prazo
            html.Div([
                html.H3(f"{kpis['sla_dentro_prazo']:.1f}%", 
                        style={'fontSize': '48px', 'color': '#f39c12', 'margin': '0'}),
                html.P("SLA Dentro do Prazo", 
                       style={'fontSize': '16px', 'color': '#7f8c8d', 'margin': '0'})
            ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#ecf0f1', 
                     'borderRadius': '10px', 'margin': '10px'}),
            
            # Reaberturas
            html.Div([
                html.H3(f"{kpis['reaberturas']:.1f}%", 
                        style={'fontSize': '48px', 'color': '#9b59b6', 'margin': '0'}),
                html.P("Reaberturas", 
                       style={'fontSize': '16px', 'color': '#7f8c8d', 'margin': '0'})
            ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#ecf0f1', 
                     'borderRadius': '10px', 'margin': '10px'})
            
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-around'})
    ], style={'marginBottom': '40px'}),
    
    # Seção de Análise por Dimensão (Visão Média)
    html.Div([
        html.H2("Análise por Dimensão", 
                style={'color': '#34495e', 'marginBottom': '20px'}),
        
        html.Div([
            # Gráfico de Chamados por Empresa
            html.Div([
                dcc.Graph(id='grafico-chamados-empresa')
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            # Gráfico de Status TIT/SLA
            html.Div([
                dcc.Graph(id='grafico-status-tit-sla')
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ])
    ], style={'marginBottom': '40px'}),
    
    # Seção de Visão Histórica
    html.Div([
        html.H2("Visão Histórica", 
                style={'color': '#34495e', 'marginBottom': '20px'}),
        
        html.Div([
            # Tendência de Chamados ao Longo do Tempo
            html.Div([
                dcc.Graph(id='grafico-tendencia-chamados')
            ], style={'width': '100%'})
        ])
    ], style={'marginBottom': '40px'}),
    
    # Seção de Filtros e Detalhes (Visão Micro)
    html.Div([
        html.H2("Filtros e Detalhes", 
                style={'color': '#34495e', 'marginBottom': '20px'}),
        
        # Filtros
        html.Div([
            html.Div([
                html.Label("Filtrar por Empresa:"),
                dcc.Dropdown(
                    id='filtro-empresa',
                    options=[{'label': 'Todas', 'value': 'Todas'}] + 
                            [{'label': emp, 'value': emp} for emp in df_entrantes['Empresa'].unique()],
                    value='Todas'
                )
            ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),
            
            html.Div([
                html.Label("Filtrar por Status TIT:"),
                dcc.Dropdown(
                    id='filtro-tit',
                    options=[{'label': 'Todos', 'value': 'Todos'}] + 
                            [{'label': status, 'value': status} for status in df_fechados['TIT'].unique()],
                    value='Todos'
                )
            ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),
            
            html.Div([
                html.Label("Filtrar por Status SLA:"),
                dcc.Dropdown(
                    id='filtro-sla',
                    options=[{'label': 'Todos', 'value': 'Todos'}] + 
                            [{'label': status, 'value': status} for status in df_fechados['SLA 2'].unique()],
                    value='Todos'
                )
            ], style={'width': '30%', 'display': 'inline-block'})
        ], style={'marginBottom': '20px'}),
        
        # Tabela de Detalhes
        html.Div([
            dash_table.DataTable(
                id='tabela-detalhes',
                columns=[
                    {'name': 'ID Chamado', 'id': 'ID_Chamado'},
                    {'name': 'Empresa', 'id': 'Empresa'},
                    {'name': 'Data Abertura', 'id': 'Data_Abertura'},
                    {'name': 'Data Encerramento', 'id': 'Data_Encerramento'},
                    {'name': 'TIT', 'id': 'TIT'},
                    {'name': 'SLA', 'id': 'SLA_2'},
                    {'name': 'Reaberto', 'id': 'Reabertos'}
                ],
                data=[],
                page_size=10,
                style_cell={'textAlign': 'left'},
                style_header={'backgroundColor': '#3498db', 'color': 'white'},
                style_data={'backgroundColor': '#ecf0f1'}
            )
        ])
    ])
    
], style={'padding': '20px', 'fontFamily': 'Arial, sans-serif'})

# Callbacks para interatividade
@app.callback(
    Output('grafico-chamados-empresa', 'figure'),
    Input('filtro-empresa', 'value')
)
def atualizar_grafico_empresa(empresa_selecionada):
    # Contar chamados por empresa
    chamados_entrantes = df_entrantes['Empresa'].value_counts()
    chamados_fechados = df_fechados['Empresa'].value_counts()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Entrantes', x=chamados_entrantes.index, y=chamados_entrantes.values))
    fig.add_trace(go.Bar(name='Fechados', x=chamados_fechados.index, y=chamados_fechados.values))
    
    fig.update_layout(
        title='Total de Chamados por Empresa',
        xaxis_title='Empresa',
        yaxis_title='Número de Chamados',
        barmode='group'
    )
    
    return fig

@app.callback(
    Output('grafico-status-tit-sla', 'figure'),
    Input('filtro-tit', 'value')
)
def atualizar_grafico_status(tit_selecionado):
    # Contar status TIT e SLA
    tit_counts = df_fechados['TIT'].value_counts()
    sla_counts = df_fechados['SLA 2'].value_counts()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='TIT', x=tit_counts.index, y=tit_counts.values))
    fig.add_trace(go.Bar(name='SLA', x=sla_counts.index, y=sla_counts.values))
    
    fig.update_layout(
        title='Status TIT e SLA',
        xaxis_title='Status',
        yaxis_title='Número de Chamados',
        barmode='group'
    )
    
    return fig

@app.callback(
    Output('grafico-tendencia-chamados', 'figure'),
    Input('filtro-empresa', 'value')
)
def atualizar_tendencia_chamados(empresa_selecionada):
    # Agrupar chamados por mês
    df_entrantes_copy = df_entrantes.copy()
    df_fechados_copy = df_fechados.copy()
    
    df_entrantes_copy['Mes'] = df_entrantes_copy['Data/hora abertura'].dt.to_period('M')
    df_fechados_copy['Mes'] = df_fechados_copy['Data/hora encerramento'].dt.to_period('M')
    
    entrantes_por_mes = df_entrantes_copy.groupby('Mes').size()
    fechados_por_mes = df_fechados_copy.groupby('Mes').size()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[str(mes) for mes in entrantes_por_mes.index], 
        y=entrantes_por_mes.values,
        mode='lines+markers',
        name='Chamados Entrantes'
    ))
    fig.add_trace(go.Scatter(
        x=[str(mes) for mes in fechados_por_mes.index], 
        y=fechados_por_mes.values,
        mode='lines+markers',
        name='Chamados Fechados'
    ))
    
    fig.update_layout(
        title='Tendência de Chamados ao Longo do Tempo',
        xaxis_title='Mês',
        yaxis_title='Número de Chamados'
    )
    
    return fig

@app.callback(
    Output('tabela-detalhes', 'data'),
    [Input('filtro-empresa', 'value'),
     Input('filtro-tit', 'value'),
     Input('filtro-sla', 'value')]
)
def atualizar_tabela_detalhes(empresa, tit, sla):
    # Combinar dados de entrantes e fechados
    df_combinado = pd.merge(df_entrantes, df_fechados, on=['ID_Chamado', 'Empresa'], how='left')
    
    # Aplicar filtros
    if empresa != 'Todas':
        df_combinado = df_combinado[df_combinado['Empresa'] == empresa]
    if tit != 'Todos' and not df_combinado.empty:
        df_combinado = df_combinado[df_combinado['TIT'] == tit]
    if sla != 'Todos' and not df_combinado.empty:
        df_combinado = df_combinado[df_combinado['SLA 2'] == sla]
    
    if df_combinado.empty:
        return []
    
    # Preparar dados para a tabela
    df_tabela = df_combinado.copy()
    df_tabela['Data_Abertura'] = df_tabela['Data/hora abertura'].dt.strftime('%d/%m/%Y %H:%M')
    df_tabela['Data_Encerramento'] = df_tabela['Data/hora encerramento'].dt.strftime('%d/%m/%Y %H:%M')
    df_tabela['SLA_2'] = df_tabela['SLA 2']
    
    # Preencher valores nulos
    df_tabela = df_tabela.fillna('N/A')
    
    # Selecionar apenas as colunas necessárias
    colunas_tabela = ['ID_Chamado', 'Empresa', 'Data_Abertura', 'Data_Encerramento', 'TIT', 'SLA_2', 'Reabertos']
    df_tabela = df_tabela[colunas_tabela]
    
    return df_tabela.to_dict('records')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8051)

