from flask import Flask, render_template
from routes.usuario_routes import usuario_bp
import os

# Ruta absoluta a tus carpetas externas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Frontend', 'src'))
template_path = os.path.join(base_dir, 'templates')
static_path = base_dir  # Esto incluye css/, js/, public/

app = Flask(__name__, template_folder=template_path, static_folder=static_path)

app.register_blueprint(usuario_bp)

@app.route('/')
def home():
    return render_template('Home.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True)