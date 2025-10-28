from flask import Blueprint, jsonify
from controller.controlador_progreso import ControladorProgreso

progreso_bp = Blueprint("progreso_bp", __name__, url_prefix="/api/progreso")

@progreso_bp.route("/<int:id_curso>")
def progreso_curso(id_curso):
    try:
        data = ControladorProgreso.progreso_curso(id_curso)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
