from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen

class NarrativeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.922, 0.7647, 0.8078, 1)
            self.rect = Rectangle(size = self.size, pos = self.pos)

        self.bind(size = self.update_rect, pos = self.update_rect)

        self.text_lines = [
            "Many women face challenges in managing their finances independently due to various reasons.",
            "Lack of financial literacy, cultural expectations, and societal pressures contribute to this.",
            "However, it's important for women to empower themselves with knowledge about budgeting, saving, investing, and growing their wealth.",
            "This is where InvestHER comes in!",
            "Let the journey begin..."
        ]
        
        self.current_line = 0
        self.label = Label(text='', size_hint_y=None, height=200, font_size=18,color=[0, 0, 0, 1])
        self.label.text_size = (500, None)
        
        layout = BoxLayout(orientation='vertical')
        scroll_view = ScrollView(size_hint=(1, None), size=(800, 400))
        scroll_view.add_widget(self.label)
        layout.add_widget(scroll_view)

        self.continue_button = Button(text="Continue", size_hint=(None, None), size=(200, 50),background_normal="",background_color=[0.984, 0.984, 0.898, 1], color=[0, 0, 0, 1], pos_hint={'center_x': 0.5})
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
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_continue_pressed(self, instance):
        self.manager.current = 'start'



