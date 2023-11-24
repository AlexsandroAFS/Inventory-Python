import mysql.connector
from mysql.connector import Error

class DBManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """ Estabelece conexão com o banco de dados MySQL. """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Conexão ao MySQL foi estabelecida")
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")

    def get_descricao(self, codigo):
        """
        Busca a descrição de um item no banco de dados com base no código fornecido.
        """
        try:
            cursor = self.connection.cursor()
            query = "SELECT descricao FROM estoque WHERE codigo = %s"
            cursor.execute(query, (codigo,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            print(f"Erro ao buscar descrição: {e}")
            return None

    def close_connection(self):
        """ Fecha a conexão com o banco de dados. """
        if self.connection.is_connected():
            self.connection.close()
            print("Conexão com o MySQL foi encerrada")

    def add_inventory_item(self, contagem, parametrizacao, endereco, codigo, quantidade):
        try:
            cursor = self.connection.cursor()
            query = """
               INSERT INTO tabela_inventario (contagem, parametrizacao, endereco, codigo, quantidade)
               VALUES (%s, %s, %s, %s, %s)
               """
            cursor.execute(query, (contagem, parametrizacao, endereco, codigo, quantidade))
            self.connection.commit()
        except Error as e:
            print(f"Erro ao adicionar item ao inventário: {e}")