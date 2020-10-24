import os
from flask import send_from_directory

static_dir = os.path.join(os.path.dirname(__file__), 'static')


def send_js(path):
    js_dir = os.path.join(static_dir, 'js')
    return send_from_directory(js_dir, path)


def send_css(path):
    css_dir = os.path.join(static_dir, 'css')
    return send_from_directory(css_dir, path)


def send_fonts(path):
    font_dir = os.path.join(static_dir, 'fonts')
    return send_from_directory(font_dir, path)


def send_sounds(path):
    font_dir = os.path.join(static_dir, 'sounds')
    return send_from_directory(font_dir, path)
