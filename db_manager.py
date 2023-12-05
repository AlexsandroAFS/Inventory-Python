import mysql.connector
from mysql.connector import Error
from screen import mostrar_popup


class DBManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        self.connection = None
        self.connect()

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
            self.connection = None

    def get_descricao(self, codigo):
        """
        Busca a descrição de um item no banco de dados com base no código fornecido.
        """
        try:
            cursor = self.connection.cursor()
            query = "SELECT descricao FROM item WHERE iditem = %s"
            cursor.execute(query, (codigo,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            # mostrar_popup('Error',f"Erro ao buscar descrição: {e}")
            print(f"Erro ao buscar descrição: {e}")
            return None

    def get_reference(self, codigo):
        """
        Busca a referência de um item no banco de dados com base no código fornecido.
        """
        try:
            cursor = self.connection.cursor()
            query = "SELECT descricao FROM item WHERE iditem = %s"
            cursor.execute(query, (codigo,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            # mostrar_popup('Error',f"Erro ao buscar descrição: {e}")
            print(f"Erro ao buscar descrição: {e}")
            return None

    def get_localizacao(self, codigo):
        """
        Busca a descrição de um localizacao no banco de dados com base no código fornecido.
        """
        try:
            cursor = self.connection.cursor()
            query = "SELECT endereco FROM localizacao WHERE id = %s"
            cursor.execute(query, (codigo,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            print(f"Erro ao buscar localizacao: {e}")
            return None

    def close_connection(self):
        """ Fecha a conexão com o banco de dados. """
        if self.connection.is_connected():
            self.connection.close()
            print("Conexão com o MySQL foi encerrada")

    def add_inventory_item(self, contagem, usuario, endereco, codigo, quantidade):
        try:
            cursor = self.connection.cursor()
            query = """
               INSERT INTO inventario (contagem, usuario, endereco, codigo, quantidade)
               VALUES (%s, %s, %s, %s, %s)
               """
            cursor.execute(query, (contagem, usuario, endereco, codigo, quantidade))
            self.connection.commit()
        except Error as e:

            print(f"Erro ao adicionar item ao inventário: {e}")

    def contagem_existente(self, contagem, endereco):
        if self.connection is None or not self.connection.is_connected():
            print("Conexão com o banco de dados não está estabelecida.")
            return False
        """ Verifica se a combinação de contagem e endereço já existe. """
        try:
            cursor = self.connection.cursor()
            query = "SELECT COUNT(*) FROM inventario WHERE contagem = %s AND endereco = %s"
            cursor.execute(query, (contagem, endereco))
            (count,) = cursor.fetchone()
            return count > 0
        except Error as e:
            print(f"Erro ao verificar contagem existente: {e}")
            return False


