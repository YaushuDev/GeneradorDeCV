from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

CV_DATA_FILE = 'cv_data.json'

def load_data():
    if os.path.exists(CV_DATA_FILE):
        try:
            with open(CV_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data_to_file(data):
    try:
        with open(CV_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html', title="Generador de CV")

@app.route('/get_cv_data', methods=['GET'])
def get_cv_data():
    data = load_data()
    return jsonify(data)

@app.route('/save_cv_data', methods=['POST'])
def save_cv_data():
    data = request.json
    if save_data_to_file(data):
        return jsonify({"success": True})
    return jsonify({"success": False}), 500

@app.route('/perfil')
def profile():
    return render_template('page.html', title="Perfil", content="Esta es la página de perfil.")

@app.route('/configuracion')
def settings():
    return render_template('page.html', title="Configuración", content="Ajustes y preferencias aquí.")

if __name__ == '__main__':
    app.run(debug=True)
