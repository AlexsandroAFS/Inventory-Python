from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemanddock')
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog



from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivymd.uix.list import OneLineListItem, MDList
from kivy.metrics import dp
from kivymd.uix.textfield import MDTextField


# Label Auto Ajuste
class MyLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = dp(20)
        self.bold = True
        self.halign = 'center'  # Alinhamento horizontal
        self.valign = 'middle'  # Alinhamento vertical
        self.bind(size=self.update_text_size)
        self.size_hint = (1, None)  # Ajustar para largura total e altura mínima necessária


    def update_text_size(self, *args):
        self.text_size = (self.width, None)


# Tela de Contagem
def mostrar_popup(motivo, mensagem):
    """ Exibe um pop-up estilizado com uma mensagem. """

    # Botão para fechar o popup
    fechar_button = MDFlatButton(text='Fechar', on_release=lambda x: dialog.dismiss())

    # Cria o MDDialog
    dialog = MDDialog(
        title=motivo,
        text=mensagem,
        size_hint=(0.8, None),
        height=dp(100),  # Altura do popup
        buttons=[fechar_button]
    )

    # Abre o popup
    dialog.open()


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
        # Adiciona Label
        self.layout.add_widget(Label(text='Número da Contagem:'))

        # Adiciona MDTextField
        self.contagem_input = MDTextField(multiline=False,
                                          hint_text='Contagem Atual do Inventario',
                                          input_type='null',
                                          mode='rectangle',
                                          )

        self.layout.add_widget(self.contagem_input)

        self.layout.add_widget(Label(text='Número do usuario:'))
        self.usuario_input = MDTextField(multiline=False,
                                         hint_text='Código Atribuído ao Contador',
                                         input_type='null',
                                         mode='rectangle',
                                         )
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


# Tela de Contagem
class ContagemScreen(Screen):
    def __init__(self, db_manager, offline_queue, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(size_hint=(1, 1),
                                height=dp(150),
                                orientation='vertical',
                                padding=(10, 10, 15, 15),
                                spacing=15)

        # Label para mostrar a localização
        self.desc_loc_label = Label(text="Localização", font_size=dp(25), bold=True)
        self.layout.add_widget(self.desc_loc_label)

        # Adiciona widgets à tela
        self.endereco_input = MDTextField(multiline=False,
                                          hint_text='Localização',
                                          input_type='null',
                                          mode='rectangle',
                                          )
        self.layout.add_widget(self.endereco_input)

        # Label para mostrar a descrição
        # Usar size_hint_x=None e text_size para controlar a largura do texto
        self.descricao_label = MyLabel(text="Descrição do Produto")
        # Atualizar text_size quando o tamanho do Label muda
        self.descricao_label.bind(
            size=self.descricao_label.setter('text_size'))
        self.layout.add_widget(self.descricao_label)

        # Label para mostrar a descrição
        self.reference_label = Label(text="Referencia", font_size=dp(15), bold=False)
        self.layout.add_widget(self.reference_label)

        # Campo
        # self.layout.add_widget(Label(text='Código:'))
        self.codigo_input = MDTextField(multiline=False,
                                        hint_text='Código do SKU',
                                        input_type='null',
                                        mode='rectangle',
                                        )
        self.layout.add_widget(self.codigo_input)

        # Ligando o evento de texto modificado no campo de código
        self.codigo_input.bind(text=self.on_codigo_text)
        self.codigo_input.bind(text=self.on_reference_text)
        self.endereco_input.bind(text=self.on_locate_text)

        # self.layout.add_widget(Label(text='Quantidade:'))
        self.quantidade_input = MDTextField(multiline=False,
                                            hint_text='Quantidade',
                                            input_type='null',
                                            mode='rectangle',
                                            )
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

    def on_reference_text(self, instance, value):
        # Busca a descrição quando o texto do código é modificado
        try:
            reference = self.db_manager.get_reference(value)
            self.reference_label.text = reference if reference else "Referencia: Não encontrado"
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
            if self.db_manager.connection:
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


# Tela Dos Itens Contados Offline
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
                or not self.db_manager.connection):
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
