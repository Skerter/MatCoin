import os
os.environ["KIVY_NO_FILELOG"] = "1"
os.environ["KIVY_NO_CONSOLELOG"] = "1"
os.environ["KIVY_LOG_LEVEL"] = "critical"
os.environ["KIVY_LOG_MODE"] = "PYTHON"

import asyncio
import logging

import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger

from modules import db_funcs
from modules.logger_config import configure_logger

log_folder = "log"
os.makedirs(log_folder, exist_ok=True)
logger = configure_logger("main")

tmp_folder = "./tmp"
os.makedirs(tmp_folder, exist_ok=True)

Logger.disabled = True
logging.getLogger("kivy").propagate = False
logging.getLogger("kivy").setLevel(logging.INFO)
    
kivy.require('2.3.0')
os.environ['KIVY_TEXT'] = 'pil'
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
        if username and password:
            logger.info(f"Вхожу в аккаунт {username}...")
            try:
                if await db_funcs.username_exists(username):
                    result = await db_funcs.login_to_app(username, password)
                else:
                    result = False
            except Exception as e:
                logger.error(f"Ошибка при выполнении запроса: {e}")
                result = False
                
            if result:
                self.show_popup("Вы успешно вошли", "OK")
            else:
                self.show_popup("Неправильный логин или пароль", "OK")
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

class matcoinapp(App):
    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    matcoinapp().run()