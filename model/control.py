from data import conexao as CX

#exibir os jogos na pagina inicial

def pega_jogos():

        conexao = CX.Conexao.conexao()
        cursor = conexao.cursor(dictionary = True)

        sql = "select * from tb_jogo inner join foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_foto inner join tb_categoria ON tb_jogo.cod_jogo = tb_categoria.cod_categoria;"

        cursor.execute(sql, )

        infos = cursor.fetchall()

        cursor.close()
        conexao.close()

        return infos

def pega_jogos_destaque():

        conexao = CX.Conexao.conexao()
        cursor = conexao.cursor(dictionary = True)

        sql = """select * from tb_jogo inner join foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_foto inner join tb_categoria ON tb_jogo.cod_jogo = tb_categoria.cod_categoria WHERE nome_jogo = "GTA VI" or nome_jogo = "elden ring" or nome_jogo = "Assassin's Creed Rogue";"""

        cursor.execute(sql, )

        infos = cursor.fetchall()

        cursor.close()
        conexao.close()

        return infos

def pega_jogos_destaque2():

        conexao = CX.Conexao.conexao()
        cursor = conexao.cursor(dictionary = True)

        sql = """select * from tb_jogo inner join foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_foto inner join tb_categoria ON tb_jogo.cod_jogo = tb_categoria.cod_categoria WHERE nome_jogo = "dark souls" or nome_jogo = "dark souls II" or nome_jogo = "dark souls III";"""

        cursor.execute(sql, )

        infos = cursor.fetchall()

        cursor.close()
        conexao.close()

        return infos

def busca_jogos_por_nome(termo):
    conexao = CX.Conexao.conexao()
    cursor = conexao.cursor(dictionary=True)

    # SQL com LIKE para buscar pelo termo em nome_jogo
    sql = """
    SELECT * 
    FROM tb_jogo 
    INNER JOIN foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_foto 
    INNER JOIN tb_categoria ON tb_jogo.cod_jogo = tb_categoria.cod_categoria
    WHERE nome_jogo LIKE %s;
    """

    cursor.execute(sql, (f"%{termo}%",))
    resultados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultados
