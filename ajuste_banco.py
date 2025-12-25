import sqlite3

con = sqlite3.connect("estoque.db")
cur = con.cursor()

cur.execute("ALTER TABLE pedidos ADD COLUMN cliente TEXT")

con.commit()
con.close()

print("Coluna cliente adicionada com sucesso!")
