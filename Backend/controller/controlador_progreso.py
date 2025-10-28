import psycopg2
from controller.entrega_controller import ControladorEntregas
import SecretConfig  # tus credenciales de DB
from decimal import Decimal

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
            estudiantes = cursor.fetchall()  

            # 2️⃣ Obtener actividades del curso
            cursor.execute("""
                SELECT id, titulo, peso
                FROM actividades
                WHERE id_curso = %s
                ORDER BY fecha_entrega
            """, (id_curso,))
            actividades = cursor.fetchall()  

            progreso = []
            for est_id, est_nombre in estudiantes:
                est_data = {
                    "id": est_id,
                    "nombre": est_nombre,
                    "actividades": [],
                    "promedio": None,
                    "alertas": []
                }
                suma_ponderada = Decimal('0')
                suma_pesos = Decimal('0')

                for act_id, act_titulo, act_peso in actividades:
                    cursor.execute("""
                        SELECT calificacion, estado
                        FROM entregas
                        WHERE id_estudiante = %s AND id_actividad = %s
                    """, (est_id, act_id))
                    entrega = cursor.fetchone()
                    cal = entrega[0] if entrega and entrega[0] is not None else None
                    estado = entrega[1] if entrega else "Pendiente"

                    # Agregar alerta si la tarea está pendiente
                    if cal is None:
                        est_data["alertas"].append(f"Tarea pendiente: {act_titulo}")
                    else:
                        suma_ponderada += Decimal(cal) * Decimal(act_peso) / Decimal(100)
                        suma_pesos += Decimal(act_peso)
                        
                    est_data["actividades"].append({
                        "titulo": act_titulo,
                        "calificacion": cal,
                        "estado": estado
                    })

                # Calcular promedio ponderado
                if suma_pesos > 0:
                    promedio = round(float(suma_ponderada), 2)
                    est_data["promedio"] = promedio

                # Agregar alerta si el promedio es menor a 3
                    if promedio < 3.0:
                        est_data["alertas"].append("Bajo desempeño académico")
                        
                progreso.append(est_data)

            return {
                "actividades": [a[1] for a in actividades],  # lista de títulos de actividades
                "estudiantes": progreso
            }

        finally:
            cursor.close()
            conn.close()