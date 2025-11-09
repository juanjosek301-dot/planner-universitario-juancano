from flask import Flask, render_template, send_from_directory, request, jsonify
from routes.usuario_routes import usuario_bp
from routes.curso_routes import curso_bp 
from routes.inscripciones import inscripciones_bp
from routes.actividad_routes import actividad_bp
from routes.entrega_routes import entrega_bp
from routes.montar_routes import montar_nota_bp
from routes.porgreso_routes import progreso_bp 

from flask_cors import CORS
import os
from groq import Groq
import os
from dotenv import load_dotenv

from contexto import obtener_contexto_estudiante

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)

AVAILABLE_MODELS = ["mixtral-8x7b-32768", "llama3-8b-8192", "llama3-70b-8192"]


app = Flask(
    __name__,
    template_folder="../Fronted/src/templates",  
    static_folder="../Fronted/src",              
    static_url_path=""                           
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

@app.route('/agente')
def vista_agente():
    return render_template('agente.html')

@app.route("/api/groq", methods=["POST"])
def usar_groq():
    data = request.get_json()
    prompt = data.get("prompt")
    id_estudiante = data.get("id_estudiante", 1)
    model = data.get("model")
    max_tokens = data.get("max_tokens", 512)
    temperature = data.get("temperature", 0.7)

    if not prompt or not prompt.strip():
        return jsonify({"error": "El prompt no puede estar vacío"}), 400

    contexto = obtener_contexto_estudiante(id_estudiante)
    prompt_con_contexto = f"{contexto}\n\nPregunta del estudiante: {prompt}"

    modelos = [model] if model else AVAILABLE_MODELS
    last_error = None

    for modelo in modelos:
        try:
            response = groq_client.chat.completions.create(
                model=modelo,
                messages=[
                    {"role": "system", "content": "Eres un asistente académico que responde con base en el contexto del estudiante."},
                    {"role": "user", "content": prompt_con_contexto}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return jsonify({
                "text": response.choices[0].message.content,
                "model": modelo,
                "tokens": response.usage.total_tokens,
                "finish_reason": response.choices[0].finish_reason
            })
        except Exception as e:
            print("🚨 Error con modelo", modelo, ":", e)
            last_error = str(e)
            continue

    return jsonify({"error": f"No se pudo generar respuesta. Último error: {last_error}"}), 502
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)