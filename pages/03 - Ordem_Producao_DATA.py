import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.tseries.offsets import MonthEnd
import streamlit as st

st.set_page_config(layout='wide')
st.header("Ordem de produção por data")

#---------------------------------------
destino_pendente = r"C:\Users\pcp\OneDrive\#jeff\Dev\Analise_Producao\dados\relatorio_intranet_pendente.csv"
df = pd.read_csv(destino_pendente)
#---------------------------------------

df['Conclusão'] = pd.to_datetime(df['Conclusão'], errors='coerce')
df['Entrega'] = pd.to_datetime(df['Entrada'], errors='coerce')
df['Previsão'] = pd.to_datetime(df['Previsão'], errors='coerce')
df['Em Produção Área'] = pd.to_datetime(df['Em Produção Área'], errors='coerce')
#---------------------------------------
df['Pedido Área'] = pd.to_numeric(df['Pedido Área'], errors='coerce')
df['Pedido Peças'] = pd.to_numeric(df['Pedido Peças'])
df['Em Produção Área'] = pd.to_numeric(df['Em Produção Área'])
#---------------------------------------
col01, col02, col03 = st.columns(3, border=True)


#---------------------------------------
datas_entrada = df.dropna(subset=['Entrada'])  # Remove valores nulos
data_filtro = datas_entrada[datas_entrada["Entrada"].str.strip() != ""]  # Remove strings vazias
data_filtro = data_filtro["Entrada"].unique().tolist()
#---------------------------------------

#---------------------------------------
with col01:    
    data_minima = st.selectbox("Data Minima:", data_filtro)
    data_maxima = st.selectbox("Data Máxima:", data_filtro)
#---------------------------------------



#---------------------------------------

filtro_data = df[(df['Entrega']>= data_minima ) &(df['Entrada'] <= data_maxima)]
total_unidade = filtro_data['Pedido Peças'].sum()
total_area = filtro_data['Pedido Área'].sum()



with col02:    
    
    st.markdown(f'TOTAL UN: **{total_unidade:,.2f}**')
    st.markdown(f'ÁREA M² : **{total_area:,.2f}**')
#---------------------------------------


#---------------------------------------


filtro_engenharia = df[(df['Entrega']>= data_minima ) & (df['Entrada'] <= data_maxima) & (df['tipo_servico'] <= 'ENGENHARIA')]
filtro_padrao = df[(df['Entrega']>= data_minima ) & (df['Entrada'] <= data_maxima) & (df['tipo_servico'] <= 'PADRÃO')]

total_engenharia = filtro_engenharia['Pedido Peças'].sum()
total_padrao = filtro_padrao['Pedido Área'].sum()



with col03:
    st.markdown(f'ENGENHARIA: M2: **{total_engenharia:,.2f}**')
    st.markdown(f'PADRÃO M2     : **{total_padrao:,.2f}**')

st.divider()

