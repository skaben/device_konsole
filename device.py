import webview
import threading

from io import StringIO
from contextlib import redirect_stdout
from flask_socketio import SocketIO

from skabenclient.device import BaseDevice
from web.app import app as flask_app
from config import KonsoleConfig


class KonsoleDevice(BaseDevice):

    """ Test device should be able to generate all kind of messages

        state_reload -> загрузить текущий конфиг из файла
        state_update(data) -> записать конфиг в файл (и послать на сервер)
        send_message(data) -> отправить сообщение от имени девайса во внутреннюю очередь
    """

    GUI = 'qt'  # qt or gtk
    # TODO: move to config
    host = "http://127.0.0.1:5000/"
    ws_path = "ws"
    config_class = KonsoleConfig

    def __init__(self, system_config, device_config):
        super().__init__(system_config, device_config)
        self.running = None
        self.socketio = SocketIO(flask_app, path=self.ws_path)
        self.socketio.on_event("testws", self.testws)

    def testws(self):
        self.logger.info("IT WORKS")

    def start_webserver(self):

        def flask_io():
            return self.socketio.run(flask_app)

        ft = threading.Thread(target=flask_io,
                              daemon=True)
        ft.start()

    def start_webclient(self):
        webview.create_window('TERMINAL',
                              self.host,
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
