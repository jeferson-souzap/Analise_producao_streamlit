import streamlit as st
import pandas as pd
import numpy as np
import datetime

from hidden_pages.config_db import local_banco



# Configuração da página
st.set_page_config(layout='wide', page_title='Inicio', page_icon='🏠', initial_sidebar_state='collapsed')

st.title('Analise e Controle - TTR')

st.markdown(local_banco)