from data import conexao as CX

#exibir os jogos na pagina inicial

def pega_jogos():

        conexao = CX.Conexao.conexao()
        cursor = conexao.cursor(dictionary = True)

        sql = "select * from tb_jogo inner join foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_jogos inner join tb_categoria ON tb_jogo.cod_categoria = tb_categoria.cod_categoria;"

        cursor.execute(sql, )

        infos = cursor.fetchall()

        cursor.close()
        conexao.close()

        return infos

def pega_jogos_destaque():

        conexao = CX.Conexao.conexao()
        cursor = conexao.cursor(dictionary = True)

        sql = """select * from tb_jogo inner join foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_jogos inner join tb_categoria ON tb_jogo.cod_categoria = tb_categoria.cod_categoria WHERE nome_jogo = 'GTA VI' or nome_jogo = 'elden ring' or nome_jogo = 'Assassin s Creed Rogue';"""

        cursor.execute(sql, )

        infos = cursor.fetchall()

        cursor.close()
        conexao.close()

        return infos

def pega_jogos_destaque2():

        conexao = CX.Conexao.conexao()
        cursor = conexao.cursor(dictionary = True)

        sql = """select * from tb_jogo inner join foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_jogos inner join tb_categoria ON tb_jogo.cod_categoria = tb_categoria.cod_categoria WHERE nome_jogo = 'dark souls' or nome_jogo = 'dark souls II' or nome_jogo = 'dark souls III';"""

        cursor.execute(sql, )

        infos = cursor.fetchall()

        cursor.close()
        conexao.close()

        return infos

def busca_jogos_por_nome(termo):
    if not termo or len(termo.strip()) < 2:
        return []  # Evita busca com 0 ou 1 caractere

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
        FROM 
            tb_jogo
        INNER JOIN 
            foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_jogos
        INNER JOIN 
            tb_categoria ON tb_jogo.cod_categoria = tb_categoria.cod_categoria
        WHERE 
            tb_jogo.nome_jogo LIKE %s;
    """
    cursor.execute(sql, (f"%{termo}%",))
    return cursor.fetchall()


def comprar_produto(codigo):

        conexao = CX.Conexao.conexao()
        cursor = conexao.cursor(dictionary=True)

        valor = (codigo,)

        sql = """select * from tb_jogo inner join foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_jogos inner join tb_categoria ON tb_jogo.cod_categoria = tb_categoria.cod_categoria WHERE cod_jogo = %s;"""

        cursor.execute(sql, valor)

        infos = cursor.fetchone()

        cursor.close()
        conexao.close()

        return infos


def carrinho_produto(codigo):

        conexao = CX.Conexao.conexao()
        cursor = conexao.cursor()

        valor = (codigo, codigo)

        sql = """INSERT INTO tb_carrinho(codigo_produto, cod_jogo) VALUES(%s, %s);
        
                        DELETE FROM tb_carrinho
                WHERE cod_carrinho IN (
                SELECT cod_carrinho FROM (
                        SELECT MAX(cod_carrinho) AS cod_carrinho
                        FROM tb_carrinho
                        GROUP BY codigo_produto
                        HAVING COUNT(*) > 1
                ) AS temp
                );"""

        cursor.execute(sql, valor)
        
        conexao.commit()
        cursor.close()
        conexao.close()

def resgata_produto():
       
        conexao = CX.Conexao.conexao()
        cursor = conexao.cursor(dictionary=True)

        sql = """select * from tb_jogo 

                inner join foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_jogos 
                inner join tb_categoria on tb_jogo.cod_categoria = tb_categoria.cod_categoria
                inner join tb_carrinho on tb_jogo.cod_jogo = tb_carrinho.cod_jogo;"""

        cursor.execute(sql)

        infos = cursor.fetchall()

        cursor.close()
        conexao.close()

        return infos

def excluir_produtos(codigo):
        valor = (codigo,)

        conexao = CX.Conexao.conexao()
        cursor = conexao.cursor()

        sql = """DELETE FROM tb_carrinho WHERE cod_jogo = %s;"""

        cursor.execute(sql,valor)

        infos = cursor.fetchall()

        conexao.commit()
        cursor.close()
        conexao.close()

        return infos