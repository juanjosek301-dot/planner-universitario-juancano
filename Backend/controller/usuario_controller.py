import psycopg2
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
                INSERT INTO usuarios (nombre, correo, clave)
                VALUES (%s, %s, %s)
            """, (usuario.nombre, usuario.correo, usuario.clave))
            conn.commit()
        except psycopg2.IntegrityError as e:
            conn.rollback()
            raise Exception("El correo ya está registrado") from e
        finally:
            cursor.close()
            conn.close() 
    
    @staticmethod
    def buscar_por_correo(correo):
        conn = ControladorUsuarios.obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, correo FROM usuarios WHERE correo = %s
        """, (correo,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        if fila:
            return {
                "id": fila[0],
                "nombre": fila[1],
                "correo": fila[2]
            }
        return None                    