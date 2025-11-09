import psycopg2
from psycopg2 import extras
from model.Usuario import Usuario
import SecretConfig

class ControladorUsuarios:
    
    @staticmethod
    def obtener_cursor():
        connection = psycopg2.connect(
            database=SecretConfig.PGDATABASE,
            user=SecretConfig.PGUSER,
            password=SecretConfig.PGPASSWORD,
            host=SecretConfig.PGHOST,
            port=SecretConfig.PGPORT
        )
        return connection.cursor()
    
    @staticmethod
    def obtener_conexion():
        return psycopg2.connect(
        database=SecretConfig.PGDATABASE,
        user=SecretConfig.PGUSER,
        password=SecretConfig.PGPASSWORD,
        host=SecretConfig.PGHOST,
        port=SecretConfig.PGPORT
    )
    
    @staticmethod
    def crear_tabla():
        cursor = ControladorUsuarios.obtener_cursor()
        with open("sql/crear_usuarios.sql", "r") as archivo:
            consulta = archivo.read()
            
        cursor.execute(consulta)
        cursor.connection.commit()
        cursor.close()

    @staticmethod
    def insertar_usuario(usuario: Usuario):
        conn = ControladorUsuarios.obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, clave, rol)
                VALUES (%s, %s, %s, %s)
            """, (usuario.nombre, usuario.correo, usuario.clave, usuario.rol))
            conn.commit()
        except psycopg2.IntegrityError as e:
            conn.rollback()
            raise Exception("El correo ya está registrado") from e
        finally:
            cursor.close()
            conn.close() 
    
    @staticmethod
    def buscar_usuario(correo):
        conn = ControladorUsuarios.obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, nombre, correo, clave, rol FROM usuarios WHERE correo = %s", (correo,))
            row = cursor.fetchone()
            if row:
                return Usuario(id= row[0], nombre=row[1], correo=row[2], clave=row[3], rol=row[4])
            return None
        finally:
            cursor.close()
            conn.close()   
            
    @staticmethod
    def obtener_usuario_por_id(id_usuario):
        conn = ControladorUsuarios.obtener_conexion()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id, nombre, correo, rol 
                FROM usuarios 
                WHERE id = %s;
            """, (id_usuario,))
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()
            
    @staticmethod
    def obtener_profesor_por_id(profesor_id):
        conn = ControladorUsuarios.obtener_conexion()
        cursor = conn.cursor(cursor_factory=extras.DictCursor)  
        cursor.execute("""
            SELECT id, nombre, correo, rol
            FROM usuarios
            WHERE id = %s AND rol = 'profesor';
        """, (profesor_id,))
        profesor = cursor.fetchone()
        cursor.close()
        conn.close()
        return profesor
            
             