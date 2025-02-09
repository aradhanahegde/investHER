from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class socialScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a BoxLayout
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=50)

        # Set the background color using Canvas
        with self.canvas.before:
            Color(0.922, 0.761, 0.807, 1)  # Pink background
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Bind the size and position of the Rectangle to match the screen
        self.bind(size=self.update_rect, pos=self.update_rect)

        # Title
        self.title = Label(text="Social Life", font_size=24, bold=True, color=[0, 0, 0, 1])
        
        # Description Label
        self.life = Label(
            text="Your friends invited you to a party, but there is an entry fee of $40. What will you do?",
            font_size=18,
            size_hint_y=None,
            height=150,
            color=[0, 0, 0, 1]
        )


        self.button1 = Button(text="Spend $40 for the entry.", size_hint=(1, 0.3), background_normal="", background_color=[0.984, 0.984, 0.898, 1], color=[0, 0, 0, 1])
        self.button1.bind(on_press=lambda x: self.showres("It was a fun night, but now you are running low on cash"))

        self.button2 = Button(text="Tell your friends everyone can stay in", size_hint=(1, 0.3), background_normal="", background_color=[0.984, 0.984, 0.898, 1], color=[0, 0, 0, 1])
        self.button2.bind(on_press=lambda x: self.showres("Your friends agree that it's a smart financial decision, and everyone had fun!"))

        self.button3 = Button(text="Decline and decide to stay in", size_hint=(1, 0.3), background_normal="",background_color=[0.984, 0.984, 0.898, 1], color=[0, 0, 0, 1])
        self.button3.bind(on_press=lambda x: self.showres("You miss out on the fun, but you saved money:)"))


        self.res = Label(text="", font_size=16, size_hint_y=None, height=50, color=[0, 0, 0, 1])  

        # Navigation Buttons
        self.backButton = Button(text="Back", size_hint=(None, None), size=(200, 50),background_normal="", pos_hint={'center_x': 0.5}, background_color=[0.984, 0.984, 0.898, 1], color=[0, 0, 0, 1])
        self.backButton.bind(on_press=self.goBack)
        
        self.nextButton = Button(text="Next", size_hint=(None, None), size=(200, 50), background_normal="",pos_hint={'center_x': 0.5}, background_color=[0.984, 0.984, 0.898, 1], color=[0, 0, 0, 1])
        self.nextButton.bind(on_press=self.gotoStock)

        # Add widgets to layout
        self.layout.add_widget(self.title)
        self.layout.add_widget(self.life)
        self.layout.add_widget(self.button1)
        self.layout.add_widget(self.button2)
        self.layout.add_widget(self.button3)
        self.layout.add_widget(self.res)
        self.layout.add_widget(self.backButton)
        self.layout.add_widget(self.nextButton)

        self.add_widget(self.layout)


    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def showres(self, msg):
        self.res.text = msg

    def goBack(self, instance):
        self.manager.current = 'profile'

    def gotoStock(self, instance):
        self.manager.current = 'stock'


# class SocialApp(App):
#     def build(self):
#         return socialScreen()
#
# if __name__ == '__main__':
#     SocialApp().run()