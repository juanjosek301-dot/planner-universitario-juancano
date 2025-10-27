import psycopg2
from model.Actividades import Actividad
import SecretConfig

class ControladorActividades:    

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
    def insertar_actividad(actividad: Actividad):
        conn = ControladorActividades.obtener_conexion()
        cursor = conn.cursor()
        query = """
            INSERT INTO actividades (id_curso, titulo, descripcion, fecha_entrega, peso)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """
        cursor.execute(query, (
            actividad.id_curso,
            actividad.titulo,
            actividad.descripcion,
            actividad.fecha_entrega,
            actividad.peso
        ))
        nuevo_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return nuevo_id

    @staticmethod
    def listar_actividades_por_curso(id_curso):
        conn = ControladorActividades.obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, titulo, descripcion, fecha_entrega, peso
            FROM actividades
            WHERE id_curso=%s
        """, (id_curso,))
        actividades = cursor.fetchall()
        cursor.close()
        conn.close()
        return actividades
