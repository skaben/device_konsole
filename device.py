import os
import time
import webview

from skabenclient.device import BaseDevice
from config import KonsoleConfig
from web.app import app as flask_app
from contextlib import redirect_stdout
from io import StringIO

GUI = 'qt'


class KonsoleDevice(BaseDevice):

    """ Test device should be able to generate all kind of messages

        state_reload -> загрузить текущий конфиг из файла
        state_update(data) -> записать конфиг в файл (и послать на сервер)
        send_message(data) -> отправить сообщение от имени девайса во внутреннюю очередь
    """

    config_class = KonsoleConfig

    def __init__(self, system_config, device_config, **kwargs):
        super().__init__(system_config, device_config)
        self.running = None

    def run(self):
        """ Main device run routine """
        super().run()
        self.running = True
        stream = StringIO()
        return flask_app.run(host="0.0.0.0", debug=True)
        try:
            with redirect_stdout(stream):
                # fixme: qt autoplay
                # browser = QWebEngineView()
                # browser.page().settings().setAttribute(
                #         QWebEngineSettings.PlaybackRequiresUserGesture, False)

                window = webview.create_window('TERMINAL',
                                               flask_app,
                                               fullscreen=False,
                                               width=1024,
                                               height=780
                                               )
                webview.start(gui=GUI,
                              debug=True)
        except Exception:
            raise
