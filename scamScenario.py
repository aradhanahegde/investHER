#scam scenerio
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

class PhishingScam(Screen):
    def __init__(self, **kwargs):
        super(PhishingScam, self).__init__(**kwargs)
       
        
        with self.canvas.before:
            Color(0.922, 0.7647, 0.8078, 1) 
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)


        #email text
        self.label = Label(text='You received an email saying: "Congrats! You just won a free IPhone 14!', color=[0, 0, 0, 1])
        self.layout.add_widget(self.label)

        #buttons
        self.button_click = Button(
        text="Click the link", 
        background_color=[0.984, 0.984, 0.898, 1],  # FBFBE5 in RGBA
        background_normal='',  # Forces the color to apply
        color=[0, 0, 0, 1]
        )
        


        self.button_click.size_hint = (1, 0.1)
        self.button_click.bind(on_press=self.click_link)
        self.layout.add_widget(self.button_click)

        self.button_ignore = Button(
        text="Ignore the email",
        background_color=[0.984, 0.984, 0.898, 1],  
        background_normal='',
        color=[0, 0, 0, 1])
        


        self.button_ignore.size_hint = (1, 0.1) 
        self.button_ignore.bind(on_press=self.ignore_link)
        self.layout.add_widget(self.button_ignore)

        self.add_widget(self.layout)
    
    def click_link(self, instance):
        self.manager.current = "Phishing_Fail"
    
    def ignore_link(self, instance):
        self.manager.current = "Phishing_Success"

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class PhishingFail(Screen):
    def __init__(self, **kwargs):
        super(PhishingFail, self).__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.922, 0.7647, 0.8078, 1)  
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)



        # Label for failure message
        self.label = Label(text="You fell for a phishing scam! You lose 50 dollars.", color=[0, 0, 0, 1])
        self.layout.add_widget(self.label)

        # Button to go back to the phishing scenario
        self.button_continue = Button(
        text="Continue",
        background_color=[0.984, 0.984, 0.898, 1],  
        background_normal='',
        color=[0, 0, 0, 1]
        , size_hint=(None, None),
        size=(1600, 80))
        


        self.button_continue.bind(on_press=self.go_next)
        self.layout.add_widget(self.button_continue)

        self.add_widget(self.layout)

    def go_next(self, instance):
        self.manager.current = 'dashboard'


    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class PhishingSuccess(Screen):
    def __init__(self, **kwargs):
        super(PhishingSuccess, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0.922, 0.7647, 0.8078, 1) 
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        
        # Label for success message
        self.label = Label(text="Nice job, you avoided the phishing scam! You kept your money.", color=[0, 0, 0, 1])
        self.layout.add_widget(self.label)

        # Button to go back to the phishing scenario
        self.button_continue = Button(
        text="Continue",
        background_color=[0.984, 0.984, 0.898, 1],  
        background_normal='',
        color=[0, 0, 0, 1]
        , size_hint=(None, None),
        size=(1600, 80))
       


        self.button_continue.bind(on_press=self.go_next)
        self.layout.add_widget(self.button_continue)
        self.add_widget(self.layout)

    def go_next(self, instance):
        self.manager.current = 'dashboard'
    
    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

