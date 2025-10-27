import psycopg2
from model.Entrega import Entrega
import SecretConfig

class ControladorEntregas:

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
    def insertar_entrega(entrega: Entrega):
        conn = ControladorEntregas.obtener_conexion()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO entregas (id_actividad, id_estudiante, archivo_url, estado)
            VALUES (%s, %s, %s, %s) RETURNING id
        """, (entrega.id_actividad, entrega.id_estudiante, entrega.archivo_url, entrega.estado))
        nuevo_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return nuevo_id

    @staticmethod
    def listar_entregas_por_actividad(id_actividad):
        conn = ControladorEntregas.obtener_conexion()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, id_estudiante, archivo_url, fecha_envio, calificacion, estado
            FROM entregas
            WHERE id_actividad=%s
        """, (id_actividad,))
        entregas = cur.fetchall()
        cur.close()
        conn.close()
        return entregas
    
    # ✅ Listar entregas de un estudiante (nueva función)
    @staticmethod
    def listar_entregas_por_estudiante(id_estudiante):
        conn = ControladorEntregas.obtener_conexion()
        cursor = conn.cursor()
        query = """
            SELECT id, id_actividad, archivo_url, fecha_envio, calificacion, estado
            FROM entregas
            WHERE id_estudiante = %s
            ORDER BY fecha_envio DESC;
        """
        cursor.execute(query, (id_estudiante,))
        entregas = cursor.fetchall()
        cursor.close()
        conn.close()
        return entregas

    # ✅ Obtener entrega por ID (ya existente)
    @staticmethod
    def obtener_entrega_por_id(id_entrega):
        conn = ControladorEntregas.obtener_conexion()
        cursor = conn.cursor()
        query = """
            SELECT id, id_actividad, id_estudiante, archivo_url, fecha_envio, calificacion, estado
            FROM entregas
            WHERE id = %s;
        """
        cursor.execute(query, (id_entrega,))
        entrega = cursor.fetchone()
        cursor.close()
        conn.close()
        if entrega:
            return Entrega(
                id_actividad=entrega[1],
                id_estudiante=entrega[2],
                archivo_url=entrega[3],
                fecha_envio=entrega[4],
                calificacion=entrega[5],
                estado=entrega[6]
            )
        return None
