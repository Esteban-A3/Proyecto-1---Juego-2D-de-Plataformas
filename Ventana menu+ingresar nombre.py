import tkinter as tk

# -----------------------------------------------------------------
# BrickBound — main.py
# Curso: Introducción a la Programación LL — ITCR
# Descripción: Archivo principal del juego. Contiene toda la lógica, ventanas y funciones del programa.
# -----------------------------------------------------------------

#Variables utilizadas
nombre_jugador = ""  #Se utiliza principalmente para registrar el nombre en la pantalla de Score ademas para poder implementar otras funciones

# ── Paleta de colores ──
COLOR_FONDO       = "#0a0a0f"   # Negro azulado profundo
COLOR_TITULO      = "#f5c542"   # Amarillo arcade
COLOR_SUBTITULO   = "#888899"   # Gris azulado
COLOR_BOTON       = "#e0e0f0"   # Blanco suave
COLOR_BOTON_HOVER = "#f5c542"   # Amarillo al pasar el mouse
COLOR_ACENTO      = "#3a3a5c"   # Azul oscuro para separadores
COLOR_PIXEL_1     = "#1a1a2e"   # Para el fondo de cuadrícula
COLOR_PIXEL_2     = "#16213e"   # Alternado

# ── Tipografías ──
FUENTE_TITULO    = ("Courier", 42, "bold")
FUENTE_SUBTITULO = ("Courier", 11)
FUENTE_BOTON     = ("Courier", 15, "bold")
FUENTE_PEQUENA   = ("Courier", 9)

# -----------------------------------------------------------------
# SECCIÓN 1 — MENÚ PRINCIPAL
# Copia de esta sección va en: Diseño-de-Ventanas/ventana_menu.py
# -----------------------------------------------------------------

# Función auxiliar: efecto hover en botones
# Cambia color al pasar y al salir el mouse del botón
def aplicar_hover(boton):
    boton.bind("<Enter>", lambda e: boton.config(fg=COLOR_BOTON_HOVER))
    boton.bind("<Leave>", lambda e: boton.config(fg=COLOR_BOTON))

# Función auxiliar: animación de parpadeo en el título
# Alterna entre el color normal y transparente (fondo) cada 600ms
def parpadeo_texto(label_Texto, estado_visible):
    if estado_visible[0]:
        label_Texto.config(fg=COLOR_TITULO)
    else:
        label_Texto.config(fg="#7a6210")  #Amarillo un poco mas oscuro que el titulo
    estado_visible[0] = not estado_visible[0]  #Niega el estado para poder intercalar los colores
    label_Texto.after(600, parpadeo_texto, label_Texto, estado_visible) #Hace un conteo para despues volver a llamar a la funcion

# Función: dibujar cuadrícula de fondo tipo pixel art
# Dibuja una grilla sutil en el canvas de fondo
def dibujar_fondo_pixel(canvas, ancho, alto):
    tamano = 32  # tamaño de cada "pixel" de fondo
    for fila in range(0, alto, tamano): #Iteracion simple que va a ir intercalando los rectangulos pero en vertical
        for col in range(0, ancho, tamano):  #Iteracion simple que va a ir intercalando los rectangulos pero en horizontal
            # Alterna colores para dar textura de cuadrícula sutil
            if (fila // tamano + col // tamano) % 2 == 0:
                color = COLOR_PIXEL_1
            else:
                color = COLOR_PIXEL_2
            #Crea rectangulos individuales que van escalando primeramente horizontal y despues vertical
            canvas.create_rectangle(col, fila, col + tamano, fila + tamano,fill=color, outline="") 

# Función principal: mostrar_menu 
# Limpia la ventana y construye la pantalla del menú principal
# Recibe la ventana principal y los callbacks de navegación
def mostrar_menu():
    # Limpiar ventana
    for widget in ventana.winfo_children():
        widget.destroy()

    #Dimensiones
    ancho = 800
    alto  = 600

    # ── Canvas de fondo con cuadrícula pixel art ──
    canvas_fondo = tk.Canvas(ventana, width=ancho, height=alto,bg=COLOR_FONDO, highlightthickness=0)
    canvas_fondo.place(x=0, y=0)
    dibujar_fondo_pixel(canvas_fondo, ancho, alto)

    # Línea decorativa horizontal superior
    canvas_fondo.create_rectangle(0, 0, ancho, 4, fill=COLOR_TITULO, outline="")
    # Línea decorativa horizontal inferior
    canvas_fondo.create_rectangle(0, alto - 4, ancho, alto, fill=COLOR_TITULO, outline="")

    # ── Frame central sobre el canvas ──
    frame_centro = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_centro.place(relx=0.5, rely=0.5, anchor="center")

    # ── Título del juego ──
    label_titulo = tk.Label(frame_centro,text="BRICKBOUND",bg=COLOR_FONDO,fg=COLOR_TITULO,font=FUENTE_TITULO)
    label_titulo.pack(pady=(0, 4))
    estado_visible = [True]
    parpadeo_texto(label_titulo, estado_visible)

    # ── Subtítulo ──
    frame_sub = tk.Frame(frame_centro, bg=COLOR_FONDO)
    frame_sub.pack(pady=(0, 40))
    #Texto del subtitulo
    tk.Label(frame_sub,text="2D PLATFORM ADVENTURE",bg=COLOR_FONDO,fg=COLOR_SUBTITULO,font=FUENTE_SUBTITULO).pack(side="left")

    # ── Separador decorativo ──
    tk.Label(frame_centro,text="── ■ ──────────────────── ■ ──",bg=COLOR_FONDO,fg=COLOR_ACENTO,font=FUENTE_PEQUENA).pack(pady=(0, 30))

    # ── Botones del menú ──
    # Cada botón llama a su callback correspondiente al presionar

    # Botón JUGAR
    btn_jugar = tk.Button(frame_centro,text="▶  JUGAR", bg=COLOR_FONDO,fg=COLOR_BOTON,font=FUENTE_BOTON,relief=tk.FLAT,
    bd=0,activebackground=COLOR_FONDO,activeforeground=COLOR_BOTON_HOVER,cursor="hand2",command=mostrar_nombre)
    btn_jugar.pack(pady=8)
    aplicar_hover(btn_jugar)

    # Botón EDITOR DE MAPAS
    btn_editor = tk.Button(frame_centro,text="✎  EDITOR DE MAPAS",bg=COLOR_FONDO,fg=COLOR_BOTON,font=FUENTE_BOTON,relief=tk.FLAT,
    bd=0,activebackground=COLOR_FONDO,activeforeground=COLOR_BOTON_HOVER,cursor="hand2",command=())
    btn_editor.pack(pady=8)
    aplicar_hover(btn_editor)

    # Botón PUNTAJES
    btn_puntajes = tk.Button(frame_centro,text="★  PUNTAJES",bg=COLOR_FONDO,fg=COLOR_BOTON,font=FUENTE_BOTON,relief=tk.FLAT,
    bd=0,activebackground=COLOR_FONDO,activeforeground=COLOR_BOTON_HOVER,cursor="hand2",command=())
    btn_puntajes.pack(pady=8)
    aplicar_hover(btn_puntajes)

    # Separador antes de Salir
    tk.Label(frame_centro,text="── ■ ──────────────────── ■ ──",bg=COLOR_FONDO,fg=COLOR_ACENTO,font=FUENTE_PEQUENA).pack(pady=(20, 8))

    # Botón SALIR (menos llamativo, color más tenue)
    btn_salir = tk.Button(frame_centro,text="✕  SALIR",bg=COLOR_FONDO,fg=COLOR_SUBTITULO,font=("Courier", 11),relief=tk.FLAT, bd=0,
    activebackground=COLOR_FONDO,activeforeground=COLOR_BOTON_HOVER,cursor="hand2",command=ventana.quit)
    btn_salir.pack(pady=(0, 10))
    #Se hace una logica igual a la de la funcion para hover, solamente que esta es menos llamativa
    btn_salir.bind("<Enter>", lambda e: btn_salir.config(fg=COLOR_BOTON_HOVER)) #Eventos de presionar, ademas tiene un lamba para identificar si es presionado pero no activado
    btn_salir.bind("<Leave>", lambda e: btn_salir.config(fg=COLOR_SUBTITULO))

    # ── Pie de página ──
    tk.Label(ventana,text="© 2026  BRICKBOUND  —  ITCR  Introducción a la Programación LL",bg=COLOR_FONDO,fg=COLOR_ACENTO,
             font=FUENTE_PEQUENA).place(relx=0.5, rely=0.97, anchor="center")

# -----------------------------------------------------------------
# Seccion 1,5 - Nombre del Jugador
# Pantalla donde se establece el nombre del jugador
# -----------------------------------------------------------------

# Función: generar_nombre_predeterminado
# Propósito: si el jugador no ingresa un nombre, genera uno
# automático tipo "Brick Player 1". Si ese ya existe
# en los puntajes, incrementa el número.
def generar_nombre_predeterminado():
    puntajes = leer_puntajes()                          # Lee los puntajes guardados
    nombres_guardados = [p[0] for p in puntajes]        # Extrae solo los nombres
    contador = 1                                        # Para saber si ya se uso un nombre predeterminado
    while True:
        candidato = "Brick Player " + str(contador)
        if candidato not in nombres_guardados:          # Si el nombre no está usado, lo usa
            return candidato
        contador = contador + 1                         # Si ya está, prueba con el siguiente número

# Función: mostrar_nombre
# Propósito: pantalla donde el jugador ingresa su nombre antes
# de seleccionar el mapa. Guarda el resultado en la variable global nombre_jugador.
def mostrar_nombre():
    global nombre_jugador #importa la variable del nombre 
    for widget in ventana.winfo_children():    #Escanea todos los elementos de la pantalla anterior
        widget.destroy()  #Los destrulle

    #Dimensiones del canvas
    ancho = 800 
    alto  = 600

    # Canvas de fondo con cuadrícula pixel art (igual al menú), se llama la funcion del pixel art
    canvas_fondo = tk.Canvas(ventana, width=ancho, height=alto,bg=COLOR_FONDO, highlightthickness=0)
    canvas_fondo.place(x=0, y=0)
    dibujar_fondo_pixel(canvas_fondo, ancho, alto)
    canvas_fondo.create_rectangle(0, 0, ancho, 4, fill=COLOR_TITULO, outline="")
    canvas_fondo.create_rectangle(0, alto - 4, ancho, alto, fill=COLOR_TITULO, outline="")

    # Frame central
    frame_centro = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_centro.place(relx=0.5, rely=0.5, anchor="center")

    # Título con parpadeo (igual al menú)
    label_titulo = tk.Label(frame_centro, text="BRICKBOUND",bg=COLOR_FONDO,fg=COLOR_TITULO,font=FUENTE_TITULO)
    label_titulo.pack(pady=(0, 6))
    estado_titulo = [True]
    parpadeo_texto(label_titulo, estado_titulo)

    # Subtítulo
    tk.Label(frame_centro,text="INGRESA TU NOMBRE",bg=COLOR_FONDO,fg=COLOR_SUBTITULO,font=FUENTE_SUBTITULO).pack(pady=(0, 30))

    # Separador
    tk.Label(frame_centro, text="── ■ ──────────────────── ■ ──",bg=COLOR_FONDO,fg=COLOR_ACENTO,font=FUENTE_PEQUENA).pack(pady=(0, 20))

    # Campo de texto para el nombre
    entry_nombre = tk.Entry(frame_centro,bg=COLOR_PIXEL_1,fg=COLOR_BOTON,font=("Courier", 16),
    insertbackground=COLOR_TITULO,   # cursor de escritura amarillo
    relief=tk.FLAT,width=20,justify="center")
    entry_nombre.pack(pady=(0, 6))
    entry_nombre.focus()  # El cursor aparece directo en el campo

    # Mensaje de ayuda debajo del campo
    label_ayuda = tk.Label(frame_centro,text="(dejá vacío para un nombre automático)",bg=COLOR_FONDO,fg=COLOR_ACENTO,font=FUENTE_PEQUENA)
    label_ayuda.pack(pady=(0, 30))

    # Separador
    tk.Label(frame_centro,text="── ■ ──────────────────── ■ ──",bg=COLOR_FONDO,fg=COLOR_ACENTO,font=FUENTE_PEQUENA).pack(pady=(0, 20))

    # Función interna: confirmar_nombre
    # Propósito: lee el entry, asigna nombre o genera uno predeterminado, y avanza a selección de mapa.
    def confirmar_nombre():
        global nombre_jugador  #Llama para verificar el nombre
        texto = entry_nombre.get().strip()          # Elimina espacios al inicio y al final
        if texto == "":   #Si no tiene genera uno
            nombre_jugador = generar_nombre_predeterminado()
        else:
            nombre_jugador = texto                  #Asigna a la variable el nombre escogido por el usuario
        mostrar_seleccion_mapa()                    # Avanza a la siguiente pantalla

    # Botón CONFIRMAR — también responde al Enter
    btn_confirmar = tk.Button(frame_centro,text="▶  CONFIRMAR",bg=COLOR_FONDO,fg=COLOR_BOTON,font=FUENTE_BOTON,relief=tk.FLAT,bd=0,activebackground=COLOR_FONDO,
    activeforeground=COLOR_BOTON_HOVER,cursor="hand2",command=confirmar_nombre)
    btn_confirmar.pack(pady=8)
    aplicar_hover(btn_confirmar)

    # Enter también confirma, más cómodo para el jugador
    ventana.bind("<Return>", lambda e: confirmar_nombre())

    # Botón VOLVER
    btn_volver = tk.Button(frame_centro,text="← VOLVER",bg=COLOR_FONDO,fg=COLOR_SUBTITULO,font=("Courier", 11),relief=tk.FLAT,bd=0,activebackground=COLOR_FONDO,
    activeforeground=COLOR_BOTON_HOVER,cursor="hand2",command=mostrar_menu)
    btn_volver.pack(pady=(0, 10))
    #Colores cuando se presiona el boton menos llamativos
    btn_volver.bind("<Enter>", lambda e: btn_volver.config(fg=COLOR_BOTON_HOVER))
    btn_volver.bind("<Leave>", lambda e: btn_volver.config(fg=COLOR_SUBTITULO))

    # Pie de página
    tk.Label(ventana,text="© 2026  BRICKBOUND  —  ITCR  Introducción a la Programación LL", bg=COLOR_FONDO,fg=COLOR_ACENTO,font=FUENTE_PEQUENA).place(relx=0.5, rely=0.97, anchor="center")

ventana = tk.Tk()
ventana.title("BrickBound")
ventana.geometry("800x600")
ventana.resizable(False, False)
ventana.config(bg=COLOR_FONDO)
 
mostrar_menu()
 
ventana.mainloop()