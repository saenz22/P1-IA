from clases import Profesor, Salon, Franja, Clase


def cargarProfes(r):
    """Carga los datos de los profesores desde un archivo txt.
    
    Recibe la ruta del archivo y devuelve una lista de objetos Profesor.
    Lanza un ValueError si se esperan 2 datos y se encuentran más o menos.
    """
    profes = []

    with open(r, "r", encoding="utf-8") as script:
        for num, line in enumerate(script, start=1):

            line = line.strip()

            if not line: continue

            datos = [d.strip() for d in line.split(";")]

            if len(datos) != 2:
                raise ValueError(f"Error en la línea {num}: se esperaban 2 datos, pero se encontraron {len(datos)}.")
            
            id_profe, nombre = datos

            profes.append(Profesor(id_profe, nombre))
    return profes

def cargarSalones(r):
    """Carga los datos de los salones desde un archivo txt.

    Recibe la ruta del archivo y devuelve una lista de objetos Salon. 
    Lanza un ValueError si el identificador del salón contiene un punto y coma.
    """
    salones = []
    
    with open(r, "r", encoding="utf-8") as script:
        for num, line in enumerate(script, start=1):
            line = line.strip()

            if not line: continue

            id_salon = line

            if ";" in id_salon:
                raise ValueError(f"Error en la línea {num}: El identificador del salón no debe contener ';'.")

            salones.append(Salon(id_salon))
    return salones

def cargarFranjas(r):
    """Carga los datos de las franjas horarias desde un archivo txt.

    Recibe la ruta del archivo y devuelve una lista de objetos Franja.
    Lanza un ValueError si se esperan 4 datos y se encuentran más o menos.
    """
    franjas = []

    with open(r, "r", encoding="utf-8") as script:
        for num, line in enumerate(script, start=1):
            line = line.strip()

            if not line: continue

            datos = [d.strip() for d in line.split(";")]

            if len(datos) != 4:
                raise ValueError(f"Error en la línea {num}: se esperaban 4 datos, pero se encontraron {len(datos)}.")

            id_franja, dia, inicio, fin = datos

            franjas.append(Franja(id_franja, dia, inicio, fin))

    return franjas

def cargarClases(r):
    """Carga los datos de las clases desde un archivo txt.

    Recibe la ruta del archivo y devuelve una lista de objetos Clase.
    Lanza un ValueError si se esperan 4 datos y se encuentran más o menos.
    """
    clases = []

    with open(r, "r", encoding="utf-8") as script:
        for num, line in enumerate(script, start=1):
            line = line.strip()

            if not line: continue

            datos = [d.strip() for d in line.split(";")]

            if len(datos) != 4:
                raise ValueError(f"Error en la línea {num}: se esperaban 4 datos, pero se encontraron {len(datos)}.")

            id_, materia, profeId, grupo = datos

            clases.append(Clase(id_, materia, profeId, grupo))

    return clases