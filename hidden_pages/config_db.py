import sqlite3 as db

conn = db.connect(r'C:\Users\pcp\OneDrive\#jeff\Dev\Analise_Producao\db\ttr.db')
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


