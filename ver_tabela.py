import sqlite3

con = sqlite3.connect("estoque.db")
cur = con.cursor()

cur.execute("PRAGMA table_info(pedidos)")
for linha in cur.fetchall():
    print(linha)

con.close()