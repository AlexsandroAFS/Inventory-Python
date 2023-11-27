from kivy.app import App
from screen import ScreenManagement
from db_manager import DBManager
from offline_queue import OfflineQueue

class MainApp(App):
    def build(self):
        # Inicializa o gerenciador do banco de dados e a fila offline
        self.db_manager = DBManager(host='172.25.0.73', user='inventarioUS', password='PnakW}q60MY7', database='inventarioDB')
        self.db_manager.connect()

        self.offline_queue = OfflineQueue()

        # Passa db_manager e offline_queue para ScreenManagement
        return ScreenManagement(db_manager=self.db_manager, offline_queue=self.offline_queue)

if __name__ == '__main__':
    MainApp().run()
