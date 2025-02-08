from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        self.label = Label(text='Where would you like to start?', size_hint_y=None, height=200, font_size=18)
        layout.add_widget(self.label)

        buttons = [
            ("High School", "username", "$500", "Allowance- $20", "50"),
            ("College", "username", "$1000", "Subway- $15/hr", "50"),
            ("Job", "username", "$100,000", "Software Engineer at Canva", "50")
        ]

        for text, profile, amount, job, confidence in buttons:
            btn = Button(text=text, size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5})
            btn.bind(on_press=lambda instance, p=profile, a=amount, j=job, c=confidence: self.go_to_profile(p, a, j, c))
            layout.add_widget(btn)

        self.add_widget(layout)

    def go_to_profile(self, profile, amount, job, confidence):
        """Pass data to ProfileScreen and navigate"""
        profile_screen = self.manager.get_screen('profile')
        profile_screen.update_profile(profile, amount, job, confidence)
        self.manager.current = 'profile'
