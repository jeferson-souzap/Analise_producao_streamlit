import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import locale 
from hidden_pages.config_db import local_banco
from pages.Graficos import prod_mes_servico

#-----------------------------------------------------------
#CONFIGURAÇÃO DATAFRAME

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

destino_concluido = r"D:\#Mega\Jeferson - Dev\02 - Linguagens\Python\Analise_producao_streamlit\dados\relatorio_intranet_concluido.csv"
destino_pendente = r"D:\#Mega\Jeferson - Dev\02 - Linguagens\Python\Analise_producao_streamlit\dados\relatorio_intranet_pendente.csv"
destino_prod_forno = r"D:\#Mega\Jeferson - Dev\02 - Linguagens\Python\Analise_producao_streamlit\dados\relatorio_forno.csv"

df_concluido = pd.read_csv(destino_concluido)
df_concluido['Conclusão'] = pd.to_datetime(df_concluido['Conclusão'], errors='coerce')
df_concluido['Entrada'] = pd.to_datetime(df_concluido['Entrada'], errors='coerce')


df_concluido['dia_n'] = df_concluido['Conclusão'].dt.day
df_concluido['mes_n'] = df_concluido['Conclusão'].dt.month
df_concluido['ano_n'] = df_concluido['Conclusão'].dt.year


#-------------------------------------------------------------------------------
#CONFIGURAÇÃO PAGINA
st.set_page_config(layout='wide', page_title='Inicio', page_icon='🏠')
data_atual = datetime.now()

#-------------------------------------------------------------------------------
#FUNÇÕES
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


#-------------------------------------------------------------------------------
#SIDEBAR 

mes_prod = data_atual.month
ano_prod = data_atual.year

mes_prod = st.sidebar.selectbox('Selecione o mês', df_concluido['mes_n'].unique())
ano_prod = st.sidebar.selectbox('Selecione o mês', df_concluido['ano_n'].unique())

#-------------------------------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.info(f'PRODUÇÃO TOTAL MÊS {mes_prod}')

    num_producao = total_concluido(mes_prod, ano_prod)
    num_formatado = locale.format_string("%.2f", num_producao, grouping=True)
    st.metric(label='', value=num_formatado, border=True, )

with col2:
    st.info('Total Engenharia')
    col_m01, col_m02 = st.columns(2, border=True)
    
    
    with col_m01:
        st.metric(label='PADRÃO', value=10)
    with col_m02:
        st.metric(label='ENGENHARIA', value=18)

with col3:
    st.info('Melhor Mês')

with col4:
    st.info('Pior Mês')


st.divider()