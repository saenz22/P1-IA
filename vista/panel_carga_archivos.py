import tkinter as tk
from tkinter import filedialog
from parser import cargarProfes, cargarSalones, cargarFranjas, cargarClases, construir_no_disponibles

datos = {}   

def cargar_archivo(clave, funcion_lectura, etiqueta_ruta, etiqueta_estado):
    """Abre el explorador, lee el archivo elegido y actualiza los indicadores."""
    ruta = filedialog.askopenfilename(filetypes=[("Texto", "*.txt")])
    if not ruta:
        return
    etiqueta_ruta.config(text=ruta)
    try:
        datos[clave] = funcion_lectura(ruta)
        etiqueta_estado.config(text="Leído correctamente", fg="green")
    except (ValueError, FileNotFoundError) as e:
        datos.pop(clave, None)
        etiqueta_estado.config(text=f"Error: {str(e)}", fg="red")

ARCHIVOS = [
    ("profesores", "Cargar profesores.txt", cargarProfes),
    ("cursos", "Cargar cursos.txt", cargarClases),
    ("salones", "Cargar salones.txt", cargarSalones),
    ("franjas", "Cargar franjas.txt", cargarFranjas),
]

def crear_panel(padre):
    """Crea el panel de carga dentro del contenedor 'padre'."""
    for fila, (clave, texto, funcion) in enumerate(ARCHIVOS):
        etiqueta_ruta = tk.Label(padre, text="(sin archivo)", anchor="w", width=45)
        etiqueta_estado = tk.Label(padre, text="Pendiente", width=35, anchor="w")
        boton = tk.Button(padre, text=texto, command=lambda c=clave, f=funcion, er=etiqueta_ruta, es=etiqueta_estado: cargar_archivo(c, f, er, es))
        boton.grid(row=fila, column=0, padx=5, pady=3)
        etiqueta_ruta.grid(row=fila, column=1)
        etiqueta_estado.grid(row=fila, column=2)

def preparar_datos(datos):
    """Valida lo cargado y arma las estructuras que piden los algoritmos.

    Devuelve (estructuras, None) si todo está bien, o (None, mensaje) si hay un problema.
    """
    faltan = [c for c in ("profesores", "cursos", "salones", "franjas") if c not in datos]
    if faltan:
        return None, f"Faltan por cargar: {', '.join(faltan)}"

    for clave in ("cursos", "franjas", "salones"):
        if not datos[clave]:
            return None, f"El archivo de {clave} está vacío"

    dic_clases = {c.id: c for c in datos["cursos"]}

    if len(dic_clases) != len(datos["cursos"]):
        return None, "Hay clases con el id repetido en cursos.txt"



    ids_franjas = {f.id for f in datos["franjas"]}
    for p in datos["profesores"]:
        desconocidas = p.franjas_no_disponibles - ids_franjas
        if desconocidas:
            return None, f"El profesor {p.id} tiene franjas que no existen: {', '.join(desconocidas)}"
    no_disponibles = construir_no_disponibles(datos["profesores"])
    orden_clases = [c.id for c in datos["cursos"]]

    ids_profes = {p.id for p in datos["profesores"]}
    for c in datos["cursos"]:
        if c.profesorId not in ids_profes:
            return None, f"La clase {c.id} tiene un profesor que no existe: {c.profesorId}"

    return (dic_clases, no_disponibles, orden_clases, datos["franjas"], datos["salones"]), None

if __name__ == "__main__":
    ventana = tk.Tk()
    crear_panel(ventana)
    ventana.mainloop()