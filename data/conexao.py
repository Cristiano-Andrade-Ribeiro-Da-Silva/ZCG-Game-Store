import mysql.connector

class Conexao:

    # CONEXAO LOCAL (INTERNO)
    # def conexao():
    #     mydb = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="root",
    #     database="game_store"
    #     )
    #     return mydb
    
    # CONEXAO AINVEN (EXTERNO) VICTOR
    # def conexao():
    #     mydb = mysql.connector.connect(
    #     host="bd-zcgstore-bancodedados-zcgstore-v.c.aivencloud.com",
    #     port = "25525",
    #     user="avnadmin",
    #     password="AVNS_FTRFUcQTSYmqL1jKDDL",
    #     database="game_store"
    #     )
    #     return mydb
    
    #conexão aiven adrian
    def conexao():
        mydb = mysql.connector.connect(
            host="adrian-zcg-game-store-adrian-zcg-game-store-21.c.aivencloud.com",
            port="25781",
            user="avnadmin",
            password="AVNS_jgx-3UO-5H_xZRimX4d",
            database="game_store"
        )
        return mydb