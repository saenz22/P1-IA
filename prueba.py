from parser import cargarClases
from restricciones import es_consistente
from clases import Franja, Salon, Clase
from sucesores import generar_sucesores

clases = cargarClases("C:/Users/PauRescate/Desktop/P1-IA/datos/cursos.txt")
dic_clases = {c.id: c for c in clases}
asignaciones = {"C1": ("F1", "S101")}

"""print(dic_clases["C1"].materia)  # Imprime la materia de la clase con id "C1"
print(es_consistente("C2", "F1", "S102", dic_clases, asignaciones))
print(es_consistente("C3", "F1", "S102", dic_clases, asignaciones))
print(es_consistente("C4", "F2", "S101", dic_clases, asignaciones))
print(es_consistente("C4", "F1", "S101", dic_clases, asignaciones))
print(es_consistente("C4", "F1", "S102", dic_clases, asignaciones)) """


franjas = [Franja("F1", "Lunes", "07", "09"), Franja("F2", "Lunes", "09", "11")]
salones = [Salon("S1"), Salon("S2")]
clases = [Clase("C1", "Calculo", "P1", "G1"), Clase("C2", "Algebra", "P1", "G2")]
dic_clases = {c.id: c for c in clases}
orden = ["C1", "C2"]

print(len(generar_sucesores({}, orden, franjas, salones, dic_clases)))
print(len(generar_sucesores({"C1": ("F1", "S1")}, orden, franjas, salones, dic_clases)))
print(generar_sucesores({}, orden, franjas, salones, dic_clases)[0])