class Profesor:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

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