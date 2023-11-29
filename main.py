from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from kivymd.app import MDApp

from screen import ScreenManagement, mostrar_popup
from db_manager import DBManager
from offline_queue import OfflineQueue
import socket


class MainApp(MDApp):

    def esta_online(self):
        try:
            # Tenta estabelecer uma conexão com um servidor conhecido
            host = socket.gethostbyname("www.google.com")
            s = socket.create_connection((host, 80), 2)
            s.close()
            return True
        except:
            return False

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        # Inicializa o gerenciador do banco de dados e a fila offline
        self.root = BoxLayout(orientation='vertical')
        self.db_manager = DBManager(host='172.25.0.73', user='inventarioUS', password='PnakW}q60MY7',
                                    database='inventarioDB')
        self.db_manager.connect()
        self.offline_queue = OfflineQueue()

        # Navbar
        navbar = BoxLayout(size_hint_y=None, height=50,  padding=(10, 10, 5, 5))
        btn_param = Button(text='Configuração')
        btn_contagem = Button(text='Contagem')

        btn_param.bind(on_press=lambda x: self.mudar_tela('usuario'))
        btn_contagem.bind(on_press=lambda x: self.mudar_tela('contagem'))

        btn_monitor_fila = Button(text='Monitorar Fila')
        btn_monitor_fila.bind(on_press=lambda x: self.mudar_tela('monitorFila'))

        navbar.add_widget(btn_param)
        navbar.add_widget(btn_contagem)
        navbar.add_widget(btn_monitor_fila)

        self.root.add_widget(navbar)

        # Screen Manager
        self.screen_manager = ScreenManagement(db_manager=self.db_manager, offline_queue=self.offline_queue)
        self.root.add_widget(self.screen_manager)

        return self.root

    def mudar_tela(self, nome_tela):
        self.screen_manager.current = nome_tela


if __name__ == '__main__':
    MainApp().run()
