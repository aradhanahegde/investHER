from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

class loginpage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    pass

class loginPageApp(App):
    def build(self):
        return loginpage()

if __name__ == '__main__':
    loginPageApp().run()