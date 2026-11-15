from collections import deque
from restricciones import es_meta
from sucesores import generar_sucesores

def busqueda_por_amplitud(asignaciones_iniciales, orden_clases, franjas, salones, dic_clases, limite_nodos_explorados=100000):
    """
    Función que implementa la búsqueda por amplitud para encontrar una asignación de clases a franjas y salones.
    
    Parámetros:
    asignaciones_iniciales: Diccionario con las asignaciones iniciales de clases a franjas y salones.
    orden_clases: Lista con el orden de las clases a asignar.
    franjas: Lista de objetos Franja que representan las franjas horarias disponibles.
    salones: Lista de objetos Salon que representan los salones disponibles.
    dic_clases: Diccionario con las clases cargadas desde el archivo.
    limite_nodos_explorados: Límite de nodos a explorar durante la búsqueda (por defecto 100000).

    La búsqueda retorna una tupla con:
    - La asignación final de clases a franjas y salones si se encontró una solución, o None si no se encontró.
    - El número de nodos explorados durante la búsqueda.    
    - Un mensaje indicando si se encontró una solución (Se encontró una solución.), 
    si se alcanzó el límite de nodos explorados (Se alcanzó el límite de nodos explorados.) 
    o si no se encontró una solución (No se encontró una solución.).

    """
    nodos_explorados = 0
    cola = deque([asignaciones_iniciales])
    while cola:

        if nodos_explorados >= limite_nodos_explorados:
            return None, nodos_explorados, "Se alcanzó el límite de nodos explorados."

        estado_actual = cola.popleft()
        nodos_explorados += 1

        if es_meta(dic_clases, estado_actual):
            return estado_actual, nodos_explorados, "Se encontró una solución."

        sucesores = generar_sucesores(estado_actual, orden_clases, franjas, salones, dic_clases)
        for sucesor, _ in sucesores:
            cola.append(sucesor)

    return None, nodos_explorados, "No se encontró una solución."

