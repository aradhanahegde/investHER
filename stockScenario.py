from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

class stockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=20, padding=20)

        eligibility_label = Label(text="Congratulations! You are eligible to invest in stocks.",
                                  font_size=24, size_hint=(1, 0.2))

        # Placeholder for stock market API
        stock_placeholder = Widget(size_hint=(1, 0.5))
        with stock_placeholder.canvas.before:
            Color(0.8, 0.8, 0.8, 1)  
            self.rect = Rectangle(size=stock_placeholder.size, pos=stock_placeholder.pos)


        stock_placeholder.bind(size=self.update_rect, pos=self.update_rect)

        learn_more_button = Button(text="Learn More About Investing", size_hint=(1, 0.1))
        learn_more_button.bind(on_press=self.learn_more)

        invest_button = Button(text="I'm Ready to Invest", size_hint=(1, 0.1))
        invest_button.bind(on_press=self.start_investing)


        layout.add_widget(eligibility_label)
        layout.add_widget(stock_placeholder)
        layout.add_widget(learn_more_button)
        layout.add_widget(invest_button)

        self.add_widget(layout)

    def update_rect(self, instance, value):
        """Update rectangle size when widget resizes."""
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def learn_more(self, instance):
        """Navigate to an Investing Info Screen."""
        self.manager.current = "learnMore"

    def start_investing(self, instance):
        """Navigate to an Investment Platform Screen."""
        self.manager.current = "invest"



