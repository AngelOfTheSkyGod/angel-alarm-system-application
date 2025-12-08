# filename: kivy_with_rest.py

import socket
import threading

from flask import Flask, jsonify, request
from kivy.app import App
from kivy.config import Config
from kivy.uix.label import Label
import numpy as np
import base64
from io import BytesIO
from PIL import Image
from pathlib import Path
import os
import requests
# Config.set('graphics', 'fullscreen', 'auto')  # use 'auto' to match display resolution

imageCount = 0
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

def base64_to_pil(base64_string):
    if base64_string.startswith("data:"):
        base64_string = base64_string.split(",")[1]

    image_bytes = base64.b64decode(base64_string)
    return Image.open(BytesIO(image_bytes))

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
    
print("Local IP address:", get_local_ip())
@flask_app.route('/ping', methods=['POST'])
def hello():

    # returns a dict if JSON, else None
    data = request.get_json(silent=True)
    current_directory = os.getcwd()
    newpath = current_directory + r'\slideShowImages' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    img = base64_to_pil(data["slideShowData"][0]["imageDataUrl"])
    print(data["slideShowData"][0]["imageDataUrl"][:100])
    img_700 = img.resize((700, 700))
    img_700.save("output_700x700.jpg")
    print("Saved image → received.jpg")

    return jsonify({"message": "ping!"})

@flask_app.route('/connect', methods=['POST'])
def connect():
    current_directory = os.getcwd()
    path = current_directory + r'/slideShowImages' 
    print("path", path);
    directory = Path(path)
    imageList = [];
    count = 0;
    for entry in directory.iterdir():
        if (count >= 3):
            break;
        if entry.is_file():
            count += 1;
            imageList.append(image_to_base64(entry.absolute()))
            print("File:", entry)
    imageCount = count;
    return jsonify({"imageCount": imageCount, "imageList": imageList})

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
    current_directory = os.getcwd()
    path = current_directory + r'\slideShowImages' 
    if not os.path.exists(path):
        os.makedirs(path)
    dictToSend = {'deviceName':'angelpi0', 'password': 'password123', 'ipAddress': get_local_ip()}
    res = requests.post('http://quinonesangel.com:1312/connectDevice', json=dictToSend)
    print('response from server:',res.text)

    # run the Kivy app (main GUI loop)
    MyKivyApp().run()