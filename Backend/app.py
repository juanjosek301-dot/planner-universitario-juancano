from flask import Flask, render_template
from routes.usuario_routes import usuario_bp
import os

app = Flask(
    __name__,
    template_folder="../Fronted/src/templates",  # ruta a tus HTML
    static_folder="../Fronted/src"               # ruta a tus CSS/JS
)

app.register_blueprint(usuario_bp)

@app.route('/')
def home():
    return render_template('Home.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True)