import os
import time
import threading

import subprocess

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
        "menu": "menu",
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
        self.resolution = system_config.get("resolution", (1024, 768))
        self.fullscreen = system_config.get("fullscreen", False)
        self.is_master = system_config.get("is_master")
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
        self.socketio.on_event("block", self.block)
        self.socketio.on_event("user-input", self.user_input)
        self.socketio.on_event("console", self.send_console)
        return self.socketio

    def send_console(self, payload):
        message = payload.get("message")
        if self.is_master and message:
            message = message.upper()
        self.send_message({
            "type": "console",
            "response": self.is_master,
            "content": message
        })

    def user_input(self, payload):
        self.logger.info(f'received user input: {payload}')
        self.send_message({
            "type": "input",
            "content": payload.get("action"),
            "success": payload.get("success")
        })

    def get_mode(self) -> dict:
        """get workmode for current alert state and terminal status (hacked|normal)"""
        result = {}
        try:
            result = self.config.get_mode()
        except Exception:
            self.logger.exception('while getting mode: ')
            self.state_update({'blocked': True})
        finally:
            return result

    def api_menu(self):
        self.logger.debug('MENU requested')
        mode_data = self.config.parse_menu(self.get_mode())
        self.logger.debug(f'MODE: {mode_data}')
        return jsonify(mode_data or [])

    def api_main(self):
        mode = self.get_mode()
        data = {
            "header": mode.get("header"),
            "footer": mode.get("footer"),
            "blocked": self.config.get("blocked", False),
            "powered": self.config.get("powered", True),
            "timeout": self.config.get("timeout", 0),
            "alert": self.config.get("alert"),
            'shape': mode.get('shape')
        }
        return jsonify(data)

    def api_hack(self):
        self.logger.info('GAME requested')
        result = {}
        mode_data = self.config.parse_menu(self.get_mode())
        data = [i for i in mode_data if i.get('type') == 'game'] or ['',]
        conf = data[0]
        if conf:
            game_conf = conf.get('data')
            word_dir = os.path.join(self.config.system.root, 'resources', 'wordsets', self.wordset_type)
            word_gen = WordGen(word_dir, game_conf['wordcount'], game_conf['difficulty'])
            result = {
                "words": word_gen.words,
                "password": word_gen.password,
                "tries": game_conf['attempts'],
                "timeout": conf['timer'],
                "chance": game_conf['chance'],
                "header": f'процедура `{conf["name"]}` запущена',
                "footer": 'доступ без авторизации строго воспрещен'
            }
            self.logger.info(result)
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
        self.send_message({
            "type": "hack",
            "success": False
        })
        self.switch_page("main")

    def block(self):
        self.logger.debug('blocking...')
        self.state_update({"blocked": True})
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

    def start_kiosk(self):
        subprocess.run(["killall", "firefox"])
        subprocess.run(["firefox", "--kiosk", "http://127.0.0.1:5000", "--fullscreen"])

    def run(self):
        """device run routine"""
        super().run()
        self.running = True

        try:
            stream = StringIO()
            with redirect_stdout(stream):
                self.start_webserver()
                if self.headless:
                    while self.running:
                        time.sleep(100)
                else:
                    self.start_kiosk()
        except Exception as e:
            raise
