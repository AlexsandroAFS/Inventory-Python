from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import socket


# Tela de Contagem
def mostrar_popup(motivo, mensagem):
    """ Exibe um pop-up com uma mensagem de erro. """
    popup = Popup(title=motivo,
                  content=Label(text=mensagem),
                  size_hint=(None, None),
                  size=(400, 100))
    popup.open()


# Tela de Parametrização de Contagem
class UsuarioScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=(10, 10, 15, 15), spacing=15)

        # Adiciona widgets à tela
        self.layout.add_widget(Label(text='Número da Contagem:'))
        self.contagem_input = TextInput(multiline=False)
        self.layout.add_widget(self.contagem_input)

        self.layout.add_widget(Label(text='Número do Operador:'))
        self.operador_input = TextInput(multiline=False)
        self.layout.add_widget(self.operador_input)

        self.add_widget(self.layout)
        # Adiciona um botão para salvar e ir para a tela de contagem
        self.save_button = Button(text='Salvar e Continuar')
        self.save_button.bind(on_press=self.salvar_e_continuar)
        self.layout.add_widget(self.save_button)

    def salvar_e_continuar(self, instance):
        # Salva os valores inseridos
        contagem = self.contagem_input.text
        operador = self.operador_input.text

        # Define os valores na tela de contagem
        contagem_screen = self.manager.get_screen('contagem')
        contagem_screen.set_usuario(contagem, operador)

        # Muda para a tela de contagem
        self.manager.current = 'contagem'


class ContagemScreen(Screen):
    def __init__(self, db_manager, offline_queue, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical',
                                padding=(10, 10, 15, 15),
                                spacing=15,
                                )
        # Label para mostrar a localização
        self.desc_loc_label = Label(text="Vaga: ")
        self.layout.add_widget(self.desc_loc_label)

        # Adiciona widgets à tela
        self.layout.add_widget(Label(text='Endereço:'))
        self.endereco_input = TextInput(multiline=False)
        self.layout.add_widget(self.endereco_input)

        # Label para mostrar a descrição
        self.descricao_label = Label(text="Descrição:")
        self.layout.add_widget(self.descricao_label)

        # Campo
        self.layout.add_widget(Label(text='Código:'))
        self.codigo_input = TextInput(multiline=False, )
        self.layout.add_widget(self.codigo_input)

        # Ligando o evento de texto modificado no campo de código
        self.codigo_input.bind(text=self.on_codigo_text)

        self.layout.add_widget(Label(text='Quantidade:'))
        self.quantidade_input = TextInput(multiline=False)
        self.layout.add_widget(self.quantidade_input)

        # Botão para enviar dados
        self.submit_button = Button(text='Enviar')
        self.submit_button.bind(on_press=self.enviar_dados)
        self.layout.add_widget(self.submit_button)

        # Referências ao DBManager e OfflineQueue
        self.db_manager = db_manager
        self.offline_queue = offline_queue

        self.add_widget(self.layout)

        self.contagem = None
        self.operador = None

    def resetar_campos(self):
        # Limpa os campos de entrada
        self.endereco_input.text = ''
        self.codigo_input.text = ''
        self.quantidade_input.text = ''

    def on_codigo_text(self, instance, value):
        # Busca a descrição quando o texto do código é modificado
        try:
            descricao = self.db_manager.get_descricao(value)
            self.descricao_label.text = f"Descrição do Item: {descricao}" if descricao else "Descrição do Item: Não encontrado"
        except BaseException as e:
            print(e)
            pass

    def on_locate_text(self, instance, value):
        # Busca a descrição quando o código da localização é inserido
        localizacao = self.db_manager.get_localizacao(value)
        self.desc_loc_label.text = f"Descrição do Local: {localizacao}" if localizacao else "Descrição do Local: Não encontrado"

    def set_usuario(self, contagem, operador):
        self.contagem = contagem
        self.operador = operador

    def enviar_dados(self, instance):
        # Coleta dados dos inputs
        endereco = self.endereco_input.text
        codigo = self.codigo_input.text
        quantidade = self.quantidade_input.text

        # Validação dos campos
        if not self.contagem:
            mostrar_popup("Erro", "Número da contagem não pode ser vazio.")
            return

        if not endereco or not codigo or not quantidade:
            mostrar_popup("Erro", "Todos os campos devem ser preenchidos.")
            return

        # Verifica se a contagem já existe
        if self.db_manager.contagem_existente(self.contagem, endereco):
            mostrar_popup("Erro", "Erro: Contagem já realizada para este endereço.")
            self.resetar_campos()
            return

        # Tentativa de adicionar item ao banco de dados ou salvar na fila offline
        try:
            if self.esta_online() and self.db_manager.connection and self.db_manager.connection.is_connected():
                self.db_manager.add_inventory_item(self.contagem, self.operador, endereco, codigo, quantidade)
                mostrar_popup("Sucesso", "Dados enviados com sucesso.")
            else:
                raise Exception("Offline")
        except Exception as e:
            # Tratamento de erros e salvar na fila offline
            data = {'action': 'add',
                    'item_data': {'contagem': self.contagem,
                                  'operador': self.operador,
                                  'endereco': endereco,
                                  'codigo': codigo,
                                  'quantidade': quantidade}}
            self.offline_queue.add_to_queue(data)
            mostrar_popup("Informação", "Sem conexão. Dados salvos offline.")

        self.resetar_campos()

    def esta_online(self):
        """
        Verifica se o dispositivo está conectado à internet tentando abrir um socket
        para um host comum (por exemplo, Google) na porta 80.
        """
        try:
            # Tenta estabelecer um socket com um host comum (google.com)
            # na porta 80, que é a porta padrão para o protocolo HTTP.
            host = socket.gethostbyname("www.google.comxbr")
            s = socket.create_connection((host, 80), 2)
            s.close()
            return True
        except BaseException as e:
            mostrar_popup(f"Online Error", e)
        return False


class MonitorFilaScreen(Screen):
    def __init__(self, offline_queue, **kwargs):
        super().__init__(**kwargs)
        self.offline_queue = offline_queue

        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        self.lista_fila = RecycleView()
        self.layout.add_widget(self.lista_fila)

        self.atualizar_lista_fila()

        btn_processar_fila = Button(text='Processar Fila')
        btn_processar_fila.bind(on_press=self.processar_fila)
        self.layout.add_widget(btn_processar_fila)

    def atualizar_lista_fila(self):
        # Atualiza a lista com os itens da fila offline
        self.lista_fila.data = [{'text': str(item)} for item in self.offline_queue.queue]

    def processar_fila(self, instance):
        # Implemente a lógica para processar a fila
        pass


# Gerenciador de Telas
class ScreenManagement(ScreenManager):
    def __init__(self, db_manager, offline_queue, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.add_widget(UsuarioScreen(name='usuario'))
        self.add_widget(ContagemScreen(name='contagem', db_manager=db_manager, offline_queue=offline_queue))
        self.add_widget(MonitorFilaScreen(name='monitorFila', offline_queue=offline_queue))
