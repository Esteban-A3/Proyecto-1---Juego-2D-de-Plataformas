def leer_puntajes():
    puntajes = []
    try:
        archivo = open("puntajes.txt", "r", encoding="utf-8")
        lineas = archivo.readlines()
        archivo.close()
    except:
        return puntajes
    for linea in lineas:
        linea = linea.strip()
        if linea == "":
            continue
        partes = linea.split(";")
        if len(partes) == 2:
            puntajes.append([partes[0], int(partes[1])])
    for i in range(len(puntajes)):
        for j in range(len(puntajes) - 1 - i):
            if puntajes[j][1] < puntajes[j + 1][1]:
                puntajes[j], puntajes[j + 1] = puntajes[j + 1], puntajes[j]
    return puntajes

def guardar_puntaje(nombre, puntaje):
    puntajes = leer_puntajes()
    puntajes.append([nombre, puntaje])
    for i in range(len(puntajes)):
        for j in range(len(puntajes) - 1 - i):
            if puntajes[j][1] < puntajes[j + 1][1]:
                puntajes[j], puntajes[j + 1] = puntajes[j + 1], puntajes[j]
    puntajes = puntajes[:5]
    archivo = open("puntajes.txt", "w", encoding="utf-8")
    for entrada in puntajes:
        archivo.write(entrada[0] + ";" + str(entrada[1]) + "\n")
    archivo.close()

def mostrar_puntajes():
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

    tk.Label(frame_centro, text="MEJORES PUNTAJES",
             bg=COLOR_FONDO, fg=COLOR_SUBTITULO, font=FUENTE_SUBTITULO).pack(pady=(0, 20))

    tk.Label(frame_centro, text="-- [] ---------------------- [] --",
             bg=COLOR_FONDO, fg=COLOR_ACENTO, font=FUENTE_PEQUENA).pack(pady=(0, 16))

    puntajes = leer_puntajes()
    medallas = ["1.", "2.", "3.", "4.", "5."]
    colores_puesto = ["#F5C542", "#C0C0C0", "#CD7F32", COLOR_BOTON, COLOR_BOTON]

    if len(puntajes) == 0:
        tk.Label(frame_centro, text="Aun no hay puntajes registrados.",
                 bg=COLOR_FONDO, fg=COLOR_SUBTITULO, font=("Courier", 12)).pack(pady=20)
    else:
        for i in range(len(puntajes)):
            frame_fila = tk.Frame(frame_centro, bg=COLOR_FONDO)
            frame_fila.pack(fill="x", pady=5)
            tk.Label(frame_fila, text=medallas[i], bg=COLOR_FONDO,
                     fg=colores_puesto[i], font=("Courier", 16, "bold"),
                     width=4).pack(side="left")
            tk.Label(frame_fila, text=puntajes[i][0], bg=COLOR_FONDO,
                     fg=COLOR_BOTON, font=("Courier", 14),
                     width=22, anchor="w").pack(side="left")
            tk.Label(frame_fila, text=str(puntajes[i][1]) + " pts",
                     bg=COLOR_FONDO, fg=colores_puesto[i],
                     font=("Courier", 14, "bold"),
                     width=10, anchor="e").pack(side="left")

    tk.Label(frame_centro, text="-- [] ---------------------- [] --",
             bg=COLOR_FONDO, fg=COLOR_ACENTO, font=FUENTE_PEQUENA).pack(pady=(20, 12))

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