from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import socket


# Tela de Parametrização de Contagem
class ParametrizacaoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

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
        contagem_screen.set_parametrizacao(contagem, operador)

        # Muda para a tela de contagem
        self.manager.current = 'contagem'

# Tela de Contagem
class ContagemScreen(Screen):
    def __init__(self, db_manager, offline_queue, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        # Adiciona widgets à tela
        self.layout.add_widget(Label(text='Endereço:'))
        self.endereco_input = TextInput(multiline=False)
        self.layout.add_widget(self.endereco_input)

        self.layout.add_widget(Label(text='Código:'))
        self.codigo_input = TextInput(multiline=False)
        self.layout.add_widget(self.codigo_input)

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

    def set_parametrizacao(self, contagem, operador):
        self.contagem = contagem
        self.operador = operador

    def enviar_dados(self, instance):
        # Coleta dados dos inputs
        endereco = self.endereco_input.text
        codigo = self.codigo_input.text
        quantidade = self.quantidade_input.text

        # Utiliza self.contagem e self.operador
        if self.esta_online():
            self.db_manager.add_inventory_item(self.contagem, self.operador, endereco, codigo, quantidade)
        else:
            data = {'action': 'add', 'item_data': {'contagem': self.contagem, 'operador': self.operador, 'endereco': endereco, 'codigo': codigo, 'quantidade': quantidade}}
            self.offline_queue.add_to_queue(data)

    def esta_online(self):
        """
        Verifica se o dispositivo está conectado à internet tentando abrir um socket
        para um host comum (por exemplo, Google) na porta 80.
        """
        try:
            # Tenta estabelecer um socket com um host comum (google.com)
            # na porta 80, que é a porta padrão para o protocolo HTTP.
            host = socket.gethostbyname("www.google.com")
            s = socket.create_connection((host, 80), 2)
            s.close()
            return True
        except:
            pass
        return False


# Gerenciador de Telas
class ScreenManagement(ScreenManager):
    def __init__(self, db_manager, offline_queue, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.add_widget(ParametrizacaoScreen(name='parametrizacao'))
        self.add_widget(ContagemScreen(name='contagem', db_manager=db_manager, offline_queue=offline_queue))
