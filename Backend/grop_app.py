from flask import Flask, request, jsonify
from groq import Groq
import os
from dotenv import load_dotenv

# 🔐 Cargar la API Key desde .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# 📦 Inicializar cliente Groq
client = Groq(api_key=GROQ_API_KEY)

# 🧠 Modelos disponibles
AVAILABLE_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-70b-versatile",
    "mixtral-8x7b-32768",
    "llama-3.1-8b-instant"
]

# 🚀 Inicializar Flask
app = Flask(__name__)

@app.route("/api/groq", methods=["POST"])
def usar_groq():
    data = request.get_json()
    prompt = data.get("prompt")
    model = data.get("model")
    max_tokens = data.get("max_tokens", 512)
    temperature = data.get("temperature", 0.7)

    if not prompt or not prompt.strip():
        return jsonify({"error": "El prompt no puede estar vacío"}), 400

    modelos = [model] if model else AVAILABLE_MODELS
    last_error = None

    for modelo in modelos:
        try:
            response = client.chat.completions.create(
                model=modelo,
                messages=[{"role": "user", "content": prompt}],
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
            last_error = str(e)
            continue

    return jsonify({"error": f"No se pudo generar respuesta. Último error: {last_error}"}), 502

# 🧪 Ruta para listar modelos
@app.route("/api/groq/models", methods=["GET"])
def listar_modelos():
    return jsonify({
        "models": AVAILABLE_MODELS,
        "count": len(AVAILABLE_MODELS),
        "provider": "Groq"
    })

if __name__ == "__main__":
    app.run(debug=True)
