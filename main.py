import socket
from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem, MDList
from kivymd.uix.toolbar import MDTopAppBar

from db_manager import DBManager
from offline_queue import OfflineQueue
from screen import ScreenManagement


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.material_style = "M2"

        # Inicializa o gerenciador do banco de dados e a fila offline
        self.db_manager = DBManager(host='172.25.0.73',
                                    user='inventarioUS',
                                    password='PnakW}q60MY7',
                                    database='inventarioDB')
        self.db_manager.connect()
        self.offline_queue = OfflineQueue()

        # Screen Manager
        self.screen_manager = ScreenManagement(db_manager=self.db_manager, offline_queue=self.offline_queue)

        # Navigation Drawer com MDList
        self.nav_drawer = MDNavigationDrawer()
        self.nav_drawer.anchor = 'left'
        drawer_list = MDList()
        for item_name in ["Configuração", "Contagem", "Monitorar Fila"]:
            item = OneLineListItem(text=item_name)
            item.bind(on_release=lambda x, name=item_name: self.nav_drawer_item_selected(name))
            drawer_list.add_widget(item)
        self.nav_drawer.add_widget(drawer_list)

        # Main Layout
        self.main_layout = MDBoxLayout(orientation='vertical')

        # Top AppBar
        self.top_app_bar = MDTopAppBar(title="Inventario",orientation="vertical")
        self.top_app_bar.left_action_items = [['menu', lambda x: self.nav_drawer.set_state("open")]]
        # self.top_app_bar.elevation = 10
        self.main_layout.add_widget(self.top_app_bar)

        # Navigation Layout
        self.nav_layout = MDNavigationLayout()
        self.nav_layout.add_widget(self.screen_manager)
        self.nav_layout.add_widget(self.nav_drawer)
        self.main_layout.add_widget(self.nav_layout)

        return self.main_layout

    def nav_drawer_item_selected(self, item_name):
        # Troca a tela com base no item selecionado
        if item_name == "Configuração":
            self.screen_manager.current = 'usuario'
        elif item_name == "Contagem":
            self.screen_manager.current = 'contagem'
        elif item_name == "Monitorar Fila":
            self.screen_manager.current = 'monitorFila'
        self.nav_drawer.set_state("close")

    def esta_online(self):
        try:
            host = socket.gethostbyname("www.google.com")
            s = socket.create_connection((host, 80), 2)
            s.close()
            return True
        except:
            return False

if __name__ == '__main__':
    MainApp().run()
