import json
import os


class OfflineQueue:
    def __init__(self, file_path='offline_queue.json'):
        self.file_path = file_path
        self.queue = self.load_queue()

    def load_queue(self):
        """ Carrega a fila a partir de um arquivo JSON. """
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return json.load(file)
        return []

    def add_to_queue(self, data):
        """
        Adiciona um item à fila. 'data' deve ser um dicionário contendo as informações
        necessárias para sincronização posterior.
        """
        self.queue.append(data)
        self.save_queue()

    def save_queue(self):
        """ Salva a fila atual no arquivo JSON. """
        with open(self.file_path, 'w') as file:
            json.dump(self.queue, file)

    # Em offline_queue.py
    def process_queue(self, db_manager):
        for data in self.queue:
            action = data.get('action')
            item_data = data.get('item_data')

            if action == 'add':
                # Desempacotar os dados do item
                contagem = item_data.get('contagem')
                usuario = item_data.get('usuario')
                endereco = item_data.get('endereco')
                codigo = item_data.get('codigo')
                quantidade = item_data.get('quantidade')

                # Adicionar o item ao banco de dados
                db_manager.add_inventory_item(contagem, usuario, endereco, codigo, quantidade)

        # Limpar a fila após o processamento
        self.queue = []
        self.save_queue()
