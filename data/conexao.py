import mysql.connector

class Conexao:
    def conexao():
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Victor@!2020",
        database="game_store"
        )
        return mydb