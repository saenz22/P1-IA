COSTO_BASE = 1
PENALIZACION_NO_DISPONIBLE = 5

def costo_asignacion(id_clase, id_franja, dic_clases, no_disponibles):
    """Calcula el costo de asignar una clase a una franja horaria.

    Recibe:
        id_clase: El ID de la clase a asignar.
        id_franja: El ID de la franja horaria.
        dic_clases: Un diccionario {id_clase: Clase} con las clases cargadas desde el archivo.
        no_disponibles: Un diccionario {id_profesor: conjunto de id_franja} con las franjas que cada profesor marcó como no disponibles.
    Devuelve un número que representa el costo de la asignación.
    """
    id_profesor = dic_clases[id_clase].profesorId        
    franjas_no_disp = no_disponibles.get(id_profesor, set())  
    if id_franja in franjas_no_disp:
        return COSTO_BASE + PENALIZACION_NO_DISPONIBLE
    return COSTO_BASE

def costo_solucion(solucion, dic_clases, no_disponibles):
    """Calcula el costo total de un horario completo.

    Recibe:
        solucion: Diccionario {id_clase: (id_franja, id_salon)}, o None si no hubo solución.
        dic_clases: Diccionario {id_clase: Clase}.
        no_disponibles: Diccionario {id_profesor: conjunto de id_franja}.
    Devuelve la suma de los costos de cada asignación, o None si no hay solución.
    """
    if solucion is None:
        return None                                         
    total = 0
    for id_clase, (id_franja, _) in solucion.items():
        total += costo_asignacion(id_clase, id_franja, dic_clases, no_disponibles)
    return total