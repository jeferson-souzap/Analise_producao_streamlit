import pandas as pd
import os
import datetime
import sqlite3 as db

local_banco = r'C:\Users\pcp\OneDrive\#jeff\Dev\Analise_Producao\db\ttr.db'

#-------------------------------------------------------------------------------
# VARIAVEIS GLOBAIS

LOCAL_EXCEL = r"C:\Users\pcp\OneDrive\#jeff\Dev\Analise_Producao\dados\relatorio_modelo_v01.xlsx"
LOCAL_CSV = 'C:/Users/pcp/OneDrive/#jeff/Dev/Analise_Producao/dados/'
LOCAL_TEMP = 'C:/Users/pcp/OneDrive/#jeff/Dev/Analise_Producao/dados/'

NOME_CSV_C = 'relatorio_intranet_concluido'
NOME_CSV_P ='relatorio_intranet_pendente'
NOME_CSV_F = 'relatorio_forno'


#-------------------------------------------------------------------------------

def gerar_caminho_csv(nome):
    return f'{LOCAL_CSV}{nome}.csv'

def Salvar_update(dt_update):
    conn = db.connect(local_banco)
    c = conn.cursor()
    c.execute("INSERT INTO ultimo_update (dt_update) VALUES (?)", (dt_update,))
    
    conn.commit()
    conn.close()

def Verificar_update():
    pass

def verificar_csv(nome_arquivo):
    destino_csv = gerar_caminho_csv(nome_arquivo)

    if os.path.exists(destino_csv):
        data_modificado = datetime.date.fromtimestamp(os.path.getmtime(destino_csv))
        hoje = datetime.date.today()

        if data_modificado == hoje - datetime.timedelta(days=1):            
            return True
        else:
            return False
    else:
        return True

def Formatando_df_concluido(nome_aba='relatorio_intranet_concluido'):
    destino_concluido = gerar_caminho_csv(nome_aba)
    
    if verificar_csv(nome_aba):
        aba_concluido = pd.read_excel(LOCAL_EXCEL, sheet_name=nome_aba)    
        aba_concluido.to_csv(destino_concluido, index=False, encoding='utf-8')
        df_concluido = pd.read_csv(destino_concluido)

        df_concluido['Conclusão'] = pd.to_datetime(df_concluido['Conclusão'], errors='coerce')
        df_concluido['Entrega'] = pd.to_datetime(df_concluido['Entrada'], errors='coerce')
        df_concluido['Previsão'] = pd.to_datetime(df_concluido['Previsão'], errors='coerce')
        df_concluido['Em Produção Área'] = pd.to_datetime(df_concluido['Em Produção Área'], errors='coerce')
        df_concluido['Pedido Área'] = pd.to_numeric(df_concluido['Pedido Área'], errors='coerce')
        df_concluido['Pedido Peças'] = pd.to_numeric(df_concluido['Pedido Peças'])
        df_concluido['Em Produção Área'] = pd.to_numeric(df_concluido['Em Produção Área'])
    else:
        df_concluido = pd.read_csv(destino_concluido)

    return df_concluido
  
def Formatando_df_pendente(nome_aba='relatorio_intranet_pendente'):
    destino_pendente = gerar_caminho_csv(nome_aba)

    if verificar_csv(nome_aba):
        aba_pendente = pd.read_excel(LOCAL_EXCEL, sheet_name=nome_aba)    
        aba_pendente.to_csv(destino_pendente, index=False, encoding='utf-8')
        df_pendente = pd.read_csv(destino_pendente)    

        df_pendente['Conclusão'] = pd.to_datetime(df_pendente['Conclusão'], errors='coerce')
        df_pendente['Entrega'] = pd.to_datetime(df_pendente['Entrada'], errors='coerce')
        df_pendente['Previsão'] = pd.to_datetime(df_pendente['Previsão'], errors='coerce')
        df_pendente['Em Produção Área'] = pd.to_datetime(df_pendente['Em Produção Área'], errors='coerce')
        df_pendente['Pedido Área'] = pd.to_numeric(df_pendente['Pedido Área'], errors='coerce')
        df_pendente['Pedido Peças'] = pd.to_numeric(df_pendente['Pedido Peças'])
        df_pendente['Em Produção Área'] = pd.to_numeric(df_pendente['Em Produção Área'])
    else:
        df_pendente = pd.read_csv(destino_pendente)

    return df_pendente

def Formatando_df_forno(nome_aba='relatorio_forno'):
    destino_prod_forno = gerar_caminho_csv(nome_aba)

    if verificar_csv(nome_aba):        
        aba_prod_forno = pd.read_excel(LOCAL_EXCEL, sheet_name=nome_aba)    
        aba_prod_forno.to_csv(destino_prod_forno, index=False, encoding='utf-8')
        df_forno = pd.read_csv(destino_prod_forno)   

        df_forno['Data'] = pd.to_datetime(df_forno['Data'], errors='coerce')
        df_forno['data2'] = pd.to_datetime(df_forno['data2'], errors='coerce')

    else:
         df_forno = pd.read_csv(destino_prod_forno)

    return df_forno

def main():
    df_concluido = Formatando_df_concluido('relatorio_intranet_concluido')
    df_pendente = Formatando_df_pendente('relatorio_intranet_pendente')
    df_forno = Formatando_df_forno('relatorio_forno')

    print(df_concluido.info())
    print(df_pendente.info())
    print(df_forno.info())

if __name__ == "__main__":
    main()