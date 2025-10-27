class Actividad:
    def __init__(self, id_curso, titulo, descripcion, fecha_entrega, peso, id=None):
        self.id = id
        self.id_curso = id_curso
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_entrega = fecha_entrega
        self.peso = peso 