import tkinter as tk
from tkinter import ttk
import time
from tkinter import messagebox
from vista.panel_carga_archivos import crear_panel, preparar_datos, datos
from vista.cuadricula import construir_datos_grilla, mostrar_horario
from algoritmos import (
    busqueda_por_amplitud,
    busqueda_costo_uniforme,
    busqueda_a_asterisco,
    busqueda_profundizacion_iterativa,
)
from costos import costo_solucion
from heuristica import heuristica

FONDO = "#F4F6FB"
ENCABEZADO = "#1F2A44"
ACENTO = "#4F46E5"
ACENTO_HOVER = "#4338CA"
TEXTO = "#1F2937"
BORDES = "#E5E7EB"
EXITO = "#16A34A"
ERROR = "#DC2626"
FUENTE = "Segoe UI"


def a_asterisco(asignaciones, orden_clases, franjas, salones, dic_clases, no_disponibles=None):
    return busqueda_a_asterisco(asignaciones, orden_clases, franjas, salones, dic_clases, heuristica, no_disponibles)

ALGORITMOS = {
    "Búsqueda por Amplitud": busqueda_por_amplitud,
    "Búsqueda de Costo Uniforme": busqueda_costo_uniforme,
    "Búsqueda A*": a_asterisco,
    "Profundización Iterativa": busqueda_profundizacion_iterativa,
}

NOMBRES_ALGORITMOS = list(ALGORITMOS.keys())

root = tk.Tk()
root.title("Asignación de Clases")
root.geometry("1000x700")
root.resizable(False, False)
root.configure(bg=FONDO)
root.option_add("*Font", "{Segoe UI} 11")

estilo = ttk.Style(root)
estilo.theme_use("clam")
estilo.configure(
    "Treeview",
    rowheight=28,
    font=(FUENTE, 10),
    background="white",
    fieldbackground="white",
    foreground=TEXTO,
    bordercolor=BORDES,
    lightcolor=BORDES,
    darkcolor=BORDES,
)
estilo.configure(
    "Treeview.Heading",
    background=ENCABEZADO,
    foreground="white",
    font=("Segoe UI Semibold", 10),
    relief="flat",
)
estilo.map(
    "Treeview",
    background=[("selected", ACENTO)],
    foreground=[("selected", "white")],
)
estilo.configure(
    "TCombobox",
    fieldbackground="white",
    background="white",
    foreground=TEXTO,
    arrowcolor=ACENTO,
    padding=6,
)
estilo.map(
    "TCombobox",
    fieldbackground=[("readonly", "white")],
    foreground=[("readonly", TEXTO)],
)

encabezado = tk.Frame(root, bg=ENCABEZADO, padx=28, pady=14)
encabezado.pack(fill="x")
tk.Label(
    encabezado,
    text="Asignación de clases",
    bg=ENCABEZADO,
    fg="white",
    font=("Segoe UI Semibold", 20),
).pack(anchor="w")
tk.Label(
    encabezado,
    text="Organiza y visualiza los horarios de tus cursos.",
    bg=ENCABEZADO,
    fg="#D1D5DB",
    font=(FUENTE, 10),
).pack(anchor="w", pady=(2, 0))

marco_carga = tk.Frame(root, bg=FONDO)
marco_carga.pack(pady=8)
crear_panel(marco_carga)
texto_instrucciones = tk.Label(
    root,
    text="Seleccione un algoritmo de búsqueda:",
    bg=FONDO,
    fg=TEXTO,
    font=("Segoe UI Semibold", 11),
)
texto_instrucciones.pack(pady=(8, 4))


selector_algoritmo = ttk.Combobox(root, values=NOMBRES_ALGORITMOS, state="readonly", width=30)
selector_algoritmo.current(0)
selector_algoritmo.pack(pady=6)
columnas = ("algoritmo", "nodos", "tiempo", "solucion", "costo")

tabla = ttk.Treeview(root, columns=columnas, show="headings", height=5)
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
tabla.tag_configure("fila_par", background="white", foreground=TEXTO)
tabla.tag_configure("fila_impar", background="#F3F4F6", foreground=TEXTO)
tabla.tag_configure("resultado_exitoso", background="#DCFCE7", foreground=EXITO)
tabla.tag_configure("resultado_fallido", background="#FEE2E2", foreground=ERROR)
tabla.pack(pady=8)

for indice, nombre in enumerate(NOMBRES_ALGORITMOS):
    etiqueta_fila = "fila_par" if indice % 2 == 0 else "fila_impar"
    tabla.insert(
        "",
        "end",
        iid=nombre,
        values=(nombre, "-", "-", "-", "-"),
        tags=(etiqueta_fila,),
    )

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
    etiqueta_resultado = (
        "resultado_exitoso" if solucion is not None else "resultado_fallido"
    )
    tabla.item(
        nombre,
        values=(
            nombre,
            nodos,
            f"{tiempo:.4f}",
            encontro,
            costo if costo is not None else "-",
        ),
        tags=(etiqueta_resultado,),
    )
    if solucion is not None:
        nombres_profes = {p.id: p.nombre for p in datos["profesores"]}
        dias, horarios, celdas = construir_datos_grilla(
            solucion, franjas, dic_clases, nombres_profes
        )
        mostrar_horario(root, dias, horarios, celdas)

boton_generar_horario = tk.Button(
    root,
    text="Generar Horario",
    command=generar_horario,
    font=("Segoe UI Semibold", 11),
    bg=ACENTO,
    fg="white",
    activebackground=ACENTO_HOVER,
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=22,
    pady=10,
)
boton_generar_horario.bind("<Enter>", lambda event: boton_generar_horario.config(bg=ACENTO_HOVER))
boton_generar_horario.bind("<Leave>", lambda event: boton_generar_horario.config(bg=ACENTO))
boton_generar_horario.pack(pady=10)

root.mainloop()