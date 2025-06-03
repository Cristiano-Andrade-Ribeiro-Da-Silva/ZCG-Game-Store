from flask import Flask, render_template, request, redirect, session
from model import control as ct


app=Flask(__name__)

app.secret_key ="zcggamestore"


# ROTAS

@app.route("/")
def pagina_inicial():

    produto = ct.pega_jogos()
    jogos_em_destaque = ct.pega_jogos_destaque()
    jogos_em_destaque2 = ct.pega_jogos_destaque2()

    return render_template("Pagina_inicial.html", produto = produto, jogos_em_destaque = jogos_em_destaque, jogos_em_destaque2 = jogos_em_destaque2)

@app.route("/login")
def pagina_login():
    return render_template("Pagina_logar.html")

@app.route("/cadastro")
def pagina_cadastro():
    return render_template("Pagina_cadastrar.html")

@app.route("/carrinho")
def pagina_carrinho():
    return render_template("Pagina_carrinho.html")

@app.route("/apresentacao")
def pagina_apresentacao():
    return render_template("Pagina_apresentacao.html")

@app.route("/perfil-usuario")
def pagina_perfil_usuario():
    return render_template("Pagina_perfil-usuario.html")

@app.route("/categoria-jogos")
def pagina_categoria():
    return render_template("Pagina_categoria-jogos.html")

@app.route("/comprar-produto")
def pagina_comprar_produto():
    return render_template("Pagina_comprar-produto.html")

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=8080)


