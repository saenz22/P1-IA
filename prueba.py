from clases import Franja, Salon, Clase
from costos import costo_asignacion
from algoritmos import busqueda_costo_uniforme, busqueda_a_asterisco

h_cero = lambda estado, orden, dic: 0
h_restantes = lambda estado, orden, dic: len(orden) - len(estado)

def costo_total(solucion, dic_clases, no_disp):
    if solucion is None:
        return None
    return sum(costo_asignacion(c, f, dic_clases, no_disp) for c, (f, _) in solucion.items())

def probar(titulo, franjas, salones, clases, no_disp=None, limite=100000):
    dic = {c.id: c for c in clases}
    orden = [c.id for c in clases]
    nd = no_disp or {}
    print("==", titulo)
    for nombre, res in [
        ("UCS     ", busqueda_costo_uniforme({}, orden, franjas, salones, dic, nd, limite)),
        ("A* h=0  ", busqueda_a_asterisco({}, orden, franjas, salones, dic, h_cero, nd, limite)),
        ("A* h=res", busqueda_a_asterisco({}, orden, franjas, salones, dic, h_restantes, nd, limite)),
    ]:
        sol, nodos, msg = res
        print(nombre, "| costo:", costo_total(sol, dic, nd), "| nodos:", nodos, "|", sol, "|", msg)

F = lambda n: Franja(f"F{n}", "Lunes", "07", "09")
S = lambda n: Salon(f"S{n}")

probar("1. Sin disponibilidad", [F(1), F(2)], [S(1), S(2)],
       [Clase("C1", "Calculo", "P1", "G1"), Clase("C2", "Algebra", "P2", "G2")])

probar("2. Penalizacion evitable", [F(1), F(2), F(3)], [S(1), S(2)],
       [Clase("C1", "Calculo", "P1", "G1"), Clase("C2", "Algebra", "P1", "G2")], {"P1": {"F1"}})

probar("3. Penalizacion inevitable", [F(1), F(2)], [S(1), S(2)],
       [Clase("C1", "Calculo", "P1", "G1"), Clase("C2", "Algebra", "P1", "G2")], {"P1": {"F1"}})

probar("4. Sin solucion (mismo profesor, una franja)", [F(1)], [S(1), S(2)],
       [Clase("C1", "Calculo", "P1", "G1"), Clase("C2", "Algebra", "P1", "G2")])

probar("5. Conflicto de grupo", [F(1), F(2)], [S(1), S(2)],
       [Clase("C1", "Calculo", "P1", "G1"), Clase("C2", "Fisica", "P2", "G1")])

probar("6. Un solo salon, tres clases, dos profesores", [F(1), F(2), F(3)], [S(1)],
       [Clase("C1", "Calculo", "P1", "G1"), Clase("C2", "Algebra", "P1", "G2"), Clase("C3", "Fisica", "P2", "G3")],
       {"P1": {"F1", "F2"}, "P2": {"F3"}})

probar("7. Limite de nodos", [F(1), F(2), F(3)], [S(1), S(2)],
       [Clase("C1", "Calculo", "P1", "G1"), Clase("C2", "Algebra", "P2", "G2")], None, 2)