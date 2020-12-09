import os
from flask import send_from_directory

static_dir = os.path.join(os.path.dirname(__file__), 'static')
assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')


def send_from(dirname, path, root=static_dir):
    _dir = os.path.join(root, dirname)
    return send_from_directory(_dir, path)


def send_js(path):
    return send_from('js', path)


def send_css(path):
    return send_from('css', path)


def send_font(path):
    return send_from('fonts', path)


def send_sound(path):
    return send_from('sounds', path)


def send_image(path):
    return send_from('images', path)


def send_asset_sound(path):
    return send_from('audio', path, assets_dir)


def send_asset_image(path):
    return send_from('image', path, assets_dir)


def send_asset_text(path):
    return send_from('text', path, assets_dir)


def send_asset_video(path):
    return send_from('video', path, assets_dir)
