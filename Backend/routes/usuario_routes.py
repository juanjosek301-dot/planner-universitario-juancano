from flask import Blueprint, request, jsonify
from controller.usuario_controller import ControladorUsuarios
from model.Usuario import Usuario

usuario_bp = Blueprint('usuario_bp', __name__, url_prefix='/api')

@usuario_bp.route('/usuario', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    clave = data.get('clave')

    if not nombre or not correo or not clave:
        return jsonify({'error': 'Faltan datos'}), 400

    usuario = usuario(nombre, correo, clave)

    try:
        ControladorUsuarios.insertar_usuario(usuario)
        return jsonify({'nombre': usuario.nombre, 'correo': usuario.correo}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 409
