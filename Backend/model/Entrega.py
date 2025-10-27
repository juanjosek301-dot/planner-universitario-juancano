class Entrega:
    def __init__(self, id_actividad, id_estudiante, archivo_url, fecha_envio=None, calificacion=None, estado="Entregado"):
        self.id_actividad = id_actividad
        self.id_estudiante = id_estudiante
        self.archivo_url = archivo_url
        self.fecha_envio = fecha_envio
        self.calificacion = calificacion
        self.estado = estado