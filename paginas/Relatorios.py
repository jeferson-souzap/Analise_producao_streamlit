import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.tseries.offsets import MonthEnd
import streamlit as st

st.set_page_config(layout='wide')

df = pd.read_csv(r'C:\Users\pcp\OneDrive\#jeff\Dev\Analise_Producao\dados\relatorio_intranet_concluido.csv')

df['Conclusão'] = pd.to_datetime(df['Conclusão'], errors='coerce')
df['Entrega'] = pd.to_datetime(df['Entrada'], errors='coerce')
df['Previsão'] = pd.to_datetime(df['Previsão'], errors='coerce')
df['Em Produção Área'] = pd.to_datetime(df['Em Produção Área'], errors='coerce')

# Em Produção Área

#df['Pedido Área'] = df['Pedido Área'].str.replace(',', '.')
df['Pedido Área'] = pd.to_numeric(df['Pedido Área'], errors='coerce')

df['Pedido Peças'] = pd.to_numeric(df['Pedido Peças'])
df['Em Produção Área'] = pd.to_numeric(df['Em Produção Área'])


#--------------------------------------------------    
col01, col02, col03 = st.columns(3, border=True)
#--------------------------------------------------

with col01:
    ano = st.number_input("Indique o ano: ", value=2025)
    mes = st.number_input("Indique o mês: ", min_value=1, max_value=12, value=1)
    meta = st.number_input("Indique a META: ", min_value=100, max_value=800, value=700)


st.divider()


#--------------------------------------------------
# GRAFICOS
#--------------------------------------------------
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


#--------------------------------------------------

st.divider()

  


# Graficos 
# 01 - Produção por dia
# 02 - Produção por mes e por serviço
# 03 - Produção por mes
# 04 - Percentual de produção por serviço
# 05 - Castilho Vs Engenharia
# 06 - Forno Vs Pedido
 