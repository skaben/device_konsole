import os

from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin

from . import views
from . import serve

template_dir = os.path.join(os.path.dirname(__file__), 'static')


app = Flask(__name__,
            static_url_path='',
            template_folder=template_dir)

CORS(app, supports_credentials=True)

app.config['CORS_HEADERS'] = ['Content-Type', 'application/json']
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1  # disable caching

socketio = SocketIO(app, path="/ws")

# URLs

app.add_url_rule('/', view_func=views.index)
# serve static the dumb way
app.add_url_rule('/js/<path:path>', view_func=serve.send_js)
app.add_url_rule('/css/<path:path>', view_func=serve.send_css)
app.add_url_rule('/fonts/<path:path>', view_func=serve.send_fonts)
app.add_url_rule('/sounds/<path:path>', view_func=serve.send_sounds)
# api
app.add_url_rule('/api/event', view_func=views.api, methods=["POST", "PUT"])
app.add_url_rule('/api/menu', view_func=views.menu)
app.add_url_rule('/api/device', view_func=views.device)
app.add_url_rule('/api/hack', view_func=views.gamedata)


@app.errorhandler(404)
def page_not_found(e):
    return views.index()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """ catch all for serving JS CSR """
    return views.index()


def run_flask_app():
    return socketio.run(app)
