from flask import Flask, render_template, send_from_directory
from routes.usuario_routes import usuario_bp
from routes.curso_routes import curso_bp 
from routes.inscripciones import inscripciones_bp
from routes.actividad_routes import actividad_bp
from routes.entrega_routes import entrega_bp
from routes.montar_routes import montar_nota_bp
from routes.porgreso_routes import progreso_bp
import os
from flask_cors import CORS

app = Flask(
    __name__,
    template_folder="../Fronted/src/templates",  # ruta a tus HTML
    static_folder="../Fronted/src"               # ruta a tus CSS/JS
)
CORS(app)

app.register_blueprint(usuario_bp, url_prefix="/api")
app.register_blueprint(curso_bp, url_prefix='/api')
app.register_blueprint(inscripciones_bp,  url_prefix='/api')
app.register_blueprint(actividad_bp, url_prefix="/api")
app.register_blueprint(entrega_bp, url_prefix='/api' )
app.register_blueprint(montar_nota_bp)
app.register_blueprint(progreso_bp)

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/public/<path:filename>')
def public_files(filename):
    ruta_public = os.path.join(os.path.dirname(__file__), '../Fronted/src/public')
    return send_from_directory(ruta_public, filename)

@app.route('/estudiante')
def vista_estudiante():
    return render_template('vista_estudiante.html')

@app.route('/profesor')
def vista_profesor():
    return render_template('vista_profesor.html')

if __name__ == '__main__':
    print("🔍 Blueprints registrados:")
    for name, bp in app.blueprints.items():
        print(f" - {name} -> {bp.url_prefix}")
    app.run(port=5000, debug=True)
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)