import sqlite3


def conectar():
    con = sqlite3.connect("estoque.db")
    con.row_factory = sqlite3.Row
    return con


def criar_tabela_pedidos():
    con = conectar()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_cliente TEXT,
        endereco TEXT,
        produto_id TEXT,
        produto_nome TEXT,
        quantidade INTEGER,
        status TEXT DEFAULT 'Pendente'
    )""")

    con.commit()
    con.close()



def criar_tabelas():
    con = conectar()
    cur = con.cursor()


    cur.execute("""
    CREATE TABLE IF NOT EXISTS produtos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        quantidade INTEGER 
    )""")

    con.commit()
    con.close()



criar_tabela_pedidos()
criar_tabelas()
print ("Banco de dados criado com sucesso !")