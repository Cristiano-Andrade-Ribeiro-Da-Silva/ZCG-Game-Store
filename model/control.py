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
    conexao = CX.Conexao.conexao()
    cursor = conexao.cursor(dictionary=True)

    # SQL com LIKE para buscar pelo termo em nome_jogo
    sql = """
    select * from tb_jogo inner join foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_jogos inner join tb_categoria ON tb_jogo.cod_categoria = tb_categoria.cod_categoria LIKE %s;
    """

    cursor.execute(sql, (f"%{termo}%",))
    resultados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultados


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

        sql = "INSERT INTO tb_carrinho(codigo_produto, cod_jogo) VALUES(%s, %s);"

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