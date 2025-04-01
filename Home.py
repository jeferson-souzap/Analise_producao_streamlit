import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

from hidden_pages.config_db import local_banco

#-----------------------------------------------------------
destino_concluido = r"D:\#Mega\Jeferson - Dev\02 - Linguagens\Python\Analise_producao_streamlit\dados\relatorio_intranet_concluido.csv"
destino_pendente = r"D:\#Mega\Jeferson - Dev\02 - Linguagens\Python\Analise_producao_streamlit\dados\relatorio_intranet_pendente.csv"
destino_prod_forno = r"D:\#Mega\Jeferson - Dev\02 - Linguagens\Python\Analise_producao_streamlit\dados\relatorio_forno.csv"

df_concluido = pd.read_csv(destino_concluido)
df_concluido['Conclusão'] = pd.to_datetime(df_concluido['Conclusão'], errors='coerce')
df_concluido['Entrada'] = pd.to_datetime(df_concluido['Entrada'], errors='coerce')
#-----------------------------------------------------------


# Configuração da página
st.set_page_config(layout='wide', page_title='Inicio', page_icon='🏠', initial_sidebar_state='collapsed')

data_atual = datetime.now()
mes = data_atual.month
ano = data_atual.year


@st.cache_data
def total_concluido(mes=3, ano=2025):   
    
    df_concluido['Conclusão'] = pd.to_datetime(df_concluido['Conclusão'], errors='coerce')
    df_concluido['Entrada'] = pd.to_datetime(df_concluido['Entrada'], errors='coerce')

    df_concluido['dia_n'] = df_concluido['Conclusão'].dt.day
    df_concluido['mes_n'] = df_concluido['Conclusão'].dt.month
    df_concluido['ano_n'] = df_concluido['Conclusão'].dt.year

    tot_concluido = df_concluido[['dia_n', 'mes_n', 'ano_n', 'tipo_servico', 'Pedido Área']]
    prod_dia_filtro = tot_concluido[(tot_concluido['mes_n']== mes) & (tot_concluido['ano_n']== ano)]
    df_prod_dia = prod_dia_filtro.groupby('mes_n')['Pedido Área'].sum()    
    return df_prod_dia.values[0]


mes = 3
ano =2025

col1, col2, col3, col4, col5 = st.columns(5)
    # col1, col2, col3, col4, col5 = st.columns(5, gap='large')

with col1:
    st.info(f'PRODUÇÃO TOTAL MÊS {mes}', icon='📌')
    st.metric(label='sum TZs', value=f'{total_concluido():.1f}')
    #st.metric(label='sum TZs', value=total_concluido())


