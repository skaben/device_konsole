import json
import os
import webbrowser
from functools import wraps

from flask import Flask, render_template, request
from werkzeug.wrappers import BaseResponse as Response

import webview
from . import webapi

webview.gui = 'gtk'

static_dir = os.path.join(os.path.dirname(__file__), 'static')
template_dir = os.path.join(os.path.dirname(__file__), 'templates')

for _dir in (static_dir, template_dir):
    if not os.path.exists(_dir):
        raise FileNotFoundError(f'missing directory: {_dir}')


app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1  # disable caching


def verify_token(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        data = json.loads(request.data)
        token = data.get('token')
        if token == webview.token:
            return function(*args, **kwargs)
        else:
            raise Exception('Authentication error')

    return wrapper


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


@app.route('/')
def root():
    """
    Render index.html. Initialization is performed asynchronously in initialize() function
    """
    return render_template('index.html', token=webview.token)


@app.route('/init', methods=['POST'])
@verify_token
def initialize():
    '''
    Perform heavy-lifting initialization asynchronously.
    :return:
    '''
    can_start = webapi.initialize()

    if can_start:
        return Response('ok', status=200)
    else:
        return Response('error', status=500)


@app.route('/fullscreen', methods=['POST'])
@verify_token
def fullscreen():
    webview.windows[0].toggle_fullscreen()
    return Response('', status=200)
