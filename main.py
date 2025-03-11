__version__ = "1.0.0"

import os
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

kivy.require('2.3.1')
os.environ['KIVY_TEXT'] = 'pil'

log_folder = "log"
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, "main.log")

tmp_folder = "./tmp"
os.makedirs(tmp_folder, exist_ok=True)

class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

class matcoinapp(App):
    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    matcoinapp().run()
