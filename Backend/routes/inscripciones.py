from flask import Blueprint, request, jsonify
from controller.controlador_inscripciones import ControladorInscripciones
from model.Inscripcion import Inscripcion

inscripciones_bp = Blueprint('inscripciones_bp', __name__, url_prefix='/api/inscripciones')

# 🧩 Listar todos los cursos disponibles
@inscripciones_bp.route('/cursos/', methods=['GET'])
def listar_cursos():
    try:
        cursos = ControladorInscripciones.listar_cursos_disponibles()
        cursos_json = [
            {"id": c[0], "nombre": c[1], "codigo": c[2], "descripcion": c[3]}
            for c in cursos
        ]
        return jsonify(cursos_json), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🧩 Inscribir estudiante en un curso
@inscripciones_bp.route('/inscripciones/', methods=['POST'])
def inscribir():
    try:
        data = request.get_json()
        id_estudiante = data.get('id_estudiante')
        id_curso = data.get('id_curso')

        if not id_estudiante or not id_curso:
            return jsonify({'error': 'Faltan datos'}), 400

        inscripcion = Inscripcion(id_estudiante, id_curso)
        ControladorInscripciones.inscribir_estudiante(inscripcion)

        return jsonify({'mensaje': '✅ Inscripción exitosa'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 🧩 Listar cursos en los que está inscrito el estudiante
@inscripciones_bp.route('/inscripciones/estudiante/<int:id_estudiante>', methods=['GET'])
def listar_cursos_estudiante(id_estudiante):
    try:
        cursos = ControladorInscripciones.listar_cursos_estudiante(id_estudiante)
        cursos_json = [
            {"id": c[0], "nombre": c[1], "codigo": c[2], "descripcion": c[3]}
            for c in cursos
        ]
        return jsonify(cursos_json), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500