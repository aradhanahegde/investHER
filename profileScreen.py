from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set background color using Canvas
        with self.canvas.before:
            Color(0.922, 0.761, 0.806, 1)  # RGB for EBC3CE
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=50)

        # Set the text color to black
        self.profile_label = Label(text="Profile: ", font_size=24, color=(0, 0, 0, 1))
        self.money_label = Label(text="Amount: ", font_size=20, color=(0, 0, 0, 1))
        self.job_label = Label(text="Job: ", font_size=20, color=(0, 0, 0, 1))
        self.confidence_label = Label(text="Confidence: ", font_size=20, color=(0, 0, 0, 1))

        # Create the continue button
        cont_button = Button(text="Continue", size_hint=(None, None), size=(200, 50),
                              background_normal='', background_color=(0.988, 0.992, 0.898, 1),
                              color=(0, 0, 0, 1))  # Set button text to black

        # Center the button horizontally, keep it positioned at the bottom of the screen
        cont_button.pos_hint = {'center_x': 0.5, 'y': 0.1}

        cont_button.bind(on_press=self.on_continue_pressed)

        # Add widgets to layout
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

    def on_continue_pressed(self, instance):
        self.manager.current = 'social'

    # Update background when screen size changes
    def on_size(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class SocialScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set background color using Canvas
        with self.canvas.before:
            Color(0.922, 0.761, 0.806, 1)  # RGB for EBC3CE
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        self.layout.add_widget(Label(text="Social Screen", font_size=24, color=(0, 0, 0, 1)))
        self.add_widget(self.layout)

    # Update background when screen size changes
    def on_size(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class MyApp(App):
    def build(self):
        # Create ScreenManager to manage different screens
        sm = ScreenManager()
        profile_screen = ProfileScreen(name='profile')
        social_screen = SocialScreen(name='social')

        # Add screens to ScreenManager
        sm.add_widget(profile_screen)
        sm.add_widget(social_screen)

        # Set the initial screen
        profile_screen.update_profile('John Doe', '1000', 'Developer', 'High')

        return sm


if __name__ == '__main__':
    MyApp().run()
