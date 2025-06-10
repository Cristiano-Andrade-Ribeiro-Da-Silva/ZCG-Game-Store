from data import conexao as CX


class Mensagem:

    @staticmethod

    def cadastrar_mensagem(usuario, comentarios, cod_jogo):
        try:
            conexao = CX.Conexao.conexao()

            cursor = conexao.cursor()

            sql = """INSERT INTO tb_comentario (nome, comentario, cod_jogo) VALUES (%s, %s, %s)""" 
            
            valores = (usuario, comentarios, cod_jogo)
            cursor.execute(sql, valores)

            conexao.commit()

        except Exception as e:

            print("Erro ao inserir no banco:", e)
            
        finally:

            cursor.close()

            conexao.close()



    @staticmethod

    def mostra_mensagens(cod_jogo):

        conexao = CX.Conexao.conexao()

        cursor = conexao.cursor(dictionary=True)

        
        sql = """SELECT nome as usuario, comentario FROM tb_comentario WHERE cod_jogo = %s ORDER BY cod_comentario DESC"""
        
        cursor.execute(sql, (cod_jogo,))
        
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