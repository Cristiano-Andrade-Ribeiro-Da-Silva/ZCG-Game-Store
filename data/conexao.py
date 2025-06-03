import mysql.connector

class Conexao:
    def conexao():
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="game_store"
        )
        return mydb