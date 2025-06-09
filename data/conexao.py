import mysql.connector

class Conexao:

    # CONEXAO LOCAL (INTERNO)
    def conexao():
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="game_store"
        )
        return mydb
    
    # CONEXAO AINVEN (EXTERNO)
    # def conexao():
    #     mydb = mysql.connector.connect(
    #     host="bd-zcgstore-bancodedados-zcgstore-v.c.aivencloud.com",
    #     port = "25525",
    #     user="avnadmin",
    #     password="AVNS_FTRFUcQTSYmqL1jKDDL",
    #     database="game_store"
    #     )
    #     return mydb