from flask import Flask, send_from_directory
from flask_cors import CORS
from controllers.controllerChat import chat_bp
from config.settings import HOST, PORT, DEBUG

app = Flask(__name__, static_folder='static') 
CORS(app) 

app.register_blueprint(chat_bp)

@app.route('/')
def serve_index():
    """Serve o arquivo HTML principal da pasta static"""
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)