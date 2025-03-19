import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.tseries.offsets import MonthEnd
from numerize.numerize import numerize
import streamlit as st

st.set_page_config(layout='wide')

df = pd.read_csv(r'D:\#Mega\Jeferson - Dev\02 - Linguagens\Python\Analise_producao_streamlit\dados\relatorio_intranet_concluido.csv')

df['Conclusão'] = pd.to_datetime(df['Conclusão'], errors='coerce')
df['Entrega'] = pd.to_datetime(df['Entrada'], errors='coerce')
df['Previsão'] = pd.to_datetime(df['Previsão'], errors='coerce')
df['Em Produção Área'] = pd.to_datetime(df['Em Produção Área'], errors='coerce')

#df['Pedido Área'] = df['Pedido Área'].str.replace(',', '.')
df['Pedido Área'] = pd.to_numeric(df['Pedido Área'], errors='coerce')
df['Pedido Peças'] = pd.to_numeric(df['Pedido Peças'])
df['Em Produção Área'] = pd.to_numeric(df['Em Produção Área'])



#-------------------------------------------------------
#FUNÇÕES
#-------------------------------------------------------

def PedidosVS_Forno(ano, mes_selecionado, meta):

    df_mes = df[(df['ano_conclusao'] == ano) & (df['mes_conclusao'] == mes)]
    soma_diaria = df_mes.groupby('dia_conclusao')['Pedido Área'].sum()

    plt.figure(figsize=(19, 6))

    plt.bar(soma_diaria.index, soma_diaria.values, label='Área (m²)')
    plt.axhline(y=meta, color='r', linestyle='--', label=f'Meta {meta} m²)')

    for dia, area in soma_diaria.items():
        plt.text(dia, area + 0.1, f'{area:.2f}', ha='center', va='bottom')

    plt.xlabel('Dia de Entrada')
    plt.ylabel('Pedido Área (m²)')
    plt.title(f'Área por Dia - {ano}-{mes:02}')
    plt.xticks(soma_diaria.index)
    #plt.legend()
    plt.show()

    st.pyplot(plt)



def Total_area_concluida_mes(data_minima, data_maxima):
    filtro_pedido_conclido = df[(df['Conclusão'] >= data_minima) & (df['Conclusão'] <= data_maxima)]
    total_pedido_concluido = filtro_pedido_conclido['Pedido Área'].sum()
    return total_pedido_concluido




#-------------------------------------------------------








#COLUNAS DE FILTRO
col_filtro01,col_filtro02,col_filtro03,col_filtro04 = st.columns(4, border=True)
#-------------------------------------------------------


#COLUNAS DE INFORMAÇÃO
col01, col02, col03 = st.columns(3, border=True)
#-------------------------------------------------------


with col_filtro01:
    mes = st.number_input("MÊS", min_value=1, max_value=12, value=1)    

with col_filtro02:
    ano = st.number_input("ANO: ", value=2025)    

with col_filtro03:
    meta = st.number_input("META: ", min_value=100, max_value=800, value=700)
    

with col_filtro04:
    datas_entrada = df.dropna(subset=['Entrada'])  # Remove valores nulos
    data_filtro = datas_entrada[datas_entrada["Entrada"].str.strip() != ""]  # Remove strings vazias
    data_filtro = data_filtro["Entrada"].unique().tolist()

    c01, c02 = st.columns(2)
    with c01:
        data_minima = st.selectbox("Data Minima:", data_filtro)
    
    with c02:
        data_maxima = st.selectbox("Data Máxima:", data_filtro)
#---------------------------------------


with col01:
    #st.info('Total Pedidos Concluidos!')
    total_area = Total_area_concluida_mes(data_minima, data_maxima)
    st.metric(label='TOTAL CONCLUIDO', value=f'{total_area:,.2f}')
    #st.metric(label='TOTAL CONCLUIDO', value=numerize(Total_area_concluida_mes(data_minima, data_maxima)))









#-------------------------------------------------------
#----------------- GRAFICOS
#-------------------------------------------------------


with st.expander('Graficos de Produção', expanded=False):
    st.markdown('Graficos de produção concluida')
    #PedidosVS_Forno(3, 2025, 700)


with st.expander('Comprativos', expanded=False):
    st.markdown('Pedidos Vs Produção **Forno**')


# Graficos 
# 01 - Produção por dia
# 02 - Produção por mes e por serviço
# 03 - Produção por mes
# 04 - Percentual de produção por serviço
# 05 - Castilho Vs Engenharia
# 06 - Forno Vs Pedido
 