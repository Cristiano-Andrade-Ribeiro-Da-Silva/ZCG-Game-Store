from data import conexao as CX


class Mensagem:

    def cadastrar_mensagem(usuario, comentarios):

        conexao = CX.Conexao.conexao()

        cursor = conexao.cursor()

        sql = """ INSERT INTO tb_comentario (nome, comentario) VALUES (%s, %s)""" 

        valores = (usuario, comentarios)

        cursor.execute(sql, valores)

        conexao.commit()

        cursor.close()

        conexao.close()


    def mostra_mensagens():

        conexao = CX.Conexao.conexao()

        cursor = conexao.cursor(dictionary=True)

        sql = """SELECT nome as usuario, cod_comentario, comentario from tb_comentario"""

        cursor.execute(sql)

        resultado = cursor.fetchall()

        cursor.close()

        conexao.close()

        return resultado
    
    def last_mensage(usuario):
        
        conexao = CX.Conexao.conexao()

        cursor = conexao.cursor(dictionary=True)

        sql = """SELECT comentario from tb_comentario where comentario = %s ORDER BY comentario DESC"""

        valores = (usuario, )

        cursor.execute(sql, valores)

        resultado = cursor.fetchone()
        conexao.close()

        return resultado