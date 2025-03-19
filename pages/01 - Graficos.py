import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.tseries.offsets import MonthEnd
from numerize.numerize import numerize
import streamlit as st
import datetime as dt

from hidden_pages.config_db import local_banco
from hidden_pages.Formatar_relatorio import LOCAL_CSV, gerar_caminho_csv, NOME_CSV_P, NOME_CSV_C, NOME_CSV_F


#-------------------------------------------------------------------------------------
#------------        Area de configuração do DATAFRAME


localdf_forno =  gerar_caminho_csv(NOME_CSV_F)
localdf_concluido = gerar_caminho_csv(NOME_CSV_C)
localdf_pendente = gerar_caminho_csv(NOME_CSV_P)

df_concluido = pd.read_csv(localdf_concluido)
df_pendente = pd.read_csv(localdf_pendente)
df_forno = pd.read_csv(localdf_forno)




#-------------------------------------------------------------------------------------





# Configuração da página
st.set_page_config(layout='wide')


df_resumo_forno = df_forno.groupby('data2')['Área (m2)'].sum().reset_index()
df_resumo_forno.rename(columns={'data2': 'Data', 'Área (m2)':'Área'}, inplace=True)

df_resumo_concluido = df_concluido.groupby('Entrada')['Pedido Área'].sum().reset_index()
df_resumo_concluido.rename(columns={'Entrada': 'Data', 'Pedido Área':'Área'}, inplace=True)

df_resumo_pendente = df_pendente.groupby('Entrada')['Pedido Área'].sum().reset_index()
df_resumo_pendente.rename(columns={'Entrada': 'Data', 'Pedido Área':'Área'}, inplace=True)

df_resumo_total01 = pd.merge(df_resumo_concluido, df_resumo_pendente, on='Data', how='outer')
df_resumo_total01.fillna(0, inplace=True)

df_resumo_total02 = pd.merge(df_resumo_total01, df_resumo_forno, on='Data', how='outer')
df_resumo_total02.fillna(0, inplace=True)

df_resumo_total02.rename(columns={'Área_x': 'Pedidos concluidos', 'Área_y':'Pedidos_pendentes', 'Área':'Forno'}, inplace=True)
df_resumo_total02['Total Pedidos'] = df_resumo_total02['Pedidos concluidos'] + df_resumo_total02['Pedidos_pendentes']

df_resumo_total02['Data'] = pd.to_datetime(df_resumo_total02['Data'], errors='coerce')


with st.expander('Forno Vs Entrada Pedido (Pendentes + Concluidos)', expanded=False):
    st.markdown('**PRODUÇÃO FORNO VS ENTRADA DE PEDIDO***')

    col01, col02 = st.columns(2, border=True)

    with col01:
        mes = st.number_input('Informe o Mês:', min_value=1, max_value=12, value=1)
    
    with col02:
        ano = st.number_input('Informe o Ano: ', min_value=2024, value=2025)
    

    df_resumo_total02['dia'] = df_resumo_total02['Data'].dt.day
    df_resumo_total02['mes'] = df_resumo_total02['Data'].dt.month
    df_resumo_total02['ano'] = df_resumo_total02['Data'].dt.year

    
    
    #plt.figure(figsize=(10, 15))
    fig, ax = plt.subplots(figsize=(19, 6))
    
    df_filtro_forno = df_resumo_total02[(df_resumo_total02['mes']== mes)& (df_resumo_total02['ano'] == ano)]
    df_filtro_forno.plot(x='dia', y=['Forno', 'Total Pedidos'], kind='bar', color=['skyblue', 'orange'], ax=ax)
    
    plt.title('PRODUÇÃO FORNO VS ENTRADA DE PEDIDO', fontsize=16)
       

    for p in ax.patches:
        ax.annotate(
            f'{p.get_height():.0f}',  # Texto (valor da barra)
            (p.get_x() + p.get_width() / 2, p.get_height()),  # Posição (x, y)
            ha='center',  # Alinhamento horizontal
            va='bottom',  # Alinhamento vertical
            fontsize=10,  # Tamanho da fonte
            color='black',  # Cor do texto
            xytext=(0, 5),  # Deslocamento do texto em relação à posição
            textcoords='offset points'  # Sistema de coordenadas do deslocamento
        )


    plt.tight_layout()
    #plt.show()

    st.pyplot(fig)

with st.expander('Graficos de produção', expanded=True):
    st.markdown('***Gráficos informativos de produção***')

    
