class Profesor:
    def __init__(self, id, nombre, franjas_no_disponibles):
        self.id = id
        self.nombre = nombre
        self.franjas_no_disponibles = franjas_no_disponibles

class Salon:
    def __init__(self, id):
        self.id = id

class Franja:
    def __init__(self, id, dia, inicio, fin):
        self.id = id
        self.dia = dia
        self.inicio = inicio
        self.fin = fin

class Clase:
    def __init__(self, id, materia, profesorId, grupo):
        self.id = id
        self.materia = materia
        self.profesorId = profesorId
        self.grupo = grupo