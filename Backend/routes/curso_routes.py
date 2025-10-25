from flask import Blueprint, request, jsonify
from controller.curso_controller import ControladorCursos
from model.Curso import Curso

curso_bp = Blueprint('curso_bp', __name__, url_prefix='/api')

# ✅ Crear un curso
@curso_bp.route('/cursos', methods=['POST'])
def crear_curso():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400

    try:
        curso = Curso(
            nombre=data.get("nombre"),
            codigo=data.get("codigo"),
            descripcion=data.get("descripcion"),
            id_profesor=data.get("id_profesor")
        )
        nuevo_id = ControladorCursos.insertar_curso(curso)
        return jsonify({"mensaje": "Curso creado correctamente", "id": nuevo_id}), 201
    except Exception as e:
        print("❌ Error al crear curso:", e)
        return jsonify({"error": str(e)}), 500



# ✅ Obtener todos los cursos de un profesor
@curso_bp.route("/cursos/<int:id_profesor>", methods=["GET"])
def listar_cursos_por_profesor(id_profesor):
    try:
        cursos = ControladorCursos.listar_cursos_por_profesor(id_profesor)
        cursos_json = [
            {
                "id": c[0],
                "nombre": c[1],
                "codigo": c[2],
                "descripcion": c[3]
            } for c in cursos
        ]
        return jsonify(cursos_json), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500