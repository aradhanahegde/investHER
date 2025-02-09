from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from setup_screen import SetupScreen
from avatar_screen import AvatarScreen
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase Initialization
cred = credentials.Certificate("firebase-admin-sdk-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

class InvestHerApp(MDApp):
    def build(self):
        sm = MDScreenManager()

        # Add all screens to the ScreenManager
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SetupScreen(name="setup"))
        sm.add_widget(AvatarScreen(name="avatar"))
        sm.add_widget(NarrativeScreen(name="narrative"))

        # Start with the login screen
        sm.current = "login"

        return sm


if __name__ == "__main__":
    InvestHerApp().run()