def es_consistente(id_clase, id_franja, id_salon, dic_clases, asignaciones):
    """Indica si una clase puede asignarse a una franja y un salón.

    Recibe:
        id_clase: El ID de la clase a asignar.
        id_franja: El ID de la franja horaria.
        id_salon: El ID del salón.
        dic_clases: Un diccionario {id_clase: Clase} con las clases cargadas desde el archivo.
        asignaciones: Un diccionario {id_clase: (id_franja, id_salon)} con las asignaciones actuales.
    Devuelve True si no hay conflicto y False si lo hay.
    """
    for id_otra_clase, (otra_franja, otro_salon) in asignaciones.items():
        clase_nueva = dic_clases[id_clase]
        otra_clase = dic_clases[id_otra_clase]


        if id_otra_clase == id_clase:
            continue
        # Salón: misma franja y mismo salón.
        if otra_franja == id_franja and otro_salon == id_salon:
            return False
        # Profesor: misma franja y mismo profesor.
        if otra_franja == id_franja and otra_clase.profesorId == clase_nueva.profesorId:
            return False
        # Grupo: misma franja y mismo grupo.
        if otra_franja == id_franja and otra_clase.grupo == clase_nueva.grupo:
            return False
    return True

def es_meta(asignaciones, dic_clases):
    """Indica si todas las clases han sido asignadas.

    Recibe:
        asignaciones: Un diccionario {id_clase: (id_franja, id_salon)} con las asignaciones actuales.
        dic_clases: Un diccionario {id_clase: Clase} con las clases cargadas desde el archivo.
    Devuelve True si todas las clases han sido asignadas y False si no.
    """
    len(asignaciones) == len(dic_clases)