COSTO_BASE = 1
N_MAX_CONSECUTIVAS = 3

def costo_asignacion(id_clase, id_franja, asignaciones):
    """Devuelve el costo de asignar una clase a una franja (por ahora solo el costo base)."""
    return COSTO_BASE