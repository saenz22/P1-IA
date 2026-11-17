import tkinter as tk

FONDO = "#F4F6FB"
ACENTO = "#4F46E5"
TEXTO = "#1F2937"
BORDES = "#E5E7EB"
CELDA_LIBRE = "#F3F4F6"
COLORES_MATERIA = (
    "#DBEAFE",
    "#FEF3C7",
    "#DCFCE7",
    "#FCE7F3",
    "#EDE9FE",
    "#FFEDD5",
    "#CFFAFE",
    "#FEE2E2",
)


def construir_datos_grilla(solucion, franjas, dic_clases, nombres_profes):
    """
    PARTE 1 (sin tkinter): convierte la solución en datos listos para dibujar.

    Recibe:
        solucion: {id_clase: (id_franja, id_salon)}
        franjas: lista de objetos Franja (tienen id, dia, inicio, fin)
        dic_clases: {id_clase: Clase}
        nombres_profes: {id_profesor: nombre}

    Devuelve (dias, horarios, celdas):
        dias: lista de días distintos, en orden de aparición (columnas)
        horarios: lista de tuplas (inicio, fin) distintas (filas)
        celdas: {(dia, inicio, fin): [texto, texto, ...]}

    Pasos:
      1. Recorrer 'franjas' y llenar 'dias' y 'horarios' sin repetir.
         (Piensa: ¿lista o conjunto? ¿qué pasa con el orden?)
      2. Armar un diccionario {id_franja: objeto Franja} para buscar rápido.
      3. Recorrer 'solucion'. Para cada clase, buscar su franja y su Clase,
         y armar el texto "materia / profesor / salón".
      4. Guardar ese texto en la lista de su celda (dia, inicio, fin).
         Una celda puede tener VARIAS clases (salones distintos), por eso es lista.
    """
    dias = []
    horarios = []
    franjas_por_id = {}

    for franja in franjas:
        franjas_por_id[franja.id] = franja
        if franja.dia not in dias:
            dias.append(franja.dia)

        horario = (franja.inicio, franja.fin)
        if horario not in horarios:
            horarios.append(horario)

    celdas = {}
    for id_clase, (id_franja, id_salon) in (solucion or {}).items():
        franja = franjas_por_id[id_franja]
        clase = dic_clases[id_clase]
        nombre_profesor = nombres_profes.get(
            clase.profesorId, clase.profesorId
        )
        texto = f"{clase.materia} / {nombre_profesor} / Salón {id_salon}"
        clave_celda = (franja.dia, franja.inicio, franja.fin)
        celdas.setdefault(clave_celda, []).append(texto)

    return dias, horarios, celdas


def mostrar_horario(padre, dias, horarios, celdas):
    """
    PARTE 2 (tkinter): abre una ventana Toplevel con la grilla.

    Pasos:
      1. Crear tk.Toplevel(padre) y ponerle título.
      2. Fila 0: una Label por día (cabecera de columnas).
      3. Columna 0: una Label por horario "inicio-fin" (cabecera de filas).
      4. Para cada (día, horario): buscar su lista en 'celdas'.
         Si tiene textos, unirlos con saltos de línea en una Label.
         Si no tiene, dejar la celda vacía o con fondo gris.
      5. Ubicar todo con .grid(row=..., column=...).
    """
    ventana = tk.Toplevel(padre)
    ventana.title("Horario de clases")
    ventana.configure(bg=FONDO)
    ventana.option_add("*Font", "{Segoe UI} 11")

    colores_materias = {}
    for textos in celdas.values():
        for texto in textos:
            materia = texto.partition(" / ")[0]
            if materia not in colores_materias:
                indice = len(colores_materias) % len(COLORES_MATERIA)
                colores_materias[materia] = COLORES_MATERIA[indice]

    def crear_cabecera(texto):
        return tk.Label(
            ventana,
            text=texto,
            bg=ACENTO,
            fg="white",
            relief="solid",
            bd=1,
            padx=8,
            pady=6,
            font=("Segoe UI Semibold", 10),
        )

    crear_cabecera("").grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
    for columna, dia in enumerate(dias, start=1):
        crear_cabecera(dia).grid(
            row=0, column=columna, sticky="nsew", padx=1, pady=1
        )
        ventana.grid_columnconfigure(columna, weight=1)

    for fila, (inicio, fin) in enumerate(horarios, start=1):
        crear_cabecera(f"{inicio}-{fin}").grid(
            row=fila, column=0, sticky="nsew", padx=1, pady=1
        )
        ventana.grid_rowconfigure(fila, weight=1)

        for columna, dia in enumerate(dias, start=1):
            textos = celdas.get((dia, inicio, fin), [])
            fondo_celda = BORDES if textos else CELDA_LIBRE
            celda = tk.Frame(ventana, bg=fondo_celda, bd=1, relief="solid")
            celda.grid(
                row=fila, column=columna, sticky="nsew", padx=1, pady=1
            )
            if textos:
                for texto in textos:
                    materia = texto.partition(" / ")[0]
                    tk.Label(
                        celda,
                        text=texto,
                        bg=colores_materias[materia],
                        fg=TEXTO,
                        justify="left",
                        anchor="w",
                        wraplength=220,
                        padx=8,
                        pady=6,
                    ).pack(fill="x", padx=1, pady=1)

    ventana.grid_columnconfigure(0, weight=0)