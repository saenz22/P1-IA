from collections import deque
from restricciones import es_meta
from sucesores import generar_sucesores
import heapq

def busqueda_por_amplitud(asignaciones_iniciales, orden_clases, franjas, salones, dic_clases, no_disponibles=None, limite_nodos_explorados=100000):
    """
    Función que implementa la búsqueda por amplitud para encontrar una asignación de clases a franjas y salones.
    
    Parámetros:
    asignaciones_iniciales: Diccionario con las asignaciones iniciales de clases a franjas y salones.
    orden_clases: Lista con el orden de las clases a asignar.
    franjas: Lista de objetos Franja que representan las franjas horarias disponibles.
    salones: Lista de objetos Salon que representan los salones disponibles.
    dic_clases: Diccionario con las clases cargadas desde el archivo.
    no_disponibles: Diccionario con las franjas no disponibles para cada profesor (opcional).
    limite_nodos_explorados: Límite de nodos a explorar durante la búsqueda (por defecto 100000).

    La búsqueda retorna una tupla con:
    - La asignación final de clases a franjas y salones si se encontró una solución, o None si no se encontró.
    - El número de nodos explorados durante la búsqueda.    
    - Un mensaje indicando si se encontró una solución (Se encontró una solución.), 
    si se alcanzó el límite de nodos explorados (Se alcanzó el límite de nodos explorados.) 
    o si no se encontró una solución (No se encontró una solución.).

    """
    if no_disponibles is None:
            no_disponibles = {}

    nodos_explorados = 0
    cola = deque([asignaciones_iniciales])
    while cola:

        if nodos_explorados >= limite_nodos_explorados:
            return None, nodos_explorados, "Se alcanzó el límite de nodos explorados."

        estado_actual = cola.popleft()
        nodos_explorados += 1

        if es_meta(dic_clases, estado_actual):
            return estado_actual, nodos_explorados, "Se encontró una solución."

        sucesores = generar_sucesores(estado_actual, orden_clases, franjas, salones, dic_clases, no_disponibles)
        for sucesor, _ in sucesores:
            cola.append(sucesor)

    return None, nodos_explorados, "No se encontró una solución."

def busqueda_costo_uniforme(asignaciones_iniciales, orden_clases, franjas, salones, dic_clases, no_disponibles=None, limite_nodos_explorados=100000):
    """
    Función que implementa la búsqueda de costo uniforme para encontrar una asignación de clases a franjas y salones.
    Parámetros:
    asignaciones_iniciales: Diccionario con las asignaciones iniciales de clases a franjas y salones.
    orden_clases: Lista con el orden de las clases a asignar.
    franjas: Lista de objetos Franja que representan las franjas horarias disponibles.
    salones: Lista de objetos Salon que representan los salones disponibles.
    dic_clases: Diccionario con las clases cargadas desde el archivo.
    no_disponibles: Diccionario con las franjas no disponibles para cada profesor (opcional).
    limite_nodos_explorados: Límite de nodos a explorar durante la búsqueda (por defecto 100000).

    La búsqueda retorna una tupla con:
    - La asignación final de clases a franjas y salones si se encontró una solución, o None si no se encontró.
    - El número de nodos explorados durante la búsqueda.
    - Un mensaje indicando si se encontró una solución (Se encontró una solución.),
    si se alcanzó el límite de nodos explorados (Se alcanzó el límite de nodos explorados.) o si no se encontró una solución (No se encontró una solución.).
    """
    if no_disponibles is None:
        no_disponibles = {}
    nodos_explorados = 0
    contador = 0
    cola = [(0,contador, asignaciones_iniciales)]  

    while cola:
        costo_actual, _, estado_actual = heapq.heappop(cola)
        nodos_explorados += 1

        if es_meta(dic_clases, estado_actual):
            return estado_actual, nodos_explorados, "Se encontró una solución."

        if nodos_explorados >= limite_nodos_explorados:
            return None, nodos_explorados, "Se alcanzó el límite de nodos explorados."

        sucesores = generar_sucesores(estado_actual, orden_clases, franjas, salones, dic_clases, no_disponibles)
        for sucesor, costo in sucesores:
            contador+= 1
            heapq.heappush(cola, (costo_actual + costo, contador, sucesor))

    return None, nodos_explorados, "No se encontró una solución."

def busqueda_a_asterisco(asignaciones_iniciales, orden_clases, franjas, salones, dic_clases, heuristica, no_disponibles=None, limite_nodos_explorados=100000):
    """
    Función que implementa la búsqueda A* para encontrar una asignación de clases a franjas y salones.

    Ordena la cola de prioridad por f(n) = g(n) + h(n), donde g(n) es el costo acumulado
    desde el estado inicial y h(n) es la estimación de lo que falta hasta la meta.

    Parámetros:
    asignaciones_iniciales: Diccionario con las asignaciones iniciales de clases a franjas y salones.
    orden_clases: Lista con el orden de las clases a asignar.
    franjas: Lista de objetos Franja que representan las franjas horarias disponibles.
    salones: Lista de objetos Salon que representan los salones disponibles.
    dic_clases: Diccionario con las clases cargadas desde el archivo.
    heuristica: Función heuristica(asignaciones_iniciales, orden_clases, franjas, dic_clases, no_disponibles) que estima el costo que falta hasta la meta.
    no_disponibles: Diccionario con las franjas no disponibles para cada profesor (opcional).
    limite_nodos_explorados: Límite de nodos a explorar durante la búsqueda (por defecto 100000).

    La búsqueda retorna una tupla con:
    - La asignación final de clases a franjas y salones si se encontró una solución, o None si no se encontró.
    - El número de nodos explorados durante la búsqueda.
    - Un mensaje indicando si se encontró una solución (Se encontró una solución.),
    si se alcanzó el límite de nodos explorados (Se alcanzó el límite de nodos explorados.) o si no se encontró una solución (No se encontró una solución.).
    """
    if no_disponibles is None:
        no_disponibles = {}
    nodos_explorados = 0
    contador = 0
    f_inicial = heuristica(asignaciones_iniciales, orden_clases, franjas, dic_clases, no_disponibles)  # g = 0
    cola = [(f_inicial, contador, 0, asignaciones_iniciales)]

    while cola:
        f_actual, _, g_actual, estado_actual = heapq.heappop(cola)
        nodos_explorados += 1

        if es_meta(dic_clases, estado_actual):
            return estado_actual, nodos_explorados, "Se encontró una solución."

        if nodos_explorados >= limite_nodos_explorados:
            return None, nodos_explorados, "Se alcanzó el límite de nodos explorados."

        sucesores = generar_sucesores(estado_actual, orden_clases, franjas, salones, dic_clases, no_disponibles)
        for sucesor, costo in sucesores:
            contador += 1
            g_sucesor = g_actual + costo                                # g(n): costo acumulado
            h_sucesor = heuristica(sucesor, orden_clases, franjas, dic_clases, no_disponibles)   # h(n): estimación de lo que falta
            f_sucesor = g_sucesor + h_sucesor                           # f(n) = g(n) + h(n)
            heapq.heappush(cola, (f_sucesor, contador, g_sucesor, sucesor))

    return None, nodos_explorados, "No se encontró una solución."

# Búsqueda por profundización iterativa con límites de profundidad crecientes.

def _buscar_con_limite(estado, limite, orden_clases, franjas, salones, dic_clases, no_disponibles, contador, limite_nodos):
    """
    FUNCIÓN AUXILIAR RECURSIVA.

    Realiza una búsqueda en profundidad limitada desde el estado actual.

    Parámetros:
        estado: estado actual de las asignaciones.
        limite: profundidad máxima permitida.
        orden_clases: orden en que se asignan las clases.
        franjas: franjas horarias disponibles.
        salones: salones disponibles.
        dic_clases: diccionario con la información de las clases.
        no_disponibles: restricciones de disponibilidad.
        contador: lista que almacena los nodos explorados.
        limite_nodos: máximo de nodos que pueden explorarse.

    Retorna:
        dict: una solución encontrada.
        None: si no encuentra solución dentro del límite.
        "LIMITE_NODOS": si alcanza el máximo de nodos explorados.
    """

    # 1. Contar el nodo actual
    contador[0] += 1

    # 2. Comprobar si el estado es una solución
    if es_meta(dic_clases, estado):
        return estado

    # 3. Comprobar el límite de nodos
    if contador[0] >= limite_nodos:
        return "LIMITE_NODOS"

    # 4. No expandir si alcanzamos el límite de profundidad
    if len(estado) == limite:
        return None

    # 5. Generar sucesores
    sucesores = generar_sucesores(estado, orden_clases, franjas, salones, dic_clases, no_disponibles)

    for sucesor, _ in sucesores:

        resultado = _buscar_con_limite(sucesor, limite, orden_clases, franjas, salones, dic_clases, no_disponibles, contador, limite_nodos)

        # Si encontramos una solución, la propagamos
        if resultado is not None and resultado != "LIMITE_NODOS":
            return resultado

        # Si alcanzamos el límite de nodos, detenemos toda la búsqueda
        if resultado == "LIMITE_NODOS":
            return "LIMITE_NODOS"

    # 6. Ningún sucesor produjo una solución
    return None


def busqueda_profundizacion_iterativa(
    asignaciones_iniciales,
    orden_clases,
    franjas,
    salones,
    dic_clases,
    no_disponibles=None,
    limite_nodos_explorados=100000
):
    """
    Realiza una búsqueda por profundización iterativa (IDDFS).

    Repite una búsqueda en profundidad limitada, aumentando
    progresivamente el límite de profundidad desde 0 hasta
    la cantidad total de clases.

    Parámetros:
        asignaciones_iniciales: estado inicial de las asignaciones.
        orden_clases: orden en que se asignan las clases.
        franjas: franjas horarias disponibles.
        salones: salones disponibles.
        dic_clases: diccionario con la información de las clases.
        no_disponibles: restricciones de disponibilidad.
        limite_nodos_explorados: máximo de nodos que se pueden explorar.

    Retorna:
        (solucion, nodos, mensaje):
            solucion: estado encontrado o None.
            nodos: cantidad total de nodos explorados.
            mensaje: resultado de la búsqueda.
    """

    # 1. Inicializar las restricciones
    if no_disponibles is None:
        no_disponibles = {}

    # 2. Inicializar el contador una sola vez
    contador = [0]

    # 3. Aumentar progresivamente el límite de profundidad
    for limite in range(len(dic_clases) + 1):

        resultado = _buscar_con_limite(
            asignaciones_iniciales,
            limite,
            orden_clases,
            franjas,
            salones,
            dic_clases,
            no_disponibles,
            contador,
            limite_nodos_explorados
        )

        # Solución encontrada
        if resultado is not None and resultado != "LIMITE_NODOS":
            return (
                resultado,
                contador[0],
                "Se encontró una solución."
            )

        # Se alcanzó el límite de nodos
        if resultado == "LIMITE_NODOS":
            return (
                None,
                contador[0],
                "Se alcanzó el límite de nodos explorados."
            )

    # 4. No se encontró ninguna solución
    return (
        None,
        contador[0],
        "No se encontró una solución."
    )
