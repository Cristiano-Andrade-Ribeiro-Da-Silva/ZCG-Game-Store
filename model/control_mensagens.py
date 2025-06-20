from data import conexao as CX


class Mensagem:

    @staticmethod

    def cadastrar_mensagem(cod_usuario, comentario, cod_jogo):
        try:
            conexao = CX.Conexao.conexao()
            cursor = conexao.cursor()
            sql = """
                INSERT INTO tb_comentario (cod_usuario, comentario, cod_jogo)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (cod_usuario, comentario, cod_jogo))
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

        sql = """
        SELECT 
            c.comentario,
            IFNULL(u.nome, 'Anônimo') AS nome,
            IFNULL(u.foto_perfil, 'default.png') AS foto_perfil
        FROM tb_comentario c
        LEFT JOIN tb_usuario u ON c.cod_usuario = u.cod_usuario
        WHERE c.cod_jogo = %s
        ORDER BY c.cod_comentario DESC
        """

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