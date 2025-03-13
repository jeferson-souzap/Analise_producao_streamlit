import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.tseries.offsets import MonthEnd
import streamlit as st

import sqlite3 as db

st.set_page_config(layout='wide')
st.title('Pagina de configuração')



def Adicionar_meta(data_meta, turno01=0, turno02=0):    
    turno01_num = int(turno01) if turno01 else 0
    turno02_num = int(turno02) if turno02 else 0

    meta_total =  turno01_num + turno02_num

    conn = db.connect(r'C:\Users\pcp\OneDrive\#jeff\Dev\Analise_Producao\db\ttr.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO metas(data_meta,turno01,turno02, meta_total) VALUES(?,?,?,?)", (data_meta, turno01, turno02, meta_total))

    

    conn.commit()
    conn.close()


def Listar_meta_db():
    conn = db.connect(r'C:\Users\pcp\OneDrive\#jeff\Dev\Analise_Producao\db\ttr.db')    
    
    query = "SELECT * FROM metas"
    df = pd.read_sql_query(query, conn)
    df['data_meta'] = pd.to_datetime(df['data_meta']).dt.strftime('%d/%m/%Y')
    conn.close()
    return df


def Editar_meta(id_meta, data_meta, turno01, turno02):
    meta_total = turno01 + turno02
    conn = db.connect(r'C:\Users\pcp\OneDrive\#jeff\Dev\Analise_Producao\db\ttr.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE metas
        SET data_meta = ?, turno01 = ?, turno02 = ?, meta_total = ?
        WHERE id = ?
    """, (data_meta, turno01, turno02, meta_total, id_meta))

    conn.commit()
    conn.close()


def Excluir_meta(id_meta):
    conn = db.connect(r'C:\Users\pcp\OneDrive\#jeff\Dev\Analise_Producao\db\ttr.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM metas WHERE id = ?", (id_meta,))

    conn.commit()
    conn.close()



def validar_data(data_str, formato='%d/%m/%Y'):
    try:
        # Tenta converter a string para um objeto datetime
        data_obj = datetime.strptime(data_str, formato)
        return data_obj
    except ValueError:
        # Se a conversão falhar, retorna None
        return None
    


#-------------------------------------------
col01, col02 = st.columns(2, border=True)
#-------------------------------------------


with col01:    
    st.markdown('**Cadastro de Meta do FORNO**')
    data_meta =  st.text_input('Data de Inicio da META (dd/mm/ano)')
    
    if data_meta:
        data_obj = validar_data(data_meta)
        if data_obj:
            st.success(f"Data válida: {data_obj.strftime('%d/%m/%Y')}")
        else:
            st.error("Data inválida! Use o formato dd/mm/aaaa.")
    
    turno01 = st.number_input('META turno 01')
    turno02 = st.number_input('META turno 02')


    bt_col01, bt_col02, bt_col03 = st.columns(3)

    with bt_col01:
        if st.button('Salvar Meta'):
            if data_obj:
                # Converter a data para o formato do banco de dados (aaaa-mm-dd)
                data_banco = data_obj.strftime('%Y-%m-%d')
                Adicionar_meta(data_banco, turno01, turno02)
                st.success("Meta salva com sucesso!")
                
                st.session_state['data_meta'] = ""
                st.session_state['turno01'] = ""
                st.session_state['turno02'] = ""


            else:
                st.error("Por favor, insira uma data válida antes de salvar.")
    
    with bt_col02:
        df_metas = Listar_meta_db()
        meta_selecionada = st.session_state.get('meta_selecionada')

        if st.button('Editar Meta'):
            data_obj = validar_data(data_meta)
            if data_obj:
                data_banco = data_obj.strftime('%Y-%m-%d')
                Editar_meta(meta_selecionada, data_banco, turno01, turno02)
                st.success("Meta editada com sucesso!")
            else:
                st.error("Por favor, insira uma data válida antes de editar.")

    
    with bt_col03:
        if st.button('Excluir Meta',):
            Excluir_meta(meta_selecionada)
            st.success("Meta excluída com sucesso!")

with col02: 
    df_metas = Listar_meta_db()
    
    meta_selecionada = st.selectbox('Selecione uma meta para editar ou excluir', df_metas['id'])
    st.session_state['meta_selecionada'] = meta_selecionada  # Armazenar o valor
    
    
    #meta_detalhes = df_metas[df_metas['id'] == meta_selecionada].iloc[0]


    st.markdown('**Lista de Metas**')
    df_metas = Listar_meta_db()
    st.table(df_metas)