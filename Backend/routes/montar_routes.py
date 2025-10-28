from flask import Blueprint, request, jsonify
from controller.entrega_controller import ControladorEntregas

montar_nota_bp = Blueprint("montar_nota_bp", __name__, url_prefix="/api/montar-nota")

@montar_nota_bp.route("", methods=["POST"])

def montar_nota():
    data = request.get_json()
    print("📩 Datos recibidos del frontend:", data)  # 🔍 Depuración
    
    id_actividad = data.get("id_actividad")
    id_estudiante = data.get("id_estudiante")
    calificacion = data.get("calificacion")
    id_profesor = data.get("id_profesor")  # si tu backend requiere identificación del profesor

    # ✅ Validación corregida
    if id_actividad is None or id_estudiante is None or calificacion is None:
        return jsonify({"error": "Faltan datos necesarios"}), 400

    try:
        exito = ControladorEntregas.montar_nota(
            id_actividad=id_actividad,
            id_estudiante=id_estudiante,
            calificacion=calificacion,
            id_profesor=int(id_profesor)
        )
        if exito:
            return jsonify({"message": "Nota montada correctamente"}), 200
        else:
            return jsonify({"error": "No se encontró la entrega o profesor no autorizado"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500