from restricciones import es_consistente
from costos import costo_asignacion

def generar_sucesores(asignaciones, orden_clases, franjas, salones, dic_clases):
    posicion = len(asignaciones)

    if posicion >= len(orden_clases):
        return []

    id_clase = orden_clases[posicion]
    sucesores = []
    
    for franja in franjas:
        for salon in salones:
            if es_consistente(id_clase, franja.id, salon.id, dic_clases, asignaciones):
                costo = costo_asignacion(id_clase, franja.id, asignaciones)
                nueva_asignacion = asignaciones.copy()
                nueva_asignacion[id_clase] = (franja.id, salon.id)
                sucesores.append((nueva_asignacion, costo))
    return sucesores