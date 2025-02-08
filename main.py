from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from startScreen import StartScreen
from profileScreen import ProfileScreen
from narrative import NarrativeScreen  

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(NarrativeScreen(name='narrative'))
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(ProfileScreen(name='profile'))

        return sm

if __name__ == '__main__':
    MyApp().run()
