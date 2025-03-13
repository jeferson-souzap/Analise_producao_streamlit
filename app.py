import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Configuração da página
st.set_page_config(layout='wide', page_title='Inicio', page_icon='🏠', initial_sidebar_state='collapsed')

st.title('Analise e Controle - TTR')

# Funções que representam cada página
def configuracao():
    st.write("Conteúdo da Página de Configuração")
    # Adicione o conteúdo da página de Configuração aqui

def op_data():
    st.write("Conteúdo da Página OP - DATA")
    # Adicione o conteúdo da página OP - DATA aqui

def op_rota():
    st.write("Conteúdo da Página OP - ROTA")
    # Adicione o conteúdo da página OP - ROTA aqui

def relatorios():
    st.write("Conteúdo da Página de Relatórios")
    # Adicione o conteúdo da página de Relatórios aqui

# Dicionário de páginas
paginas = {
    "Configuração": configuracao,
    "OP - DATA": op_data,
    "OP - ROTA": op_rota,
    "Relatorios": relatorios,
}

# Barra lateral
st.sidebar.title('Menu')
pagina_selecionada = st.sidebar.selectbox("Paginas...", list(paginas.keys()))

# Exibir a página selecionada
if pagina_selecionada:
    paginas[pagina_selecionada]()