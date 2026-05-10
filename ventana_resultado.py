# -----------------------------------------------------------------
# SECCIÓN 6 — RESULTADO FINAL
# -----------------------------------------------------------------
# Función: mostrar_resultado
# Propósito: pantalla final que muestra si el jugador ganó o perdió, el puntaje obtenido y opciones para continuar.
# Recibe gano(True o False) y puntaje (numeros).
def mostrar_resultado(gano, puntaje):
    # Cancela el loop del juego si todavía estuviera corriendo
    if estado_juego["loop_id"] is not None:
        ventana.after_cancel(estado_juego["loop_id"]) #Cancela el loop
        estado_juego["loop_id"] = None #cambia la variable

    # Desvincula las teclas del juego
    ventana.unbind("<KeyPress>")
    ventana.unbind("<KeyRelease>")

    #Limpia la ventana
    for widget in ventana.winfo_children():#por cada objeto
        widget.destroy() #lo borra

    #Ajusta las dimenciones de la ventana
    ventana.geometry("800x600")

    #Dimenciones del canva del fondo
    ancho = 800
    alto  = 600

    # Canvas de fondo igual al menú
    canvas_fondo = tk.Canvas(ventana, width=ancho, height=alto,bg=COLOR_FONDO, highlightthickness=0)
    canvas_fondo.place(x=0, y=0)
    dibujar_fondo_pixel(canvas_fondo, ancho, alto) #Utiliza la funcion para el pixel art
    canvas_fondo.create_rectangle(0, 0, ancho, 4, fill=COLOR_TITULO, outline="")
    canvas_fondo.create_rectangle(0, alto - 4, ancho, alto, fill=COLOR_TITULO, outline="")

    #Frame para poder mostrar la informacion
    frame_centro = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_centro.place(relx=0.5, rely=0.5, anchor="center")

    # Título BRICKBOUND con parpadeo
    label_titulo = tk.Label(frame_centro,text="BRICKBOUND",bg=COLOR_FONDO,fg=COLOR_TITULO,font=FUENTE_TITULO)
    label_titulo.pack(pady=(0, 6))
    parpadeo_texto(label_titulo, [True])

    # Mensaje principal según resultado
    if gano: #Sigano se muestra verde
        color_resultado = "#27AE60"   # verde
        texto_resultado = "** VICTORIA **"
        texto_sub       = "Completaste el nivel!"
    else: #Si perdio se muestra rojo
        color_resultado = "#E74C3C"   # rojo
        texto_resultado = "** DERROTA **"
        texto_sub       = "Mejor suerte la proxima vez."

    #Texto del resultado
    tk.Label(frame_centro,text=texto_resultado,bg=COLOR_FONDO,fg=color_resultado,font=("Courier", 28, "bold")).pack(pady=(0, 4))
    #Texto del subtitulo que conrtiene un mensaje
    tk.Label(frame_centro,text=texto_sub,bg=COLOR_FONDO,fg=COLOR_SUBTITULO,font=FUENTE_SUBTITULO).pack(pady=(0, 20))

    #Decoracion
    tk.Label(frame_centro,text="-- [] ---------------------- [] --", bg=COLOR_FONDO,fg=COLOR_ACENTO,font=FUENTE_PEQUENA).pack(pady=(0, 16))

    #Texto con el nombre del jugador y puntaje
    tk.Label(frame_centro,text=nombre_jugador,bg=COLOR_FONDO,fg=COLOR_BOTON,font=("Courier", 14)).pack(pady=(0, 4))

    #Texto con el puntaje, convierte los nuemeros en texto para visualisar
    tk.Label(frame_centro,text=str(puntaje) + " pts",bg=COLOR_FONDO,fg=COLOR_TITULO,font=("Courier", 26, "bold")).pack(pady=(0, 20))

    tk.Label(frame_centro,text="-- [] ---------------------- [] --",bg=COLOR_FONDO,fg=COLOR_ACENTO,font=FUENTE_PEQUENA).pack(pady=(0, 20))

    # Botón JUGAR DE NUEVO — vuelve a la selección de mapa
    btn_nuevo = tk.Button(frame_centro,text="▶  JUGAR DE NUEVO",bg=COLOR_FONDO,fg=COLOR_BOTON,font=FUENTE_BOTON,relief=tk.FLAT,bd=0,activebackground=COLOR_FONDO,activeforeground=COLOR_BOTON_HOVER,cursor="hand2",
                            command=mostrar_seleccion_mapa)
    btn_nuevo.pack(pady=6)
    aplicar_hover(btn_nuevo) #Aplica el afecto al pasar el puntero o al presionar

    # Botón MENÚ PRINCIPAL
    btn_menu = tk.Button(frame_centro,text="⌂  MENU PRINCIPAL",bg=COLOR_FONDO,fg=COLOR_SUBTITULO,font=("Courier", 11),relief=tk.FLAT,bd=0,activebackground=COLOR_FONDO,activeforeground=COLOR_BOTON_HOVER,cursor="hand2",
                         command=mostrar_menu)
    btn_menu.pack(pady=4)
    btn_menu.bind("<Enter>", lambda e: btn_menu.config(fg=COLOR_BOTON_HOVER)) #al presionar
    btn_menu.bind("<Leave>", lambda e: btn_menu.config(fg=COLOR_SUBTITULO)) #al pasar el puntero por arriba

    # Pie de página
    tk.Label(ventana,text="2026  BRICKBOUND  --  ITCR  Introduccion a la Programacion LL",bg=COLOR_FONDO,fg=COLOR_ACENTO,font=FUENTE_PEQUENA).place(relx=0.5, rely=0.97, anchor="center")
