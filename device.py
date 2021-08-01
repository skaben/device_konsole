import os
import time
import webview
import threading

from io import StringIO
from contextlib import redirect_stdout
from flask import jsonify
from flask_socketio import SocketIO

from skabenclient.device import BaseDevice

from web.app import app as flask_app
from web.helpers import cors_origins
from config import KonsoleConfig
from helpers import WordGen


class KonsoleDevice(BaseDevice):

    """ Test device should be able to generate all kind of messages

        state_reload -> загрузить текущий конфиг из файла
        state_update(data) -> записать конфиг в файл (и послать на сервер)
        send_message(data) -> отправить сообщение от имени девайса во внутреннюю очередь
    """

    config_class = KonsoleConfig
    ws_path = "ws"

    pages = {
        "load": "load",
        "hack": "hack",
        "main": "main"
    }

    cmd_test = "cmd_test"
    cmd_switch = "cmd_switch"
    cmd_send = "cmd_send"

    word_gen = None
    wordset_type = 'default'

    def __init__(self, system_config, device_config):
        super().__init__(system_config, device_config)
        self.running = None
        self.headless = system_config.get("headless")
        self.host = system_config.get("host", "http://127.0.0.1:5000/")
        self.gui = system_config.get("gui", "qt")
        self.resolution = system_config.get("resolution", (1024, 768))
        self.fullscreen = system_config.get("fullscreen", False)
        self.resources_dir = os.path.join(system_config.root,
                                          system_config.get('asset_root'))
        self.init_socketio()

    def init_socketio(self):
        self.socketio = SocketIO(flask_app,
                                 path=self.ws_path,
                                 ping_interval=1,
                                 cors_allowed_origins=cors_origins)
        # events from frontend
        self.socketio.on_event("gamewin", self.game_win)
        self.socketio.on_event("gamelose", self.game_lose)
        self.socketio.on_event("unblock", self.unblock)
        #self.socketio.on_event("fetch", self.api_data)
        self.socketio.on_event("testws", self.testws)
        return self.socketio

    def get_mode(self) -> dict:
        """get workmode for current alert state and terminal status (hacked|normal)"""
        result = {}
        try:
            current_state = self.config.get("alert")
            mode_type = "extended" if self.config.get("hacked") else "normal"
            if not current_state:
                raise Exception('no current state - blocking!')
            mode_switch = self.config.get_mode_switch()
            all_modes = self.config.get("menu", {})
            if mode_switch and all_modes:
                current_switch = mode_switch.get(current_state)
                if current_switch:
                    mode_id = current_switch.get(mode_type)
                    result = all_modes.get(mode_id)
                else:
                    raise Exception('blocking')
        except Exception:
            self.logger.exception('while getting mode: ')
            self.state_update({'blocked': True})
        finally:
            return result

    def api_menu(self):
        self.logger.debug('MENU requested')
        mode = self.get_mode()
        data = mode.get("menu_set")
        self.logger.debug(f'MODE: {mode}')
        return jsonify(data or {})

    def api_main(self):
        self.logger.debug('MAIN requested')
        mode = self.get_mode()
        data = {
            "header": mode.get("header"),
            "footer": mode.get("footer"),
            "blocked": self.config.get("blocked", False),
            "powered": self.config.get("powered", True),
            "timeout": self.config.get("timeout", 0)
        }
        return jsonify(data)

    def api_hack(self):
        self.logger.info('GAME requested')
        game_data = [data for data in self.get_mode().get('menu_set')
                     if isinstance(data, dict) and data.get('type') == 'game']

        if game_data:
            data = game_data[0]
            hack = data.get('data')
            # word_dir = os.path.join(self.resources_dir, 'wordsets', self.wordset_type)
            word_dir = os.path.join(self.config.system.root, 'resources', 'wordsets', self.wordset_type)
            word_gen = WordGen(word_dir, hack['wordcount'], hack['difficulty'])
            result = {
                "words": word_gen.words,
                "password": word_gen.password,
                "tries": hack['attempts'],
                "timeout": data['timer'],
                "chance": hack['chance'],
                "header": 'процедура эскалации запущена',
                "footer": 'доступ без авторизации строго воспрещен'
            }
            self.logger.debug(result)
            return jsonify(result)

    def testws(self):
        self.logger.info("receive test, reply with full config")
        self.socketio.emit(self.cmd_test, self.config.data)

    def game_win(self):
        self.logger.info("[!] terminal game solved")
        self.state_update({"hacked": True})
        self.switch_page("main")

    def game_lose(self):
        self.logger.info("[!] terminal game not solved")
        self.state_update({"blocked": True})
        self.send_message({"message": "access denied"})
        self.switch_page("main")

    def unblock(self):
        self.logger.debug('unblocking...')
        self.state_update({"blocked": False})
        self.switch_page("main")

    def switch_page(self, page_name: str):
        if not self.headless:
            page = self.pages.get(page_name)
            if not page:
                self.logger.error(f"no route for page {page_name}")
            self.socketio.emit(self.cmd_switch, {"data": page})

    def start_webserver(self):
        """start flask app in separate thread"""
        flask_app.add_url_rule("/api/menu", view_func=self.api_menu)
        flask_app.add_url_rule("/api/main", view_func=self.api_main)
        flask_app.add_url_rule("/api/hack", view_func=self.api_hack)

        def flask_io():
            return self.socketio.run(flask_app)

        ft = threading.Thread(target=flask_io,
                              daemon=True)
        ft.start()

    def start_webclient(self):
        """start pywebview web-client in main thread"""
        (width, height) = self.resolution
        webview.create_window(
            "TERMINAL",
            self.host,
            fullscreen=self.fullscreen,
            width=width,
            height=height
        )
        webview.start(gui=self.gui)

    def run(self):
        """device run routine"""
        super().run()
        self.running = True

        try:
            stream = StringIO()
            with redirect_stdout(stream):
                self.start_webserver()
                if not self.headless:
                    self.start_webclient()
                else:
                    while self.running:
                        time.sleep(100)
        except Exception:
            raise
