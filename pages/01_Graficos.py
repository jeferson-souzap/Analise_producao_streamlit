import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.tseries.offsets import MonthEnd
from numerize.numerize import numerize
import streamlit as st
import datetime

from hidden_pages.config_db import local_banco
from hidden_pages.Formatar_relatorio import LOCAL_CSV, gerar_caminho_csv, NOME_CSV_P, NOME_CSV_C, NOME_CSV_F



#-------------------------------------------------------------------------------------
#------------        Area de configuração do DATAFRAME


localdf_forno =  gerar_caminho_csv(NOME_CSV_F)
localdf_concluido = gerar_caminho_csv(NOME_CSV_C)
localdf_pendente = gerar_caminho_csv(NOME_CSV_P)


df_concluido = pd.read_csv(localdf_concluido)
df_concluido['Conclusão'] = pd.to_datetime(df_concluido['Conclusão'], errors='coerce')
df_concluido['Entrega'] = pd.to_datetime(df_concluido['Entrada'], errors='coerce')
df_concluido['Previsão'] = pd.to_datetime(df_concluido['Previsão'], errors='coerce')
df_concluido['Em Produção Área'] = pd.to_datetime(df_concluido['Em Produção Área'], errors='coerce')
df_concluido['Pedido Área'] = pd.to_numeric(df_concluido['Pedido Área'], errors='coerce')
df_concluido['Pedido Peças'] = pd.to_numeric(df_concluido['Pedido Peças'])
df_concluido['Em Produção Área'] = pd.to_numeric(df_concluido['Em Produção Área'])


df_pendente = pd.read_csv(localdf_pendente)
df_pendente['Conclusão'] = pd.to_datetime(df_pendente['Conclusão'], errors='coerce')
df_pendente['Entrega'] = pd.to_datetime(df_pendente['Entrada'], errors='coerce')
df_pendente['Previsão'] = pd.to_datetime(df_pendente['Previsão'], errors='coerce')
df_pendente['Em Produção Área'] = pd.to_datetime(df_pendente['Em Produção Área'], errors='coerce')
df_pendente['Pedido Área'] = pd.to_numeric(df_pendente['Pedido Área'], errors='coerce')
df_pendente['Pedido Peças'] = pd.to_numeric(df_pendente['Pedido Peças'])
df_pendente['Em Produção Área'] = pd.to_numeric(df_pendente['Em Produção Área'])

df_forno = pd.read_csv(localdf_forno)
df_forno['Data'] = pd.to_datetime(df_forno['Data'], errors='coerce')
df_forno['data2'] = pd.to_datetime(df_forno['data2'], errors='coerce')

df_concluido['dia_n'] = df_concluido['Conclusão'].dt.day
df_concluido['mes_n'] = df_concluido['Conclusão'].dt.month
df_concluido['ano_n'] = df_concluido['Conclusão'].dt.year

#-------------------------------------------------------------------------------------
largura_grafico = 18
altura_grafico = 7



# Configuração da página
st.set_page_config(layout='wide')

@st.cache_data
def producao_forno():

    df_resumo_forno = df_forno.groupby('data2')['Área (m2)'].sum().reset_index()
    df_resumo_forno.rename(columns={'data2': 'Data', 'Área (m2)':'Área'}, inplace=True)

    df_resumo_concluido = df_concluido.groupby('Entrada')['Pedido Área'].sum().reset_index()
    df_resumo_concluido.rename(columns={'Entrada': 'Data', 'Pedido Área':'Área'}, inplace=True)

    df_resumo_pendente = df_pendente.groupby('Entrada')['Pedido Área'].sum().reset_index()
    df_resumo_pendente.rename(columns={'Entrada': 'Data', 'Pedido Área':'Área'}, inplace=True)

    df_resumo_total01 = pd.merge(df_resumo_concluido, df_resumo_pendente, on='Data', how='outer')
    df_resumo_total01.fillna(0, inplace=True)

    df_resumo_total01['Data'] = pd.to_datetime(df_resumo_total01['Data'], errors='coerce')

    df_resumo_total02 = pd.merge(df_resumo_total01, df_resumo_forno, on='Data', how='outer')
    df_resumo_total02.fillna(0, inplace=True)

    df_resumo_total02.rename(columns={'Área_x': 'Pedidos concluidos', 'Área_y':'Pedidos_pendentes', 'Área':'Forno'}, inplace=True)
    df_resumo_total02['Total Pedidos'] = df_resumo_total02['Pedidos concluidos'] + df_resumo_total02['Pedidos_pendentes']

    df_resumo_total02['Data'] = pd.to_datetime(df_resumo_total02['Data'], errors='coerce')

    return df_resumo_total02

#---------------------------------------------------------------------------


mes = st.sidebar.selectbox('Selecione o mês', df_concluido['mes_n'].unique())
ano = st.sidebar.selectbox('Selecione o mês', df_concluido['ano_n'].unique())

#mes = st.number_input('Informe o Mês:', min_value=1, max_value=12, value=1)
#ano = st.number_input('Informe o Ano: ', min_value=2024, value=2025)

#---------------------------------------------------------------------------
#chave = st.checkbox('Teste')
#st.write(chave)

#---------------------------------------------------------------------------

st.header('Gráficos de Produção', )



with st.expander('Forno Vs Entrada Pedido (Pendentes + Concluidos)', expanded=True):
    st.markdown('**PRODUÇÃO FORNO VS ENTRADA DE PEDIDO***')    
    
    df_resumo_total02 = producao_forno()
    df_resumo_total02['dia'] = df_resumo_total02['Data'].dt.day
    df_resumo_total02['mes'] = df_resumo_total02['Data'].dt.month
    df_resumo_total02['ano'] = df_resumo_total02['Data'].dt.year
        
    fig01, ax = plt.subplots(figsize=(largura_grafico, altura_grafico))
    
    df_filtro_forno = df_resumo_total02[(df_resumo_total02['mes']== mes)& (df_resumo_total02['ano'] == ano)]
    df_filtro_forno.plot(x='dia', y=['Forno', 'Total Pedidos'], kind='bar', color=['skyblue', 'orange'], ax=ax)
    
    plt.title(f'PRODUÇÃO FORNO VS ENTRADA DE PEDIDO (m²) - {mes}/{ano}', fontsize=16)

    for p in ax.patches:
        ax.annotate(
            f'{p.get_height():.2f}',  # Texto (valor da barra)
            (p.get_x() + p.get_width() / 2, p.get_height()),  # Posição (x, y)
            ha='center',  # Alinhamento horizontal
            va='bottom',  # Alinhamento vertical
            fontsize=10,  # Tamanho da fonte
            color='black',  # Cor do texto
            xytext=(0, 6),  # Deslocamento do texto em relação à posição
            textcoords='offset points'  # Sistema de coordenadas do deslocamento
        )


    plt.tight_layout()
    st.pyplot(fig01)



#----------------------------------------------------------------------------------------

with st.expander('Graficos de produção', expanded=True):
    st.markdown('***Gráficos informativos de produção***')    

    df_prod_concluido = df_concluido[['dia_n', 'mes_n', 'ano_n', 'tipo_servico', 'Pedido Área']]
    prod_dia_filtro = df_prod_concluido[(df_prod_concluido['mes_n']== mes) & (df_prod_concluido['ano_n']== ano)]
    df_prod_dia = prod_dia_filtro.groupby('dia_n')['Pedido Área'].sum()
    #df_prod_dia

    fig02, ax = plt.subplots(figsize=(19, 6))
    df_prod_dia.plot(kind='bar', ax=ax, color='skyblue')

    plt.title(F'PRODUÇÃO TOTAL POR DIA (m²) - {mes}/{ano}', fontsize=16)

    for p in ax.patches:
        ax.annotate(
            f'{p.get_height():.2f}',  # Texto (valor da barra)
            (p.get_x() + p.get_width() / 2, p.get_height()),  # Posição (x, y)
            ha='center',  # Alinhamento horizontal
            va='bottom',  # Alinhamento vertical
            fontsize=10,  # Tamanho da fonte
            color='black',  # Cor do texto
            xytext=(0, 5),  # Deslocamento do texto em relação à posição
            textcoords='offset points'  # Sistema de coordenadas do deslocamento
        )

     
    plt.tight_layout()
    st.pyplot(fig02)

    st.divider()
    #--------------------------------------------------------------------
    df_prod_concluido = df_concluido[['dia_n', 'mes_n', 'ano_n', 'tipo_servico', 'Pedido Área']]
    prod_dia_filtro = df_prod_concluido[(df_prod_concluido['mes_n']== mes) & (df_prod_concluido['ano_n']== ano)]
    df_prod_dia_serv = prod_dia_filtro.groupby(['dia_n', 'tipo_servico'])['Pedido Área'].sum().unstack()
    #df_prod_dia_serv

    fig03, ax = plt.subplots(figsize=(largura_grafico, altura_grafico))
    df_prod_dia_serv.plot(kind='bar', ax=ax, color=['skyblue', 'orange'])

    plt.title('PRODUÇÃO POR DIA E SERVIÇO', fontsize=16)

    for p in ax.patches:
            ax.annotate(
                f'{p.get_height():.2f}',  # Texto (valor da barra)
                (p.get_x() + p.get_width() / 2, p.get_height()),  # Posição (x, y)
                ha='center',  # Alinhamento horizontal
                va='bottom',  # Alinhamento vertical
                fontsize=10,  # Tamanho da fonte
                color='black',  # Cor do texto
                xytext=(0, 5),  # Deslocamento do texto em relação à posição
                textcoords='offset points'  # Sistema de coordenadas do deslocamento
            )

    
    plt.tight_layout()
    st.pyplot(fig03)

    st.divider()

    #--------------------------------------------------------------------
    pd_concluido_mes_serv01 = df_concluido[['dia_n', 'mes_n', 'ano_n', 'tipo_servico', 'Pedido Área']]
    pd_concluido_mes_serv02 = pd_concluido_mes_serv01.groupby(['mes_n', 'tipo_servico'])['Pedido Área'].sum().reset_index()
    
    fig04, ax = plt.subplots(figsize=(largura_grafico, altura_grafico))
    #pd_concluido_mes_serv02.plot(x='mes_n', y=['tipo_servico', 'Pedido Área'], kind='bar', ax=ax, stacked=True)
    pd_concluido_mes_serv02.groupby(['mes_n', 'tipo_servico'])['Pedido Área'].sum().unstack().plot(
            kind='bar', 
            ax=ax,
            color=['skyblue', 'orange']
    )
    
    plt.title(f'PRODUÇÃO POR MÊS E SERVIÇO (m²) - {mes}/{ano}', fontsize=16)

    for p in ax.patches:
            ax.annotate(
                f'{p.get_height():.2f}',  # Texto (valor da barra)
                (p.get_x() + p.get_width() / 2, p.get_height()),  # Posição (x, y)
                ha='center',  # Alinhamento horizontal
                va='bottom',  # Alinhamento vertical
                fontsize=10,  # Tamanho da fonte
                color='black',  # Cor do texto
                xytext=(0, 5),  # Deslocamento do texto em relação à posição
                textcoords='offset points'  # Sistema de coordenadas do deslocamento
            )

    
    plt.tight_layout()
    st.pyplot(fig04)


