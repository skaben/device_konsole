import json
import webview
from flask import render_template, jsonify, request


def index():
    return render_template('index.html', token=webview.token)


def gamedata():
    data = {
        "words": ['AARDVARK', "TESTWORD", "WORDTEST", "VAARDARK", "TESTTEST", "WORDWORD", "ESTESTTT"],
        "password": "PASSWORD",
        "tries": 4,
        "timeout": 0,
        "cheatChance": 20,
        "cheatRemove": 10,
        "cheatRestore": 50,
        "text_header": 'text in header',
        "text_footer": 'text in footer'
    }
    return jsonify(data)


def menu():
    data = [
        ["hack", "gain access"],
        ["menu", "main menu"],
        ["main", "show loading screen"]
    ]
    return jsonify(data)


def device():
    data = {
        "blocked": False,
        "online": True,
        "powered": True,
        "sound": True,
        "header": "terminal konsole flask test",
        "footer": "terminal footer"
    }
    return jsonify(data)


def api():
    data = json.loads(request.data)
    if data.get('gamewin'):
        result = {"switchpage": "menu"}
    else:
        result = {"switchpage": "main"}
    return jsonify(result)
