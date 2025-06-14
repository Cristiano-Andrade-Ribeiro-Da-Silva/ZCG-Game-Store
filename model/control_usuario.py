from data import conexao as CX
from hashlib import sha256
from flask import session, flash

class Usuario:

    @staticmethod
    def controle_cadastra_usuario(nome, email, senha, telefone):
        try:

            #CRIPTOGRAFAR SENHA
            senha_criptografada = sha256(senha.encode()).hexdigest()


            # ABRINDO CONEXÃO
            conexao = CX.Conexao.conexao()
            if conexao is None:
                flash("Erro! Talvez a conexão com o banco de dados tenha falhado. Atualize a página e tente novamente")
                return False

            mycursor = conexao.cursor()


            # COMANDO DO SQL

            sql = """ INSERT INTO tb_usuario (nome, email, senha, num_telefone) VALUES (%s, %s, %s, %s)"""

            valores = (nome, email, senha_criptografada, telefone)
            
            mycursor.execute(sql, valores)
            conexao.commit()

            flash("Você completou seu cadstro com êxito!")
            return True
        
        finally:
            try:
                if mycursor:
                    mycursor.close()
                if conexao:
                    conexao.close()
            except:
                pass


    @staticmethod
    def controle_login_usuario(email, senha):
        
        senha_criptografada = sha256(senha.encode()).hexdigest()


        conexao = CX.Conexao.conexao()
        cursor = conexao.cursor(dictionary = True)

        sql  = """SELECT email, nome FROM tb_usuario WHERE  email = %s and binary senha = %s"""

        valores = (email, senha_criptografada)
        cursor.execute(sql, valores)
        resultado = cursor.fetchone()

        cursor.close()
        conexao.close()

        if resultado:
            session['Usuario'] = resultado['email']
            session['nome_usuario'] = resultado['nome']
            return True
        else:
            return False
        

    def logoff():
        session.clear()

