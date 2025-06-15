from flask import Flask, render_template, request, redirect, session, flash, jsonify
from model import control as ct
from model import control_usuario
from model import control_categoria_jg
from model.control_mensagens import Mensagem
from types import SimpleNamespace
import stripe
import qrcode
from io import BytesIO
import base64



app=Flask(__name__)

stripe.api_key = "sk_test_51RZxmcQVQ7xKDVyzobtUiCoBHsvMOJbxNAJAjhtVd5VzDVPQVZBHAmevSjvlZ7SLoAem43PV2ZR2GOO8UbA5ixKQ00c1x0Y7wS"


# ROTAS
@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

@app.route("/criar_pagamento", methods=["POST"])
def criar_pagamento():
    metodo = request.form.get("metodo")
    if metodo == "stripe":
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "brl",
                    "product_data": {"name": "Jogo Exemplo"},
                    "unit_amount": 4990,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=request.url_root + "confirmado",
            cancel_url=request.url_root + "checkout",
        )
        return redirect(session.url, code=303)

    elif metodo == "pix":
        dados_pix = "00020126360014BR.GOV.BCB.PIX0114+559999999999520400005303986540549.905802BR5920ZCG Game Store6009Sao Paulo62070503***6304ABCD"
        img = qrcode.make(dados_pix)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
        return f'''
        <h2>Escaneie o QR Code com seu app de banco:</h2>
        <img src="data:image/png;base64,{qr_code_base64}" alt="QR Code Pix"/>
        <p><a href="/">Voltar</a></p>
        '''

@app.route("/confirmado")
def confirmado():
    return "<h2>Pagamento confirmado com sucesso!</h2><p><a href='/'>Voltar à loja</a></p>"
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

@app.route("/comprar-produto/<codigo>")
def pagina_comprar_produto(codigo):
    from types import SimpleNamespace

    produto_data = ct.comprar_produto(codigo)

    if not produto_data:
        flash("Produto não encontrado", "error")
        return redirect("/")
    
    produto_jogo = SimpleNamespace(**produto_data)

    mensagens = Mensagem.mostra_mensagens(codigo)
    if mensagens is None:
        mensagens = []

    return render_template("Pagina_comprar-produto.html", produto=produto_jogo, mensagens=mensagens)

@app.route("/categoria-jogos")
def pagina_categoria():
    categorias = control_categoria_jg.listar_categorias()
    return render_template("Pagina_categoria-jogos.html", categorias=categorias, jogos=[])

@app.route("/categoria/<int:cod_categoria>")
def jogos_por_categoria(cod_categoria):
    jogos = control_categoria_jg.pega_jogos_por_categoria(cod_categoria)
    categorias = control_categoria_jg.listar_categorias()
    return render_template("Pagina_categoria-jogos.html", jogos=jogos, categorias=categorias)




@app.route("/excluir/<codigo>")
def excluir_produto(codigo):
    ct.excluir_produtos(codigo)
    return redirect("/carrinho")


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

    

@app.route("/get/logout")
def pagina_logout():
    flash("Você saiu da sua conta com êxito")
    control_usuario.Usuario.logoff()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=8080)
    #oloko mano




