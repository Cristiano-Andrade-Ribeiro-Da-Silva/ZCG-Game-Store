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
import os
from werkzeug.utils import secure_filename

# === APP SETUP ===
app = Flask(__name__)
app.secret_key = "zcgamestore"  # CORRIGIDO: era Flask.secret_key, o correto é app.secret_key


# Diretório onde as fotos de perfil serão salvas
UPLOAD_FOLDER = os.path.join("static", "uploads", "perfis")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    return render_template("Inicial.html", produto=produto, jogos_em_destaque=jogos_em_destaque, jogos_em_destaque2=jogos_em_destaque2)


@app.route("/login")
def pagina_login():
    return render_template("Logar.html")


@app.route("/post/login", methods=["POST"])
def pagina_login_usuario():
    email = request.form.get("email")
    senha = request.form.get("senha")

    if control_usuario.Usuario.controle_login_usuario(email, senha):
        flash('Entrou com êxito', 'success')
        return redirect("/")
    else:
        flash('Email ou senha inválidos', 'error')
        return redirect("/login")


@app.route("/cadastro")
def pagina_cadastro():
    return render_template("Cadastrar.html")


@app.route("/post/cadastro", methods=["POST"])
def pagina_cadas():
    email = request.form.get("email")
    nome = request.form.get("nome")
    senha = request.form.get("senha")
    telefone = request.form.get("telefone")

    sucesso = control_usuario.Usuario.controle_cadastra_usuario(nome, email, senha, telefone)

    if sucesso:
        session['usuario_email'] = email
        return redirect("/login")
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
    return render_template('Busca.html', jogos=resultados, termo=termo)


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
    return render_template("Carrinho.html", carrinho=produtos, total=total)


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


@app.route("/cancelar-compra")
def cancelar_compra():
    return redirect("/")


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
    pega_video = ct.resgata_veido_produto(codigo)

    if not produto_data:
        flash("Produto não encontrado", "error")
        return redirect("/")

    produto_jogo = SimpleNamespace(**produto_data)
    mensagens = Mensagem.mostra_mensagens(codigo) or []
    return render_template("Comprar_produtos.html", produto=produto_jogo, mensagens=mensagens, video = pega_video)

@app.route("/comprar/individual/<codigo>")
def comprar_individual(codigo):
    if "cod_usuario" not in session:
        flash("Você precisa estar logado para comprar.", "warning")
        return redirect("/login")

    cod_usuario = session["cod_usuario"]

    try:
        ct.compra_individual(codigo, cod_usuario)
        flash("Compra realizada com sucesso!", "success")
    except Exception as e:
        print(f"Erro na compra individual: {e}")
        flash("Erro ao realizar a compra.", "error")

    return redirect("/carrinho")

@app.route("/comprar-tudo", methods=["POST"])
def comprar_tudo():
    if "cod_usuario" not in session:
        flash("Você precisa estar logado para comprar.", "warning")
        return redirect("/login")
    

    cod_usuario = session["cod_usuario"]

    try:
        ct.comprar_tudo(cod_usuario)
        flash("Compra realizada com sucesso!", "success")
    except Exception as e:
        print(f"Erro na compra individual: {e}")
        flash("Erro ao realizar a compra.", "error")

    return redirect("/carrinho")

@app.route("/post/comentario", methods=["POST"])
def postar_comentario():
    cod_jogo = request.form.get("cod_jogo")
    comentario = request.form.get("mensagem")

    if "cod_usuario" in session:
        cod_usuario = session["cod_usuario"]
    else:
        return redirect("/login")

    if comentario and cod_jogo:
        try:
            Mensagem.cadastrar_mensagem(cod_usuario, comentario, cod_jogo)
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
    return render_template("Categoria_jogos.html", categorias=categorias, jogos=[])


@app.route("/categoria/<int:cod_categoria>")
def jogos_por_categoria(cod_categoria):
    jogos = control_categoria_jg.pega_jogos_por_categoria(cod_categoria)
    categorias = control_categoria_jg.listar_categorias()
    return render_template("Categoria_jogos.html", jogos=jogos, categorias=categorias)


# === OUTRAS PÁGINAS ===

@app.route("/apresentacao")
def pagina_apresentacao():
    return render_template("Apresentacao.html")


@app.route("/perfil-usuario")
def pagina_perfil_usuario():
    if "cod_usuario" not in session:
        flash("Faça login para acessar o perfil.", "warning")
        return redirect("/login")

    cod_usuario = session["cod_usuario"]
    historico = ct.resgata_historico(cod_usuario)

    # Pega os dados completos do usuário
    usuario = control_usuario.Usuario.busca_usuario_por_id(cod_usuario)

    return render_template("Perfil_usuario.html", historico=historico, usuario=usuario)



# === USUÁRIO ===
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/upload_foto_perfil", methods=["POST"])
def upload_foto_perfil():
    if "cod_usuario" not in session:
        flash("Você precisa estar logado para mudar a foto de perfil.", "warning")
        return redirect("/login")

    if 'foto' not in request.files:
        flash("Nenhuma foto enviada.", "danger")
        return redirect("/perfil-usuario")

    file = request.files['foto']
    if file.filename == '':
        flash("Nenhum arquivo selecionado.", "danger")
        return redirect("/perfil-usuario")

    if file and allowed_file(file.filename):
        cod_usuario = session["cod_usuario"]
        filename = secure_filename(f"user_{cod_usuario}.{file.filename.rsplit('.', 1)[1]}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Garante que a pasta exista
        file.save(filepath)

        # Aqui você pode atualizar no banco de dados o caminho da imagem, se desejar
        control_usuario.Usuario.atualizar_foto_perfil(cod_usuario, filename)

        flash("Foto de perfil atualizada!", "success")
        return redirect("/perfil-usuario")

    flash("Arquivo inválido. Envie uma imagem PNG, JPG, JPEG ou GIF.", "danger")
    return redirect("/perfil-usuario")

# === EXECUÇÃO DO APP ===

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=8080)
    # oloko mano
