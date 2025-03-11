__version__ = "1.0.0"

import os
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
import logging 
from rich.logging import RichHandler
import asyncio
from modules import db_funcs

kivy.require('2.3.0')
os.environ['KIVY_TEXT'] = 'pil'

log_folder = "log"
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, "main.log")

tmp_folder = "./tmp"
os.makedirs(tmp_folder, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(),
        logging.FileHandler(log_file, encoding="utf-8")
    ]
)

logger = logging.getLogger("rich")

tmp_folder = "./tmp"
os.makedirs(tmp_folder, exist_ok=True)

logging.info("Starting the application...")

class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='Имя пользователя: '))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='Пароль: '))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

        self.login_button = Button(text="Войти")
        self.login_button.bind(on_press=self.login_button_callback)
        self.add_widget(self.login_button)

    def login_button_callback(self, _):
        username = self.username.text
        password = self.password.text
        if username and password:
            asyncio.run(self.handle_login(username, password))
        else:
            self.show_popup("Заполните все поля", "OK")

    async def handle_login(self, username, password):
        result = await db_funcs.login_to_app(username, password)
        if result:
            self.show_popup("Вы успешно вошли", "OK")
        else:
            self.show_popup("Неправильный логин или пароль", "OK")

    def show_popup(self, message, button_text):
        layout = BoxLayout(orientation='vertical')
        label = Label(text=message)
        button = Button(text=button_text)
        button.bind(on_press=self.close_popup)
        layout.add_widget(label)
        layout.add_widget(button)

        self.popup = Popup(title='', content=layout, size_hint=(0.6, 0.4))
        self.popup.open()

    def close_popup(self, instance):
        self.popup.dismiss()

# Главный класс приложения
class matcoinapp(App):
    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    matcoinapp().run()