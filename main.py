import threading
import json
import os
import sys
import subprocess
from time import sleep
from random import randint

from flask import Flask, send_from_directory, jsonify, request
from flask_socketio import SocketIO
from watchfiles import watch

# from utilities.read_yaml import read_yaml
# from utilities.frontend_reloader import frontend_reloader
# from helenite.backend.controller.controller import Controller

FROZEN = getattr(sys, 'frozen', False)
# NAME, VERSION, DEBUG = read_yaml()

# ----- Initial Setup -----
app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')

# ----- Routes -----
@app.route('/')
def server_index():
    return send_from_directory('app/frontend/public', 'index.html')

@app.route('/<path:path>')
def server_static_files(path):
    return send_from_directory('app/frontend/public', path)

@app.route('/node_modules/<path:path>')
def server_frontend_dependencies(path):
    return send_from_directory('app/frontend/node_modules', path)
    
@app.route('/temp_images/<path:path>')
def serve_images(path):
    return send_from_directory('app/frontend/public/temp_images', path)

def rand_generator():
    while True:
        socketio.emit('number', randint(0,100))
        sleep(0.1)

def launch_server():
    websocket_thread = threading.Thread(
    target=lambda: socketio.run(
        app,
        debug=False,
        allow_unsafe_werkzeug=True,
        use_reloader=False,
        host='0.0.0.0',
        port=5000
        )
    )
    websocket_thread.daemon = True
    websocket_thread.start()

    randint_thread = threading.Thread(target=rand_generator)
    randint_thread.start()

def main():
    controller = launch_server()
    try: 
        while True:
            sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()