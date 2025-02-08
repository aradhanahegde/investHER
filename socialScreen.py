from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.label import Label

class socialScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout= BoxLayout(orientation='vertical', spacing=20, padding=50)
        self.title = Label(text="Social Life", font_size=24, bold=True)
        self.life =Label(
            text="Your friends invited you to a party, but there is an entry fee of $40. What will you do?",
            font_size=18,
            size_hint_y = None,
            height = 150
        )
        self.button1 = Button(text="Spend $40 for the entry.", size_hint=(None,None), size = (300,50) )
        self.button1.bind(on_press=lambda x : self.showres("It was a fun night, but now you are running low on cash"))

        self.button2 = Button(text="Tell your friends everyone can stay in ", size_hint=(None, None), size =(400,50))
        self.button2.bind(on_press=lambda x :self.showres("Your friends agree that its a smart financial decision, and everyone had fun!"))

        self.button3 = Button(text="Decline and decide to stay in", size_hint=(None, None), size=(300,50))
        self.button3.bind(on_press=lambda x:self.showres("You miss out on the fun, but you saved money:)"))

        self.res = Label(text="",font_size=16, size_hint_y=None, height = 50)
        self.backButton = Button(text="Back",size_hint=(None, None), size = (200,50))
        self.backButton.bind(on_press=self.goBack)
        self.nextButton = Button(text="Next", size_hint=(None, None), size=(200, 50))
        self.nextButton.bind(on_press=self.gotoStock)

        self.layout.add_widget(self.title)
        self.layout.add_widget(self.life)
        self.layout.add_widget(self.button1)
        self.layout.add_widget(self.button2)
        self.layout.add_widget(self.button3)
        self.layout.add_widget(self.res)
        self.layout.add_widget(self.backButton)
        self.layout.add_widget(self.nextButton)
        self.add_widget(self.layout)




    def showres(self, msg):
        self.res.text = msg

    def goBack(self, instance):
        self.manager.current = 'profile'

    def gotoStock(self, instance):
        self.manager.current = 'stock'
