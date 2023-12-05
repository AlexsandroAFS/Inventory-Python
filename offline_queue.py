import json
import os


class OfflineQueue:
    def __init__(self, file_path='offline_queue.json'):
        self.file_path = file_path
        self.queue = self.load_queue()

    def load_queue(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    # Se o arquivo JSON estiver vazio ou for inválido, retorne uma lista vazia
                    return []
        else:
            # Se o arquivo não existir, retorne uma lista vazia
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
