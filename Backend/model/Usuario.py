class Usuario:
    def __init__(self, nombre, correo, clave, rol, id=None):
        self.id = id 
        self.nombre = nombre 
        self.correo = correo 
        self.clave = clave
        self.rol = rol