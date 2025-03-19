import streamlit as st
import pandas as pd
import numpy as np
import datetime

from hidden_pages.config_db import local_banco
from hidden_pages.Formatar_relatorio import Formatando_df_concluido, Formatando_df_pendente, Formatando_df_forno


# Configuração da página
st.set_page_config(layout='wide', page_title='Inicio', page_icon='🏠', initial_sidebar_state='collapsed')

st.title('Indicadores')



