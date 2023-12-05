from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivymd.uix.list import OneLineListItem, MDList
from kivy.metrics import dp


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
        self.layout = BoxLayout(size_hint=(1, 1),
                                height=dp(150),
                                orientation='vertical',
                                padding=(10, 10, 15, 15),
                                spacing=15)

        # Adiciona widgets à tela
        self.layout.add_widget(Label(text='Número da Contagem:'))
        self.contagem_input = TextInput(multiline=False)
        self.layout.add_widget(self.contagem_input)

        self.layout.add_widget(Label(text='Número do usuario:'))
        self.usuario_input = TextInput(multiline=False)
        self.layout.add_widget(self.usuario_input)

        self.add_widget(self.layout)
        # Adiciona um botão para salvar e ir para a tela de contagem
        self.save_button = Button(text='Salvar e Continuar')
        self.save_button.bind(on_press=self.salvar_e_continuar)
        self.layout.add_widget(self.save_button)

    def salvar_e_continuar(self, instance):
        # Salva os valores inseridos
        contagem = self.contagem_input.text
        usuario = self.usuario_input.text

        # Define os valores na tela de contagem
        contagem_screen = self.manager.get_screen('contagem')
        contagem_screen.set_usuario(contagem, usuario)

        # Muda para a tela de contagem
        self.manager.current = 'contagem'


class ContagemScreen(Screen):
    def __init__(self, db_manager, offline_queue, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(size_hint=(1, 1),
                                height=dp(150),
                                orientation='vertical',
                                padding=(10, 10, 15, 15),
                                spacing=15)

        # Label para mostrar a localização
        self.desc_loc_label = Label(text="*", font_size=dp(25), bold=True)
        self.layout.add_widget(self.desc_loc_label)

        # Adiciona widgets à tela
        self.layout.add_widget(Label(text='Endereço:'))
        self.endereco_input = TextInput(multiline=False)
        self.layout.add_widget(self.endereco_input)

        # Label para mostrar a descrição
        self.descricao_label = Label(text="*", font_size=dp(25), bold=True)
        self.layout.add_widget(self.descricao_label)

        # Campo
        self.layout.add_widget(Label(text='Código:'))
        self.codigo_input = TextInput(multiline=False, )
        self.layout.add_widget(self.codigo_input)

        # Ligando o evento de texto modificado no campo de código
        self.codigo_input.bind(text=self.on_codigo_text)
        self.endereco_input.bind(text=self.on_locate_text)

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
        self.usuario = None

    def resetar_campos(self):
        # Limpa os campos de entrada
        self.endereco_input.text = ''
        self.codigo_input.text = ''
        self.quantidade_input.text = ''

    def on_codigo_text(self, instance, value):
        # Busca a descrição quando o texto do código é modificado
        try:
            descricao = self.db_manager.get_descricao(value)
            self.descricao_label.text = descricao if descricao else "Descrição do Item: Não encontrado"
        except BaseException as e:
            print(e)
            pass

    def on_locate_text(self, instance, value):
        # Busca a descrição quando o código da localização é inserido
        try:
            localizacao = self.db_manager.get_localizacao(value)
            self.desc_loc_label.text = localizacao if localizacao else "Localização Não Encontrada"
        except BaseException as e:
            print(e)
            pass

    def set_usuario(self, contagem, usuario):
        self.contagem = contagem
        self.usuario = usuario

    def enviar_dados(self, instance):
        # Coleta dados dos inputs
        endereco = self.endereco_input.text
        codigo = self.codigo_input.text
        quantidade = self.quantidade_input.text

        # Validação dos campos
        if not self.contagem:
            mostrar_popup("Número da Contagem Invalida", "Número da Contagem Não Pode Estar Vazio.")
            return
        if not self.usuario:
            mostrar_popup("Sem Usuário", "Por Favor forneça Número de Usuário")
            return
        if not endereco:
            mostrar_popup("Sem Localização", "O item deve conter um piking para ser contado.")
            return
        if not quantidade:
            mostrar_popup("Sem Quantidade", "Insira uma quantidade valida.")
            return
        if not codigo:
            mostrar_popup("Sem Item Selecionado", "Insira um SKU valida.")
            return

        # Verifica se a contagem já existe
        if self.db_manager.contagem_existente(self.contagem, endereco):
            mostrar_popup("Erro", "Erro: Contagem já realizada para este endereço.")
            self.resetar_campos()
            return

        # Tentativa de adicionar item ao banco de dados ou salvar na fila offline
        try:
            if self.db_manager.connection and self.db_manager.connection.is_connected():
                self.db_manager.add_inventory_item(self.contagem, self.usuario, endereco, codigo, quantidade)
                mostrar_popup("Sucesso", "Dados enviados com sucesso.")
            else:
                raise Exception("Offline")
        except Exception as e:
            # Tratamento de erros e salvar na fila offline
            data = {'action': 'add',
                    'item_data': {'contagem': self.contagem,
                                  'usuario': self.usuario,
                                  'endereco': endereco,
                                  'codigo': codigo,
                                  'quantidade': quantidade}}
            self.offline_queue.add_to_queue(data)
            mostrar_popup("Informação", "Sem conexão. Dados salvos offline.")

        self.resetar_campos()


class FilaItem(RecycleDataViewBehavior, BoxLayout):
    """ Representa um item individual na lista de fila. """
    texto = StringProperty("")


class MonitorFilaScreen(Screen):
    def __init__(self, db_manager, offline_queue, **kwargs):
        super().__init__(**kwargs)
        self.db_manager = db_manager
        self.offline_queue = offline_queue
        self.layout = BoxLayout(size_hint=(1, None),
                                height=dp(150),
                                orientation='vertical',
                                padding=(10, 10, 15, 15),
                                spacing=15)

        self.add_widget(self.layout)

        # Usar MDList dentro de um ScrollView
        self.lista_fila = ScrollView()
        self.md_list = MDList()
        self.lista_fila.add_widget(self.md_list)
        self.layout.add_widget(self.lista_fila)

        self.atualizar_lista_fila()

        btn_processar_fila = Button(text='Processar Fila', size=(10, 10))
        btn_processar_fila.bind(on_press=self.processar_fila)
        self.layout.add_widget(btn_processar_fila)

    def atualizar_lista_fila(self):
        # Limpa a lista existente
        self.md_list.clear_widgets()

        # Adiciona itens à lista
        for item in self.offline_queue.load_queue():
            line_item = OneLineListItem(text=str(item))
            self.md_list.add_widget(line_item)

    def processar_fila(self, instance):
        if (not App.get_running_app().esta_online()
                or not self.db_manager.connection
                or not self.db_manager.connection.is_connected()):
            mostrar_popup("Erro", "Não há conexão com o banco de dados.")
            return

        itens_removidos = []
        for item in self.offline_queue.queue[:]:  # Faz uma cópia da fila para iterar
            contagem = item['item_data']['contagem']
            endereco = item['item_data']['endereco']

            if self.db_manager.contagem_existente(contagem, endereco):
                mostrar_popup("Aviso", f"Contagem {contagem} no endereço {endereco} já existe no banco de dados.")
                itens_removidos.append(item)
            else:
                try:
                    self.db_manager.add_inventory_item(**item['item_data'])
                    mostrar_popup("Sucesso",
                                  f"Item {item['item_data']['codigo']} adicionado ao inventário com sucesso.")
                    itens_removidos.append(item)
                except Exception as e:
                    mostrar_popup("Erro", f"Erro ao adicionar item ao banco de dados: {e}")

        # Remover itens processados ou já existentes da fila
        for item in itens_removidos:
            self.offline_queue.queue.remove(item)

        # Após o processamento, atualize a lista e salve a fila
        self.atualizar_lista_fila()
        self.offline_queue.save_queue()


# Gerenciador de Telas
class ScreenManagement(ScreenManager):
    def __init__(self, db_manager, offline_queue, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.add_widget(UsuarioScreen(name='usuario'))
        self.add_widget(ContagemScreen(name='contagem', db_manager=db_manager, offline_queue=offline_queue))
        self.add_widget(MonitorFilaScreen(name='monitorFila', db_manager=db_manager, offline_queue=offline_queue))
