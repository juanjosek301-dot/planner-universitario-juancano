from db import get_connection

def obtener_contexto_estudiante(id_estudiante):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT nombre FROM usuarios
            WHERE id = %s AND rol = 'estudiante'
        """, (id_estudiante,))
        estudiante = cursor.fetchone()
        if not estudiante:
            return "Estudiante no encontrado."

        nombre = estudiante[0]

        cursor.execute("""
            SELECT c.nombre, c.descripcion
            FROM inscripciones i
            JOIN cursos c ON i.id_curso = c.id
            WHERE i.id_estudiante = %s
        """, (id_estudiante,))
        cursos = cursor.fetchall()

        cursos_texto = "\n".join([f"- {nombre}: {desc}" for nombre, desc in cursos]) if cursos else "No tiene cursos inscritos."

        conn.close()
        return f"Estudiante: {nombre}\nCursos inscritos:\n{cursos_texto}"

    except Exception as e:
        print("🚨 Error al obtener contexto:", e)
        return "No se pudo obtener el contexto académico."