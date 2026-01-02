from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title="Inicio")

@app.route('/perfil')
def profile():
    return render_template('page.html', title="Perfil", content="Esta es la página de perfil.")

@app.route('/configuracion')
def settings():
    return render_template('page.html', title="Configuración", content="Ajustes y preferencias aquí.")

if __name__ == '__main__':
    app.run(debug=True)
