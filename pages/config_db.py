import sqlite3 as db

local_banco = r'D:\#Mega\Jeferson - Dev\02 - Linguagens\Python\Analise_producao_streamlit\db\ttr.db'

conn = db.connect(local_banco)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS metas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_meta TEXT NOT NULL,
    turno01 INTEGER NOT NULL,
    turno02 INTEGER NOT NULL,
    meta_total INTEGER NOT NULL
)
""")

# Salvar e fechar conexão
conn.commit()
conn.close()


