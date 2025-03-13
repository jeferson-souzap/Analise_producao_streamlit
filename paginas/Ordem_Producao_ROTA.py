import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

st.header("Ordem de produção TTR")


destino_pendente = r"C:\Users\pcp\OneDrive\#jeff\Dev\Analise_Producao\dados\relatorio_intranet_pendente.csv"
df = pd.read_csv(destino_pendente)


df['Conclusão'] = pd.to_datetime(df['Conclusão'], errors='coerce')
df['Entrega'] = pd.to_datetime(df['Entrada'], errors='coerce')
df['Previsão'] = pd.to_datetime(df['Previsão'], errors='coerce')
df['Em Produção Área'] = pd.to_datetime(df['Em Produção Área'], errors='coerce')

# Em Produção Área

df['Pedido Área'] = pd.to_numeric(df['Pedido Área'], errors='coerce')
df['Pedido Peças'] = pd.to_numeric(df['Pedido Peças'])
df['Em Produção Área'] = pd.to_numeric(df['Em Produção Área'])

    
rotas01 = df.dropna(subset=["Rota"])  # Remove valores nulos
rotas01 = rotas01[rotas01["Rota"].str.strip() != ""]  # Remove strings vazias

# Obter valores únicos da coluna "Rotas"
rotas_unicas = rotas01["Rota"].unique().tolist()

# Criando a "listbox" com st.multiselect
 #selecionados = st.multiselect("Selecione uma ou mais opções:", rotas_unicas)
selecionados = st.selectbox("Selecione uma opção:", rotas_unicas)




df_OP = df.groupby('')





# Criar ordem de produção por ROTA
# Comparar programado Vs Realizado (Não sei como ainda )
# Grafico de Vendas Vs Capacidade de maquina
