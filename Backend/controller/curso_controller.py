import psycopg2
from model.Curso import Curso
import SecretConfig

class ControladorCursos:
    
    @staticmethod
    def obtener_cursor():
        connection = psycopg2.connect(
            database=SecretConfig.PGDATABASE,
            user=SecretConfig.PGUSER,
            password=SecretConfig.PGPASSWORD,
            host=SecretConfig.PGHOST,
            port=SecretConfig.PGPORT
        )
        return connection
    
    @staticmethod
    def insertar_curso(curso: Curso):
        conn = ControladorCursos.obtener_cursor()
        cursor = conn.cursor()
        try:
            sql = """
                INSERT INTO cursos (nombre, codigo, descripcion, id_profesor)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """
            cursor.execute(sql, (curso.nombre, curso.codigo, curso.descripcion, curso.id_profesor))
            nuevo_id = cursor.fetchone()[0]
            conn.commit()
            return nuevo_id
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_cursos_por_profesor(id_profesor):
        conn = ControladorCursos.obtener_cursor()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id, nombre, codigo, descripcion 
                FROM cursos
                WHERE id_profesor = %s
                ORDER BY id DESC;
            """, (id_profesor,))
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()