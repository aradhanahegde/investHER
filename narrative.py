from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen

class NarrativeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.text_lines = [
            "Many women face challenges in managing their finances independently due to various reasons.",
            "Lack of financial literacy, cultural expectations, and societal pressures contribute to this.",
            "However, it's important for women to empower themselves with knowledge about budgeting, saving, investing, and growing their wealth.",
            "This is where InvestHER comes in!",
            "Let the journey begin..."
        ]
        
        self.current_line = 0
        self.label = Label(text='', size_hint_y=None, height=200, font_size=18)
        self.label.text_size = (500, None)
        
        layout = BoxLayout(orientation='vertical')
        scroll_view = ScrollView(size_hint=(1, None), size=(800, 400))
        scroll_view.add_widget(self.label)
        layout.add_widget(scroll_view)

        self.continue_button = Button(text="Continue", size_hint=(None, None), size=(200, 50), pos_hint={'right': 1, 'top': 1})
        self.continue_button.opacity = 0  
        self.continue_button.bind(on_press=self.on_continue_pressed)
        layout.add_widget(self.continue_button)

        self.add_widget(layout)
        Clock.schedule_once(self.update_text, 1)

    def update_text(self, dt):
        if self.current_line < len(self.text_lines):
            if self.label.text:
                self.label.text += '\n' + self.text_lines[self.current_line]
            else:
                self.label.text = self.text_lines[self.current_line]
            
            self.current_line += 1
            
            Clock.schedule_once(self.update_text, 3)
        else:
            self.continue_button.opacity = 1

    def on_continue_pressed(self, instance):
        self.manager.current = 'start'

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.label = Label(text='Where would you like to start?', size_hint_y=None, height=200, font_size=18)
        highschool_button = Button(text="High School", size_hint=(None, None), size=(200, 50), pos_hint={'center:x': 0.5, 'center_y': 0.5})
        college_button = Button(text="College", size_hint=(None, None), size=(200, 50), pos_hint={'center:x': 0.5, 'center_y': 0.5})
        job_button = Button(text="Job", size_hint=(None, None), size=(200, 50), pos_hint={'center:x': 0.5, 'center_y': 0.5})
        layout.add_widget(self.label)
        layout.add_widget(highschool_button)
        layout.add_widget(college_button), 
        layout.add_widget(job_button)
        self.add_widget(layout)

class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        
        self.narrative_screen = NarrativeScreen(name='narrative')
        self.start_screen = StartScreen(name='start')

        self.screen_manager.add_widget(self.narrative_screen)
        self.screen_manager.add_widget(self.start_screen)

        return self.screen_manager

            
if __name__ == '__main__':
    MyApp().run()

