import sqlite3

con = sqlite3.connect("estoque.db")
cur = con.cursor()

cur.execute("ALTER TABLE pedidos ADD COLUMN cliente TEXT")


try:
    cur.execute("ALTER TABLE produtos ADD COLUMN descricao TEXT")
except:
    print("Coluna descricao já existe")

try:
    cur.execute("ALTER TABLE produtos ADD COLUMN imagem TEXT")
except:
    print("Coluna imagem já existe")




con.commit()
con.close()


print("Tabela produtos ajustada com sucesso")
print("Coluna cliente adicionada com sucesso!")
