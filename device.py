import os
import sys
import time
import webview
import threading

from skabenclient.device import BaseDevice
from config import KonsoleConfig
from web.app import run_flask_app
from contextlib import redirect_stdout
from io import StringIO


class KonsoleDevice(BaseDevice):

    """ Test device should be able to generate all kind of messages

        state_reload -> загрузить текущий конфиг из файла
        state_update(data) -> записать конфиг в файл (и послать на сервер)
        send_message(data) -> отправить сообщение от имени девайса во внутреннюю очередь
    """

    config_class = KonsoleConfig
    GUI = 'qt'  # qt or gtk

    def __init__(self, system_config, device_config, **kwargs):
        super().__init__(system_config, device_config)
        self.running = None

    @staticmethod
    def start_webserver():
        ft = threading.Thread(target=run_flask_app,
                              daemon=True)
        ft.start()

    def start_webclient(self):
        webview.create_window('TERMINAL',
                              "http://127.0.0.1:5000/",
                              fullscreen=False,
                              width=1024,
                              height=780
                              )
        webview.start(gui=self.GUI)

    def run(self):
        """ Main device run routine """
        super().run()
        self.running = True

        try:
            stream = StringIO()
            with redirect_stdout(stream):
                self.start_webserver()
                self.start_webclient()
        except Exception:
            raise
