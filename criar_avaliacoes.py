import sqlite3

con = sqlite3.connect("banco.db")
cur = con.cursor()


cur.execute("""
    CREATE TABLE IF NOT EXISTS avaliacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_cliente TEXT NOT NULL,
        comentario TEXT NOT NULL,
        estrelas INTEGER NOT NULL,
        foto TEXT
            )""")


con.commit()
con.close()

print("Tabela de avaliações criada com sucesso !")