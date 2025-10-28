from flask import Blueprint, request, jsonify
from controller.entrega_controller import ControladorEntregas
from model.Entrega import Entrega
import os
from werkzeug.utils import secure_filename

entrega_bp = Blueprint('entrega_bp', __name__, url_prefix='/api')


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "docx", "doc", "txt", "jpg", "png"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ✅ Subir entrega con archivo
@entrega_bp.route('/entregas', methods=['POST'])
def crear_entrega():
    id_actividad = request.form.get("id_actividad")
    id_estudiante = request.form.get("id_estudiante")
    archivo = request.files.get("archivo")

    if not id_actividad or not id_estudiante or not archivo:
        return jsonify({"error": "Faltan datos para la entrega"}), 400

    if not allowed_file(archivo.filename):
        return jsonify({"error": "Tipo de archivo no permitido"}), 400

    # Guardar archivo en el servidor
    filename = secure_filename(archivo.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    archivo.save(filepath)

    try:
        entrega = Entrega(
            id_actividad=id_actividad,
            id_estudiante=id_estudiante,
            archivo_url=filepath,
            estado="Entregado"
        )
        nuevo_id = ControladorEntregas.insertar_entrega(entrega)
        return jsonify({"mensaje": "Entrega registrada correctamente", "id": nuevo_id}), 201

    except Exception as e:
        print("❌ Error al crear entrega:", e)
        return jsonify({"error": str(e)}), 500

# ✅ Listar entregas de una actividad
@entrega_bp.route("/entregas/<int:id_actividad>", methods=["GET"])
def listar_entregas(id_actividad):
    try:
        entregas = ControladorEntregas.listar_entregas_por_actividad(id_actividad)
        entregas_json = [
            {
                "id": e[0],
                "id_estudiante": e[1],
                "archivo_url": e[2],
                "fecha_envio": str(e[3]),
                "calificacion": float(e[4]) if e[4] is not None else None,
                "estado": e[5]
            } for e in entregas
        ]
        return jsonify(entregas_json), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@entrega_bp.route("/entrega_contenido/<int:id_entrega>", methods=["GET"])
def obtener_contenido_entrega(id_entrega):
    try:
        # 🔹 Primero obtenemos la ruta del archivo desde la base de datos
        entrega = ControladorEntregas.obtener_entrega_por_id(id_entrega)
        if not entrega:
            return jsonify({"error": "Entrega no encontrada"}), 404

        archivo_path = entrega.archivo_url  # Aquí es la ruta guardada en DB

        # 🔹 Abrir y leer el contenido del archivo
        with open(archivo_path, "r", encoding="utf-8") as f:
            contenido = f.read()

        return jsonify({"contenido": contenido}), 200

    except FileNotFoundError:
        return jsonify({"error": f"No se encontró el archivo en la ruta: {archivo_path}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# ✅ Listar todas las entregas de un estudiante
@entrega_bp.route("/entregas_estudiante/<int:id_estudiante>", methods=["GET"])
def listar_entregas_por_estudiante(id_estudiante):
    try:
        entregas = ControladorEntregas.listar_entregas_por_estudiante(id_estudiante)
        entregas_json = [
            {
                "id": e[0],
                "id_actividad": e[1],
                "archivo_url": e[2],
                "fecha_envio": str(e[3]),
                "calificacion": float(e[4]) if e[4] is not None else None,
                "estado": e[5]
            } for e in entregas
        ]
        return jsonify(entregas_json), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@entrega_bp.route("/actividad/<int:id_actividad>")
def entregas_por_actividad(id_actividad):
    entregas = ControladorEntregas.listar_entregas_por_actividad(id_actividad)
    return jsonify(entregas)