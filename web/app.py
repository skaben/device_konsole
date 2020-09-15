import json
import os
import webbrowser
from functools import wraps

from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.wrappers import BaseResponse as Response

import webview
from . import webapi

template_dir = os.path.join(os.path.dirname(__file__), 'static')
static_dir = os.path.join(os.path.dirname(__file__), 'static')


app = Flask(__name__,
            static_url_path='',
            template_folder=template_dir)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1  # disable caching


@app.route('/js/<path:path>')
def send_js(path):
    js_dir = os.path.join(static_dir, 'js')
    return send_from_directory(js_dir, path)


@app.route('/css/<path:path>')
def send_css(path):
    css_dir = os.path.join(static_dir, 'css')
    return send_from_directory(css_dir, path)


@app.route('/fonts/<path:path>')
def send_fonts(path):
    font_dir = os.path.join(static_dir, 'fonts')
    return send_from_directory(font_dir, path)


@app.route('/sounds/<path:path>')
def send_sounds(path):
    font_dir = os.path.join(static_dir, 'sounds')
    return send_from_directory(font_dir, path)

@app.route("/api", methods=["POST"])
def api():
    data = json.loads(request.data)
    if data.get("event"):
        print("WHEEEEEEEEE")
        return jsonify({"message": "wheeee"})

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

def get_index():
    return render_template('index.html', token=webview.token)

@app.errorhandler(404)
def page_not_found(e):
    return get_index()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """ catch all for serving JS CSR """
    return get_index()
#
#@app.route('/')
#def root():
#    """
#    Render index.html. Initialization is performed asynchronously in initialize() function
#    """
#    return render_template('index.html', token=webview.token)


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

