from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle


class Avatar(Widget):
    def __init__(self, **kwargs):
        super(Avatar, self).__init__(**kwargs)
        with self.canvas:
            # Draw the light yellow circle
            Color(0.984, 0.984, 0.898, 1)  # FBFBE5 color
            self.circle = Ellipse(size=(120, 120))

            # Draw the black outline
            Color(0, 0, 0, 1)  # Black color
            self.line = Line(circle=(60, 60, 60), width=2)

        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        self.circle.pos = (self.center_x - 60, self.center_y - 60)
        self.line.circle = (self.center_x, self.center_y, 60)


class SingleBar(BoxLayout):
    def __init__(self, percentage, **kwargs):
        super(SingleBar, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 30
        self.padding = [0, 5, 0, 5]
        self.spacing = 5
        self.percentage = percentage

        # Draw background rectangle
        with self.canvas.before:
            Color(0.85, 0.85, 0.85, 1)  # D9D9D9 color
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Create the single smaller bar
        self.create_bar()

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def create_bar(self):
        bar = BoxLayout(size_hint=(self.percentage, 1))
        with bar.canvas.before:
            Color(0.984, 0.984, 0.898, 1)  # FBFBE5 color for smaller bar
            bar.rect = Rectangle(size=bar.size, pos=bar.pos)
        bar.bind(pos=self.update_bar_rect, size=self.update_bar_rect)
        self.add_widget(bar)

    def update_bar_rect(self, instance, value):
        instance.rect.size = instance.size
        instance.rect.pos = instance.pos


class FinanceApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Background color
        with root.canvas.before:
            Color(0.922, 0.7647, 0.8078, 1)  # EBC3CE color in RGBA
            self.rect = Rectangle(size=root.size, pos=root.pos)
        root.bind(size=self.update_rect, pos=self.update_rect)

        # Top profile section
        top_section = BoxLayout(orientation='vertical', size_hint_y=None, height=250, padding=10, spacing=10)

        avatar_box = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, None), height=150)
        avatar = Avatar(size_hint=(None, None), size=(120, 120))
        avatar_box.add_widget(avatar)

        name_label_box = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, None), height=30)
        name_label = Label(text="Name:", color=[0, 0, 0, 1])
        name_label_box.add_widget(name_label)

        balance_label_box = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, None), height=30)
        balance_label = Label(text="Current Balance: $209", color=[0, 0, 0, 1])
        balance_label_box.add_widget(balance_label)

        top_section.add_widget(avatar_box)
        top_section.add_widget(name_label_box)
        top_section.add_widget(balance_label_box)

        root.add_widget(top_section)

        # Middle button section
        button_menu = GridLayout(cols=4, size_hint_y=None, height=80, spacing=250)

        # Ensure uniform button width
        button_width = 180
        button_height = 70

        customize_btn = Button(text="Customize\nAvatar", size_hint=(None, None), size=(button_width, button_height))
        stocks_btn = Button(text="Check your\nstocks", size_hint=(None, None), size=(button_width, button_height))
        bank_btn = Button(text="Check bank\nstatement", size_hint=(None, None), size=(button_width, button_height))
        earnings_btn = Button(text="Earnings", size_hint=(None, None), size=(button_width, button_height))

        button_menu.add_widget(customize_btn)
        button_menu.add_widget(stocks_btn)
        button_menu.add_widget(bank_btn)
        button_menu.add_widget(earnings_btn)

        root.add_widget(button_menu)

        # Lower section for stats and Play button
        lower_section = BoxLayout(orientation='vertical')

        stats_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.6), padding=10)
        labels_layout = BoxLayout(orientation='vertical', size_hint=(0.4, 1), padding=[10, 0, 0, 0])
        health_label = Label(text="Health", halign='left', size_hint_y=None, height=40, color=[0, 0, 0, 1])
        confidence_label = Label(text="Confidence", halign='left', size_hint_y=None, height=40, color=[0, 0, 0, 1])
        relationships_label = Label(text="Relationships", halign='left', size_hint_y=None, height=40, color=[0, 0, 0, 1])
        labels_layout.add_widget(health_label)
        labels_layout.add_widget(confidence_label)
        labels_layout.add_widget(relationships_label)

        bars_layout = BoxLayout(orientation='vertical', size_hint=(0.6, 1), padding=[10, 0, 10, 0])
        health_bar = SingleBar(percentage=0.33)
        confidence_bar = SingleBar(percentage=0.90)
        relationships_bar = SingleBar(percentage=0.65)
        bars_layout.add_widget(health_bar)
        bars_layout.add_widget(confidence_bar)
        bars_layout.add_widget(relationships_bar)

        stats_layout.add_widget(labels_layout)
        stats_layout.add_widget(bars_layout)
        lower_section.add_widget(stats_layout)

        play_button_box = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_y=None, height=70)
        play_btn = Button(text="Play", size_hint=(None, None), size=(180, 60))
        play_button_box.add_widget(play_btn)
        lower_section.add_widget(play_button_box)

        root.add_widget(lower_section)

        return root

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos


if __name__ == '__main__':
    FinanceApp().run()
