import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import locale 
import matplotlib.pyplot as plt
import seaborn as sns

from hidden_pages.config_db import local_banco


#-----------------------------------------------------------
#CONFIGURAÇÃO DATAFRAME

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

destino_concluido = r"D:\#Mega\Jeferson - Dev\02 - Linguagens\Python\Analise_producao_streamlit\dados\relatorio_intranet_concluido.csv"
destino_pendente = r"D:\#Mega\Jeferson - Dev\02 - Linguagens\Python\Analise_producao_streamlit\dados\relatorio_intranet_pendente.csv"
destino_prod_forno = r"D:\#Mega\Jeferson - Dev\02 - Linguagens\Python\Analise_producao_streamlit\dados\relatorio_forno.csv"

df_concluido = pd.read_csv(destino_concluido)
df_concluido['Conclusão'] = pd.to_datetime(df_concluido['Conclusão'], errors='coerce')
df_concluido['Entrega'] = pd.to_datetime(df_concluido['Entrada'], errors='coerce')
df_concluido['Previsão'] = pd.to_datetime(df_concluido['Previsão'], errors='coerce')
df_concluido['Em Produção Área'] = pd.to_datetime(df_concluido['Em Produção Área'], errors='coerce')
df_concluido['Pedido Área'] = pd.to_numeric(df_concluido['Pedido Área'], errors='coerce')
df_concluido['Pedido Peças'] = pd.to_numeric(df_concluido['Pedido Peças'])
df_concluido['Em Produção Área'] = pd.to_numeric(df_concluido['Em Produção Área'])


df_concluido['dia_n'] = df_concluido['Conclusão'].dt.day
df_concluido['mes_n'] = df_concluido['Conclusão'].dt.month
df_concluido['ano_n'] = df_concluido['Conclusão'].dt.year


#-------------------------------------------------------------------------------
#CONFIGURAÇÃO PAGINA
st.set_page_config(layout='wide', page_title='Inicio', page_icon='🏠')

st.header('Indicadores de produção de Vidro')

data_atual = datetime.now()


largura_grafico = 18
altura_grafico = 7



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

@st.cache_data
def total_serv(mes=3, ano=2025, serv=''):

    if serv == '':
         pass
    else:
        df_prod_concluido = df_concluido[['dia_n', 'mes_n', 'ano_n', 'tipo_servico', 'Pedido Área']]
        prod_dia_filtro = df_prod_concluido[(df_prod_concluido['mes_n']== mes) & (df_prod_concluido['ano_n']== ano) & (df_prod_concluido['tipo_servico']== serv)]
        df_prod_dia = prod_dia_filtro.groupby('mes_n')['Pedido Área'].sum().reset_index()

        total_serv = df_prod_dia['Pedido Área'].iloc[0]
    
        return total_serv







#-------------------------------------------------------------------------------
#SIDEBAR 

mes_prod = data_atual.month
ano_prod = data_atual.year

mes_prod = st.sidebar.selectbox('Selecione o mês', df_concluido['mes_n'].unique())
ano_prod = st.sidebar.selectbox('Selecione o mês', df_concluido['ano_n'].unique())

#-------------------------------------------------------------------------------

col1, col2, col3 = st.columns(3)


with col1:
    st.info(f'TOTAL CONCLUIDOS **MÊS-{mes_prod}**')

    num_producao = total_concluido(mes_prod, ano_prod)
    num_formatado = locale.format_string("%.2f", num_producao, grouping=True)
    st.metric(label='', value=num_formatado, border=True, )

with col2:
    st.info('ENGENHARIA (m²)')
    num_engenharia = total_serv(mes_prod, ano_prod, 'ENGENHARIA')
    num_eng_format = locale.format_string("%.2f", num_engenharia, grouping=True)
    st.metric(label='', value=num_eng_format , border=True)
    
with col3:
    st.info('PADRÃO (m²)')
    num_padrao = total_serv(mes_prod, ano_prod, 'PADRÃO')
    num_padrao_format = locale.format_string("%.2f", num_padrao, grouping=True)
    st.metric(label='', value=num_padrao_format, border=True)


st.divider()

df_prod_concluido = df_concluido[['dia_n', 'mes_n', 'ano_n', 'tipo_servico', 'Pedido Área']]
prod_dia_filtro = df_prod_concluido[(df_prod_concluido['mes_n']== mes_prod) & (df_prod_concluido['ano_n']== ano_prod)]
df_prod_dia = prod_dia_filtro.groupby('dia_n')['Pedido Área'].sum()
#df_prod_dia

fig02, ax = plt.subplots(figsize=(19, 6))
df_prod_dia.plot(kind='bar', ax=ax, color='skyblue')

plt.title(F'PRODUÇÃO TOTAL POR DIA (m²) - {mes_prod}/{ano_prod}', fontsize=16)

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

pd_concluido_mes_serv01 = df_concluido[['dia_n', 'mes_n', 'ano_n', 'tipo_servico', 'Pedido Área']]
pd_concluido_mes_serv02 = pd_concluido_mes_serv01.groupby(['mes_n', 'tipo_servico'])['Pedido Área'].sum().reset_index()

fig04, ax = plt.subplots(figsize=(largura_grafico, altura_grafico))
#pd_concluido_mes_serv02.plot(x='mes_n', y=['tipo_servico', 'Pedido Área'], kind='bar', ax=ax, stacked=True)
pd_concluido_mes_serv02.groupby(['mes_n', 'tipo_servico'])['Pedido Área'].sum().unstack().plot(
        kind='bar', 
        ax=ax,
        color=['skyblue', 'orange']
)

plt.title(f'PRODUÇÃO POR MÊS E SERVIÇO (m²) - {mes_prod}/{ano_prod}', fontsize=16)

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


