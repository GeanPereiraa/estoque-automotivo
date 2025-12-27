from flask import Flask, render_template, request, redirect, session
from database import conectar


app = Flask(__name__)
app.secret_key = "estoque_automotivo_secreto"

ADMIN_USER = "admin"
ADMIN_PASS = "F3a2--329"


@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None

    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario == ADMIN_USER and senha ==ADMIN_PASS:
            session["admin"] = True
            return redirect("/admin")
        
        else:
            erro = "Usuario ou senha inválidos"

    return render_template("login.html", erro=erro)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/novo_produto", methods=["GET"])
def pagina_novo_produto():
    if not session.get("admin"):
        return redirect("/login")

    return render_template("novo_produto.html")


@app.route("/salvar_produto", methods=["POST"])
def salvar_produto():
    if not session.get("admin"):
        return redirect("/login")


    nome = request.form.get("nome")
    quantidade = request.form.get("quantidade")

    if not nome or not quantidade:
        return redirect("/novo_produto")

    try:
        quantidade = int(quantidade)
    except ValueError:
        return redirect("/novo_produto")

    con = conectar()
    cur = con.cursor()

    # 🔑 REGRA: NÃO CRIAR CARD DUPLICADO
    cur.execute("SELECT * FROM produtos WHERE nome = ?", (nome,))
    produto = cur.fetchone()

    if produto:
        cur.execute(
            "UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?",
            (quantidade, produto["id"])
        )
    else:
        cur.execute(
            "INSERT INTO produtos (nome, quantidade) VALUES (?, ?)",
            (nome, quantidade)
        )

    con.commit()
    con.close()

    return redirect("/produtos")


@app.route("/pedido_resolvido/<int:id>")
def pedido_resolvido(id):
    if not session.get("admin"):
        return redirect("/login")

    con = conectar()
    cur = con.cursor()

    cur.execute(
        "UPDATE pedidos SET status = 'Resolvido' WHERE id = ?",
        (id,)
    )

    con.commit()
    con.close()

    return redirect("/admin")


@app.route("/produtos")

def listar_produtos():
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT * FROM produtos")
    produtos = cur.fetchall()

    con.close()
    return render_template("produtos.html", produtos=produtos)


@app.route("/entrada/<int:id>")

def entrada(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("UPDATE produtos SET quantidade = quantidade + 1 WHERE id=?",(id))
    con.commit()
    con.close()

    return redirect("/produtos")


@app.route("/saida/<int:id>")
def saida(id):
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT quantidade FROM produtos WHERE id=?", (id,))
    qtd = cur.fetchone()[0]

    if qtd > 0:
        cur.execute("UPDATE produtos SET quantidade = quantidade - 1 WHERE id=?", (id,))
        con.commit()

    con.close()
    return redirect("/produtos")


from urllib.parse import quote

@app.route("/solicitar/<int:id>", methods=["GET", "POST"])
def solicitar(id):
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT * FROM produtos WHERE id = ?", (id,))
    produto = cur.fetchone()

    erro = None

    if request.method == "POST":
        nome = request.form.get("nome")
        endereco = request.form.get("endereco")
        quantidade = int(request.form.get("quantidade"))

        if not endereco:
            erro = "Endereço é obrigatório"
            con.close()
            return render_template("solicitar.html", produto=produto, erro=erro)

        if quantidade > produto["quantidade"]:
            erro = "Quantidade indisponível em estoque"
            con.close()
            return render_template("solicitar.html", produto=produto, erro=erro)

        # salva pedido (SEM criar produto novo)
        cur.execute("""
            INSERT INTO pedidos (cliente, endereco, produto_nome, quantidade, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            nome,
            endereco,
            produto["nome"],
            quantidade,
            "Pendente"
        ))

        # baixa estoque do PRODUTO EXISTENTE
        cur.execute("""
            UPDATE produtos
            SET quantidade = quantidade - ?
            WHERE id = ?
        """, (quantidade, id))

        con.commit()
        con.close()

        mensagem = (
            f"📦 NOVO PEDIDO\n"
            f"Cliente: {nome}\n"
            f"Produto: {produto['nome']}\n"
            f"Quantidade: {quantidade}\n"
            f"Endereço: {endereco}"
        )

        mensagem = quote(mensagem)

        link_whatsapp = f"https://wa.me/5518991796621?text={mensagem}"
        return redirect(link_whatsapp)



    con.close()
    return render_template("solicitar.html", produto=produto, erro=erro)


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT * FROM pedidos")
    pedidos = cur.fetchall()

    cur.execute("""
        SELECT produto_nome, SUM(quantidade)
        FROM pedidos
        GROUP BY produto_nome
        ORDER BY SUM(quantidade) DESC
        """)
    vendidos = cur.fetchall()

    con.close()

    return render_template("admin.html", pedidos=pedidos, vendidos=vendidos)


@app.route("/aprovar/<int:id>")
def aprovar(id):
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT * FROM pedidos WHERE id=?", (id))
    pedido = cur.fetchone()

    cur.execute(
        "UPDATE pedidos SET status='APROVADO' WHERE id=?",
        (id,)
    )

    con.commit()
    con.close()
    return redirect("/admin")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)