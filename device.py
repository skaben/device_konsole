import webview
import threading

from io import StringIO
from contextlib import redirect_stdout
from flask import jsonify
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

    pages = {
        "main": "main",
        "menu": "menu",
        "hack": "hack"
    }

    cmd_test = "cmd_test"
    cmd_switch = "cmd_switch"
    cmd_send = "cmd_send"

    def __init__(self, system_config, device_config):
        super().__init__(system_config, device_config)
        self.running = None
        self.socketio = SocketIO(flask_app, path=self.ws_path, ping_interval=1)
        # events from frontend
        self.socketio.on_event("gamewin", self.game_win)
        self.socketio.on_event("gamelose", self.game_lose)
        #self.socketio.on_event("fetch", self.api_data)
        self.socketio.on_event("testws", self.testws)

    def get_mode(self) -> dict:
        """get workmode for current alert state and terminal status (hacked|normal)"""
        result = {}
        current_state = self.config.get('alert', '0')
        mode_type = 'external' if self.config.get('hacked') else 'normal'
        mode_switch = self.config.get('mode_switch')
        all_modes = self.config.get('mode_list', {})
        if mode_switch:
            current_switch = mode_switch.get(current_state)
            if current_switch:
                result = all_modes.get(current_switch.get(mode_type, '0'), {})
        return result

    def api_menu(self):
        mode = self.get_mode()
        data = mode.get('menu_set', [])
        return jsonify(data)

    def api_main(self):
        mode = self.get_mode()
        data = {
            'header': mode.get('header'),
            'footer': mode.get('footer'),
            'blocked': self.config.get('blocked'),
            'powered': self.config.get('powered')
        }
        return jsonify(data)

    def api_hack(self):
        return jsonify({})

    def testws(self):
        self.logger.info('receive test, reply with full config')
        self.socketio.emit(self.cmd_test, self.config.data)

    def game_win(self):
        self.logger.info("[!] terminal game solved")
        self.state_update({"hacked": True})
        self.switch_page('menu')
        self.logger.debug(self.config.data)

    def game_lose(self):
        self.logger.info("[!] terminal game solved")
        self.state_update({"blocked": True})
        self.switch_page('main')
        self.logger.debug(self.config.data)

    def switch_page(self, page_name: str):
        page = self.pages.get(page_name)
        if not page:
            self.logger.error(f'no route for page {page_name}')
        self.socketio.emit(self.cmd_switch, {"data": page})

    def start_webserver(self):
        """start flask app in separate thread"""
        flask_app.add_url_rule('/api/menu', view_func=self.api_menu)
        flask_app.add_url_rule('/api/main', view_func=self.api_main)
        flask_app.add_url_rule('/api/hack', view_func=self.api_hack)

        def flask_io():
            return self.socketio.run(flask_app)

        ft = threading.Thread(target=flask_io,
                              daemon=True)
        ft.start()

    def start_webclient(self):
        """start pywebview web-client in main thread"""
        webview.create_window('TERMINAL',
                              self.host,
                              fullscreen=False,
                              width=1024,
                              height=780
                              )
        webview.start(gui=self.GUI)

    def run(self):
        """device run routine"""
        super().run()
        self.running = True

        try:
            stream = StringIO()
            with redirect_stdout(stream):
                self.start_webserver()
                self.start_webclient()
        except Exception:
            raise
