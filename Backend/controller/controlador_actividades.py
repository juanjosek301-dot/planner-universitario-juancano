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
    
    @staticmethod
    def listar_actividades_por_estudiante(id_estudiante):
        conn = ControladorActividades.obtener_conexion()
        cursor = conn.cursor()
        query = """
            SELECT a.id, a.titulo, a.descripcion, a.fecha_entrega, a.peso, a.id_curso
            FROM actividades a
            JOIN inscripciones i ON a.id_curso = i.id_curso
            WHERE i.id_estudiante = %s
        """
        cursor.execute(query, (id_estudiante,))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados
    
    # ✅ Método que faltaba
    @staticmethod
    def listar_por_profesor(id_profesor):
        conn = ControladorActividades.obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, a.id_curso, a.titulo, a.descripcion, a.fecha_entrega, a.peso
            FROM actividades a
            JOIN cursos c ON a.id_curso = c.id
            WHERE c.id_profesor = %s
            ORDER BY a.fecha_entrega DESC
        """, (id_profesor,))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convertir a lista de diccionarios para jsonify
        actividades = []
        for row in resultados:
            actividades.append({
                "id": row[0],
                "id_curso": row[1],
                "titulo": row[2],
                "descripcion": row[3],
                "fecha_entrega": str(row[4]),
                "peso": float(row[5])
            })
        return actividades
