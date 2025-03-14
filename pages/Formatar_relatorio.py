import pandas as pd
import streamlit as st
import time

st.set_page_config(layout='wide')

st.header("Formatando arquivos CSV")



# Caminho do arquivo Excel
arquivo = r"C:\Users\pcp\OneDrive\#jeff\Dev\Analise_Producao\dados\relatorio_modelo_v01.xlsx"

# Ler as abas da planilha
aba_pendente = pd.read_excel(arquivo, sheet_name='relatorio_intranet_pendente')
aba_concluido = pd.read_excel(arquivo, sheet_name='relatorio_intranet_concluido')


destino_concluido = r"C:\Users\pcp\OneDrive\#jeff\Dev\Analise_Producao\dados\relatorio_intranet_concluido.csv"
destino_pendente = r"C:\Users\pcp\OneDrive\#jeff\Dev\Analise_Producao\dados\relatorio_intranet_pendente.csv"

aba_concluido.to_csv(destino_concluido, index=False, encoding='utf-8')
aba_pendente.to_csv(destino_pendente, index=False, encoding='utf-8')


with st.spinner("Aguarde Carregar", show_time=True):
    time.sleep(10)

st.success("Configurado!")

st.divider()

df_concluido = pd.read_csv(destino_concluido)
df_pendente = pd.read_csv(destino_pendente)


st.subheader("DataFrame - Concluido")
st.dataframe(df_concluido.head(15))

st.subheader("DataFrame - Pendente")
st.dataframe(df_pendente.head(15))


