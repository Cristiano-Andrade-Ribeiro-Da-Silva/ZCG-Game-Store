from flask import Flask, render_template, request, redirect, session, flash, jsonify
from model import control as ct
from model import control_usuario
from model.control_mensagens import Mensagem
from types import SimpleNamespace



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


@app.route("/carrinho/<codigo>")
def add_pagina_carrinho(codigo):

    ct.carrinho_produto(codigo)

    return redirect("/carrinho")

@app.route("/carrinho")
def exibir_carrinho():

    pega_produto = ct.resgata_produto()

    return render_template("Pagina_carrinho.html", pega_produto = pega_produto)


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



@app.route("/comprar-produto/<codigo>")
def pagina_comprar_produto(codigo):
    from types import SimpleNamespace

    produto_data = ct.comprar_produto(codigo)
    if not produto_data:
        flash("Produto não encontrado", "error")
        return redirect("/")

    produto_jogo = SimpleNamespace(**produto_data)


@app.route("/excluir/<codigo>")
def excluir_produto(codigo):
    ct.excluir_produtos(codigo)
    return redirect("/carrinho")

    mensagens = Mensagem.mostra_mensagens(codigo)
    if mensagens is None:
        mensagens = []

    return render_template("Pagina_comprar-produto.html", produto=produto_jogo, mensagens=mensagens)



@app.route("/post/comentario", methods=["POST"])
def postar_comentario():
    nome_usuario = session.get("usuario_email", "Anônimo")  
    comentario = request.form.get("mensagem")
    cod_jogo = request.form.get("cod_jogo")

    if comentario and cod_jogo:
        try:
            Mensagem.cadastrar_mensagem(nome_usuario, comentario, cod_jogo)  # Passa o cod_jogo
            flash("Comentário publicado com sucesso!", "success")
        except Exception as e:
            print(f"[ERRO] Falha ao salvar comentário: {e}")
            flash("Erro ao salvar o comentário.", "error")
    else:
        flash("Comentário vazio ou jogo inválido!", "error")

    return redirect(f"/comprar-produto/{cod_jogo}")

>>>>>>> 96e78f925a1adf88e3706dd8420650861133d261

@app.route("/get/logout")
def pagina_logout():
    flash("Você saiu da sua conta com êxito")
    control_usuario.Usuario.logoff()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=8080)
    #oloko mano




