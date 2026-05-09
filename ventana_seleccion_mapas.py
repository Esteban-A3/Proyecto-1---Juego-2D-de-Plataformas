# ═════════════════════════════════════════════════════════════════
# SECCIÓN 2 — MAPA PREDETERMINADO Y SELECCIÓN DE MAPA
# Copia de esta sección va en: Diseño-de-Ventanas/ventana_seleccion_mapa.py
# ═════════════════════════════════════════════════════════════════

# Mapa predeterminado hardcodeado — siempre disponible sin archivo externo.
# El jugador arranca abajo izquierda y debe subir hasta la meta arriba derecha.
# 0=vacio 1=bloque 2=escalera 3=trampa 4=patrulla 5=lanzador 6=inicio 7=meta
MAPA_PREDETERMINADO = {
    "nombre": "The Dungeon",
    "matriz": [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,4,1,1,0,2,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,1,1,1,2,0,0,0,0,0,1,1,1,1,1],
        [0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,2,0,0,0,0,5,0,0,0,0,0,0,0,0],
        [0,0,0,0,2,0,0,3,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,2,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1],
        [6,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]
}

# Variable global que guarda el mapa elegido para pasarlo al juego
mapa_seleccionado = None

def obtener_lista_mapas():
    mapas = [MAPA_PREDETERMINADO]
    guardados = leer_todos_los_mapas()
    for m in guardados:
        mapas.append(m)
    return mapas

def mostrar_seleccion_mapa():
    global mapa_seleccionado
    for widget in ventana.winfo_children():
        widget.destroy()

    ancho = 800
    alto  = 600

    canvas_fondo = tk.Canvas(ventana, width=ancho, height=alto,
                             bg=COLOR_FONDO, highlightthickness=0)
    canvas_fondo.place(x=0, y=0)
    dibujar_fondo_pixel(canvas_fondo, ancho, alto)
    canvas_fondo.create_rectangle(0, 0, ancho, 4, fill=COLOR_TITULO, outline="")
    canvas_fondo.create_rectangle(0, alto - 4, ancho, alto, fill=COLOR_TITULO, outline="")

    frame_centro = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_centro.place(relx=0.5, rely=0.5, anchor="center")

    label_titulo = tk.Label(frame_centro, text="BRICKBOUND",
                            bg=COLOR_FONDO, fg=COLOR_TITULO, font=FUENTE_TITULO)
    label_titulo.pack(pady=(0, 4))
    parpadeo_texto(label_titulo, [True])

    tk.Label(frame_centro, text="SELECCIONA UN MAPA",
             bg=COLOR_FONDO, fg=COLOR_SUBTITULO, font=FUENTE_SUBTITULO).pack(pady=(0, 16))

    tk.Label(frame_centro, text="-- [] ---------------------- [] --",
             bg=COLOR_FONDO, fg=COLOR_ACENTO, font=FUENTE_PEQUENA).pack(pady=(0, 12))

    frame_lista = tk.Frame(frame_centro, bg=COLOR_FONDO)
    frame_lista.pack(pady=(0, 12))

    mapas = obtener_lista_mapas()

    def seleccionar_y_jugar(mapa):
        global mapa_seleccionado
        mapa_seleccionado = mapa
        mostrar_juego()

    for i in range(len(mapas)):
        mapa = mapas[i]
        es_predeterminado = (i == 0)

        frame_fila = tk.Frame(frame_lista, bg=COLOR_FONDO)
        frame_fila.pack(fill="x", pady=3)

        # Estrella para el mapa predeterminado
        if es_predeterminado:
            tk.Label(frame_fila, text="*", bg=COLOR_FONDO, fg=COLOR_TITULO,
                     font=("Courier", 14, "bold"), width=3).pack(side="left")
        else:
            tk.Label(frame_fila, text="  ", bg=COLOR_FONDO, width=3).pack(side="left")

        color_nombre = COLOR_TITULO if es_predeterminado else COLOR_BOTON
        fuente_nombre = ("Courier", 13, "bold") if es_predeterminado else ("Courier", 12)

        btn_mapa = tk.Button(frame_fila,
                             text=mapa["nombre"],
                             bg=COLOR_FONDO, fg=color_nombre,
                             font=fuente_nombre,
                             relief=tk.FLAT, bd=0,
                             activebackground=COLOR_FONDO,
                             activeforeground=COLOR_BOTON_HOVER,
                             cursor="hand2", anchor="w", width=30,
                             command=lambda m=mapa: seleccionar_y_jugar(m))
        btn_mapa.pack(side="left")
        btn_mapa.bind("<Enter>", lambda e, b=btn_mapa: b.config(fg=COLOR_BOTON_HOVER))
        btn_mapa.bind("<Leave>", lambda e, b=btn_mapa, c=color_nombre: b.config(fg=c))

        puntaje_base = calcular_puntaje_mapa(mapa["matriz"])
        tk.Label(frame_fila, text=str(puntaje_base) + " pts",
                 bg=COLOR_FONDO, fg=COLOR_SUBTITULO,
                 font=("Courier", 10)).pack(side="left", padx=(8, 0))

    if len(mapas) == 1:
        tk.Label(frame_lista,
                 text="(No hay mapas creados aun -- usa el Editor)",
                 bg=COLOR_FONDO, fg=COLOR_ACENTO, font=FUENTE_PEQUENA).pack(pady=(8, 0))

    tk.Label(frame_centro, text="-- [] ---------------------- [] --",
             bg=COLOR_FONDO, fg=COLOR_ACENTO, font=FUENTE_PEQUENA).pack(pady=(4, 12))

    btn_volver = tk.Button(frame_centro, text="<- VOLVER",
                           bg=COLOR_FONDO, fg=COLOR_SUBTITULO,
                           font=("Courier", 11), relief=tk.FLAT, bd=0,
                           activebackground=COLOR_FONDO,
                           activeforeground=COLOR_BOTON_HOVER,
                           cursor="hand2", command=mostrar_menu)
    btn_volver.pack()
    btn_volver.bind("<Enter>", lambda e: btn_volver.config(fg=COLOR_BOTON_HOVER))
    btn_volver.bind("<Leave>", lambda e: btn_volver.config(fg=COLOR_SUBTITULO))

    tk.Label(ventana, text="2026  BRICKBOUND  --  ITCR",
             bg=COLOR_FONDO, fg=COLOR_ACENTO,
             font=FUENTE_PEQUENA).place(relx=0.5, rely=0.97, anchor="center")