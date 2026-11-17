from restricciones import es_consistente
from costos import costo_asignacion
from dominio import dominio

def generar_sucesores(asignaciones, orden_clases, franjas, salones, dic_clases, no_disponibles=None):
    """Recibe el estado actual (un diccionario {id_clase: (id_franja, id_salon)}), el orden de las clases, 
    las franjas, los salones, el diccionario de clases y, opcionalmente, las franjas no disponibles de cada 
    profesor, y devuelve una lista de tuplas (nueva_asignacion, costo), una por cada par (franja, salón) 
    que no choca con lo ya asignado, donde nueva_asignacion es una copia del estado con la siguiente clase
    añadida, y la lista queda vacía si ya no hay clases por asignar o ningún par es válido.
    """
    
    if no_disponibles is None:
        no_disponibles = {}

    posicion = len(asignaciones)

    if posicion >= len(orden_clases):
        return []

    id_clase = orden_clases[posicion]
    sucesores = []

    for id_franja, id_salon in dominio(franjas, salones):
        if es_consistente(id_clase, id_franja, id_salon, dic_clases, asignaciones):
            costo = costo_asignacion(id_clase, id_franja, dic_clases, no_disponibles)
            nueva_asignacion = asignaciones.copy()
            nueva_asignacion[id_clase] = (id_franja, id_salon)
            sucesores.append((nueva_asignacion, costo))
    return sucesores