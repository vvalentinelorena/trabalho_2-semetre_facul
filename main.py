from kivymd.app import MDApp
from controller import Controller

class MainApp(MDApp):
    def build(self):
        self.controller = Controller()
        self.theme_cls.theme_style = "Dark"          
        self.theme_cls.primary_palette = "Pink"   

        return self.controller.view.get_root_widget()

if __name__ == "__main__":
    MainApp().run()

