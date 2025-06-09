from flask import Flask, render_template, request, redirect, session, flash, jsonify
from model import control as ct
from model import control_usuario


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


@app.route("/post/login", methods = ["POST"])
def pagina_login_usuario():
    email = request.form.get("email")
    senha = request.form.get("senha")

    if control_usuario.Usuario.controle_login_usuario(email, senha):
        flash('Entrou com êxito', 'success')
        return redirect("/")
    else:
        flash('Email ou senha inválidos', 'error')
        return redirect("/")


@app.route("/cadastro")
def pagina_cadastro():
    return render_template("Pagina_cadastrar.html")


@app.route("/post/cadastro", methods = ["POST"])
def pagina_cadas():
    email = request.form.get("email")
    nome = request.form.get("nome")
    senha = request.form.get("senha")
    telefone = request.form.get("telefone")

    print(f"RECEBIDO! EMAIL{email} / SENHA{senha} / NOME{nome} / TELEFONE {telefone}")

    sucesso = control_usuario.Usuario.controle_cadastra_usuario(nome, email, senha, telefone)
    print(f"Resultado do cadastro: {sucesso}")

    if sucesso:
        session['usuario_email'] = email
        return redirect("/")
    else:
        flash('Algum campo incorreto! Por favor, preencha novamente.', 'error')
        return redirect("/cadastro")
    
@app.route("/buscar_jogos", methods=["GET"])
def buscar_jogos():
    # "q" se refere ao query, ou seja, a URL | o outro parâmetro é se o usuario acessar sem buscar nada, ou seja, retorna em uma string vazia
    termo = request.args.get('q', '')
    resultados = ct.busca_jogos_por_nome(termo)


    return render_template('Pagina_busca.html', jogos=resultados, termo=termo)


@app.route("/carrinho")
def pagina_carrinho():
    return render_template("Pagina_carrinho.html")

@app.route("/apresentacao")
def pagina_apresentacao():
    return render_template("Pagina_apresentacao.html")

@app.route("/perfil-usuario")
def pagina_perfil_usuario():
    return render_template("Pagina_perfil-usuario.html")


# CATEGORIA
@app.route("/categoria-jogos")
def pagina_categoria():
    return render_template("Pagina_categoria-jogos.html")




@app.route("/comprar-produto")
def pagina_comprar_produto():
    return render_template("Pagina_comprar-produto.html")


@app.route("/get/logout")
def pagina_logout():
    flash("Você saiu da sua conta com êxito")
    control_usuario.Usuario.logoff()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=8080)




