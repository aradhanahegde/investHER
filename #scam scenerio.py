#scam scenerio
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class PhishingScam(Screen):
    def __init__(self, **kwargs):
        super(PhishingScam, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        #email text
        self.label = Label(text='You received an email saying: "Congrats! You just won a free IPhone 14!')
        self.layout.add_widget(self.label)

        #buttons
        self.button_click = Button(text="Click the link")
        self.button_click.size_hint = (1, 0.1)
        self.button_click.bind(on_press=self.click_link)
        self.layout.add_widget(self.button_click)

        self.button_ignore = Button(text="Ignore the email")
        self.button_ignore.size_hint = (1, 0.1) 
        self.button_ignore.bind(on_press=self.ignore_link)
        self.layout.add_widget(self.button_ignore)

        self.add_widget(self.layout)
    
    def click_link(self, instance):
        self.manager.current = "Phishing_Fail"
    
    def ignore_link(self, instance):
        self.manager.current = "Phishing_Success"


class PhishingFail(Screen):
    def __init__(self, **kwargs):
        super(PhishingFail, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Label for failure message
        self.label = Label(text="You fell for a phishing scam! You lose 50 dollars.")
        self.layout.add_widget(self.label)

        # Button to go back to the phishing scenario
        self.button_restart = Button(text="Go Back", size_hint=(1, 0.1))
        self.button_restart.bind(on_press=self.restart)
        self.layout.add_widget(self.button_restart)

        self.add_widget(self.layout)

    def restart(self, instance):
        # Go back to the phishing scenario
        self.manager.current = 'phishing_scenario'

class PhishingSuccess(Screen):
    def __init__(self, **kwargs):
        super(PhishingSuccess, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Label for success message
        self.label = Label(text="Nice job, you avoided the phishing scam! You kept your money.")
        self.layout.add_widget(self.label)

        # Button to go back to the phishing scenario
        self.button_restart = Button(text="Go Back", size_hint=(1, 0.1))
        self.button_restart.bind(on_press=self.restart)
        self.layout.add_widget(self.button_restart)

        self.add_widget(self.layout)

    def restart(self, instance):
        # Go back to the phishing scenario
        self.manager.current = 'phishing_scenario'




class PhishingApp(App):
     def build(self):
        sm = ScreenManager()
        sm.add_widget(PhishingScam(name='phishing_scenario'))
        sm.add_widget(PhishingFail(name='Phishing_Fail'))  # Added the failure screen
        sm.add_widget(PhishingSuccess(name='Phishing_Success'))  # Added the success screen
        return sm

if __name__ == '__main__':
    PhishingApp().run()
       
