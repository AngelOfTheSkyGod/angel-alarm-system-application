# filename: kivy_with_rest.py

import socket
import threading

from flask import Flask, jsonify, request
from kivy.app import App
from kivy.config import Config
from kivy.uix.label import Label
import numpy as np
from PIL import Image
# Config.set('graphics', 'fullscreen', 'auto')  # use 'auto' to match display resolution
# -- REST server side (Flask) --
flask_app = Flask(__name__)
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # connect to a public IP (does not send data) just to get the OS to fill in the local IP
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

print("Local IP address:", get_local_ip())
@flask_app.route('/ping', methods=['POST'])
def hello():

    data = request.get_json(silent=True)  # returns a dict if JSON, else None
    print("body: " + str(data));
    img = Image.fromarray(data["slideShowData"][0]["imageArray"])
    img.show()

    return jsonify({"message": "ping!"})

def run_server():
    # run on localhost:5000 — change host/port if needed
    flask_app.run(host="0.0.0.0", port=80, debug=False)

# -- Kivy GUI side --
class MyKivyApp(App):
    def build(self):
        # simple UI showing a message
        return Label(text="app")

if __name__ == '__main__':
    # start the Flask server in a background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    import requests

    #     private String deviceName;
    # private String password;
    # private String ipAddress;
    dictToSend = {'deviceName':'angelpi0', 'password': 'password123', 'ipAddress': get_local_ip()}
    res = requests.post('http://quinonesangel.com:1312/connectDevice', json=dictToSend)
    print('response from server:',res.text)

    # run the Kivy app (main GUI loop)
    MyKivyApp().run()