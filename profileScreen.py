from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=50)

        self.profile_label = Label(text="Profile: ", font_size=24)
        self.money_label = Label(text="Amount: ", font_size=20)
        self.job_label = Label(text="Job: ", font_size=20) 
        self.confidence_label = Label(text="Confidence: ", font_size=20)

        # need to connect to next page- actual game
        cont_button = Button(text="Continue", size_hint=(None, None), size=(200, 50))
        

        self.layout.add_widget(self.profile_label)
        self.layout.add_widget(self.money_label)
        self.layout.add_widget(self.job_label)
        self.layout.add_widget(self.confidence_label)
        self.layout.add_widget(cont_button)

        self.add_widget(self.layout)

    def update_profile(self, name, amount, job, confidence):
        """Update displayed profile details"""
        self.profile_label.text = f"Profile: {name}"
        self.money_label.text = f"Amount: {amount}"
        self.job_label.text = f"Job: {job}" 
        self.confidence_label.text = f"Confidence: {confidence}" 

