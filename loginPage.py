import firebase_admin
from firebase_admin import credentials, auth, firestore
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.metrics import dp
from kivy.animation import Animation
import requests
import json
import matplotlib.pyplot as plt
import yfinance as yf
import cohere

# --------------------------- API KEYS & Constants ---------------------------
FIREBASE_CERT = "firebase-admin-sdk-key.json"  # Path to your Firebase Admin SDK key
FIREBASE_API_KEY = "AIzaSyDaBUSoH83rCLDpGjWUA4TZ89Fp4cFyBTo"  # Your Firebase API key
FIREBASE_AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

# Cohere configuration – replace with your actual key!
COHERE_API_KEY = "dutvIUVVbr9NahmBtZySPgJ8l1qsJDAW86ReshoC"
# Initialize the Cohere client using the new ClientV2 interface
co = cohere.ClientV2(COHERE_API_KEY)

# --------------------------- Firebase Initialization ---------------------------
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-admin-sdk-key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --------------------------- Helper Functions for Stock Data using yfinance ---------------------------
def fetch_current_price(ticker):
    try:
        t = yf.Ticker(ticker)
        price = t.info.get("regularMarketPrice")
        if price is not None:
            return price
        hist = t.history(period="1d")
        if not hist.empty:
            return float(hist['Close'].iloc[-1])
        print("No market price found for ticker:", ticker)
        return None
    except Exception as e:
        print("Error in fetch_current_price:", e)
        return None

def fetch_stock_history(ticker):
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="1mo")
        history_list = [(str(date.date()), row["Close"]) for date, row in hist.iterrows()]
        return history_list
    except Exception as e:
        print("Error in fetch_stock_history:", e)
        return None

# --------------------------- Cohere API Helper Functions ---------------------------
def create_cohere_learning_content(topic):
    prompt = (
        f"Explain the concept of '{topic}' in clear, engaging language. "
        "Include one real-world analogy. "
        "Write a short, easy-to-understand paragraph for a beginner. Start the response with Sure. Generate the response within 50-60 hours"
    )
    try:
        response = co.chat(
            model="command-r-plus",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        return str(response.message.content)
    except Exception as e:
        print("Error in create_cohere_learning_content:", e)
        return "Error generating content. Please try again later."

def create_cohere_quiz(topic):
    prompt = (
        f"Create a multiple-choice quiz question about '{topic}' that tests a basic real-world application of the concept. "
        "Provide one clear question and three answer options labeled A, B, and C. Indicate which option is correct and assign a reward of 50 points for a correct answer. "
        "Return the result as a JSON object with keys: question, options, answer, reward."
    )
    try:
        response = co.chat(
            model="command-r-plus",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        output = str(response.message.content)
        try:
            quiz_data = json.loads(output)
            return quiz_data
        except Exception as e:
            print("JSON parse error:", e)
            return {
                "question": "What is a key benefit of understanding personal finance?",
                "options": {"A": "Better money management", "B": "Increased spending", "C": "Higher debts"},
                "answer": "A",
                "reward": 50
            }
    except Exception as e:
        print("Error in create_cohere_quiz:", e)
        return {
            "question": "What is a key benefit of understanding personal finance?",
            "options": {"A": "Better money management", "B": "Increased spending", "C": "Higher debts"},
            "answer": "A",
            "reward": 50
        }

# --------------------------- SCREENS ---------------------------
# BASE SCREEN (Draws background with circles)
class BaseScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.96, 0.8, 0.86, 1)  # Soft pink background
            self.rect = Rectangle(size=self.size, pos=self.pos)
            # White Circles
            Color(1, 1, 1, 0.3)
            Ellipse(size=(200, 200), pos=(50, 400))
            Ellipse(size=(250, 250), pos=(250, 100))
            # Pink Outlined Circles
            Color(0.9, 0.5, 0.7, 1)
            Line(circle=(100, 500, 50), width=2)
            Line(circle=(300, 150, 40), width=2)
        self.bind(size=self.update_canvas, pos=self.update_canvas)
    def update_canvas(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

# Splash Screen (Starting animation page)
class AnimatedSplashScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Background setup
        with self.canvas.before:
            Color(0.95, 0.87, 0.92, 1)  # Soft pink background
            self.rect = Widget(size=self.size, pos=self.pos)

        # Adding cloud animation
        self.cloud1 = Image(source="assets/cloud1.png", size_hint=(None, None), size=(200, 100), pos=(-200, 400))
        self.cloud2 = Image(source="assets/cloud2.png", size_hint=(None, None), size=(250, 120), pos=(-300, 300))
        self.add_widget(self.cloud1)
        self.add_widget(self.cloud2)

        # Adding a bold title label with typewriter animation
        self.title_label = MDLabel(
            text="Welcome to InvestHER",
            font_style="H2",
            halign="center",
            theme_text_color="Primary",
            size_hint=(1, None),
            height=100,
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            opacity=0
        )
        self.add_widget(self.title_label)

        # Adding a sub-title
        self.subtitle_label = MDLabel(
            text="Empower. Educate. Elevate.",
            font_style="H5",
            halign="center",
            theme_text_color="Secondary",
            size_hint=(1, None),
            height=60,
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            opacity=0
        )
        self.add_widget(self.subtitle_label)

        # Play button setup
        self.play_button = MDRaisedButton(
            text="Play",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            md_bg_color=(0.41, 0.22, 0.72, 1),
            opacity=0
        )
        self.play_button.bind(on_release=self.start_app)
        self.add_widget(self.play_button)

        # Starting animations
        self.animate_clouds()
        self.animate_text()

    def animate_clouds(self):
        anim1 = Animation(pos_hint={"center_x": 1.5}, duration=15, t="linear")
        anim2 = Animation(pos_hint={"center_x": 1.5}, duration=20, t="linear")
        anim1.start(self.cloud1)
        anim2.start(self.cloud2)

    def animate_text(self):
        Animation(opacity=1, duration=1).start(self.title_label)
        Animation(opacity=1, duration=1, delay=1).start(self.subtitle_label)
        Animation(opacity=1, duration=1, delay=2).start(self.play_button)

    def start_app(self, instance):
        anim = Animation(opacity=0, duration=1)
        anim.bind(on_complete=lambda animation, widget: self.switch_to_login())
        anim.start(self)

    def switch_to_login(self):
        self.manager.current = "login"

# Login Screen
class LoginScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=30)
        layout.add_widget(Image(source="assets/center_icon.png", size_hint_y=0.4, pos_hint={"center_x": 0.5}))
        layout.add_widget(MDLabel(text="invest[b][i]HER[/i][/b]", theme_text_color="Primary",
                                  font_style="H3", halign="center", markup=True))
        layout.add_widget(MDLabel(text="\"Empower. Educate. Elevate.\"", theme_text_color="Secondary",
                                  font_style="H5", halign="center"))
        self.email_input = MDTextField(hint_text="Enter your email", size_hint_x=0.9, pos_hint={"center_x": 0.5})
        layout.add_widget(self.email_input)
        self.password_input = MDTextField(hint_text="Enter your password", password=True,
                                          size_hint_x=0.9, pos_hint={"center_x": 0.5})
        layout.add_widget(self.password_input)
        buttons_layout = MDBoxLayout(spacing=10, size_hint_x=0.8, pos_hint={"center_x": 0.5})
        signup_button = MDRaisedButton(text="Sign Up", size_hint_x=0.5, pos_hint={"center_x": 0.5},
                                       md_bg_color=(0.91, 0.12, 0.39, 1), on_release=self.sign_up)
        login_button = MDRaisedButton(text="Login", size_hint_x=0.5, pos_hint={"center_x": 0.5},
                                      md_bg_color=(0.41, 0.22, 0.72, 1), on_release=self.login)
        buttons_layout.add_widget(signup_button)
        buttons_layout.add_widget(login_button)
        layout.add_widget(buttons_layout)
        self.add_widget(layout)

    def login(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        if email and password:
            try:
                response = requests.post(FIREBASE_AUTH_URL,
                                         json={"email": email, "password": password, "returnSecureToken": True})
                data = response.json()
                if "idToken" in data:
                    self.manager.get_screen("setup").set_user(email)
                    self.manager.current = "setup"
                else:
                    error_message = data.get("error", {}).get("message", "Invalid login")
                    self.show_popup("Error", error_message)
            except Exception as e:
                self.show_popup("Error", "Something went wrong! Try again.")
        else:
            self.show_popup("Error", "Please enter both email and password.")

    def sign_up(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        if email and password:
            try:
                auth.create_user(email=email, password=password)
                self.show_popup("Success", "Account created! Please log in.")
            except Exception as e:
                self.show_popup("Error", "Email already in use or invalid password.")
        else:
            self.show_popup("Error", "Please enter both email and password.")

    def show_popup(self, title, message):
        popup = MDDialog(title=title, text=message, size_hint=(0.8, 0.3))
        popup.open()

# Setup Screen
class SetupScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_email = None
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=30)
        layout.add_widget(MDLabel(text="Setup Your Profile", theme_text_color="Primary",
                                  font_style="H4", halign="center"))
        layout.add_widget(Image(source="assets/center_icon.png", size_hint_y=0.3, pos_hint={"center_x": 0.5}))
        self.name_input = MDTextField(hint_text="Enter your name", size_hint_x=0.9, pos_hint={"center_x": 0.5})
        layout.add_widget(self.name_input)
        next_button = MDRaisedButton(text="Next", size_hint_x=0.5, pos_hint={"center_x": 0.5},
                                     on_release=self.go_to_avatar_selection)
        layout.add_widget(next_button)
        self.add_widget(layout)

    def set_user(self, email):
        self.user_email = email

    def go_to_avatar_selection(self, instance):
        name = self.name_input.text.strip()
        if name:
            self.manager.get_screen("avatar").set_user(name, self.user_email)
            self.manager.current = "avatar"
        else:
            self.show_popup("Error", "Please enter your name.")

    def show_popup(self, title, message):
        popup = MDDialog(title=title, text=message, size_hint=(0.8, 0.3))
        popup.open()

# Avatar Screen
class AvatarScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_name = None
        self.user_email = None
        self.selected_avatar = None
        layout = MDBoxLayout(orientation="vertical", spacing=30, padding=20)
        layout.add_widget(Image(source="assets/center_icon.png", size_hint=(None, None),
                                size=(250, 250), pos_hint={"center_x": 0.5}))
        layout.add_widget(MDLabel(size_hint_y=None, height=20))
        self.greeting_label = MDLabel(text="", theme_text_color="Primary",
                                      font_style="H5", halign="center")
        layout.add_widget(self.greeting_label)
        self.avatar_grid = MDGridLayout(cols=4, spacing=20, size_hint_y=None, height=300)
        self.load_avatars()
        layout.add_widget(self.avatar_grid)
        submit_button = MDRaisedButton(text="Confirm", size_hint=(0.5, None),
                                       height=50, pos_hint={"center_x": 0.5},
                                       on_release=self.confirm_avatar)
        layout.add_widget(submit_button)
        self.add_widget(layout)

    def set_user(self, name, email):
        self.user_name = name
        self.user_email = email
        self.greeting_label.text = f"{name}, select your avatar"

    def load_avatars(self):
        avatar_folder = "assets/avatars/"
        for i in range(1, 9):
            avatar_path = f"{avatar_folder}avatar{i}.jpg"
            avatar_img = Image(source=avatar_path, size_hint=(1, 1))
            avatar_img.bind(on_touch_down=self.select_avatar)
            self.avatar_grid.add_widget(avatar_img)

    def select_avatar(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.selected_avatar = instance.source
            for child in self.avatar_grid.children:
                child.opacity = 1
            instance.opacity = 0.5

    def confirm_avatar(self, instance):
        if self.selected_avatar:
            db.collection("users").add({"name": self.user_name,
                                         "email": self.user_email,
                                         "avatar": self.selected_avatar})
            self.manager.current = "narrative"
        else:
            self.show_popup("Error", "Please select an avatar.")

    def show_popup(self, title, message):
        popup = MDDialog(title=title, text=message, size_hint=(0.8, 0.3))
        popup.open()

# Narrative Screen
class NarrativeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.slides = [
            {"text": "Many women struggle with financial independence due to societal expectations and lack of financial education.\n\nBut the world is changing, and so can YOU.",
             "image": "assets/slide1_financial_struggles.png"},
            {"text": "Financial knowledge is power.\n\nBy understanding budgeting, investing, and saving, you can take control of your future.",
             "image": "assets/slide2_financial_literacy.png"},
            {"text": "Welcome to InvestHER.\n\nYour journey to financial confidence starts NOW.",
             "image": "assets/slide3_success_path.png"}
        ]
        self.current_slide = 0
        self.layout = MDBoxLayout(orientation="vertical", spacing=20, padding=30)
        self.image = Image(source=self.slides[self.current_slide]["image"],
                           size_hint_y=0.6, pos_hint={"center_x": 0.5})
        self.layout.add_widget(self.image)
        self.label = MDLabel(text=self.slides[self.current_slide]["text"],
                             halign="center", theme_text_color="Primary",
                             font_style="H5", markup=True, text_size=(400, None))
        self.layout.add_widget(self.label)
        self.next_button = MDRaisedButton(text="Next", size_hint=(0.3, None),
                                          height=50, pos_hint={"center_x": 0.5},
                                          md_bg_color=(0.91, 0.12, 0.39, 1),
                                          on_release=self.next_slide)
        self.layout.add_widget(self.next_button)
        self.add_widget(self.layout)

    def next_slide(self, instance):
        self.current_slide += 1
        if self.current_slide < len(self.slides):
            self.image.source = self.slides[self.current_slide]["image"]
            self.image.reload()
            self.label.text = self.slides[self.current_slide]["text"]
        else:
            avatar_screen = self.manager.get_screen("avatar")
            track_screen = self.manager.get_screen("track_selection")
            track_screen.set_user(avatar_screen.user_name, avatar_screen.user_email)
            self.manager.current = "track_selection"

# Track Selection Screen
class TrackSelectionScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_name = None
        self.user_email = None
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=30)
        layout.add_widget(MDLabel(text="Choose Your Starting Point", theme_text_color="Primary",
                                  font_style="H4", halign="center"))
        buttons = [
            ("High School", "$500", "Allowance- $20"),
            ("College", "$1000", "Subway- $15/hr"),
            ("Early Career", "$5,000", "Software Engineer at Canva")
        ]
        for text, amount, job in buttons:
            btn = MDRaisedButton(text=text, size_hint_x=0.7, pos_hint={"center_x": 0.5},
                                 md_bg_color=(0.41, 0.22, 0.72, 1),
                                 on_release=lambda instance, t=text, a=amount, j=job: self.save_selection(t, a, j))
            layout.add_widget(btn)
        self.add_widget(layout)

    def set_user(self, name, email):
        self.user_name = name
        self.user_email = email

    def save_selection(self, track, amount, job):
        user_data = {"name": self.user_name,
                     "email": self.user_email,
                     "track": track,
                     "starting_money": amount,
                     "job": job}
        db.collection("users").add(user_data)
        dashboard_screen = self.manager.get_screen("dashboard")
        avatar_screen = self.manager.get_screen("avatar")
        dashboard_screen.set_user_info(name=self.user_name,
                                        email=self.user_email,
                                        avatar=avatar_screen.selected_avatar,
                                        balance=amount,
                                        track=track)
        self.manager.current = "dashboard"

# Dashboard Screen
class DashboardScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_name = ""
        self.user_email = ""
        self.selected_avatar = ""
        self.starting_balance = 0
        self.track_name = ""
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=20)

        # Profile Section
        profile_layout = MDBoxLayout(orientation="vertical", size_hint_y=0.5, spacing=10)
        avatar_box = AnchorLayout(anchor_x="center", anchor_y="center")
        self.avatar_image = Image(size_hint=(None, None), size=(120, 120))
        avatar_box.add_widget(self.avatar_image)
        profile_layout.add_widget(avatar_box)
        self.name_label = MDLabel(text="Name: {name}", theme_text_color="Primary",
                                  halign="center", font_style="H6")
        self.track_label = MDLabel(text="Track: None", theme_text_color="Primary",
                                   halign="center", font_style="H6")
        self.balance_label = MDLabel(text="Current Balance: $0.00", theme_text_color="Primary",
                                     halign="center", font_style="H6")
        profile_layout.add_widget(self.name_label)
        profile_layout.add_widget(self.track_label)
        profile_layout.add_widget(self.balance_label)
        layout.add_widget(profile_layout)

        # Actions Section
        actions_layout = MDBoxLayout(orientation="vertical", spacing=15, size_hint_y=None, height=320)
        learn_btn = MDRaisedButton(
            text="Learn Something Today",
            size_hint=(None, None),
            size=(300, 80),
            md_bg_color=(0.41, 0.22, 0.72, 1),
            pos_hint={"center_x": 0.5}
        )
        learn_btn.bind(on_release=self.goto_learning)
        portfolio_btn = MDRaisedButton(
            text="Investment Portfolio",
            size_hint=(None, None),
            size=(300, 80),
            md_bg_color=(0.41, 0.22, 0.72, 1),
            pos_hint={"center_x": 0.5}
        )
        portfolio_btn.bind(on_release=self.goto_portfolio)
        actions_layout.add_widget(learn_btn)
        actions_layout.add_widget(portfolio_btn)

        # New Button: Let's attend Party
        party_btn = MDRaisedButton(
            text="Let's attend Party",
            size_hint=(None, None),
            size=(300, 80),
            md_bg_color=(0.41, 0.22, 0.72, 1),
            pos_hint={"center_x": 0.5}
        )
        party_btn.bind(on_release=self.attend_party)
        actions_layout.add_widget(party_btn)

        # New Button: Win Iphone connected to scam scenario
        iphone_btn = MDRaisedButton(
            text="Win Iphone",
            size_hint=(None, None),
            size=(300, 80),
            md_bg_color=(0.41, 0.22, 0.72, 1),
            pos_hint={"center_x": 0.5}
        )
        iphone_btn.bind(on_release=self.win_iphone)
        actions_layout.add_widget(iphone_btn)

        anchor_actions = AnchorLayout(anchor_x="center", anchor_y="top", size_hint_y=0.3)
        anchor_actions.add_widget(actions_layout)
        layout.add_widget(anchor_actions)

        self.add_widget(layout)

    def set_user_info(self, name, email, avatar, balance, track):
        self.user_name = name
        self.user_email = email
        self.selected_avatar = avatar
        try:
            bal = float(balance.replace("$", "").replace(",", ""))
        except Exception:
            bal = float(balance)
        self.starting_balance = bal
        self.track_name = track
        self.avatar_image.source = avatar
        self.name_label.text = f"Name: {self.user_name}"
        self.track_label.text = f"Track: {track}"
        self.balance_label.text = f"Current Balance: ${self.starting_balance:.2f}"

    def add_reward(self, reward):
        self.starting_balance += reward
        self.balance_label.text = f"Current Balance: ${self.starting_balance:.2f}"

    def goto_learning(self, instance):
        self.manager.current = "learning"

    def goto_portfolio(self, instance):
        self.manager.get_screen("investment").set_balance(self.starting_balance)
        self.manager.current = "investment"

    def attend_party(self, instance):
        self.manager.current = "social"

    def win_iphone(self, instance):
        self.manager.current = "PhishingScam"

# Investment Portfolio Screen
class InvestmentPortfolioScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.balance = 0.0
        self.portfolio = {}  # {ticker: {"shares": int, "avg_price": float}}
        self.transaction_history = []  # List of transaction strings
        self.selected_company = None  # Dict with keys "text" and "ticker"
        self.company_list = [
            {"text": "Apple Inc.", "ticker": "AAPL"},
            {"text": "Microsoft Corporation", "ticker": "MSFT"},
            {"text": "Alphabet Inc.", "ticker": "GOOGL"},
            {"text": "Amazon.com, Inc.", "ticker": "AMZN"},
            {"text": "Tesla, Inc.", "ticker": "TSLA"},
            {"text": "Johnson & Johnson", "ticker": "JNJ"},
            {"text": "JPMorgan Chase & Co.", "ticker": "JPM"},
            {"text": "Visa Inc.", "ticker": "V"},
            {"text": "Procter & Gamble Co.", "ticker": "PG"},
            {"text": "Walmart Inc.", "ticker": "WMT"},
            {"text": "NVIDIA Corporation", "ticker": "NVDA"},
            {"text": "UnitedHealth Group Inc.", "ticker": "UNH"},
            {"text": "Home Depot, Inc.", "ticker": "HD"},
            {"text": "Mastercard Incorporated", "ticker": "MA"},
            {"text": "The Coca-Cola Company", "ticker": "KO"},
            {"text": "PepsiCo, Inc.", "ticker": "PEP"},
            {"text": "Intel Corporation", "ticker": "INTC"},
            {"text": "Cisco Systems, Inc.", "ticker": "CSCO"},
            {"text": "Exxon Mobil Corporation", "ticker": "XOM"},
            {"text": "Chevron Corporation", "ticker": "CVX"}
        ]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": item["text"],
                "on_release": lambda x=item: self.set_company(x)
            } for item in self.company_list
        ]
        self.menu = MDDropdownMenu(
            caller=None,
            items=menu_items,
            width_mult=4,
        )
        pastel_color = (0.41, 0.22, 0.72, 1)

        layout = MDBoxLayout(orientation="vertical", spacing=10, padding=10)
        title_label = MDLabel(text="Investment Portfolio", font_style="H4", halign="center", theme_text_color="Primary")
        layout.add_widget(title_label)
        self.balance_label = MDLabel(text="Balance: $0.00", font_style="H6", halign="center", theme_text_color="Primary")
        layout.add_widget(self.balance_label)
        self.company_button = MDRaisedButton(
            text="Select Company",
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={"center_x": 0.5},
            md_bg_color=pastel_color
        )
        self.company_button.bind(on_release=self.open_menu)
        layout.add_widget(self.company_button)
        history_button = MDRaisedButton(
            text="View Transaction History",
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={"center_x": 0.5},
            md_bg_color=pastel_color
        )
        history_button.bind(on_release=self.view_transaction_history)
        layout.add_widget(history_button)
        self.shares_input = MDTextField(
            hint_text="Enter number of shares",
            size_hint_x=0.8,
            input_filter='int',
            pos_hint={"center_x": 0.5}
        )
        layout.add_widget(self.shares_input)
        fetch_button = MDRaisedButton(
            text="Fetch Stock Data",
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={"center_x": 0.5},
            md_bg_color=pastel_color
        )
        fetch_button.bind(on_release=self.fetch_stock_data)
        layout.add_widget(fetch_button)
        self.price_label = MDLabel(text="Current Price: N/A", halign="center", theme_text_color="Primary")
        layout.add_widget(self.price_label)
        self.graph_image = Image(size_hint=(1, 2))
        self.graph_image.opacity = 0
        layout.add_widget(self.graph_image)
        trade_layout = MDBoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=50)
        buy_button = MDRaisedButton(text="Buy", md_bg_color=pastel_color)
        sell_button = MDRaisedButton(text="Sell", md_bg_color=pastel_color)
        buy_button.bind(on_release=self.buy_stock)
        sell_button.bind(on_release=self.sell_stock)
        trade_layout.add_widget(buy_button)
        trade_layout.add_widget(sell_button)
        layout.add_widget(trade_layout)
        back_button = MDRaisedButton(
            text="Back to Dashboard",
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={"center_x": 0.5},
            md_bg_color=pastel_color
        )
        back_button.bind(on_release=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def open_menu(self, instance):
        self.menu.caller = instance
        self.menu.open()

    def set_company(self, company):
        self.selected_company = company
        self.company_button.text = company["text"]
        self.menu.dismiss()

    def set_balance(self, balance):
        self.balance = balance
        self.update_balance_label()

    def update_balance_label(self):
        self.balance_label.text = f"Balance: ${self.balance:.2f}"

    def view_transaction_history(self, instance):
        history_text = "\n".join(self.transaction_history) if self.transaction_history else "No transactions yet."
        popup = MDDialog(title="Transaction History", text=history_text, size_hint=(0.8, 0.5))
        popup.open()

    def fetch_stock_data(self, instance):
        if self.selected_company is None:
            self.price_label.text = "Please select a company"
            return
        ticker = self.selected_company["ticker"]
        price = fetch_current_price(ticker)
        if price is not None:
            self.price_label.text = f"Current Price: ${price:.2f}"
            self.update_graph(ticker)
        else:
            self.price_label.text = "Error fetching price"

    def update_graph(self, ticker):
        history = fetch_stock_history(ticker)
        if history:
            dates = [x[0] for x in history]
            prices = [x[1] for x in history]
            plt.figure(figsize=(8, 6))
            plt.plot(dates, prices, marker='o')
            plt.xticks(rotation=45)
            plt.title(f"{ticker} Price History")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.tight_layout()
            graph_file = f"{ticker}_graph.png"
            plt.savefig(graph_file)
            plt.close()
            self.graph_image.source = graph_file
            self.graph_image.opacity = 1
        else:
            self.graph_image.source = ""
            self.graph_image.opacity = 0

    def buy_stock(self, instance):
        if self.selected_company is None:
            self.price_label.text = "Select a company first"
            return
        ticker = self.selected_company["ticker"]
        shares_text = self.shares_input.text.strip()
        if not shares_text:
            self.price_label.text = "Enter number of shares"
            return
        shares = int(shares_text)
        price = fetch_current_price(ticker)
        if price is None:
            self.price_label.text = "Error fetching price"
            return
        cost = shares * price
        if cost > self.balance:
            self.price_label.text = "Insufficient balance"
            return
        if ticker in self.portfolio:
            current_shares = self.portfolio[ticker]["shares"]
            current_avg = self.portfolio[ticker]["avg_price"]
            new_total_shares = current_shares + shares
            new_avg = ((current_shares * current_avg) + (shares * price)) / new_total_shares
            self.portfolio[ticker] = {"shares": new_total_shares, "avg_price": new_avg}
        else:
            self.portfolio[ticker] = {"shares": shares, "avg_price": price}
        self.balance -= cost
        self.update_balance_label()
        self.transaction_history.append(f"Bought {shares} shares of {self.selected_company['text']} at ${price:.2f} each")
        self.price_label.text = f"Bought {shares} shares."

    def sell_stock(self, instance):
        if self.selected_company is None:
            self.price_label.text = "Select a company first"
            return
        ticker = self.selected_company["ticker"]
        shares_text = self.shares_input.text.strip()
        if not shares_text:
            self.price_label.text = "Enter number of shares"
            return
        shares = int(shares_text)
        if ticker not in self.portfolio or self.portfolio[ticker]["shares"] < shares:
            self.price_label.text = "Not enough shares to sell"
            return
        price = fetch_current_price(ticker)
        if price is None:
            self.price_label.text = "Error fetching price"
            return
        proceeds = shares * price
        self.portfolio[ticker]["shares"] -= shares
        if self.portfolio[ticker]["shares"] == 0:
            del self.portfolio[ticker]
        self.balance += proceeds
        self.update_balance_label()
        self.transaction_history.append(f"Sold {shares} shares of {self.selected_company['text']} at ${price:.2f} each")
        self.price_label.text = f"Sold {shares} shares."

    def go_back(self, instance):
        dashboard = self.manager.get_screen("dashboard")
        dashboard.set_user_info(
            dashboard.user_name, dashboard.user_email, dashboard.selected_avatar,
            f"${self.balance:.2f}", dashboard.track_name
        )
        self.manager.current = "dashboard"

# Social Screen (Party Page)
class SocialScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', spacing=20, padding=50)
        self.title = MDLabel(text="Social Life", theme_text_color="Primary", font_style="H4", halign="center")
        self.life = MDLabel(text="Your friends invited you to a party, but there is an entry fee of $40. What will you do?",
                            theme_text_color="Primary", font_style="H5", halign="center", size_hint_y=None, height=150)
        self.button1 = MDRaisedButton(text="Spend $40 for the entry.", size_hint=(1, None), height=50,
                                      md_bg_color=(0.41, 0.22, 0.72, 1))
        self.button1.bind(on_release=lambda x: self.showres("It was a fun night, but now you are running low on cash"))
        self.button2 = MDRaisedButton(text="Tell your friends everyone can stay in", size_hint=(1, None), height=50,
                                      md_bg_color=(0.41, 0.22, 0.72, 1))
        self.button2.bind(on_release=lambda x: self.showres("Your friends agree that it's a smart financial decision, and everyone had fun!"))
        self.button3 = MDRaisedButton(text="Decline and decide to stay in", size_hint=(1, None), height=50,
                                      md_bg_color=(0.41, 0.22, 0.72, 1))
        self.button3.bind(on_release=lambda x: self.showres("You miss out on the fun, but you saved money :)"))
        self.res = MDLabel(text="", theme_text_color="Primary", font_style="H6",
                           halign="center", size_hint_y=None, height=50)
        nav_layout = MDBoxLayout(orientation="horizontal", spacing=20, size_hint_y=None, height=50)
        self.nextButton = MDRaisedButton(text="Back to Dashboard", size_hint=(None, None), size=(150, 50),
                                         md_bg_color=(0.91, 0.12, 0.39, 1))
        self.nextButton.bind(on_release=self.gotoDashboard)
        nav_layout.add_widget(self.nextButton)
        self.layout.add_widget(self.title)
        self.layout.add_widget(self.life)
        self.layout.add_widget(self.button1)
        self.layout.add_widget(self.button2)
        self.layout.add_widget(self.button3)
        self.layout.add_widget(self.res)
        self.layout.add_widget(nav_layout)
        self.add_widget(self.layout)

    def showres(self, msg):
        self.res.text = msg

    def goBack(self, instance):
        self.manager.current = 'dashboard'

    def gotoDashboard(self, instance):
        self.manager.current = 'dashboard'

# Learn More Screen
class LearnMoreScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        investing_text = (
            "Investing is the process of putting your money into assets like stocks, bonds, and funds "
            "to grow your wealth over time. Here are some key concepts to know:\n\n"
            "**Stocks:** A share in a company’s ownership. Prices fluctuate based on market conditions.\n"
            "**Bonds:** A type of loan where you lend money to a company or government in exchange for interest.\n"
            "**Mutual Funds & ETFs:** A collection of stocks or bonds managed by professionals.\n"
            "**Risk & Reward:** Higher returns often come with greater risks. Diversifying your investments helps balance this.\n"
            "**Compound Growth:** The longer you invest, the more your money grows due to compounding interest.\n\n"
            "Understanding these basics will help you make smart financial decisions!"
        )
        info_label = MDLabel(text=investing_text, size_hint_y=None, height=200,
                             font_style="Body1", halign="center")
        info_label.bind(texture_size=self.update_label_height)
        info_label.text_size = (500, None)
        scroll_view = MDScrollView(size_hint=(1, None), size=(800, 400))
        scroll_view.add_widget(info_label)
        back_button = MDRaisedButton(text="Back", size_hint=(None, None), size=(200, 50),
                                     md_bg_color=(0.91, 0.12, 0.39, 1), pos_hint={'center_x': 0.5})
        back_button.bind(on_release=self.go_back)
        spacer = Widget(size_hint_y=None, height=20)
        next_button = MDRaisedButton(text="I'm Ready to Invest", size_hint=(None, None), size=(200, 50),
                                     md_bg_color=(0.91, 0.12, 0.39, 1), pos_hint={'center_x': 0.5})
        next_button.bind(on_release=self.go_to_investment)
        layout.add_widget(scroll_view)
        layout.add_widget(back_button)
        layout.add_widget(spacer)
        layout.add_widget(next_button)
        self.add_widget(layout)

    def update_label_height(self, instance, value):
        instance.height = instance.texture_size[1]

    def go_back(self, instance):
        self.manager.current = "stock"

    def go_to_investment(self, instance):
        self.manager.current = "invest"

# Learning Screen – Using Cohere for content generation
class LearningScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.topic = ""
        self.generated_content = ""
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=30)
        layout.add_widget(MDLabel(text="What would you like to learn or get creative about?",
                                  theme_text_color="Primary", font_style="H5", halign="center"))
        self.search_input = MDTextField(hint_text="Enter a topic (e.g., teach me about bonds)",
                                        size_hint_x=0.9, pos_hint={"center_x": 0.5})
        layout.add_widget(self.search_input)
        teach_button = MDRaisedButton(text="Teach Me", size_hint=(0.5, None), height=50,
                                      pos_hint={"center_x": 0.5},
                                      md_bg_color=(0.91, 0.12, 0.39, 1), on_release=self.generate_content)
        layout.add_widget(teach_button)
        self.content_label = MDLabel(text="", theme_text_color="Primary",
                                     halign="center", font_style="Body1")
        layout.add_widget(self.content_label)
        self.quiz_button = MDRaisedButton(text="Take me to the Quiz", size_hint=(0.5, None), height=50,
                                          pos_hint={"center_x": 0.5},
                                          md_bg_color=(0.91, 0.12, 0.39, 1), on_release=self.go_to_quiz)
        self.quiz_button.opacity = 0
        layout.add_widget(self.quiz_button)
        self.add_widget(layout)

    def format_generated_content(self, raw_content):
        content_start = raw_content.find("text='") + 6
        content_end = raw_content.rfind("')")
        if content_start > 0 and content_end > 0:
            content = raw_content[content_start:content_end]
        else:
            content = raw_content
        formatted_content = content.replace("\\n", "\n\n").replace("[b]", "**").replace("[/b]", "**").strip()
        index = formatted_content.find("Sure")
        return formatted_content[index:]

    def generate_content(self, instance):
        self.topic = self.search_input.text.strip()
        if self.topic:
            raw_content = create_cohere_learning_content(self.topic)
            formatted_content = self.format_generated_content(raw_content)
            self.content_label.text = f"Here’s what we found:\n\n{formatted_content}"
            self.quiz_button.opacity = 1
        else:
            self.show_popup("Error", "Please enter a topic.")

    def go_to_quiz(self, instance):
        quiz_screen = self.manager.get_screen("quiz")
        quiz_screen.setup_quiz(self.topic)
        self.manager.current = "quiz"

    def show_popup(self, title, message):
        popup = MDDialog(title=title, text=message, size_hint=(0.8, 0.3))
        popup.open()

# Quiz Screen – Using Cohere for quiz generation
class QuizScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quiz_data = {}
        self.selected_answer = None
        self.layout = MDBoxLayout(orientation="vertical", spacing=20, padding=30)
        self.question_label = MDLabel(text="", theme_text_color="Primary",
                                      halign="center", font_style="H6")
        self.layout.add_widget(self.question_label)
        self.answers_layout = MDBoxLayout(orientation="vertical", spacing=10)
        self.layout.add_widget(self.answers_layout)
        self.back_button = MDRaisedButton(text="Back to Dashboard", size_hint=(0.5, None),
                                          height=50, pos_hint={"center_x": 0.5},
                                          md_bg_color=(0.91, 0.12, 0.39, 1),
                                          on_release=self.go_back_dashboard)
        self.layout.add_widget(self.back_button)
        self.back_button.opacity = 0
        self.add_widget(self.layout)

    def setup_quiz(self, topic):
        self.quiz_data = create_cohere_quiz(topic)
        self.display_quiz()

    def display_quiz(self):
        self.question_label.text = self.quiz_data.get("question", "No quiz available for this topic.")
        self.answers_layout.clear_widgets()
        for option_key, option_text in self.quiz_data.get("options", {}).items():
            btn = MDRaisedButton(text=f"{option_key}: {option_text}", size_hint=(1, None),
                                 height=50, md_bg_color=(0.41, 0.22, 0.72, 1))
            btn.bind(on_release=lambda instance, key=option_key: self.check_answer(key))
            self.answers_layout.add_widget(btn)

    def check_answer(self, selected):
        correct = self.quiz_data.get("answer")
        if selected == correct:
            reward = self.quiz_data.get("reward", 50)
            self.show_popup("Correct!", f"Well done! You've earned {reward} points.")
            dashboard = self.manager.get_screen("dashboard")
            dashboard.add_reward(reward)
        else:
            self.show_popup("Incorrect", "That's not correct. Better luck next time!")
        self.back_button.opacity = 1
        for child in self.answers_layout.children:
            child.disabled = True

    def go_back_dashboard(self, instance):
        self.manager.current = "dashboard"

    def show_popup(self, title, message):
        popup = MDDialog(title=title, text=message, size_hint=(0.8, 0.3))
        popup.open()

# Scam Scenario Screens (Phishing)
class PhishingScam(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Inherits background with circles from BaseScreen
        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        self.label = MDLabel(text='You received an email saying:\n"Congrats! You just won a free IPhone 14!"',
                             theme_text_color="Primary", halign="center", font_style="H5")
        layout.add_widget(self.label)
        self.button_click = MDRaisedButton(
            text="Click the link",
            md_bg_color=(0.91, 0.12, 0.39, 1),
            pos_hint={"center_x": 0.5}
        )
        self.button_click.bind(on_release=self.click_link)
        layout.add_widget(self.button_click)
        self.button_ignore = MDRaisedButton(
            text="Ignore the email",
            md_bg_color=(0.91, 0.12, 0.39, 1),
            pos_hint={"center_x": 0.5}
        )
        self.button_ignore.bind(on_release=self.ignore_link)
        layout.add_widget(self.button_ignore)
        self.add_widget(layout)

    def click_link(self, instance):
        # Deduct $50 when the user clicks (reads) the email
        dashboard = self.manager.get_screen("dashboard")
        dashboard.add_reward(-50)
        self.manager.current = "Phishing_Fail"

    def ignore_link(self, instance):
        self.manager.current = "Phishing_Success"

class PhishingFail(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        self.label = MDLabel(text="You fell for a phishing scam! You lose $50.",
                             theme_text_color="Primary", halign="center", font_style="H5")
        layout.add_widget(self.label)
        self.button_continue = MDRaisedButton(
            text="Continue",
            md_bg_color=(0.91, 0.12, 0.39, 1),
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={"center_x": 0.5}
        )
        self.button_continue.bind(on_release=self.go_next)
        layout.add_widget(self.button_continue)
        self.add_widget(layout)

    def go_next(self, instance):
        self.manager.current = 'dashboard'

class PhishingSuccess(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        self.label = MDLabel(text="Nice job, you avoided the phishing scam! You kept your money.",
                             theme_text_color="Primary", halign="center", font_style="H5")
        layout.add_widget(self.label)
        self.button_continue = MDRaisedButton(
            text="Continue",
            md_bg_color=(0.91, 0.12, 0.39, 1),
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={"center_x": 0.5}
        )
        self.button_continue.bind(on_release=self.go_next)
        layout.add_widget(self.button_continue)
        self.add_widget(layout)

    def go_next(self, instance):
        self.manager.current = 'dashboard'

# --------------------------- MAIN APP ---------------------------
class InvestHerApp(MDApp):
    def build(self):import firebase_admin
from firebase_admin import credentials, auth, firestore
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.metrics import dp
from kivy.animation import Animation
import requests
import json
import matplotlib.pyplot as plt
import yfinance as yf
import cohere

# --------------------------- API KEYS & Constants ---------------------------
FIREBASE_CERT = "firebase-admin-sdk-key.json"  # Path to your Firebase Admin SDK key
FIREBASE_API_KEY = "AIzaSyDaBUSoH83rCLDpGjWUA4TZ89Fp4cFyBTo"  # Your Firebase API key
FIREBASE_AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

# Cohere configuration – replace with your actual key!
COHERE_API_KEY = "dutvIUVVbr9NahmBtZySPgJ8l1qsJDAW86ReshoC"
# Initialize the Cohere client using the new ClientV2 interface
co = cohere.ClientV2(COHERE_API_KEY)

# --------------------------- Helper Functions for Stock Data using yfinance ---------------------------
def fetch_current_price(ticker):
    try:
        t = yf.Ticker(ticker)
        price = t.info.get("regularMarketPrice")
        if price is not None:
            return price
        hist = t.history(period="1d")
        if not hist.empty:
            return float(hist['Close'].iloc[-1])
        print("No market price found for ticker:", ticker)
        return None
    except Exception as e:
        print("Error in fetch_current_price:", e)
        return None

def fetch_stock_history(ticker):
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="1mo")
        history_list = [(str(date.date()), row["Close"]) for date, row in hist.iterrows()]
        return history_list
    except Exception as e:
        print("Error in fetch_stock_history:", e)
        return None

# --------------------------- Cohere API Helper Functions ---------------------------
def create_cohere_learning_content(topic):
    prompt = (
        f"Explain the concept of '{topic}' in clear, engaging language. "
        "Include one real-world analogy. "
        "Write a short, easy-to-understand paragraph for a beginner. Start the response with Sure. Generate the response within 50-60 hours"
    )
    try:
        response = co.chat(
            model="command-r-plus",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        return str(response.message.content)
    except Exception as e:
        print("Error in create_cohere_learning_content:", e)
        return "Error generating content. Please try again later."

def create_cohere_quiz(topic):
    prompt = (
        f"Create a multiple-choice quiz question about '{topic}' that tests a basic real-world application of the concept. "
        "Provide one clear question and three answer options labeled A, B, and C. Indicate which option is correct and assign a reward of 50 points for a correct answer. "
        "Return the result as a JSON object with keys: question, options, answer, reward."
    )
    try:
        response = co.chat(
            model="command-r-plus",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        output = str(response.message.content)
        try:
            quiz_data = json.loads(output)
            return quiz_data
        except Exception as e:
            print("JSON parse error:", e)
            return {
                "question": "What is a key benefit of understanding personal finance?",
                "options": {"A": "Better money management", "B": "Increased spending", "C": "Higher debts"},
                "answer": "A",
                "reward": 50
            }
    except Exception as e:
        print("Error in create_cohere_quiz:", e)
        return {
            "question": "What is a key benefit of understanding personal finance?",
            "options": {"A": "Better money management", "B": "Increased spending", "C": "Higher debts"},
            "answer": "A",
            "reward": 50
        }

# --------------------------- SCREENS ---------------------------
# BASE SCREEN (Draws background with circles)
class BaseScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.96, 0.8, 0.86, 1)  # Soft pink background
            self.rect = Rectangle(size=self.size, pos=self.pos)
            # White Circles
            Color(1, 1, 1, 0.3)
            Ellipse(size=(200, 200), pos=(50, 400))
            Ellipse(size=(250, 250), pos=(250, 100))
            # Pink Outlined Circles
            Color(0.9, 0.5, 0.7, 1)
            Line(circle=(100, 500, 50), width=2)
            Line(circle=(300, 150, 40), width=2)
        self.bind(size=self.update_canvas, pos=self.update_canvas)
    def update_canvas(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

# Splash Screen (Starting animation page)
class SplashScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=50)
        self.welcome_label = MDLabel(text="Welcome to invest[b][i][color=#FF4081][u]HER[/u][/i][/b]", theme_text_color="Primary",
        font_style="H3", halign="center", markup=True)


        self.welcome_label.opacity = 0
        layout.add_widget(self.welcome_label)
        self.play_button = MDRaisedButton(text="Play", size_hint=(None, None), size=(200, 50),
                                          pos_hint={"center_x": 0.5}, md_bg_color=(0.41, 0.22, 0.72, 1))
        self.play_button.bind(on_release=self.start_app)
        layout.add_widget(self.play_button)
        self.add_widget(layout)
        Animation(opacity=1, duration=2).start(self.welcome_label)
    def start_app(self, instance):
        anim = Animation(opacity=0, duration=1)
        anim.bind(on_complete=lambda animation, widget: self.switch_to_login())
        anim.start(self)
    def switch_to_login(self):
        self.manager.current = "login"

# Login Screen
class LoginScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=30)
        layout.add_widget(Image(source="assets/center_icon.png", size_hint_y=0.4, pos_hint={"center_x": 0.5}))
        layout.add_widget(MDLabel(text="invest[b][i]HER[/i][/b]", theme_text_color="Primary",
                                  font_style="H3", halign="center", markup=True))
        layout.add_widget(MDLabel(text="\"Empower. Educate. Elevate.\"", theme_text_color="Secondary",
                                  font_style="H5", halign="center"))
        self.email_input = MDTextField(hint_text="Enter your email", size_hint_x=0.9, pos_hint={"center_x": 0.5})
        layout.add_widget(self.email_input)
        self.password_input = MDTextField(hint_text="Enter your password", password=True,
                                          size_hint_x=0.9, pos_hint={"center_x": 0.5})
        layout.add_widget(self.password_input)
        buttons_layout = MDBoxLayout(spacing=10, size_hint_x=0.8, pos_hint={"center_x": 0.5})
        signup_button = MDRaisedButton(text="Sign Up", size_hint_x=0.5, pos_hint={"center_x": 0.5},
                                       md_bg_color=(0.91, 0.12, 0.39, 1), on_release=self.sign_up)
        login_button = MDRaisedButton(text="Login", size_hint_x=0.5, pos_hint={"center_x": 0.5},
                                      md_bg_color=(0.41, 0.22, 0.72, 1), on_release=self.login)
        buttons_layout.add_widget(signup_button)
        buttons_layout.add_widget(login_button)
        layout.add_widget(buttons_layout)
        self.add_widget(layout)

    def login(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        if email and password:
            try:
                response = requests.post(FIREBASE_AUTH_URL,
                                         json={"email": email, "password": password, "returnSecureToken": True})
                data = response.json()
                if "idToken" in data:
                    self.manager.get_screen("setup").set_user(email)
                    self.manager.current = "setup"
                else:
                    error_message = data.get("error", {}).get("message", "Invalid login")
                    self.show_popup("Error", error_message)
            except Exception as e:
                self.show_popup("Error", "Something went wrong! Try again.")
        else:
            self.show_popup("Error", "Please enter both email and password.")

    def sign_up(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        if email and password:
            try:
                auth.create_user(email=email, password=password)
                self.show_popup("Success", "Account created! Please log in.")
            except Exception as e:
                self.show_popup("Error", "Email already in use or invalid password.")
        else:
            self.show_popup("Error", "Please enter both email and password.")

    def show_popup(self, title, message):
        popup = MDDialog(title=title, text=message, size_hint=(0.8, 0.3))
        popup.open()

# Setup Screen
class SetupScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_email = None
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=30)
        layout.add_widget(MDLabel(text="Setup Your Profile", theme_text_color="Primary",
                                  font_style="H4", halign="center"))
        layout.add_widget(Image(source="assets/center_icon.png", size_hint_y=0.3, pos_hint={"center_x": 0.5}))
        self.name_input = MDTextField(hint_text="Enter your name", size_hint_x=0.9, pos_hint={"center_x": 0.5})
        layout.add_widget(self.name_input)
        next_button = MDRaisedButton(text="Next", size_hint_x=0.5, pos_hint={"center_x": 0.5},
                                     on_release=self.go_to_avatar_selection)
        layout.add_widget(next_button)
        self.add_widget(layout)

    def set_user(self, email):
        self.user_email = email

    def go_to_avatar_selection(self, instance):
        name = self.name_input.text.strip()
        if name:
            self.manager.get_screen("avatar").set_user(name, self.user_email)
            self.manager.current = "avatar"
        else:
            self.show_popup("Error", "Please enter your name.")

    def show_popup(self, title, message):
        popup = MDDialog(title=title, text=message, size_hint=(0.8, 0.3))
        popup.open()

# Avatar Screen
class AvatarScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_name = None
        self.user_email = None
        self.selected_avatar = None
        layout = MDBoxLayout(orientation="vertical", spacing=30, padding=20)
        layout.add_widget(Image(source="assets/center_icon.png", size_hint=(None, None),
                                size=(250, 250), pos_hint={"center_x": 0.5}))
        layout.add_widget(MDLabel(size_hint_y=None, height=20))
        self.greeting_label = MDLabel(text="", theme_text_color="Primary",
                                      font_style="H5", halign="center")
        layout.add_widget(self.greeting_label)
        self.avatar_grid = MDGridLayout(cols=4, spacing=20, size_hint_y=None, height=300)
        self.load_avatars()
        layout.add_widget(self.avatar_grid)
        submit_button = MDRaisedButton(text="Confirm", size_hint=(0.5, None),
                                       height=50, pos_hint={"center_x": 0.5},
                                       on_release=self.confirm_avatar)
        layout.add_widget(submit_button)
        self.add_widget(layout)

    def set_user(self, name, email):
        self.user_name = name
        self.user_email = email
        self.greeting_label.text = f"{name}, select your avatar"

    def load_avatars(self):
        avatar_folder = "assets/avatars/"
        for i in range(1, 9):
            avatar_path = f"{avatar_folder}avatar{i}.jpg"
            avatar_img = Image(source=avatar_path, size_hint=(1, 1))
            avatar_img.bind(on_touch_down=self.select_avatar)
            self.avatar_grid.add_widget(avatar_img)

    def select_avatar(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.selected_avatar = instance.source
            for child in self.avatar_grid.children:
                child.opacity = 1
            instance.opacity = 0.5

    def confirm_avatar(self, instance):
        if self.selected_avatar:
            db.collection("users").add({"name": self.user_name,
                                         "email": self.user_email,
                                         "avatar": self.selected_avatar})
            self.manager.current = "narrative"
        else:
            self.show_popup("Error", "Please select an avatar.")

    def show_popup(self, title, message):
        popup = MDDialog(title=title, text=message, size_hint=(0.8, 0.3))
        popup.open()

# Narrative Screen
class NarrativeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.slides = [
            {"text": "Many women struggle with financial independence due to societal expectations and lack of financial education.\n\nBut the world is changing, and so can YOU.",
             "image": "assets/slide1_financial_struggles.png"},
            {"text": "Financial knowledge is power.\n\nBy understanding budgeting, investing, and saving, you can take control of your future.",
             "image": "assets/slide2_financial_literacy.png"},
            {"text": "Welcome to InvestHER.\n\nYour journey to financial confidence starts NOW.",
             "image": "assets/slide3_success_path.png"}
        ]
        self.current_slide = 0
        self.layout = MDBoxLayout(orientation="vertical", spacing=20, padding=30)
        self.image = Image(source=self.slides[self.current_slide]["image"],
                           size_hint_y=0.6, pos_hint={"center_x": 0.5})
        self.layout.add_widget(self.image)
        self.label = MDLabel(text=self.slides[self.current_slide]["text"],
                             halign="center", theme_text_color="Primary",
                             font_style="H5", markup=True, text_size=(400, None))
        self.layout.add_widget(self.label)
        self.next_button = MDRaisedButton(text="Next", size_hint=(0.3, None),
                                          height=50, pos_hint={"center_x": 0.5},
                                          md_bg_color=(0.91, 0.12, 0.39, 1),
                                          on_release=self.next_slide)
        self.layout.add_widget(self.next_button)
        self.add_widget(self.layout)

    def next_slide(self, instance):
        self.current_slide += 1
        if self.current_slide < len(self.slides):
            self.image.source = self.slides[self.current_slide]["image"]
            self.image.reload()
            self.label.text = self.slides[self.current_slide]["text"]
        else:
            avatar_screen = self.manager.get_screen("avatar")
            track_screen = self.manager.get_screen("track_selection")
            track_screen.set_user(avatar_screen.user_name, avatar_screen.user_email)
            self.manager.current = "track_selection"

# Track Selection Screen
class TrackSelectionScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_name = None
        self.user_email = None
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=30)
        layout.add_widget(MDLabel(text="Choose Your Starting Point", theme_text_color="Primary",
                                  font_style="H4", halign="center"))
        buttons = [
            ("High School", "$500", "Allowance- $20"),
            ("College", "$1000", "Subway- $15/hr"),
            ("Early Career", "$5,000", "Software Engineer at Canva")
        ]
        for text, amount, job in buttons:
            btn = MDRaisedButton(text=text, size_hint_x=0.7, pos_hint={"center_x": 0.5},
                                 md_bg_color=(0.41, 0.22, 0.72, 1),
                                 on_release=lambda instance, t=text, a=amount, j=job: self.save_selection(t, a, j))
            layout.add_widget(btn)
        self.add_widget(layout)

    def set_user(self, name, email):
        self.user_name = name
        self.user_email = email

    def save_selection(self, track, amount, job):
        user_data = {"name": self.user_name,
                     "email": self.user_email,
                     "track": track,
                     "starting_money": amount,
                     "job": job}
        db.collection("users").add(user_data)
        dashboard_screen = self.manager.get_screen("dashboard")
        avatar_screen = self.manager.get_screen("avatar")
        dashboard_screen.set_user_info(name=self.user_name,
                                        email=self.user_email,
                                        avatar=avatar_screen.selected_avatar,
                                        balance=amount,
                                        track=track)
        self.manager.current = "dashboard"

# Dashboard Screen
class DashboardScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_name = ""
        self.user_email = ""
        self.selected_avatar = ""
        self.starting_balance = 0
        self.track_name = ""
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=20)

        # Profile Section
        profile_layout = MDBoxLayout(orientation="vertical", size_hint_y=0.5, spacing=10)
        avatar_box = AnchorLayout(anchor_x="center", anchor_y="center")
        self.avatar_image = Image(size_hint=(None, None), size=(120, 120))
        avatar_box.add_widget(self.avatar_image)
        profile_layout.add_widget(avatar_box)
        self.name_label = MDLabel(text="Name: {name}", theme_text_color="Primary",
                                  halign="center", font_style="H6")
        self.track_label = MDLabel(text="Track: None", theme_text_color="Primary",
                                   halign="center", font_style="H6")
        self.balance_label = MDLabel(text="Current Balance: $0.00", theme_text_color="Primary",
                                     halign="center", font_style="H6")
        profile_layout.add_widget(self.name_label)
        profile_layout.add_widget(self.track_label)
        profile_layout.add_widget(self.balance_label)
        layout.add_widget(profile_layout)

        # Actions Section
        actions_layout = MDBoxLayout(orientation="vertical", spacing=15, size_hint_y=None, height=320)
        learn_btn = MDRaisedButton(
            text="Learn Something Today",
            size_hint=(None, None),
            size=(300, 80),
            md_bg_color=(0.41, 0.22, 0.72, 1),
            pos_hint={"center_x": 0.5}
        )
        learn_btn.bind(on_release=self.goto_learning)
        portfolio_btn = MDRaisedButton(
            text="Investment Portfolio",
            size_hint=(None, None),
            size=(300, 80),
            md_bg_color=(0.41, 0.22, 0.72, 1),
            pos_hint={"center_x": 0.5}
        )
        portfolio_btn.bind(on_release=self.goto_portfolio)
        actions_layout.add_widget(learn_btn)
        actions_layout.add_widget(portfolio_btn)

        # New Button: Let's attend Party
        party_btn = MDRaisedButton(
            text="Let's attend Party",
            size_hint=(None, None),
            size=(300, 80),
            md_bg_color=(0.41, 0.22, 0.72, 1),
            pos_hint={"center_x": 0.5}
        )
        party_btn.bind(on_release=self.attend_party)
        actions_layout.add_widget(party_btn)

        # New Button: Win Iphone connected to scam scenario
        iphone_btn = MDRaisedButton(
            text="Win Iphone",
            size_hint=(None, None),
            size=(300, 80),
            md_bg_color=(0.41, 0.22, 0.72, 1),
            pos_hint={"center_x": 0.5}
        )
        iphone_btn.bind(on_release=self.win_iphone)
        actions_layout.add_widget(iphone_btn)

        anchor_actions = AnchorLayout(anchor_x="center", anchor_y="top", size_hint_y=0.3)
        anchor_actions.add_widget(actions_layout)
        layout.add_widget(anchor_actions)

        self.add_widget(layout)

    def set_user_info(self, name, email, avatar, balance, track):
        self.user_name = name
        self.user_email = email
        self.selected_avatar = avatar
        try:
            bal = float(balance.replace("$", "").replace(",", ""))
        except Exception:
            bal = float(balance)
        self.starting_balance = bal
        self.track_name = track
        self.avatar_image.source = avatar
        self.name_label.text = f"Name: {self.user_name}"
        self.track_label.text = f"Track: {track}"
        self.balance_label.text = f"Current Balance: ${self.starting_balance:.2f}"

    def add_reward(self, reward):
        self.starting_balance += reward
        self.balance_label.text = f"Current Balance: ${self.starting_balance:.2f}"

    def goto_learning(self, instance):
        self.manager.current = "learning"

    def goto_portfolio(self, instance):
        self.manager.get_screen("investment").set_balance(self.starting_balance)
        self.manager.current = "investment"

    def attend_party(self, instance):
        self.manager.current = "social"

    def win_iphone(self, instance):
        self.manager.current = "PhishingScam"

# Investment Portfolio Screen
class InvestmentPortfolioScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.balance = 0.0
        self.portfolio = {}  # {ticker: {"shares": int, "avg_price": float}}
        self.transaction_history = []  # List of transaction strings
        self.selected_company = None  # Dict with keys "text" and "ticker"
        self.company_list = [
            {"text": "Apple Inc.", "ticker": "AAPL"},
            {"text": "Microsoft Corporation", "ticker": "MSFT"},
            {"text": "Alphabet Inc.", "ticker": "GOOGL"},
            {"text": "Amazon.com, Inc.", "ticker": "AMZN"},
            {"text": "Tesla, Inc.", "ticker": "TSLA"},
            {"text": "Johnson & Johnson", "ticker": "JNJ"},
            {"text": "JPMorgan Chase & Co.", "ticker": "JPM"},
            {"text": "Visa Inc.", "ticker": "V"},
            {"text": "Procter & Gamble Co.", "ticker": "PG"},
            {"text": "Walmart Inc.", "ticker": "WMT"},
            {"text": "NVIDIA Corporation", "ticker": "NVDA"},
            {"text": "UnitedHealth Group Inc.", "ticker": "UNH"},
            {"text": "Home Depot, Inc.", "ticker": "HD"},
            {"text": "Mastercard Incorporated", "ticker": "MA"},
            {"text": "The Coca-Cola Company", "ticker": "KO"},
            {"text": "PepsiCo, Inc.", "ticker": "PEP"},
            {"text": "Intel Corporation", "ticker": "INTC"},
            {"text": "Cisco Systems, Inc.", "ticker": "CSCO"},
            {"text": "Exxon Mobil Corporation", "ticker": "XOM"},
            {"text": "Chevron Corporation", "ticker": "CVX"}
        ]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": item["text"],
                "on_release": lambda x=item: self.set_company(x)
            } for item in self.company_list
        ]
        self.menu = MDDropdownMenu(
            caller=None,
            items=menu_items,
            width_mult=4,
        )
        pastel_color = (0.41, 0.22, 0.72, 1)

        layout = MDBoxLayout(orientation="vertical", spacing=10, padding=10)
        title_label = MDLabel(text="Investment Portfolio", font_style="H4", halign="center", theme_text_color="Primary")
        layout.add_widget(title_label)
        self.balance_label = MDLabel(text="Balance: $0.00", font_style="H6", halign="center", theme_text_color="Primary")
        layout.add_widget(self.balance_label)
        self.company_button = MDRaisedButton(
            text="Select Company",
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={"center_x": 0.5},
            md_bg_color=pastel_color
        )
        self.company_button.bind(on_release=self.open_menu)
        layout.add_widget(self.company_button)
        history_button = MDRaisedButton(
            text="View Transaction History",
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={"center_x": 0.5},
            md_bg_color=pastel_color
        )
        history_button.bind(on_release=self.view_transaction_history)
        layout.add_widget(history_button)
        self.shares_input = MDTextField(
            hint_text="Enter number of shares",
            size_hint_x=0.8,
            input_filter='int',
            pos_hint={"center_x": 0.5}
        )
        layout.add_widget(self.shares_input)
        fetch_button = MDRaisedButton(
            text="Fetch Stock Data",
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={"center_x": 0.5},
            md_bg_color=pastel_color
        )
        fetch_button.bind(on_release=self.fetch_stock_data)
        layout.add_widget(fetch_button)
        self.price_label = MDLabel(text="Current Price: N/A", halign="center", theme_text_color="Primary")
        layout.add_widget(self.price_label)
        self.graph_image = Image(size_hint=(1, 2))
        self.graph_image.opacity = 0
        layout.add_widget(self.graph_image)
        trade_layout = MDBoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=50)
        buy_button = MDRaisedButton(text="Buy", md_bg_color=pastel_color)
        sell_button = MDRaisedButton(text="Sell", md_bg_color=pastel_color)
        buy_button.bind(on_release=self.buy_stock)
        sell_button.bind(on_release=self.sell_stock)
        trade_layout.add_widget(buy_button)
        trade_layout.add_widget(sell_button)
        layout.add_widget(trade_layout)
        back_button = MDRaisedButton(
            text="Back to Dashboard",
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={"center_x": 0.5},
            md_bg_color=pastel_color
        )
        back_button.bind(on_release=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def open_menu(self, instance):
        self.menu.caller = instance
        self.menu.open()

    def set_company(self, company):
        self.selected_company = company
        self.company_button.text = company["text"]
        self.menu.dismiss()

    def set_balance(self, balance):
        self.balance = balance
        self.update_balance_label()

    def update_balance_label(self):
        self.balance_label.text = f"Balance: ${self.balance:.2f}"

    def view_transaction_history(self, instance):
        history_text = "\n".join(self.transaction_history) if self.transaction_history else "No transactions yet."
        popup = MDDialog(title="Transaction History", text=history_text, size_hint=(0.8, 0.5))
        popup.open()

    def fetch_stock_data(self, instance):
        if self.selected_company is None:
            self.price_label.text = "Please select a company"
            return
        ticker = self.selected_company["ticker"]
        price = fetch_current_price(ticker)
        if price is not None:
            self.price_label.text = f"Current Price: ${price:.2f}"
            self.update_graph(ticker)
        else:
            self.price_label.text = "Error fetching price"

    def update_graph(self, ticker):
        history = fetch_stock_history(ticker)
        if history:
            dates = [x[0] for x in history]
            prices = [x[1] for x in history]
            plt.figure(figsize=(8, 6))
            plt.plot(dates, prices, marker='o')
            plt.xticks(rotation=45)
            plt.title(f"{ticker} Price History")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.tight_layout()
            graph_file = f"{ticker}_graph.png"
            plt.savefig(graph_file)
            plt.close()
            self.graph_image.source = graph_file
            self.graph_image.opacity = 1
        else:
            self.graph_image.source = ""
            self.graph_image.opacity = 0

    def buy_stock(self, instance):
        if self.selected_company is None:
            self.price_label.text = "Select a company first"
            return
        ticker = self.selected_company["ticker"]
        shares_text = self.shares_input.text.strip()
        if not shares_text:
            self.price_label.text = "Enter number of shares"
            return
        shares = int(shares_text)
        price = fetch_current_price(ticker)
        if price is None:
            self.price_label.text = "Error fetching price"
            return
        cost = shares * price
        if cost > self.balance:
            self.price_label.text = "Insufficient balance"
            return
        if ticker in self.portfolio:
            current_shares = self.portfolio[ticker]["shares"]
            current_avg = self.portfolio[ticker]["avg_price"]
            new_total_shares = current_shares + shares
            new_avg = ((current_shares * current_avg) + (shares * price)) / new_total_shares
            self.portfolio[ticker] = {"shares": new_total_shares, "avg_price": new_avg}
        else:
            self.portfolio[ticker] = {"shares": shares, "avg_price": price}
        self.balance -= cost
        self.update_balance_label()
        self.transaction_history.append(f"Bought {shares} shares of {self.selected_company['text']} at ${price:.2f} each")
        self.price_label.text = f"Bought {shares} shares."

    def sell_stock(self, instance):
        if self.selected_company is None:
            self.price_label.text = "Select a company first"
            return
        ticker = self.selected_company["ticker"]
        shares_text = self.shares_input.text.strip()
        if not shares_text:
            self.price_label.text = "Enter number of shares"
            return
        shares = int(shares_text)
        if ticker not in self.portfolio or self.portfolio[ticker]["shares"] < shares:
            self.price_label.text = "Not enough shares to sell"
            return
        price = fetch_current_price(ticker)
        if price is None:
            self.price_label.text = "Error fetching price"
            return
        proceeds = shares * price
        self.portfolio[ticker]["shares"] -= shares
        if self.portfolio[ticker]["shares"] == 0:
            del self.portfolio[ticker]
        self.balance += proceeds
        self.update_balance_label()
        self.transaction_history.append(f"Sold {shares} shares of {self.selected_company['text']} at ${price:.2f} each")
        self.price_label.text = f"Sold {shares} shares."

    def go_back(self, instance):
        dashboard = self.manager.get_screen("dashboard")
        dashboard.set_user_info(
            dashboard.user_name, dashboard.user_email, dashboard.selected_avatar,
            f"${self.balance:.2f}", dashboard.track_name
        )
        self.manager.current = "dashboard"

# Social Screen (Party Page)
class SocialScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', spacing=20, padding=50)
        self.title = MDLabel(text="Social Life", theme_text_color="Primary", font_style="H4", halign="center")
        self.life = MDLabel(text="Your friends invited you to a party, but there is an entry fee of $40. What will you do?",
                            theme_text_color="Primary", font_style="H5", halign="center", size_hint_y=None, height=150)
        self.button1 = MDRaisedButton(text="Spend $40 for the entry.", size_hint=(1, None), height=50,
                                      md_bg_color=(0.41, 0.22, 0.72, 1))
        self.button1.bind(on_release=lambda x: self.showres("It was a fun night, but now you are running low on cash"))
        self.button2 = MDRaisedButton(text="Tell your friends everyone can stay in", size_hint=(1, None), height=50,
                                      md_bg_color=(0.41, 0.22, 0.72, 1))
        self.button2.bind(on_release=lambda x: self.showres("Your friends agree that it's a smart financial decision, and everyone had fun!"))
        self.button3 = MDRaisedButton(text="Decline and decide to stay in", size_hint=(1, None), height=50,
                                      md_bg_color=(0.41, 0.22, 0.72, 1))
        self.button3.bind(on_release=lambda x: self.showres("You miss out on the fun, but you saved money :)"))
        self.res = MDLabel(text="", theme_text_color="Primary", font_style="H6",
                           halign="center", size_hint_y=None, height=50)
        nav_layout = MDBoxLayout(orientation="horizontal", spacing=20, size_hint_y=None, height=50)
        self.nextButton = MDRaisedButton(text="Back to Dashboard", size_hint=(None, None), size=(150, 50),
                                         md_bg_color=(0.91, 0.12, 0.39, 1))
        self.nextButton.bind(on_release=self.gotoDashboard)
        nav_layout.add_widget(self.nextButton)
        self.layout.add_widget(self.title)
        self.layout.add_widget(self.life)
        self.layout.add_widget(self.button1)
        self.layout.add_widget(self.button2)
        self.layout.add_widget(self.button3)
        self.layout.add_widget(self.res)
        self.layout.add_widget(nav_layout)
        self.add_widget(self.layout)

    def showres(self, msg):
        self.res.text = msg

    def goBack(self, instance):
        self.manager.current = 'dashboard'

    def gotoDashboard(self, instance):
        self.manager.current = 'dashboard'

# Learn More Screen
class LearnMoreScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        investing_text = (
            "Investing is the process of putting your money into assets like stocks, bonds, and funds "
            "to grow your wealth over time. Here are some key concepts to know:\n\n"
            "**Stocks:** A share in a company’s ownership. Prices fluctuate based on market conditions.\n"
            "**Bonds:** A type of loan where you lend money to a company or government in exchange for interest.\n"
            "**Mutual Funds & ETFs:** A collection of stocks or bonds managed by professionals.\n"
            "**Risk & Reward:** Higher returns often come with greater risks. Diversifying your investments helps balance this.\n"
            "**Compound Growth:** The longer you invest, the more your money grows due to compounding interest.\n\n"
            "Understanding these basics will help you make smart financial decisions!"
        )
        info_label = MDLabel(text=investing_text, size_hint_y=None, height=200,
                             font_style="Body1", halign="center")
        info_label.bind(texture_size=self.update_label_height)
        info_label.text_size = (500, None)
        scroll_view = MDScrollView(size_hint=(1, None), size=(800, 400))
        scroll_view.add_widget(info_label)
        back_button = MDRaisedButton(text="Back", size_hint=(None, None), size=(200, 50),
                                     md_bg_color=(0.91, 0.12, 0.39, 1), pos_hint={'center_x': 0.5})
        back_button.bind(on_release=self.go_back)
        spacer = Widget(size_hint_y=None, height=20)
        next_button = MDRaisedButton(text="I'm Ready to Invest", size_hint=(None, None), size=(200, 50),
                                     md_bg_color=(0.91, 0.12, 0.39, 1), pos_hint={'center_x': 0.5})
        next_button.bind(on_release=self.go_to_investment)
        layout.add_widget(scroll_view)
        layout.add_widget(back_button)
        layout.add_widget(spacer)
        layout.add_widget(next_button)
        self.add_widget(layout)

    def update_label_height(self, instance, value):
        instance.height = instance.texture_size[1]

    def go_back(self, instance):
        self.manager.current = "stock"

    def go_to_investment(self, instance):
        self.manager.current = "invest"

# Learning Screen – Using Cohere for content generation
class LearningScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.topic = ""
        self.generated_content = ""
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=30)
        layout.add_widget(MDLabel(text="What would you like to learn or get creative about?",
                                  theme_text_color="Primary", font_style="H5", halign="center"))
        self.search_input = MDTextField(hint_text="Enter a topic (e.g., teach me about bonds)",
                                        size_hint_x=0.9, pos_hint={"center_x": 0.5})
        layout.add_widget(self.search_input)
        teach_button = MDRaisedButton(text="Teach Me", size_hint=(0.5, None), height=50,
                                      pos_hint={"center_x": 0.5},
                                      md_bg_color=(0.91, 0.12, 0.39, 1), on_release=self.generate_content)
        layout.add_widget(teach_button)
        self.content_label = MDLabel(text="", theme_text_color="Primary",
                                     halign="center", font_style="Body1")
        layout.add_widget(self.content_label)
        self.quiz_button = MDRaisedButton(text="Take me to the Quiz", size_hint=(0.5, None), height=50,
                                          pos_hint={"center_x": 0.5},
                                          md_bg_color=(0.91, 0.12, 0.39, 1), on_release=self.go_to_quiz)
        self.quiz_button.opacity = 0
        layout.add_widget(self.quiz_button)
        self.add_widget(layout)

    def format_generated_content(self, raw_content):
        content_start = raw_content.find("text='") + 6
        content_end = raw_content.rfind("')")
        if content_start > 0 and content_end > 0:
            content = raw_content[content_start:content_end]
        else:
            content = raw_content
        formatted_content = content.replace("\\n", "\n\n").replace("[b]", "**").replace("[/b]", "**").strip()
        index = formatted_content.find("Sure")
        return formatted_content[index:]

    def generate_content(self, instance):
        self.topic = self.search_input.text.strip()
        if self.topic:
            raw_content = create_cohere_learning_content(self.topic)
            formatted_content = self.format_generated_content(raw_content)
            self.content_label.text = f"Here’s what we found:\n\n{formatted_content}"
            self.quiz_button.opacity = 1
        else:
            self.show_popup("Error", "Please enter a topic.")

    def go_to_quiz(self, instance):
        quiz_screen = self.manager.get_screen("quiz")
        quiz_screen.setup_quiz(self.topic)
        self.manager.current = "quiz"

    def show_popup(self, title, message):
        popup = MDDialog(title=title, text=message, size_hint=(0.8, 0.3))
        popup.open()

# Quiz Screen – Using Cohere for quiz generation
class QuizScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quiz_data = {}
        self.selected_answer = None
        self.layout = MDBoxLayout(orientation="vertical", spacing=20, padding=30)
        self.question_label = MDLabel(text="", theme_text_color="Primary",
                                      halign="center", font_style="H6")
        self.layout.add_widget(self.question_label)
        self.answers_layout = MDBoxLayout(orientation="vertical", spacing=10)
        self.layout.add_widget(self.answers_layout)
        self.back_button = MDRaisedButton(text="Back to Dashboard", size_hint=(0.5, None),
                                          height=50, pos_hint={"center_x": 0.5},
                                          md_bg_color=(0.91, 0.12, 0.39, 1),
                                          on_release=self.go_back_dashboard)
        self.layout.add_widget(self.back_button)
        self.back_button.opacity = 0
        self.add_widget(self.layout)

    def setup_quiz(self, topic):
        self.quiz_data = create_cohere_quiz(topic)
        self.display_quiz()

    def display_quiz(self):
        self.question_label.text = self.quiz_data.get("question", "No quiz available for this topic.")
        self.answers_layout.clear_widgets()
        for option_key, option_text in self.quiz_data.get("options", {}).items():
            btn = MDRaisedButton(text=f"{option_key}: {option_text}", size_hint=(1, None),
                                 height=50, md_bg_color=(0.41, 0.22, 0.72, 1))
            btn.bind(on_release=lambda instance, key=option_key: self.check_answer(key))
            self.answers_layout.add_widget(btn)

    def check_answer(self, selected):
        correct = self.quiz_data.get("answer")
        if selected == correct:
            reward = self.quiz_data.get("reward", 50)
            self.show_popup("Correct!", f"Well done! You've earned {reward} points.")
            dashboard = self.manager.get_screen("dashboard")
            dashboard.add_reward(reward)
        else:
            self.show_popup("Incorrect", "That's not correct. Better luck next time!")
        self.back_button.opacity = 1
        for child in self.answers_layout.children:
            child.disabled = True

    def go_back_dashboard(self, instance):
        self.manager.current = "dashboard"

    def show_popup(self, title, message):
        popup = MDDialog(title=title, text=message, size_hint=(0.8, 0.3))
        popup.open()

# Scam Scenario Screens (Phishing)
class PhishingScam(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Inherits background with circles from BaseScreen
        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        self.label = MDLabel(text='You received an email saying:\n"Congrats! You just won a free IPhone 14!"',
                             theme_text_color="Primary", halign="center", font_style="H5")
        layout.add_widget(self.label)
        self.button_click = MDRaisedButton(
            text="Click the link",
            md_bg_color=(0.91, 0.12, 0.39, 1),
            pos_hint={"center_x": 0.5}
        )
        self.button_click.bind(on_release=self.click_link)
        layout.add_widget(self.button_click)
        self.button_ignore = MDRaisedButton(
            text="Ignore the email",
            md_bg_color=(0.91, 0.12, 0.39, 1),
            pos_hint={"center_x": 0.5}
        )
        self.button_ignore.bind(on_release=self.ignore_link)
        layout.add_widget(self.button_ignore)
        self.add_widget(layout)

    def click_link(self, instance):
        # Deduct $50 when the user clicks (reads) the email
        dashboard = self.manager.get_screen("dashboard")
        dashboard.add_reward(-50)
        self.manager.current = "Phishing_Fail"

    def ignore_link(self, instance):
        self.manager.current = "Phishing_Success"

class PhishingFail(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        self.label = MDLabel(text="You fell for a phishing scam! You lose $50.",
                             theme_text_color="Primary", halign="center", font_style="H5")
        layout.add_widget(self.label)
        self.button_continue = MDRaisedButton(
            text="Continue",
            md_bg_color=(0.91, 0.12, 0.39, 1),
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={"center_x": 0.5}
        )
        self.button_continue.bind(on_release=self.go_next)
        layout.add_widget(self.button_continue)
        self.add_widget(layout)

    def go_next(self, instance):
        self.manager.current = 'dashboard'

class PhishingSuccess(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        self.label = MDLabel(text="Nice job, you avoided the phishing scam! You kept your money.",
                             theme_text_color="Primary", halign="center", font_style="H5")
        layout.add_widget(self.label)
        self.button_continue = MDRaisedButton(
            text="Continue",
            md_bg_color=(0.91, 0.12, 0.39, 1),
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={"center_x": 0.5}
        )
        self.button_continue.bind(on_release=self.go_next)
        layout.add_widget(self.button_continue)
        self.add_widget(layout)

    def go_next(self, instance):
        self.manager.current = 'dashboard'

# --------------------------- MAIN APP ---------------------------
class InvestHerApp(MDApp):
    def build(self):
        sm = MDScreenManager()
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SetupScreen(name="setup"))
        sm.add_widget(AvatarScreen(name="avatar"))
        sm.add_widget(NarrativeScreen(name="narrative"))
        sm.add_widget(TrackSelectionScreen(name="track_selection"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(SocialScreen(name="social"))
        sm.add_widget(LearnMoreScreen(name="learn_more"))
        sm.add_widget(LearningScreen(name="learning"))
        sm.add_widget(QuizScreen(name="quiz"))
        sm.add_widget(InvestmentPortfolioScreen(name="investment"))
        sm.add_widget(PhishingScam(name="PhishingScam"))
        sm.add_widget(PhishingFail(name="Phishing_Fail"))
        sm.add_widget(PhishingSuccess(name="Phishing_Success"))
        return sm

if __name__ == "__main__":
    InvestHerApp().run()
