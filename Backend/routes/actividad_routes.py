from flask import Blueprint, request, jsonify
from controller.controlador_actividades import ControladorActividades
from model.Actividades import Actividad
from decimal import Decimal

actividad_bp = Blueprint('actividad_bp', __name__, url_prefix='/api')

# ✅ Crear actividad
@actividad_bp.route('/actividades', methods=['POST'])
def crear_actividad():
    data = request.get_json()
    print("🔹 Datos recibidos:", data) 
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400

    id_curso = data.get("id_curso")
    peso = Decimal(str(data.get("peso", 0)))  # ✅ convertir a Decimal

    try:
        # 1️⃣ Validar suma de pesos
        conn = ControladorActividades.obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(SUM(peso),0) FROM actividades WHERE id_curso=%s", (id_curso,))
        suma_actual = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        if suma_actual + peso > 100:
            return jsonify({
                "error": f"No se puede crear la actividad. La suma de pesos actual es {suma_actual}%, "
                        f"agregando esta actividad excedería 100%."
            }), 400

        # 2️⃣ Crear actividad normalmente
        actividad = Actividad(
            id_curso=id_curso,
            titulo=data.get("titulo"),
            descripcion=data.get("descripcion"),
            fecha_entrega=data.get("fecha_entrega"),
            peso=peso
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
    
@actividad_bp.route("/actividades_estudiante/<int:id_estudiante>", methods=["GET"])
def actividades_estudiante(id_estudiante):
    try:
        # Devuelve todas las actividades de los cursos en los que está inscrito el estudiante
        actividades = ControladorActividades.listar_actividades_por_estudiante(id_estudiante)
        actividades_json = [
            {
                "id": a[0],
                "titulo": a[1],
                "descripcion": a[2],
                "fecha_entrega": str(a[3]),
                "peso": a[4],
                "id_curso": a[5]
            } for a in actividades
        ]
        return jsonify(actividades_json), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@actividad_bp.route("/profesor/<int:id_profesor>")
def actividades_por_profesor(id_profesor):
    actividades = ControladorActividades.listar_por_profesor(id_profesor)
    return jsonify(actividades)
