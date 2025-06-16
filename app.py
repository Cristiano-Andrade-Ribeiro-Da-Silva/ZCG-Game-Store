from flask import Flask, render_template, request, redirect, session, flash, jsonify
from model import control as ct
from model import control_usuario
from model import control_categoria_jg
from model.control_mensagens import Mensagem
from types import SimpleNamespace
# import stripe
# import qrcode
from io import BytesIO
import base64

# === APP SETUP ===
app = Flask(__name__)
app.secret_key = "zcgamestore"  # CORRIGIDO: era Flask.secret_key, o correto é app.secret_key

# === ROTAS COMENTADAS (Pagamento) ===
# stripe.api_key = "sk_test_51RZxmcQVQ7xKDVyzobtUiCoBHsvMOJbxNAJAjhtVd5VzDVPQVZBHAmevSjvlZ7SLoAem43PV2ZR2GOO8UbA5ixKQ00c1x0Y7wS"

# @app.route("/checkout")
# def checkout():
#     return render_template("checkout.html")

# @app.route("/criar_pagamento", methods=["POST"])
# def criar_pagamento():
#     metodo = request.form.get("metodo")
#     if metodo == "stripe":
#         session = stripe.checkout.Session.create(
#             payment_method_types=["card"],
#             line_items=[{
#                 "price_data": {
#                     "currency": "brl",
#                     "product_data": {"name": "Jogo Exemplo"},
#                     "unit_amount": 4990,
#                 },
#                 "quantity": 1,
#             }],
#             mode="payment",
#             success_url=request.url_root + "confirmado",
#             cancel_url=request.url_root + "checkout",
#         )
#         return redirect(session.url, code=303)

#     elif metodo == "pix":
#         dados_pix = "00020126360014BR.GOV.BCB.PIX0114+559999999999520400005303986540549.905802BR5920ZCG Game Store6009Sao Paulo62070503***6304ABCD"
#         img = qrcode.make(dados_pix)
#         buffer = BytesIO()
#         img.save(buffer, format="PNG")
#         qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
#         return f'''
#         <h2>Escaneie o QR Code com seu app de banco:</h2>
#         <img src="data:image/png;base64,{qr_code_base64}" alt="QR Code Pix"/>
#         <p><a href="/">Voltar</a></p>
#         '''

# @app.route("/confirmado")
# def confirmado():
#     return "<h2>Pagamento confirmado com sucesso!</h2><p><a href='/'>Voltar à loja</a></p>"


# === ROTAS PRINCIPAIS ===

@app.route("/")
def pagina_inicial():
    produto = ct.pega_jogos()
    jogos_em_destaque = ct.pega_jogos_destaque()
    jogos_em_destaque2 = ct.pega_jogos_destaque2()
    return render_template("Pagina_inicial.html", produto=produto, jogos_em_destaque=jogos_em_destaque, jogos_em_destaque2=jogos_em_destaque2)


@app.route("/login")
def pagina_login():
    return render_template("Pagina_logar.html")


@app.route("/post/login", methods=["POST"])
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


@app.route("/post/cadastro", methods=["POST"])
def pagina_cadas():
    email = request.form.get("email")
    nome = request.form.get("nome")
    senha = request.form.get("senha")
    telefone = request.form.get("telefone")

    sucesso = control_usuario.Usuario.controle_cadastra_usuario(nome, email, senha, telefone)

    if sucesso:
        session['usuario_email'] = email
        return redirect("/")
    else:
        flash('Algum campo incorreto! Por favor, preencha novamente.', 'error')
        return redirect("/cadastro")


@app.route("/get/logout")
def pagina_logout():
    flash("Você saiu da sua conta com êxito")
    control_usuario.Usuario.logoff()
    return redirect("/")


# === BUSCA ===

@app.route("/buscar_jogos", methods=["GET"])
def buscar_jogos():
    termo = request.args.get('q', '')
    resultados = ct.busca_jogos_por_nome(termo)
    return render_template('Pagina_busca.html', jogos=resultados, termo=termo)


# === CARRINHO ===

@app.route("/carrinho/<codigo>")
def add_pagina_carrinho(codigo):
    if "cod_usuario" not in session:
        flash("Você precisa estar logado para adicionar ao carrinho.", "warning")
        return redirect("/login")

    cod_usuario = session["cod_usuario"]
    ct.carrinho_produto(codigo, cod_usuario)
    flash("Produto adicionado ao carrinho com sucesso!", "success")
    return redirect("/carrinho")


@app.route("/carrinho")
def exibir_carrinho():
    if "cod_usuario" not in session:
        flash("Faça login para ver seu carrinho.", "warning")
        return redirect("/login")

    cod_usuario = session["cod_usuario"]
    produtos = ct.resgata_produto(cod_usuario)

    if not produtos:
        flash("Seu carrinho está vazio.", "info")
        return redirect("/")

    total = sum([item['preco'] for item in produtos])
    return render_template("Pagina_carrinho.html", carrinho=produtos, total=total)


@app.route("/atualizar_carrinho", methods=["POST"])
def atualizar_carrinho():
    codigo = request.form.get("codigo")
    nova_qtd = int(request.form.get("quantidade", 1))

    if 'carrinho' in session and codigo in session['carrinho']:
        if nova_qtd <= 0:
            del session['carrinho'][codigo]
            flash("Produto removido do carrinho!", "success")
        else:
            session['carrinho'][codigo]['quantidade'] = nova_qtd
            flash("Quantidade atualizada!", "success")

    session.modified = True
    return redirect("/carrinho")


@app.route("/limpar_carrinho")
def limpar_carrinho():
    session.pop('carrinho', None)
    flash("Carrinho limpo com sucesso!", "success")
    return redirect("/carrinho")


@app.route("/excluir/<codigo>")
def excluir_produto(codigo):
    if 'carrinho' in session and codigo in session['carrinho']:
        del session['carrinho'][codigo]

    # Remover do banco de dados também
    ct.excluir_produtos(codigo)

    session.modified = True
    flash("Produto removido do carrinho!", "success")
    return redirect("/carrinho")


# === PRODUTOS ===

@app.route("/comprar-produto/<codigo>")
def pagina_comprar_produto(codigo):
    produto_data = ct.comprar_produto(codigo)

    if not produto_data:
        flash("Produto não encontrado", "error")
        return redirect("/")

    produto_jogo = SimpleNamespace(**produto_data)
    mensagens = Mensagem.mostra_mensagens(codigo) or []
    return render_template("Pagina_comprar-produto.html", produto=produto_jogo, mensagens=mensagens)


@app.route("/post/comentario", methods=["POST"])
def postar_comentario():
    nome_usuario = session.get("usuario_email", "Anônimo")
    comentario = request.form.get("mensagem")
    cod_jogo = request.form.get("cod_jogo")

    if comentario and cod_jogo:
        try:
            Mensagem.cadastrar_mensagem(nome_usuario, comentario, cod_jogo)
            flash("Comentário publicado com sucesso!", "success")
        except Exception as e:
            print(f"[ERRO] Falha ao salvar comentário: {e}")
            flash("Erro ao salvar o comentário.", "error")
    else:
        flash("Comentário vazio ou jogo inválido!", "error")

    return redirect(f"/comprar-produto/{cod_jogo}")


# === CATEGORIAS ===

@app.route("/categoria-jogos")
def pagina_categoria():
    categorias = control_categoria_jg.listar_categorias()
    return render_template("Pagina_categoria-jogos.html", categorias=categorias, jogos=[])


@app.route("/categoria/<int:cod_categoria>")
def jogos_por_categoria(cod_categoria):
    jogos = control_categoria_jg.pega_jogos_por_categoria(cod_categoria)
    categorias = control_categoria_jg.listar_categorias()
    return render_template("Pagina_categoria-jogos.html", jogos=jogos, categorias=categorias)


# === OUTRAS PÁGINAS ===

@app.route("/apresentacao")
def pagina_apresentacao():
    return render_template("Pagina_apresentacao.html")


@app.route("/perfil-usuario")
def pagina_perfil_usuario():
    
    historico = session.get("historico", [])
    return render_template("Pagina_perfil-usuario.html", historico=historico)

#compra individua

@app.route("/comprar/individual/<codigo>")
def comprar_individual(codigo):
    produto = ct.compra_individual(codigo)

    if not produto:
        flash("Produto não encontrado.")
        return redirect("/")

    # Pega histórico da sessão ou cria novo
    historico = session.get("historico", [])

    # Adiciona o produto
    historico.append(produto)

    # Atualiza a sessão
    session["historico"] = historico

    return redirect("/carrinho")


# === EXECUÇÃO DO APP ===

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=8080)
    # oloko mano
