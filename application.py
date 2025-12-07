# filename: kivy_with_rest.py

import threading

from flask import Flask, jsonify
from kivy.app import App
from kivy.config import Config
from kivy.uix.label import Label

Config.set('graphics', 'fullscreen', 'auto')  # use 'auto' to match display resolution
# -- REST server side (Flask) --
flask_app = Flask(__name__)

@flask_app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from Flask + Kivy!"})

def run_server():
    # run on localhost:5000 — change host/port if needed
    flask_app.run(host='127.0.0.1', port=5000, debug=False)

# -- Kivy GUI side --
class MyKivyApp(App):
    def build(self):
        # simple UI showing a message
        return Label(text="Kivy GUI running — check http://localhost:5000/hello")

if __name__ == '__main__':
    # start the Flask server in a background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # run the Kivy app (main GUI loop)
    MyKivyApp().run()