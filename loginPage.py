import firebase_admin
from firebase_admin import credentials, auth, firestore
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup

# Firebase Setup
cred = credentials.Certificate("firebase-admin-sdk-key.json")
firebase_admin.initialize_app(cred)


# Function to add a user to Firebase
def add_user_to_firebase(email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password,
        )
        return f"Successfully created new user: {user.uid}"
    except Exception as e:
        return f"Error creating user: {e}"


# Function to login a user
def login_user(email, password):
    try:
        user = auth.get_user_by_email(email)
        # For now, we simulate authentication by password matching
        if user.email == email:
            return f"Login successful for {user.email}"
        else:
            return "Login failed. Check your email and password."
    except Exception as e:
        return f"Login failed: {str(e)}"


# Function for the Sign-Up Popup Message
def sign_up_popup_message(message):
    popup = Popup(title='Message', content=Label(text=message), size_hint=(None, None), size=(400, 400))
    popup.open()


# Layout Class
class LoginPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = [10, 10, 10, 10]
        self.spacing = 10
        self.background_color = [0.9, 0.9, 0.9, 1]  # Light gray background

        # Title Label
        title_label = Label(text="InvestHER", font_size=32, size_hint=(None, None), size=(400, 50), bold=True)
        self.add_widget(title_label)

        # Email Input
        self.email_input = TextInput(hint_text="Enter your email", size_hint=(None, None), size=(300, 40),
                                     multiline=False)
        self.add_widget(self.email_input)

        # Password Input
        self.password_input = TextInput(hint_text="Enter your password", size_hint=(None, None), size=(300, 40),
                                        password=True, multiline=False)
        self.add_widget(self.password_input)

        # Buttons Box Layout
        button_layout = BoxLayout(size_hint=(None, None), size=(400, 50), spacing=10)
        button_layout.orientation = "horizontal"

        # Sign Up Button
        self.sign_up_button = Button(text="Sign Up", background_color=(0.1, 0.6, 0.1, 1), size_hint=(None, None),
                                     size=(180, 50), bold=True)
        self.sign_up_button.bind(on_press=self.sign_up)

        # Login Button
        self.login_button = Button(text="Login", background_color=(0.1, 0.3, 0.8, 1), size_hint=(None, None),
                                   size=(180, 50), bold=True)
        self.login_button.bind(on_press=self.login)

        button_layout.add_widget(self.sign_up_button)
        button_layout.add_widget(self.login_button)

        # Add Button Layout to Main Layout
        self.add_widget(button_layout)

    # Sign-Up Function
    def sign_up(self, instance):
        email = self.email_input.text
        password = self.password_input.text

        if email and password:
            message = add_user_to_firebase(email, password)
            sign_up_popup_message(message)
        else:
            sign_up_popup_message("Please fill in all fields.")

    # Login Function
    def login(self, instance):
        email = self.email_input.text
        password = self.password_input.text

        if email and password:
            message = login_user(email, password)
            sign_up_popup_message(message)
        else:
            sign_up_popup_message("Please fill in all fields.")


# Main App Class
class InvestHerApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)  # Set background color for the app window
        return LoginPage()


if __name__ == "__main__":
    InvestHerApp().run()
