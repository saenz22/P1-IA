from clases import Profesor, Salon, Franja, Clase

def cargarProfes(r):
    profes = []

    with open(r, "r", encoding="utf-8") as script:
        for line in script:
            line = line.strip()

            if not line: continue

            datos = line.split(";")

            id, nombre = datos

            profes.append(Profesor(id, nombre))

    return profes


def cargarSalones(r):
    salones = []
    
    with open(r, "r", encoding="utf-8") as script:
        for line in script:
            line = line.strip()

            if not line: continue

            id = line

            salones.append(Salon(id))

    return salones

def cargarFranjas(r):
    franjas = []

    with open(r, "r", encoding="utf-8") as script:
        for line in script:
            line = line.strip()

            if not line: continue

            datos = line.split(";")

            id, dia, inicio, fin = datos

            franjas.append(Franja(id, dia, inicio, fin))

    return franjas

def cargarClases(r):
    clases = []

    with open(r, "r", encoding="utf-8") as script:
        for line in script:
            line = line.strip()

            if not line: continue

            datos = line.split(";")

            id, materia, profeId, grupo = datos

            clases.append(Clase(id, materia, profeId, grupo))

    return clases