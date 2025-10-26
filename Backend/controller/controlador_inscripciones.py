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
    def inscribir_estudiante(id_estudiante, id_curso):
        conn = ControladorInscripciones.obtener_conexion()
        cur = conn.cursor()

        try:
            # 🔍 Verificar si ya está inscrito
            cur.execute("""
                SELECT 1 FROM inscripciones 
                WHERE id_estudiante = %s AND id_curso = %s;
            """, (id_estudiante, id_curso))

            if cur.fetchone():
                return {"error": "El estudiante ya está inscrito en este curso."}

            # ✅ Si no existe, insertar inscripción
            cur.execute("""
                INSERT INTO inscripciones (id_estudiante, id_curso)
                VALUES (%s, %s);
            """, (id_estudiante, id_curso))

            conn.commit()
            return {"mensaje": "Inscripción realizada con éxito ✅"}
        
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}

        finally:
            cur.close()
            conn.close()
            
    @staticmethod
    def listar_cursos_disponibles():
        conn = ControladorInscripciones.obtener_conexion()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT c.id, c.nombre, c.codigo, c.descripcion, u.nombre AS profesor
                FROM cursos c
                JOIN usuarios u ON c.id_profesor = u.id
                ORDER BY c.id DESC
            """)
            cursos = []
            for fila in cur.fetchall():
                cursos.append({
                    "id": fila[0],
                    "nombre": fila[1],
                    "codigo": fila[2],
                    "descripcion": fila[3],
                    "profesor": fila[4]
                })
            return cursos
        finally:
            cur.close()
            conn.close()