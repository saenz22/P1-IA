import tkinter as tk
from tkinter import ttk
import time
from tkinter import messagebox
from vista.panel_carga_archivos import crear_panel, preparar_datos, datos
from algoritmos import busqueda_por_amplitud, busqueda_costo_uniforme, busqueda_a_asterisco
from costos import costo_solucion
from heuristica import heuristica
                                 

def a_asterisco(asignaciones, orden_clases, franjas, salones, dic_clases, no_disponibles=None):
    return busqueda_a_asterisco(asignaciones, orden_clases, franjas, salones, dic_clases, heuristica, no_disponibles)

ALGORITMOS = {
    "Búsqueda por Amplitud": busqueda_por_amplitud,
    "Búsqueda de Costo Uniforme": busqueda_costo_uniforme,
    "Búsqueda A*": a_asterisco,
}

NOMBRES_ALGORITMOS = list(ALGORITMOS.keys())

root = tk.Tk()
root.title("Asignación de Clases")
root.geometry("1000x700")
root.resizable(False, False)
root.configure(bg="#f0f0f0")
root.option_add("*Font", "Arial 12")

texto_bienvenida = tk.Label(root, text="Bienvenido al sistema de asignación de clases", bg="#f0f0f0")
texto_bienvenida.config(font=("Arial", 12, "bold"))
texto_bienvenida.pack(pady=20)

marco_carga = tk.Frame(root)
marco_carga.pack(pady=10)
crear_panel(marco_carga)
texto_instrucciones = tk.Label(root, text="Seleccione un algoritmo de búsqueda:", bg="#f0f0f0")
texto_instrucciones.pack(pady=10)


selector_algoritmo = ttk.Combobox(root, values=NOMBRES_ALGORITMOS, state="readonly", width=30)
selector_algoritmo.current(0)
selector_algoritmo.pack(pady=20)
columnas = ("algoritmo", "nodos", "tiempo", "solucion", "costo")

tabla = ttk.Treeview(root, columns=columnas, show="headings", height=4)
tabla.heading("algoritmo", text="Algoritmo")
tabla.heading("nodos", text="Nodos")
tabla.heading("tiempo", text="Tiempo (s)")
tabla.heading("solucion", text="Solución")
tabla.heading("costo", text="Costo")
tabla.column("algoritmo", width=250, anchor="center")
tabla.column("nodos", width=100, anchor="center")
tabla.column("tiempo", width=100, anchor="center")
tabla.column("solucion", width=100, anchor="center")
tabla.column("costo", width=100, anchor="center")
tabla.pack(pady=10)

for nombre in NOMBRES_ALGORITMOS:
    tabla.insert("", "end", iid=nombre, values=(nombre, "-", "-", "-", "-")) 

def generar_horario():
    estructuras, error = preparar_datos(datos)
    if error:
        messagebox.showerror("Datos incompletos", error)
        return
    dic_clases, no_disponibles, orden_clases, franjas, salones = estructuras
    nombre = selector_algoritmo.get()       
    funcion = ALGORITMOS[nombre]       
    inicio = time.perf_counter()
    resultado = funcion({}, orden_clases, franjas, salones, dic_clases, no_disponibles)
    fin = time.perf_counter()

    tiempo = fin - inicio
    solucion, nodos, mensaje = resultado
    encontro = "Sí" if solucion is not None else "No"
    costo = costo_solucion(solucion, dic_clases, no_disponibles)
    tabla.item(nombre, values=(nombre, nodos, f"{tiempo:.4f}", encontro, costo if costo is not None else "-"))

boton_generar_horario = tk.Button(root, text="Generar Horario", command=generar_horario)
boton_generar_horario.config(font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", activebackground="#45a049", activeforeground="white")
boton_generar_horario.pack(pady=20)

root.mainloop()