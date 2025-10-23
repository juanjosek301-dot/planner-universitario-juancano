from flask import Blueprint, request, jsonify, render_template
from controller.usuario_controller import ControladorUsuarios
from model.Usuario import Usuario

usuario_bp = Blueprint('usuario_bp', __name__, url_prefix='/api')

@usuario_bp.route('/usuario', methods=['POST'])
def crear_usuario():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        correo = data.get('correo')
        clave = data.get('clave')
        rol = data.get('rol', 'estudiante')

        if not nombre or not correo or not clave:
            return jsonify({'error': 'Faltan datos'}), 400

        usuario = Usuario(nombre, correo, clave, rol)
    
        ControladorUsuarios.insertar_usuario(usuario)
    
        return jsonify({
            'mensaje': '✅ Usuario creado con éxito',
            'nombre': usuario.nombre,
            'correo': usuario.correo,
            'rol': usuario.rol
        }), 201
        
    except Exception as e:
        print("Error al crear usuario:", e)
        return jsonify({'error': str(e)}), 500
    
@usuario_bp.route('/login', methods=['POST'])
def login_usuario():
    data = request.get_json()
    correo = data.get('correo')
    clave = data.get('clave')

    if not correo or not clave:
        return jsonify({'error': 'Faltan datos'}), 400

    usuario = ControladorUsuarios.buscar_usuario(correo)

    if usuario and usuario.clave == clave:
        # ✅ Inicio de sesión exitoso
        return jsonify({
            'mensaje': 'Inicio de sesión exitoso',
            'rol': usuario.rol,
            'nombre': usuario.nombre
        }), 200
    else:
        return jsonify({'error': 'Correo o clave incorrectos'}), 401
    
  