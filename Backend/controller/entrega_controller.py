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
        resultados = cur.fetchall()
        cur.close()
        conn.close()
        
        entregas = []
        for row in resultados:
            entregas.append({
                "id": row[0],
                "id_estudiante": row[1],
                "archivo_url": row[2],
                "fecha_envio": str(row[3]),
                "calificacion": float(row[4]) if row[4] is not None else None,
                "estado": row[5]
            })
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
    
    @staticmethod
    def montar_nota(id_actividad, id_estudiante, calificacion, id_profesor):
        """
        Monta la nota de una entrega, solo si el profesor es dueño del curso de la actividad.
        """
        conn = ControladorEntregas.obtener_conexion()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT a.id
                FROM actividades a
                JOIN cursos c ON a.id_curso = c.id
                WHERE a.id = %s AND c.id_profesor = %s
            """, (id_actividad, id_profesor))
            actividad = cursor.fetchone()

            if not actividad:
                return False  # Profesor no autorizado

        # Actualizar la nota
            cursor.execute("""
                UPDATE entregas
                SET calificacion = %s,
                    estado = 'Calificado'
                WHERE id_actividad = %s AND id_estudiante = %s
                RETURNING id;
            """, (calificacion, id_actividad, id_estudiante))
            actualizado = cursor.fetchone()
            conn.commit()

            return actualizado is not None

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()
    