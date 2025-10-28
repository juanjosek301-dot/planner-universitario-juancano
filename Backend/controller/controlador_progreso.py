import psycopg2
from controller.entrega_controller import ControladorEntregas
import SecretConfig  # tus credenciales de DB

class ControladorProgreso:

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
    def progreso_curso(id_curso):
        """
        Devuelve el progreso de todos los estudiantes de un curso,
        incluyendo calificaciones por actividad y promedio.
        """
        conn = ControladorProgreso.obtener_conexion()
        cursor = conn.cursor()
        try:
            # 1️⃣ Obtener estudiantes inscritos
            cursor.execute("""
                SELECT u.id, u.nombre
                FROM usuarios u
                JOIN inscripciones i ON u.id = i.id_estudiante
                WHERE i.id_curso = %s AND u.rol = 'estudiante'
            """, (id_curso,))
            estudiantes = cursor.fetchall()  # [(id, nombre), ...]

            # 2️⃣ Obtener actividades del curso
            cursor.execute("""
                SELECT id, titulo
                FROM actividades
                WHERE id_curso = %s
                ORDER BY fecha_entrega
            """, (id_curso,))
            actividades = cursor.fetchall()  # [(id, titulo), ...]

            # 3️⃣ Construir progreso
            progreso = []
            for est_id, est_nombre in estudiantes:
                est_data = {"id": est_id, "nombre": est_nombre, "actividades": [], "promedio": 0}
                suma = 0
                count = 0

                for act_id, act_titulo in actividades:
                    cursor.execute("""
                        SELECT calificacion, estado
                        FROM entregas
                        WHERE id_estudiante = %s AND id_actividad = %s
                    """, (est_id, act_id))
                    entrega = cursor.fetchone()
                    cal = entrega[0] if entrega and entrega[0] is not None else None
                    estado = entrega[1] if entrega else "Pendiente"

                    if cal is not None:
                        suma += cal
                        count += 1

                    est_data["actividades"].append({
                        "titulo": act_titulo,
                        "calificacion": cal,
                        "estado": estado
                    })

                est_data["promedio"] = round(suma / count, 2) if count > 0 else None
                progreso.append(est_data)

            return {"actividades": [a[1] for a in actividades], "estudiantes": progreso}

        except Exception as e:
            raise e

        finally:
            cursor.close()
            conn.close()