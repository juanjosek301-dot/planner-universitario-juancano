import psycopg2
from model.Inscripcion import Inscripcion
import SecretConfig

class ControladorInscripciones:

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
    def inscribir_estudiante(inscripcion: Inscripcion):
        conn = ControladorInscripciones.obtener_conexion()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO inscripciones (id_curso, id_estudiante)
                VALUES (%s, %s)
                ON CONFLICT (id_curso, id_estudiante) DO NOTHING
            """, (inscripcion.id_curso, inscripcion.id_estudiante))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print("❌ Error al inscribir estudiante:", e)
            return False
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def listar_estudiantes_por_curso(id_curso):
        conn = ControladorInscripciones.obtener_conexion()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT u.id, u.nombre, u.correo
                FROM usuarios u
                JOIN inscripciones i ON u.id = i.id_estudiante
                WHERE i.id_curso = %s
            """, (id_curso,))
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()