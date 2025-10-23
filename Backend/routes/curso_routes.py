from flask import Blueprint, request, jsonify
from controller.curso_controller import ControladorCursos
from model.Curso import Curso

curso_bp = Blueprint('curso_bp', __name__, url_prefix='/api')

# ✅ Crear un curso
@curso_bp.route('/cursos', methods=['POST'])
def crear_curso():
    try:
        data = request.get_json()
        print("📥 Datos recibidos:", data)  # 👈 Agrega esta línea
        
        nombre = data.get('nombre')
        codigo = data.get('codigo')
        descripcion = data.get('descripcion')
        id_profesor = data.get('id_profesor')

        if not nombre or not codigo or not id_profesor:
            return jsonify({'error': 'Faltan datos obligatorios'}), 400

        curso = Curso(nombre, codigo, descripcion, id_profesor)
        ControladorCursos.insertar_curso(curso)

        return jsonify({'mensaje': '✅ Curso creado exitosamente'}), 201

    except Exception as e:
        print("Error al crear curso:", e)
        return jsonify({'error': str(e)}), 500


# ✅ Obtener todos los cursos de un profesor
@curso_bp.route('/cursos/<int:id_profesor>', methods=['GET'])
def obtener_cursos(id_profesor):
    try:
        cursos = ControladorCursos.obtener_cursos_por_profesor(id_profesor)
        return jsonify(cursos), 200
    except Exception as e:
        print("Error al obtener cursos:", e)
        return jsonify({'error': str(e)}), 500