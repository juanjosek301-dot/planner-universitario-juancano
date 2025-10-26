from flask import Blueprint, request, jsonify
from controller.controlador_inscripciones import ControladorInscripciones
from model.Inscripcion import Inscripcion

inscripciones_bp = Blueprint('inscripciones_bp', __name__, url_prefix='/api/inscripciones')

@inscripciones_bp.route('/inscripciones', methods=['POST'])
def inscribir_estudiante():
    data = request.get_json()
    id_estudiante = data.get('id_estudiante')
    id_curso = data.get('id_curso')

    if not id_estudiante or not id_curso:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        ControladorInscripciones.inscribir_estudiante(id_estudiante, id_curso)
        return jsonify({"mensaje": "✅ Estudiante inscrito correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@inscripciones_bp.route('/cursos_disponibles', methods=['GET'])
def listar_cursos_disponibles():
    try:
        cursos = ControladorInscripciones.listar_cursos_disponibles()
        return jsonify(cursos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500