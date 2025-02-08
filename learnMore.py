from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

class learnMoreScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        # Investing information text
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

        self.info_label = Label(
            text=investing_text,
            size_hint_y=None, 
            height=200, 
            font_size=18
        )
        self.info_label.bind(texture_size=self.update_label_height)
        self.info_label.text_size = (500, None)

        layout = BoxLayout(orientation='vertical')
        scroll_view = ScrollView(size_hint=(1, None), size=(800, 400))
        scroll_view.add_widget(self.info_label)

        back_button = Button(text="Back", size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)

        next_button = Button(text="I'm Ready to Invest", size_hint=(1, 0.1))
        next_button.bind(on_press=self.go_to_investment)


        layout.add_widget(scroll_view)
        layout.add_widget(back_button)
        layout.add_widget(next_button)

        self.add_widget(layout)

    def update_label_height(self, instance, value):
        instance.height = instance.texture_size[1]

    def go_back(self, instance):
        self.manager.current = "stock"

    def go_to_investment(self, instance):
        #connect to Nimrat's page
        self.manager.current = "invest"


