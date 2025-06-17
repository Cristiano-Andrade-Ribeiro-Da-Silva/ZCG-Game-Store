from data import conexao as CX

# Exibir os jogos na página inicial
def pega_jogos():
    conexao = CX.Conexao.conexao()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT * 
        FROM tb_jogo 
        INNER JOIN foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_jogos 
        INNER JOIN tb_categoria ON tb_jogo.cod_categoria = tb_categoria.cod_categoria;
    """

    cursor.execute(sql)
    infos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return infos


def pega_jogos_destaque():
    conexao = CX.Conexao.conexao()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT * 
        FROM tb_jogo 
        INNER JOIN foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_jogos 
        INNER JOIN tb_categoria ON tb_jogo.cod_categoria = tb_categoria.cod_categoria 
        WHERE nome_jogo = 'GTA VI' 
           OR nome_jogo = 'elden ring' 
           OR nome_jogo = 'Assassin s Creed Rogue';
    """

    cursor.execute(sql)
    infos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return infos


def pega_jogos_destaque2():
    conexao = CX.Conexao.conexao()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT * 
        FROM tb_jogo 
        INNER JOIN foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_jogos 
        INNER JOIN tb_categoria ON tb_jogo.cod_categoria = tb_categoria.cod_categoria 
        WHERE nome_jogo = 'dark souls' 
           OR nome_jogo = 'dark souls II' 
           OR nome_jogo = 'dark souls III';
    """

    cursor.execute(sql)
    infos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return infos


def busca_jogos_por_nome(termo):
    # Evita busca com 0 ou 1 caractere
    if not termo or len(termo.strip()) < 2:
        return []

    conexao = CX.Conexao.conexao()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT 
            tb_jogo.cod_jogo,
            tb_jogo.nome_jogo,
            tb_jogo.preco,
            tb_jogo.descricao_jogo,
            tb_categoria.categoria,
            foto_produtos.url
        FROM tb_jogo
        INNER JOIN foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_jogos
        INNER JOIN tb_categoria ON tb_jogo.cod_categoria = tb_categoria.cod_categoria
        WHERE tb_jogo.nome_jogo LIKE %s;
    """

    cursor.execute(sql, (f"%{termo}%",))
    resultados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultados


def comprar_produto(codigo):
    conexao = CX.Conexao.conexao()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT * 
        FROM tb_jogo 
        INNER JOIN foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_jogos 
        INNER JOIN tb_categoria ON tb_jogo.cod_categoria = tb_categoria.cod_categoria 
        WHERE cod_jogo = %s;
    """

    cursor.execute(sql, (codigo,))
    info = cursor.fetchone()

    cursor.close()
    conexao.close()

    return info


def carrinho_produto(cod_jogo, cod_usuario):
    conexao = CX.Conexao.conexao()
    cursor = conexao.cursor()

    sql_insert = """
        INSERT INTO tb_carrinho(codigo_produto, cod_jogo, cod_usuario) 
        VALUES (%s, %s, %s);
    """

    sql_delete = """DELETE FROM tb_carrinho
        WHERE cod_carrinho IN (
        SELECT cod_carrinho FROM (
                SELECT MAX(cod_carrinho) AS cod_carrinho
                FROM tb_carrinho
                GROUP BY codigo_produto
                HAVING COUNT(*) > 1
        ) AS temp
        );"""

    valores = (cod_jogo, cod_jogo, cod_usuario)

    cursor.execute(sql_insert, valores)
    cursor.execute(sql_delete)
    conexao.commit()

    cursor.close()
    conexao.close()


def resgata_produto(cod_usuario):
    conexao = CX.Conexao.conexao()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT 
            tb_jogo.*, 
            foto_produtos.url, 
            tb_categoria.categoria, 
            tb_carrinho.codigo_produto, 
            tb_carrinho.cod_usuario
        FROM tb_jogo 
        INNER JOIN foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_jogos 
        INNER JOIN tb_categoria ON tb_jogo.cod_categoria = tb_categoria.cod_categoria
        INNER JOIN tb_carrinho ON tb_jogo.cod_jogo = tb_carrinho.cod_jogo
        WHERE tb_carrinho.cod_usuario = %s;
    """

    cursor.execute(sql, (cod_usuario,))
    infos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return infos


def excluir_produtos(codigo):
    conexao = CX.Conexao.conexao()
    cursor = conexao.cursor()

    sql = "DELETE FROM tb_carrinho WHERE cod_jogo = %s;"
    cursor.execute(sql, (codigo,))

    conexao.commit()
    cursor.close()
    conexao.close()

def compra_individual(codigo, cod_usuario):
    conexao = CX.Conexao.conexao()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO tb_historico (nome_produto, preco_produto, cod_usuario)
        SELECT nome_jogo, preco, %s
        FROM tb_jogo
        WHERE cod_jogo = %s;

        DELETE FROM tb_carrinho WHERE cod_jogo = %s AND cod_usuario = %s;
    """
    valores = (cod_usuario, codigo, codigo, cod_usuario)

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()


def resgata_historico(cod_usuario):
    conexao = CX.Conexao.conexao()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT nome_produto, preco_produto, data_compra
        FROM tb_historico
        WHERE cod_usuario = %s
        ORDER BY data_compra DESC;
    """
    cursor.execute(sql, (cod_usuario,))
    infos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return infos

def comprar_tudo(cod_usuario):

        conexao = CX.Conexao.conexao()
        cursor = conexao.cursor()

        sql = """INSERT INTO tb_historico (nome_produto, preco_produto, cod_usuario)
                SELECT j.nome_jogo, j.preco, c.cod_usuario
                FROM tb_carrinho c
                INNER JOIN tb_jogo j ON c.cod_jogo = j.cod_jogo;"""
        
        sql_delete = """DELETE FROM tb_carrinho"""

        cursor.execute(sql)
        cursor.execute(sql_delete)

        conexao.commit()
        cursor.close()
        conexao.close()