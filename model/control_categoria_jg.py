from data.conexao import Conexao

# model/control.py

from data.conexao import Conexao

def pega_jogos_por_categoria(cod_categoria):
    conexao = Conexao.conexao()
    cursor = conexao.cursor(dictionary=True)

    try:
        query = """
        SELECT j.*, f.url, c.categoria 
        FROM tb_jogo j
        INNER JOIN foto_produtos f ON j.cod_jogo = f.cod_jogos
        INNER JOIN tb_categoria c ON j.cod_categoria = c.cod_categoria
        WHERE j.cod_categoria = %s
        """
        cursor.execute(query, (cod_categoria,))
        return cursor.fetchall()
    except Exception as e:
        print(f"[ERRO] ao buscar jogos por categoria: {e}")
        return []
    finally:
        cursor.close()
        conexao.close()



def listar_categorias():
    conexao = Conexao.conexao()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM tb_categoria")
        categorias = cursor.fetchall()
        return categorias
    except Exception as e:
        print(f"[ERRO] Falha ao buscar categorias: {e}")
        return []
    finally:
        cursor.close()
        conexao.close()
