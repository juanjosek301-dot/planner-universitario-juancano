from flask import Blueprint, request, jsonify
from controller.controlador_actividades import ControladorActividades
from model.Actividades import Actividad

actividad_bp = Blueprint('actividad_bp', __name__, url_prefix='/api')

# ✅ Crear actividad
@actividad_bp.route('/actividades', methods=['POST'])
def crear_actividad():
    data = request.get_json()
    print("🔹 Datos recibidos:", data) 
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400

    try:
        actividad = Actividad(
            id_curso=data.get("id_curso"),
            titulo=data.get("titulo"),
            descripcion=data.get("descripcion"),
            fecha_entrega=data.get("fecha_entrega"),
            peso=data.get("peso")
        )
        nuevo_id = ControladorActividades.insertar_actividad(actividad)
        return jsonify({"mensaje": "Actividad creada correctamente", "id": nuevo_id}), 201
    except Exception as e:
        print("❌ Error al crear actividad:", e)
        return jsonify({"error": str(e)}), 500

# ✅ Listar actividades por curso
@actividad_bp.route("/actividades/<int:id_curso>", methods=["GET"])
def listar_actividades(id_curso):
    try:
        actividades = ControladorActividades.listar_actividades_por_curso(id_curso)
        actividades_json = [
            {
                "id": a[0],
                "titulo": a[1],
                "descripcion": a[2],
                "fecha_entrega": str(a[3]),
                "peso": a[4]
            } for a in actividades
        ]
        return jsonify(actividades_json), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
