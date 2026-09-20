import datetime
import webbrowser
import urllib.parse
import ast
import operator
import os

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.video import Video
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.metrics import dp


# =========================
# CALCULATOR
# =========================

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def calculate(expression):
    try:

        def solve(node):

            if isinstance(node, ast.Constant):

                if isinstance(node.value, (int, float)):
                    return node.value

                raise ValueError

            if isinstance(node, ast.BinOp):

                op = OPERATORS.get(type(node.op))

                if op is None:
                    raise ValueError

                return op(
                    solve(node.left),
                    solve(node.right)
                )

            if isinstance(node, ast.UnaryOp):

                op = OPERATORS.get(type(node.op))

                if op is None:
                    raise ValueError

                return op(
                    solve(node.operand)
                )

            raise ValueError

        tree = ast.parse(
            expression,
            mode="eval"
        )

        return solve(tree.body)

    except Exception:
        return None


# =========================
# CHAT BUBBLE
# =========================

class ChatBubble(Label):

    def __init__(
        self,
        text,
        user=False,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.text = text

        self.font_size = dp(20)

        self.color = (
            1,
            1,
            1,
            1
        )

        self.padding = (
            dp(14),
            dp(12)
        )

        self.size_hint_y = None

        self.halign = "left"

        self.valign = "middle"

        self.text_size = (
            Window.width - dp(45),
            None
        )

        with self.canvas.before:

            if user:

                Color(
                    0.03,
                    0.25,
                    0.50,
                    0.92
                )

            else:

                Color(
                    0.03,
                    0.03,
                    0.03,
                    0.90
                )

            self.bg = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(12)]
            )

        self.bind(
            texture_size=self.update_size,
            pos=self.update_background,
            size=self.update_background
        )


    def update_size(self, *args):

        self.height = (
            self.texture_size[1]
            + dp(24)
        )


    def update_background(self, *args):

        self.bg.pos = self.pos

        self.bg.size = self.size


# =========================
# JARVIS APP
# =========================

class JarvisApp(App):

    def build(self):

        Window.clearcolor = (
            0,
            0,
            0,
            1
        )

        root = FloatLayout()


        # =========================
        # 3D VIDEO BACKGROUND
        # =========================

        video_path = os.path.join(
            os.path.dirname(__file__),
            "jarvis_3d.mp4"
        )

        if os.path.exists(video_path):

            self.background_video = Video(
                source=video_path,
                state="play",
                options={
                    "eos": "loop"
                },
                volume=0,
                allow_stretch=True,
                keep_ratio=False,
                size_hint=(1, 1),
                pos_hint={
                    "x": 0,
                    "y": 0
                }
            )

            root.add_widget(
                self.background_video
            )

        else:

            print(
                "WARNING: jarvis_3d.mp4 nahi mila."
            )


        # =========================
        # DARK TRANSPARENT OVERLAY
        # =========================

        overlay = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8),
            size_hint=(1, 1)
        )

        with overlay.canvas.before:

            Color(
                0,
                0,
                0,
                0.48
            )

            overlay_bg = RoundedRectangle(
                pos=overlay.pos,
                size=overlay.size
            )

        overlay.bind(
            pos=lambda obj, value:
            setattr(
                overlay_bg,
                "pos",
                value
            )
        )

        overlay.bind(
            size=lambda obj, value:
            setattr(
                overlay_bg,
                "size",
                value
            )
        )

        root.add_widget(
            overlay
        )


        # =========================
        # HEADER
        # =========================

        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(105)
        )

        title = Label(
            text="J A R V I S",
            font_size=dp(38),
            bold=True,
            color=(
                1,
                1,
                1,
                1
            ),
            size_hint_y=None,
            height=dp(58)
        )

        self.status = Label(
            text="● ONLINE  |  POWER MODE",
            font_size=dp(18),
            color=(
                0.2,
                1,
                0.5,
                1
            ),
            size_hint_y=None,
            height=dp(35)
        )

        header.add_widget(title)

        header.add_widget(
            self.status
        )

        overlay.add_widget(
            header
        )


        # =========================
        # CHAT AREA
        # =========================

        self.scroll = ScrollView(
            size_hint=(1, 1),
            bar_width=dp(4)
        )

        self.chat = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(5),
            size_hint_y=None
        )

        self.chat.bind(
            minimum_height=
            self.chat.setter(
                "height"
            )
        )

        self.scroll.add_widget(
            self.chat
        )

        overlay.add_widget(
            self.scroll
        )


        # =========================
        # WELCOME MESSAGE
        # =========================

        self.add_jarvis_message(
            "JARVIS: Namaste Boss! 🤖\n\n"
            "3D POWER MODE ONLINE ⚡\n"
            "System ready hai.\n\n"
            "Try:\n"
            "• time\n"
            "• date\n"
            "• youtube funny videos\n"
            "• google weather\n"
            "• calculate 25*4\n"
            "• maps\n"
            "• instagram"
        )


        # =========================
        # INPUT AREA
        # =========================

        input_area = BoxLayout(
            size_hint_y=None,
            height=dp(70),
            spacing=dp(8)
        )

        self.input_box = TextInput(
            hint_text="Boss, command likho...",
            multiline=False,
            font_size=dp(20),
            padding=[
                dp(12),
                dp(15)
            ],
            size_hint_x=0.78,
            background_color=(
                0.95,
                0.95,
                0.95,
                0.96
            ),
            foreground_color=(
                0.05,
                0.05,
                0.05,
                1
            )
        )

        self.input_box.bind(
            on_text_validate=
            self.send_command
        )


        send_button = Button(
            text="SEND",
            font_size=dp(18),
            bold=True,
            size_hint_x=0.22,
            background_normal="",
            background_color=(
                0.05,
                0.35,
                0.65,
                1
            )
        )

        send_button.bind(
            on_press=self.send_command
        )

        input_area.add_widget(
            self.input_box
        )

        input_area.add_widget(
            send_button
        )

        overlay.add_widget(
            input_area
        )


        return root


    # =========================
    # JARVIS MESSAGE
    # =========================

    def add_jarvis_message(
        self,
        text
    ):

        bubble = ChatBubble(
            text,
            user=False
        )

        self.chat.add_widget(
            bubble
        )

        self.scroll_to_bottom()


    # =========================
    # USER MESSAGE
    # =========================

    def add_user_message(
        self,
        text
    ):

        bubble = ChatBubble(
            "BOSS: " + text,
            user=True
        )

        self.chat.add_widget(
            bubble
        )

        self.scroll_to_bottom()


    # =========================
    # SCROLL
    # =========================

    def scroll_to_bottom(self):

        from kivy.clock import Clock

        Clock.schedule_once(
            lambda dt:
            setattr(
                self.scroll,
                "scroll_y",
                0
            ),
            0.15
        )


    # =========================
    # SEND COMMAND
    # =========================

    def send_command(
        self,
        *args
    ):

        command = (
            self.input_box.text.strip()
        )

        if not command:
            return

        self.input_box.text = ""

        self.add_user_message(
            command
        )

        response = self.process_command(
            command.lower()
        )

        if response:

            self.add_jarvis_message(
                response
            )


    # =========================
    # COMMAND SYSTEM
    # =========================

    def process_command(
        self,
        command
    ):

        # EXIT

        if command in [
            "exit",
            "quit",
            "stop",
            "band ho ja",
            "बंद हो जा"
        ]:

            self.status.text = (
                "● STANDBY MODE"
            )

            return (
                "JARVIS standby mode mein "
                "ja raha hai, Boss."
            )


        # GREETING

        if command in [
            "hi",
            "hello",
            "hey",
            "hii",
            "namaste",
            "नमस्ते"
        ]:

            return (
                "Namaste Boss! 😎\n"
                "3D JARVIS fully ready hai."
            )


        # TIME

        if (
            "time" in command
            or "samay" in command
            or "टाइम" in command
            or "समय" in command
        ):

            now = datetime.datetime.now()

            return (
                "Boss, abhi time hai "
                + now.strftime(
                    "%I:%M %p"
                )
            )


        # DATE

        if (
            "date" in command
            or "tarikh" in command
            or "तारीख" in command
        ):

            now = datetime.datetime.now()

            return (
                "Boss, aaj ki date hai "
                + now.strftime(
                    "%d-%m-%Y"
                )
            )


        # YOUTUBE SEARCH

        if command.startswith(
            "youtube "
        ):

            query = command[
                8:
            ].strip()

            if query:

                url = (
                    "https://www.youtube.com/results?"
                    "search_query="
                    + urllib.parse.quote(
                        query
                    )
                )

                webbrowser.open(url)

                return (
                    "YouTube par search kar raha hoon:\n"
                    + query
                )


        # YOUTUBE OPEN

        if command in [
            "youtube",
            "youtube kholo",
            "youtube khol",
            "यूट्यूब"
        ]:

            webbrowser.open(
                "https://www.youtube.com"
            )

            return (
                "YouTube khol raha hoon Boss. ▶️"
            )


        # GOOGLE SEARCH

        if command.startswith(
            "google "
        ):

            query = command[
                7:
            ].strip()

            if query:

                url = (
                    "https://www.google.com/search?q="
                    + urllib.parse.quote(
                        query
                    )
                )

                webbrowser.open(url)

                return (
                    "Google par search kar raha hoon:\n"
                    + query
                )


        # GOOGLE OPEN

        if command in [
            "google",
            "google kholo",
            "google khol"
        ]:

            webbrowser.open(
                "https://www.google.com"
            )

            return (
                "Google khol raha hoon Boss. 🔎"
            )


        # MAPS

        if (
            "maps" in command
            or "map" in command
            or "google maps" in command
        ):

            webbrowser.open(
                "https://www.google.com/maps"
            )

            return (
                "Google Maps khol raha hoon. 🗺️"
            )


        # INSTAGRAM

        if command in [
            "instagram",
            "instagram kholo",
            "इंस्टाग्राम"
        ]:

            webbrowser.open(
                "https://www.instagram.com"
            )

            return (
                "Instagram khol raha hoon Boss. 📱"
            )


        # WEATHER

        if (
            "weather" in command
            or "mausam" in command
            or "मौसम" in command
        ):

            url = (
                "https://www.google.com/search?q="
                + urllib.parse.quote(
                    command + " weather"
                )
            )

            webbrowser.open(url)

            return (
                "Weather search kar raha hoon. 🌦️"
            )


        # CALCULATOR

        if command.startswith(
            "calculate "
        ):

            expression = command[
                len("calculate "):
            ].strip()

            answer = calculate(
                expression
            )

            if answer is not None:

                return (
                    "Boss, answer hai: "
                    + str(answer)
                )

            return (
                "Boss, calculation samajh nahi aayi."
            )


        # SEARCH

        if command.startswith(
            "search "
        ):

            query = command[
                7:
            ].strip()

            if query:

                url = (
                    "https://www.google.com/search?q="
                    + urllib.parse.quote(
                        query
                    )
                )

                webbrowser.open(url)

                return (
                    "Search kar raha hoon:\n"
                    + query
                )


        # UNKNOWN COMMAND

        url = (
            "https://www.google.com/search?q="
            + urllib.parse.quote(
                command
            )
        )

        webbrowser.open(url)

        return (
            "Command ko Google par search "
            "kar raha hoon. 🔎"
        )


# =========================
# START APP
# =========================

if __name__ == "__main__":

    JarvisApp().run()