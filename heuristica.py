from costos import costo_asignacion

def heuristica(asignaciones, orden_clases, franjas, dic_clases, no_disponibles):
    """Estima el costo mínimo que falta para completar el horario.

    Recibe: 
        asignaciones: Diccionario con las asignaciones actuales de clases a franjas y salones.
        orden_clases: Lista con el orden de las clases a asignar.
        franjas: Lista de objetos Franja que representan las franjas horarias disponibles.
        dic_clases: Diccionario con las clases cargadas desde el archivo.
        no_disponibles: Diccionario {id_profesor: conjunto de id_franja} con las franjas no disponibles para cada profesor.
    Devuelve: 
        Un número que representa el costo mínimo estimado para completar la asignación de clases.
    """
    k = len(asignaciones)
    pendientes = orden_clases[k:]
    total = 0

    for id_clase in pendientes:
        minimo = min(costo_asignacion(id_clase, franja.id, dic_clases, no_disponibles) for franja in franjas)
        total += minimo

    return total