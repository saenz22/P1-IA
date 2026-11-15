from restricciones import es_consistente
from costos import costo_asignacion
from dominio import dominio

def generar_sucesores(asignaciones, orden_clases, franjas, salones, dic_clases, no_disponibles=None):
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