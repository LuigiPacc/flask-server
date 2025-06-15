from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)  # abilita accesso da Unity

BASE_DIR = "partite"

@app.route('/salva', methods=['POST'])
def salva_file():
    data = request.json
    codice = data['codice']
    filename = data['filename']
    contenuto = data['contenuto']

    dir_path = os.path.join(BASE_DIR, codice)
    os.makedirs(dir_path, exist_ok=True)

    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(contenuto, f, indent=4)

    return jsonify({"status": "ok", "message": f"{filename} salvato."})

@app.route('/stato/<codice>/<filename>', methods=['GET'])
def get_file(codice, filename):
    filepath = os.path.join(BASE_DIR, codice, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File non trovato"}), 404

    with open(filepath, 'r', encoding='utf-8') as f:
        contenuto = json.load(f)

    return jsonify(contenuto)

if __name__ == '__main__':
    os.makedirs(BASE_DIR, exist_ok=True)
    app.run(debug=True, host="0.0.0.0", port=10000)
