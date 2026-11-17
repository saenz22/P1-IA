def dominio(lista_franjas, lista_salones):
    """
    Genera el dominio de posibles asignaciones de clases a franjas y salones.

    Recibe:
        lista_franjas: Una lista de franjas horarias.
        lista_salones: Una lista de salones.
    Devuelve una lista de tuplas (id_franja, id_salon) con todas las posibles combinaciones.
    """
    lista_dominio = []

    for franja in lista_franjas:
        for salon in lista_salones:
            lista_dominio.append((franja.id, salon.id))

    return lista_dominio

