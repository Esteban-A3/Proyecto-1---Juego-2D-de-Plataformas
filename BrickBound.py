import tkinter as tk
import os
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# -----------------------------------------------------------------
# BrickBound — main.py
# Curso: Introducción a la Programación LL — ITCR
# Descripción: Archivo principal del juego. Contiene toda la lógica, ventanas y funciones del programa.
# -----------------------------------------------------------------

#Variables globales utilizadas
nombre_jugador = ""  #Se utiliza principalmente para registrar el nombre en la pantalla de Score ademas para poder implementar otras funciones
mapa_seleccionado = None # Variable global que guarda el mapa elegido para pasarlo al juego

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
    bd=0,activebackground=COLOR_FONDO,activeforeground=COLOR_BOTON_HOVER,cursor="hand2",command=verificar_nombre_J)
    btn_jugar.pack(pady=8)
    aplicar_hover(btn_jugar)

    # Botón EDITOR DE MAPAS
    btn_editor = tk.Button(frame_centro,text="✎  EDITOR DE MAPAS",bg=COLOR_FONDO,fg=COLOR_BOTON,font=FUENTE_BOTON,relief=tk.FLAT,
    bd=0,activebackground=COLOR_FONDO,activeforeground=COLOR_BOTON_HOVER,cursor="hand2",command=verificar_nombre_E)
    btn_editor.pack(pady=8)
    aplicar_hover(btn_editor)

    # Botón PUNTAJES
    btn_puntajes = tk.Button(frame_centro,text="★  PUNTAJES",bg=COLOR_FONDO,fg=COLOR_BOTON,font=FUENTE_BOTON,relief=tk.FLAT,
    bd=0,activebackground=COLOR_FONDO,activeforeground=COLOR_BOTON_HOVER,cursor="hand2",command=mostrar_puntajes)
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
#Función: verificar_nombre
# Propósito: si el jugador no tiene nombre le pide uno antes de avanzar al editor o al juego
# solo aparece una vez por sesion ya que una vez escrito el nombre esta funcion impide escribir otro
def verificar_nombre_J():
    if nombre_jugador == "":
        mostrar_nombre()
    else:
        mostrar_seleccion_mapa()
def verificar_nombre_E():
    if nombre_jugador == "":
        mostrar_nombre()
    else:
        mostrar_editor()


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
        mostrar_menu()                    #Registra el nombre y permite avanzar

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


# -----------------------------------------------------------------
# SECCIÓN 2 — SELECCIÓN DE MAPA
# -----------------------------------------------------------------
# Mapa predeterminado — siempre disponible sin archivo externo.
# 0=vacio 1=bloque 2=escalera 3=trampa 4=patrulla 5=lanzador 6=inicio 7=meta
MAPA_PREDETERMINADO = {
    "nombre":"The Dungeon",
    "matriz": [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,7],
        [2,1,1,1,0,0,0,0,0,0,0,0,0,5,0,0,0,1,1,1,1,0,1,1,1],
        [2,0,0,0,0,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [2,0,3,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,2],
        [1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,2],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [1,1,1,1,1,1,3,3,1,1,1,1,1,1,1,1,1,3,3,1,1,1,1,1,1],
    ]
}

# Función: obtener_lista_mapas
# Propósito: Obtiene la lista de mapas dada por la funcion leer mapas ademas hace una nueva lista con el mapa predeterminado como primero
def obtener_lista_mapas():
    mapas = [MAPA_PREDETERMINADO] #Crea una nueva lista con los mapas y teniendo de primero el mapa redeterminado
    guardados = leer_todos_los_mapas() #Extrae los mapas guardados
    for m in guardados: #por cada mapa que extrae
        mapas.append(m) #Los agrega en la lista
    return mapas

def mostrar_seleccion_mapa():

    global mapa_seleccionado #Estrae la variable para saber que selecciono
    for widget in ventana.winfo_children(): #Por cada elemento en la pantalla
        widget.destroy() #Lo borra

    #Dimensiones
    ancho = 800
    alto  = 600

    #El canvas de fondo para los cuadros
    canvas_fondo = tk.Canvas(ventana, width=ancho, height=alto,bg=COLOR_FONDO, highlightthickness=0)
    canvas_fondo.place(x=0, y=0)
    dibujar_fondo_pixel(canvas_fondo, ancho, alto)
    canvas_fondo.create_rectangle(0, 0, ancho, 4, fill=COLOR_TITULO, outline="")
    canvas_fondo.create_rectangle(0, alto - 4, ancho, alto, fill=COLOR_TITULO, outline="")

    #Frame del centro donde va la informacion
    frame_centro = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_centro.place(relx=0.5, rely=0.5, anchor="center")

    #Titulo del juego
    label_titulo = tk.Label(frame_centro, text="BRICKBOUND",bg=COLOR_FONDO, fg=COLOR_TITULO, font=FUENTE_TITULO)
    label_titulo.pack(pady=(0, 4))
    parpadeo_texto(label_titulo, [True]) #Parpadeo

    #Subtitulo
    tk.Label(frame_centro, text="SELECCIONA UN MAPA",bg=COLOR_FONDO, fg=COLOR_SUBTITULO, font=FUENTE_SUBTITULO).pack(pady=(0, 16))

    #Decoracion
    tk.Label(frame_centro, text="-- [] ---------------------- [] --",bg=COLOR_FONDO, fg=COLOR_ACENTO, font=FUENTE_PEQUENA).pack(pady=(0, 12))

    #Crea un frame lista para poder ubicar los nombres verticalmente
    frame_lista = tk.Frame(frame_centro, bg=COLOR_FONDO)
    frame_lista.pack(pady=(0, 12))

    #Variable con los mapas
    mapas = obtener_lista_mapas()

    #Funcion que establece el mapa seleccionado y lo registra en la variable
    def seleccionar_y_jugar(mapa):
        global mapa_seleccionado
        mapa_seleccionado = mapa
        mostrar_juego() #Ejecuta el juego

    for i in range(len(mapas)): #Por cada mapa en la lista de mapas
        mapa = mapas[i] #El mapa es la posicion donde se encuentra en la lista
        es_predeterminado = (i == 0) #Exepto el predeterminado

        #Crea un frame de fila para poder escribir los mapas y que se vea ordenado
        frame_fila = tk.Frame(frame_lista, bg=COLOR_FONDO)
        frame_fila.pack(fill="x", pady=3)

        #Simbolos
        if es_predeterminado:
            tk.Label(frame_fila, text="*", bg=COLOR_FONDO, fg=COLOR_TITULO,font=("Courier", 12, "bold"), width=3).pack(side="left") #Estrella para el predeterminado
        else:
            tk.Label(frame_fila, text="✎", bg=COLOR_FONDO,fg=COLOR_BOTON,font=("Courier", 12, "bold"), width=3).pack(side="left") #Lapiz para los demas que son creados con el editor de mapas

        #Colores y funente de las letras
        color_nombre = COLOR_TITULO if es_predeterminado else COLOR_BOTON  #Amarillo por si es predeterminado, si no el color gris
        fuente_nombre = ("Courier", 12, "bold") #Fuente

        #Diseño de los boton para seleccionar el mapa
        btn_mapa = tk.Button(frame_fila,text=mapa["nombre"],bg=COLOR_FONDO, fg=color_nombre,font=fuente_nombre, relief=tk.FLAT, bd=0,activebackground=COLOR_FONDO,activeforeground=COLOR_BOTON_HOVER,cursor="hand2", anchor="w", width=30,
        command=lambda m=mapa: seleccionar_y_jugar(m))
        btn_mapa.pack(side="left")
        btn_mapa.bind("<Enter>", lambda e, b=btn_mapa: b.config(fg=COLOR_BOTON_HOVER)) #Color al presionar
        btn_mapa.bind("<Leave>", lambda e, b=btn_mapa, c=color_nombre: b.config(fg=c)) #Color al pasar el puntero por encima

        puntaje_base = calcular_puntaje_mapa(mapa["matriz"]) #Es el puntaje del mapa
        #Texto del puntaje
        tk.Label(frame_fila, text=str(puntaje_base) + " pts",bg=COLOR_FONDO, fg=COLOR_SUBTITULO,font=("Courier", 10)).pack(side="left", padx=(8, 0))

    #Si solo hay un mapar(el predeterminado), que muestre un texto al jugador para que cree otro mapa
    if len(mapas) == 1:
        tk.Label(frame_lista,text="(No hay mapas creados aun -- usa el Editor)",bg=COLOR_FONDO, fg=COLOR_ACENTO, font=FUENTE_PEQUENA).pack(pady=(8, 0))

    #Decoracion
    tk.Label(frame_centro, text="-- [] ---------------------- [] --",bg=COLOR_FONDO, fg=COLOR_ACENTO, font=FUENTE_PEQUENA).pack(pady=(4, 12))

    #Boton para volver al menu
    btn_volver = tk.Button(frame_centro, text="<- VOLVER",bg=COLOR_FONDO, fg=COLOR_SUBTITULO,font=("Courier", 11), relief=tk.FLAT, bd=0,activebackground=COLOR_FONDO,activeforeground=COLOR_BOTON_HOVER,cursor="hand2", command=mostrar_menu)
    btn_volver.pack()
    btn_volver.bind("<Enter>", lambda e: btn_volver.config(fg=COLOR_BOTON_HOVER)) #Color al presioar
    btn_volver.bind("<Leave>", lambda e: btn_volver.config(fg=COLOR_SUBTITULO)) #Color al pasar el mause

    #Texto de pie de pagina
    tk.Label(ventana, text="2026  BRICKBOUND  --  ITCR",bg=COLOR_FONDO, fg=COLOR_ACENTO,font=FUENTE_PEQUENA).place(relx=0.5, rely=0.97, anchor="center")
 
# -----------------------------------------------------------------
# SECCIÓN 3 — JUEGO
# -----------------------------------------------------------------

# Constantes del juego
ANCHO_JUEGO    = 800   # ancho del canvas de juego
ALTO_JUEGO     = 480   # alto del canvas (15 filas * 32px)
ALTO_HUD       = 60    # alto de la barra superior HUD
TAM_CELDA_J    = 32    # tamaño de celda en el juego

GRAVEDAD       = 0.5   # aceleración gravitacional por frame
VEL_SALTO      = -10   # velocidad inicial del salto (negativo = arriba)
VEL_MOVIMIENTO = 4     # velocidad horizontal del jugador
VEL_ESCALERA   = 3     # velocidad al subir/bajar escalera

TIEMPO_INVENCIBLE  = 120   # frames de invencibilidad tras recibir daño (~2seg a 60fps)
TIEMPO_ANIM_FRAME  = 6     # frames entre cada cambio de sprite

PUNTAJE_PENALIZACION = 300  # puntos que se pierden por cada vida perdida

# Variables de estado del juego
# Se justifica su uso global porque son accedidas por múltiples
# funciones: movimiento, colisión, dibujo y HUD.

estado_juego = {
    "vidas":3, 
    "puntaje":0, 
    "jugando": False,   #Si esta jugando
    "invencible": 0,    # contador de frames de invencibilidad
    "loop_id": None,    # id del after() para poder cancelarlo
}

jugador = { 
    "x":0,     # posición en x
    "y":0,     # posicion en y
    "vel_x":0, #velocidad en x
    "vel_y":0, #velocidad en y
    "en_suelo":False, #Si esta tocando un suelo
    "en_escalera":False, #Si esta en la escalera
    "mirando_der":True, #si esta mirando a la derecha
    "estado":"idle",   #Estado en el que esta el jugador; idle (quieto)/ run(corriendo) / jump(saltando) / fall(callendo) / hit(lo estan golpeando)
    "frame_anim":0,"contador_anim": 0,}

# Lista de enemigos activos en la partida
enemigos_activos = []
# Lista de proyectiles activos
proyectiles_activos = []
# Teclas presionadas actualmente
teclas_presionadas = {}
# Referencias a los sprites cargados con Pillow (PhotoImage de Tkinter)
sprites = {}

# Función: cargar_sprites
# Propósito: carga todos los assets desde la carpeta /assets y los convierte a PhotoImage para usarlos en el canvas.
# Ademas extrae frames individuales de los spritesheets.
def cargar_sprites():
    global sprites
    from PIL import Image, ImageTk
 
    ruta_assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")#define la ruta en este caso la capeta
 
    # ── Extrae un frame de un spritesheet y lo convierte a PhotoImage ──
    def get_frame(nombre_archivo, frame_idx, ancho_frame, alto_frame, escala_w=None, escala_h=None):
        ruta  = os.path.join(ruta_assets, nombre_archivo)
        img   = Image.open(ruta).convert("RGBA")
        x1    = frame_idx * ancho_frame
        frame = img.crop((x1, 0, x1 + ancho_frame, alto_frame))
        if escala_w and escala_h:
            frame = frame.resize((escala_w, escala_h), Image.NEAREST)
        return ImageTk.PhotoImage(frame)
 
    # ── Igual pero también genera versión espejo ──
    def get_frame_con_espejo(nombre_archivo, frame_idx, ancho_frame, alto_frame, escala_w=None, escala_h=None):
        ruta  = os.path.join(ruta_assets, nombre_archivo)
        img   = Image.open(ruta).convert("RGBA")
        x1    = frame_idx * ancho_frame
        frame = img.crop((x1, 0, x1 + ancho_frame, alto_frame))
        if escala_w and escala_h:
            frame = frame.resize((escala_w, escala_h), Image.NEAREST)
        espejo = frame.transpose(Image.FLIP_LEFT_RIGHT)
        return ImageTk.PhotoImage(frame), ImageTk.PhotoImage(espejo)
 
    # ── Carga imagen completa escalada ──
    def get_img(nombre_archivo, ancho, alto):
        ruta = os.path.join(ruta_assets, nombre_archivo)
        img  = Image.open(ruta).convert("RGBA")
        img  = img.resize((ancho, alto), Image.NEAREST)
        return ImageTk.PhotoImage(img)
 
    # ── Genera versión blanqueada de un frame (efecto hit) ──
    def blanquear(nombre_archivo, frame_idx, ancho_frame, alto_frame):
        ruta  = os.path.join(ruta_assets, nombre_archivo)
        img   = Image.open(ruta).convert("RGBA")
        x1    = frame_idx * ancho_frame
        frame = img.crop((x1, 0, x1 + ancho_frame, alto_frame))
        r, g, b, a = frame.split()
        # Pone todos los canales de color en blanco, mantiene transparencia
        blanco = Image.new("L", frame.size, 255)
        frame_blanco = Image.merge("RGBA", (blanco, blanco, blanco, a))
        return ImageTk.PhotoImage(frame_blanco)

    # JUGADOR — 32x32px por frame
    # Se generan listas de (normal, espejo) por frame
    sprites["jugador_idle"]  = [] #lista normal
    sprites["jugador_idle_e"] = [] #lista espejo
    for i in range(11):
        n, e = get_frame_con_espejo("Jugador/Idle.png", i, 32, 32)
        sprites["jugador_idle"].append(n)
        sprites["jugador_idle_e"].append(e)
 
    sprites["jugador_run"]   = []
    sprites["jugador_run_e"] = []
    for i in range(12):
        n, e = get_frame_con_espejo("Jugador/Run.png", i, 32, 32)
        sprites["jugador_run"].append(n)
        sprites["jugador_run_e"].append(e)
 
    # Jump y fall son un solo frame
    n, e = get_frame_con_espejo("Jugador/Jump.png", 0, 32, 32)
    sprites["jugador_jump"]   = [n]
    sprites["jugador_jump_e"] = [e]
 
    n, e = get_frame_con_espejo("Jugador/Fall.png", 0, 32, 32)
    sprites["jugador_fall"]   = [n]
    sprites["jugador_fall_e"] = [e]
 
    # Hit: jugador blanqueado (usa frame 0 del idle blanqueado)
    hit_normal = blanquear("Jugador/Idle.png", 0, 32, 32)
    sprites["jugador_hit"]   = [hit_normal]
    sprites["jugador_hit_e"] = [hit_normal]   # el blanco es igual en ambas direcciones
 

    # ENEMIGO PATRULLA — 48x48px, se deja en 48px
    sprites["patrulla_run"]  = [get_frame("Enemigo Patrulla/Run.png",  i, 48, 48) for i in range(12)]
    sprites["patrulla_idle"] = [get_frame("Enemigo Patrulla/Idle.png", i, 48, 48) for i in range(11)]
 
    # Versiones espejo para cuando patrulla hacia la izquierda
    sprites["patrulla_run_e"]  = []
    sprites["patrulla_idle_e"] = []
    for i in range(12):
        _, e = get_frame_con_espejo("Enemigo Patrulla/Run.png", i, 48, 48)
        sprites["patrulla_run_e"].append(e)
    for i in range(11):
        _, e = get_frame_con_espejo("Enemigo Patrulla/Idle.png", i, 48, 48)
        sprites["patrulla_idle_e"].append(e)
 

    # ENEMIGO LANZADOR — 48x48px
    sprites["lanzador_idle"]   = [get_frame("Enemigo Lanzador/Idle.png",   i, 48, 48) for i in range(11)]
    sprites["lanzador_attack"] = [get_frame("Enemigo Lanzador/Attack.png", i, 48, 48) for i in range(7)]
    # PROYECTIL
    sprites["proyectil"] = get_img("Enemigo Lanzador/Cannonball1.png", 16, 16)
 
    # ELEMENTOS DEL MAPA
    sprites["bloque"]   = get_img("Bloque.png",         TAM_CELDA_J, TAM_CELDA_J)
    sprites["fondo"]    = get_img("Fondo.png",           TAM_CELDA_J, TAM_CELDA_J)
    sprites["escalera"] = get_img("Escalera.png",        TAM_CELDA_J, TAM_CELDA_J)
    sprites["trampa"]   = get_img("Trampa.png",          TAM_CELDA_J, TAM_CELDA_J)
 
    # Banderas: imágenes únicas, se escalan a 32x48 para que se vean altas
    # y se dibujan con offset para que el palo quede alineado a la celda
    sprites["meta"]    = get_img("Bandera Meta.png",    22, 48)
    sprites["inicio"]  = get_img("Bandera Salida.png",  22, 48)  


# Función: inicializar_enemigos
# Propósito: recorre la matriz del mapa y crea los diccionarios de estado para cada enemigo encontrado.
def inicializar_enemigos(matriz):
    enemigos = []
    for f in range(FILAS):
        for c in range(COLUMNAS):
            if matriz[f][c] == ENEMIGO_PAT:
                enemigos.append({
                    "tipo"      : "patrulla",
                    "x"         : c * TAM_CELDA_J,
                    "y"         : f * TAM_CELDA_J- 16,  # offset de 16px hacia arriba porque el sprite es 48px
                    "vel_x"     : 2,        # velocidad de patrulla
                    "frame"     : 0,
                    "contador"  : 0,
                    "mirando_der": True,
                })
            elif matriz[f][c] == ENEMIGO_LAN:
                enemigos.append({
                    "tipo"         : "lanzador",
                    "x"            : c * TAM_CELDA_J,
                    "y"            : f * TAM_CELDA_J - 16,  # offset de 16px hacia arriba porque el sprite es 48px
                    "frame"        : 0,
                    "contador"     : 0,
                    "contador_disparo": 0,   # cuenta frames entre disparos
                    "atacando"     : False,
                    "frame_ataque" : 0,
                })
    return enemigos

# ─────────────────────────────────────────────────────────────────
# Función: encontrar_inicio
# Propósito: busca en la matriz la celda marcada como INICIO (6)
#            y devuelve sus coordenadas en píxeles.
# ─────────────────────────────────────────────────────────────────
def encontrar_inicio(matriz):
    for f in range(FILAS):
        for c in range(COLUMNAS):
            if matriz[f][c] == INICIO:
                return c * TAM_CELDA_J, f * TAM_CELDA_J
    return 0, (FILAS - 2) * TAM_CELDA_J   # fallback

# ─────────────────────────────────────────────────────────────────
# Función: hay_bloque_en
# Propósito: verifica si una celda de la matriz contiene un bloque
#            sólido (sobre el que se puede caminar o chocar).
# ─────────────────────────────────────────────────────────────────
def hay_bloque_en(matriz, fila, col):
    if fila < 0 or fila >= FILAS or col < 0 or col >= COLUMNAS:
        return True   # fuera del mapa = sólido
    return matriz[fila][col] == BLOQUE

# ─────────────────────────────────────────────────────────────────
# Función: hay_escalera_en
# Propósito: verifica si una celda contiene una escalera.
# ─────────────────────────────────────────────────────────────────
def hay_escalera_en(matriz, fila, col):
    if fila < 0 or fila >= FILAS or col < 0 or col >= COLUMNAS:
        return False
    return matriz[fila][col] == ESCALERA

# ─────────────────────────────────────────────────────────────────
# Función: hay_trampa_en
# Propósito: verifica si una celda contiene una trampa.
# ─────────────────────────────────────────────────────────────────
def hay_trampa_en(matriz, fila, col):
    if fila < 0 or fila >= FILAS or col < 0 or col >= COLUMNAS:
        return False
    return matriz[fila][col] == TRAMPA

# ─────────────────────────────────────────────────────────────────
# Función: resolver_colision_vertical
# Propósito: mueve al jugador verticalmente y lo detiene si choca
#            con un bloque arriba o abajo. Actualiza en_suelo.
# ─────────────────────────────────────────────────────────────────
def resolver_colision_vertical(matriz):
    jugador["y"] += jugador["vel_y"]
    jugador["en_suelo"] = False

    pie_fila  = int((jugador["y"] + TAM_CELDA_J) // TAM_CELDA_J)
    pie_col_i = int(jugador["x"] // TAM_CELDA_J)
    pie_col_d = int((jugador["x"] + TAM_CELDA_J - 1) // TAM_CELDA_J)

    cab_fila  = int(jugador["y"] // TAM_CELDA_J)

    # Colisión hacia abajo
    if jugador["vel_y"] >= 0:
        if hay_bloque_en(matriz, pie_fila, pie_col_i) or hay_bloque_en(matriz, pie_fila, pie_col_d):
            jugador["y"]       = (pie_fila * TAM_CELDA_J) - TAM_CELDA_J
            jugador["vel_y"]   = 0
            jugador["en_suelo"] = True

    # Colisión hacia arriba
    if jugador["vel_y"] < 0:
        if hay_bloque_en(matriz, cab_fila, pie_col_i) or hay_bloque_en(matriz, cab_fila, pie_col_d):
            jugador["y"]     = (cab_fila + 1) * TAM_CELDA_J
            jugador["vel_y"] = 0

# ─────────────────────────────────────────────────────────────────
# Función: resolver_colision_horizontal
# Propósito: mueve al jugador horizontalmente y lo detiene si
#            choca con un bloque a izquierda o derecha.
# ─────────────────────────────────────────────────────────────────
def resolver_colision_horizontal(matriz):
    jugador["x"] += jugador["vel_x"]

    fila_cab = int(jugador["y"] // TAM_CELDA_J)
    fila_pie = int((jugador["y"] + TAM_CELDA_J - 1) // TAM_CELDA_J)

    col_der = int((jugador["x"] + TAM_CELDA_J) // TAM_CELDA_J)
    col_izq = int(jugador["x"] // TAM_CELDA_J)

    if jugador["vel_x"] > 0:
        if hay_bloque_en(matriz, fila_cab, col_der) or hay_bloque_en(matriz, fila_pie, col_der):
            jugador["x"] = (col_der * TAM_CELDA_J) - TAM_CELDA_J

    if jugador["vel_x"] < 0:
        if hay_bloque_en(matriz, fila_cab, col_izq) or hay_bloque_en(matriz, fila_pie, col_izq):
            jugador["x"] = (col_izq + 1) * TAM_CELDA_J

# ─────────────────────────────────────────────────────────────────
# Función: actualizar_jugador
# Propósito: aplica gravedad, lee teclas y actualiza posición
#            y estado del jugador en cada frame.
# ─────────────────────────────────────────────────────────────────
def actualizar_jugador(matriz):
    centro_col = int((jugador["x"] + TAM_CELDA_J // 2) // TAM_CELDA_J)
    centro_fil = int((jugador["y"] + TAM_CELDA_J // 2) // TAM_CELDA_J)

    # Detecta si el jugador está sobre una escalera
    en_escalera = hay_escalera_en(matriz, centro_fil, centro_col)
    jugador["en_escalera"] = en_escalera

    if en_escalera:
        # En escalera: sin gravedad, movimiento libre vertical
        jugador["vel_y"] = 0
        jugador["vel_x"] = 0

        if teclas_presionadas.get("Up") or teclas_presionadas.get("w"):
            jugador["vel_y"] = -VEL_ESCALERA
        if teclas_presionadas.get("Down") or teclas_presionadas.get("s"):
            jugador["vel_y"] = VEL_ESCALERA
        if teclas_presionadas.get("Left") or teclas_presionadas.get("a"):
            jugador["vel_x"] = -VEL_MOVIMIENTO
            jugador["mirando_der"] = False
        if teclas_presionadas.get("Right") or teclas_presionadas.get("d"):
            jugador["vel_x"] = VEL_MOVIMIENTO
            jugador["mirando_der"] = True

        jugador["y"] += jugador["vel_y"]
        jugador["x"] += jugador["vel_x"]

    else:
        # Fuera de escalera: gravedad normal
        jugador["vel_y"] += GRAVEDAD

        jugador["vel_x"] = 0
        if teclas_presionadas.get("Left") or teclas_presionadas.get("a"):
            jugador["vel_x"] = -VEL_MOVIMIENTO
            jugador["mirando_der"] = False
        if teclas_presionadas.get("Right") or teclas_presionadas.get("d"):
            jugador["vel_x"] = VEL_MOVIMIENTO
            jugador["mirando_der"] = True

        resolver_colision_horizontal(matriz)
        resolver_colision_vertical(matriz)

        # Salto solo si está en el suelo
        if (teclas_presionadas.get("space") or teclas_presionadas.get("Up")) and jugador["en_suelo"]:
            jugador["vel_y"] = VEL_SALTO
            jugador["en_suelo"] = False

    # Límites del mapa
    if jugador["x"] < 0:
        jugador["x"] = 0
    if jugador["x"] > (COLUMNAS - 1) * TAM_CELDA_J:
        jugador["x"] = (COLUMNAS - 1) * TAM_CELDA_J

    # Actualizar estado de animación
    if estado_juego["invencible"] > 0:
        jugador["estado"] = "hit"
    elif en_escalera:
        jugador["estado"] = "idle"
    elif not jugador["en_suelo"] and jugador["vel_y"] < 0:
        jugador["estado"] = "jump"
    elif not jugador["en_suelo"] and jugador["vel_y"] > 0:
        jugador["estado"] = "fall"
    elif jugador["vel_x"] != 0:
        jugador["estado"] = "run"
    else:
        jugador["estado"] = "idle"

    # Avanzar frame de animación
    jugador["contador_anim"] += 1
    if jugador["contador_anim"] >= TIEMPO_ANIM_FRAME:
        jugador["contador_anim"] = 0
        jugador["frame_anim"] += 1

# ─────────────────────────────────────────────────────────────────
# Función: actualizar_enemigo_patrulla
# Propósito: mueve al enemigo patrulla horizontalmente y lo hace
#            rebotar al llegar al borde de una plataforma o mapa.
# ─────────────────────────────────────────────────────────────────
def actualizar_enemigo_patrulla(enemigo, matriz):
    enemigo["x"] += enemigo["vel_x"]

    # El sprite es 48px pero la celda es 32px
    # Los pies están en y + 48, usamos eso para detectar el piso
    fila_pie   = (int(enemigo["y"]) + 48) // TAM_CELDA_J
    col_izq    = int(enemigo["x"] + 2)  // TAM_CELDA_J
    col_der    = int(enemigo["x"] + 46) // TAM_CELDA_J

    # Detecta pared adelante según dirección
    if enemigo["vel_x"] > 0:
        hay_pared    = hay_bloque_en(matriz, fila_pie - 1, col_der)
        hay_piso     = hay_bloque_en(matriz, fila_pie, col_der)
    else:
        hay_pared    = hay_bloque_en(matriz, fila_pie - 1, col_izq)
        hay_piso     = hay_bloque_en(matriz, fila_pie, col_izq)

    if hay_pared or not hay_piso or col_izq <= 0 or col_der >= COLUMNAS - 1:
        enemigo["vel_x"] = -enemigo["vel_x"]
        enemigo["mirando_der"] = not enemigo["mirando_der"]

    # Animación
    enemigo["contador"] += 1
    if enemigo["contador"] >= TIEMPO_ANIM_FRAME:
        enemigo["contador"] = 0
        enemigo["frame"] = (enemigo["frame"] + 1) % 12

# ─────────────────────────────────────────────────────────────────
# Función: actualizar_enemigo_lanzador
# Propósito: el lanzador permanece fijo pero dispara proyectiles
#            cada cierto tiempo hacia la izquierda.
# ─────────────────────────────────────────────────────────────────
def actualizar_enemigo_lanzador(enemigo):
    enemigo["contador_disparo"] += 1

    # Dispara cada 120 frames (~2 segundos)
    if enemigo["contador_disparo"] >= 120:
        enemigo["contador_disparo"] = 0
        enemigo["atacando"] = True
        enemigo["frame_ataque"] = 0
        # Crea un proyectil nuevo
        proyectiles_activos.append({
            "x"    : enemigo["x"],
            "y"    : enemigo["y"] + TAM_CELDA_J // 2,
            "vel_x": -5,   # dispara hacia la izquierda
        })

    # Animación de ataque
    if enemigo["atacando"]:
        enemigo["contador"] += 1
        if enemigo["contador"] >= TIEMPO_ANIM_FRAME:
            enemigo["contador"] = 0
            enemigo["frame_ataque"] += 1
            if enemigo["frame_ataque"] >= 7:
                enemigo["atacando"] = False
                enemigo["frame_ataque"] = 0
    else:
        enemigo["contador"] += 1
        if enemigo["contador"] >= TIEMPO_ANIM_FRAME:
            enemigo["contador"] = 0
            enemigo["frame"] = (enemigo["frame"] + 1) % 11

# ─────────────────────────────────────────────────────────────────
# Función: actualizar_proyectiles
# Propósito: mueve los proyectiles y elimina los que salieron
#            del mapa o chocaron con un bloque.
# ─────────────────────────────────────────────────────────────────
def actualizar_proyectiles(matriz):
    activos = []
    for p in proyectiles_activos:
        p["x"] += p["vel_x"]
        col = int(p["x"] // TAM_CELDA_J)
        fil = int(p["y"] // TAM_CELDA_J)
        # Elimina si sale del mapa o choca con bloque
        if p["x"] < 0 or p["x"] > ANCHO_JUEGO:
            continue
        if hay_bloque_en(matriz, fil, col):
            continue
        activos.append(p)
    proyectiles_activos.clear()
    for p in activos:
        proyectiles_activos.append(p)

# ─────────────────────────────────────────────────────────────────
# Función: verificar_colisiones_jugador
# Propósito: detecta si el jugador tocó una trampa, un enemigo
#            o un proyectil y aplica la penalización correspondiente.
#            También detecta si llegó a la meta.
# Devuelve "victoria", "derrota" o None
# ─────────────────────────────────────────────────────────────────
def verificar_colisiones_jugador(matriz, canvas_juego):
    # Si está invencible no recibe daño
    if estado_juego["invencible"] > 0:
        estado_juego["invencible"] -= 1
        return None

    jx = jugador["x"]
    jy = jugador["y"]

    # Celda del centro del jugador
    fil = int((jy + TAM_CELDA_J // 2) // TAM_CELDA_J)
    col = int((jx + TAM_CELDA_J // 2) // TAM_CELDA_J)

    # ── Verificar meta ──
    if 0 <= fil < FILAS and 0 <= col < COLUMNAS:
        if matriz[fil][col] == META:
            return "victoria"

    # ── Verificar trampa ──
    if hay_trampa_en(matriz, fil, col):
        # Trampa: reinicia en el inicio sin quitar vida
        ix, iy = encontrar_inicio(matriz)
        jugador["x"] = ix
        jugador["y"] = iy
        jugador["vel_x"] = 0
        jugador["vel_y"] = 0
        estado_juego["invencible"] = TIEMPO_INVENCIBLE
        return None

    # ── Verificar enemigos ──
    for enemigo in enemigos_activos:
        ex = enemigo["x"]
        ey = enemigo["y"]
        # Colisión simple por rectángulos
        if (jx + 4 < ex + 40 and jx + 28 > ex + 8 and jy + 4 < ey + 48 and jy + 28 > ey + 16):
            estado_juego["vidas"] -= 1
            estado_juego["puntaje"] -= PUNTAJE_PENALIZACION
            if estado_juego["puntaje"] < 0:
                estado_juego["puntaje"] = 0
            estado_juego["invencible"] = TIEMPO_INVENCIBLE
            if estado_juego["vidas"] <= 0:
                return "derrota"
            return None

    # ── Verificar proyectiles ──
    for p in proyectiles_activos:
        if (jx < p["x"] + 16 and jx + TAM_CELDA_J > p["x"] and
                jy < p["y"] + 16 and jy + TAM_CELDA_J > p["y"]):
            estado_juego["vidas"] -= 1
            estado_juego["puntaje"] -= PUNTAJE_PENALIZACION
            if estado_juego["puntaje"] < 0:
                estado_juego["puntaje"] = 0
            estado_juego["invencible"] = TIEMPO_INVENCIBLE
            if estado_juego["vidas"] <= 0:
                return "derrota"
            return None

    return None

# Función: obtener_sprite_jugador
# Propósito: devuelve el sprite correcto según estado y dirección.
# Usa las listas con sufijo _e cuando mira a la izquierda.
def obtener_sprite_jugador():
    estado    = jugador["estado"]
    mira_der  = jugador["mirando_der"]
 
    if estado == "run":
        lista = sprites["jugador_run"]   if mira_der else sprites["jugador_run_e"]
    elif estado == "jump":
        lista = sprites["jugador_jump"]  if mira_der else sprites["jugador_jump_e"]
    elif estado == "fall":
        lista = sprites["jugador_fall"]  if mira_der else sprites["jugador_fall_e"]
    elif estado == "hit":
        lista = sprites["jugador_hit"]   if mira_der else sprites["jugador_hit_e"]
    else:
        lista = sprites["jugador_idle"]  if mira_der else sprites["jugador_idle_e"]
 
    frame = jugador["frame_anim"] % len(lista)
    return lista[frame]

# ─────────────────────────────────────────────────────────────────
# Función: dibujar_frame
# Propósito: limpia el canvas y redibuja todo el estado del juego:
#            fondo, mapa, jugador, enemigos, proyectiles y HUD.
# ─────────────────────────────────────────────────────────────────
def dibujar_frame(canvas_juego, canvas_hud, matriz, frame_meta):
    
    canvas_juego.delete("all")

    # ── Fondo ──
    for f in range(FILAS):
        for c in range(COLUMNAS):
            x = c * TAM_CELDA_J
            y = f * TAM_CELDA_J
            canvas_juego.create_image(x, y, anchor="nw", image=sprites["fondo"])

    # ── Elementos del mapa ──
    for f in range(FILAS):
        for c in range(COLUMNAS):
            celda = matriz[f][c]
            x = c * TAM_CELDA_J
            y = f * TAM_CELDA_J
            if celda == BLOQUE:
                canvas_juego.create_image(x, y, anchor="nw", image=sprites["bloque"])
            elif celda == ESCALERA:
                canvas_juego.create_image(x, y, anchor="nw", image=sprites["escalera"])
            elif celda == TRAMPA:
                canvas_juego.create_image(x, y, anchor="nw", image=sprites["trampa"])
            elif celda == META:
                canvas_juego.create_image(x + 5, y - 16, anchor="nw", image=sprites["meta"])
            elif celda == INICIO:
                canvas_juego.create_image(x + 5, y - 16, anchor="nw", image=sprites["inicio"])
    # ── Proyectiles ──
    for p in proyectiles_activos:
        canvas_juego.create_image(int(p["x"]), int(p["y"]),anchor="nw", image=sprites["proyectil"])

    # ── Enemigos ──
    for enemigo in enemigos_activos:
        ex = int(enemigo["x"])
        ey = int(enemigo["y"])
        if enemigo["tipo"] == "patrulla":
            if enemigo["mirando_der"]:
                sp = sprites["patrulla_run_e"][enemigo["frame"]]
            else:
                sp = sprites["patrulla_run"][enemigo["frame"]]
        else:
            if enemigo["atacando"]:
                sp = sprites["lanzador_attack"][enemigo["frame_ataque"]]
            else:
                sp = sprites["lanzador_idle"][enemigo["frame"]]
        canvas_juego.create_image(ex, ey, anchor="nw", image=sp)

    # ── Jugador ──
    # Si está invencible parpadea (se muestra cada 2 frames)
    mostrar_jugador = True
    if estado_juego["invencible"] > 0 and estado_juego["invencible"] % 8 < 4:
        mostrar_jugador = False

    if mostrar_jugador:
        sp_jugador = obtener_sprite_jugador()
        jx = int(jugador["x"])
        jy = int(jugador["y"])
        canvas_juego.create_image(jx, jy, anchor="nw", image=sp_jugador)

    # ── HUD ──
    canvas_hud.delete("all")
    canvas_hud.create_rectangle(0, 0, ANCHO_JUEGO, ALTO_HUD,
                                fill=COLOR_FONDO, outline="")
    # Línea separadora
    canvas_hud.create_rectangle(0, ALTO_HUD - 3, ANCHO_JUEGO, ALTO_HUD,
                                fill=COLOR_TITULO, outline="")

    # Nombre del juego parpadeante en el HUD — se maneja desde el loop
    canvas_hud.create_text(20, ALTO_HUD // 2,
                           text="BRICKBOUND",
                           fill=COLOR_TITULO,
                           font=("Courier", 16, "bold"),
                           anchor="w")

    # Vidas
    vidas_texto = "VIDAS: " + ("♥ " * estado_juego["vidas"]).strip()
    canvas_hud.create_text(ANCHO_JUEGO // 2, ALTO_HUD // 2,
                           text=vidas_texto,
                           fill="#E74C3C",
                           font=("Courier", 13, "bold"))

    # Puntaje
    canvas_hud.create_text(ANCHO_JUEGO - 20, ALTO_HUD // 2,
                           text="PTS: " + str(estado_juego["puntaje"]),
                           fill=COLOR_TITULO,
                           font=("Courier", 13, "bold"),
                           anchor="e")

# ─────────────────────────────────────────────────────────────────
# Función: mostrar_juego
# Propósito: inicializa y arranca el loop principal del juego.
#            Carga sprites, posiciona jugador, crea canvas y
#            enlaza las teclas.
# ─────────────────────────────────────────────────────────────────
def mostrar_juego():
    global enemigos_activos, proyectiles_activos, teclas_presionadas

    # Limpia estado anterior
    for widget in ventana.winfo_children():
        widget.destroy()

    ventana.geometry("800x540")   # 540 = 60 HUD + 480 juego

    matriz = mapa_seleccionado["matriz"]

    # Carga sprites
    cargar_sprites()

    # Inicializa listas
    enemigos_activos    = inicializar_enemigos(matriz)
    proyectiles_activos = []
    teclas_presionadas  = {}

    # Inicializa estado del juego
    estado_juego["vidas"]      = 3
    estado_juego["puntaje"]    = calcular_puntaje_mapa(matriz)
    estado_juego["jugando"]    = True
    estado_juego["invencible"] = 0

    # Posiciona al jugador en el inicio del mapa
    ix, iy = encontrar_inicio(matriz)
    jugador["x"]           = ix
    jugador["y"]           = iy
    jugador["vel_x"]       = 0
    jugador["vel_y"]       = 0
    jugador["en_suelo"]    = False
    jugador["en_escalera"] = False
    jugador["mirando_der"] = True
    jugador["estado"]      = "idle"
    jugador["frame_anim"]  = 0
    jugador["contador_anim"] = 0

    # ── HUD (arriba) ──
    canvas_hud = tk.Canvas(ventana, width=ANCHO_JUEGO, height=ALTO_HUD,
                           bg=COLOR_FONDO, highlightthickness=0)
    canvas_hud.pack()

    # ── Marco retro alrededor del área de juego ──
    frame_juego = tk.Frame(ventana, bg=COLOR_TITULO, padx=3, pady=3)
    frame_juego.pack()

    # ── Canvas del juego ──
    canvas_juego = tk.Canvas(frame_juego, width=ANCHO_JUEGO, height=ALTO_JUEGO,
                             bg=COLOR_FONDO, highlightthickness=0)
    canvas_juego.pack()

    # ── Teclas ──
    def tecla_press(event):
        teclas_presionadas[event.keysym] = True

    def tecla_release(event):
        teclas_presionadas[event.keysym] = False

    ventana.bind("<KeyPress>",   tecla_press)
    ventana.bind("<KeyRelease>", tecla_release)
    ventana.focus_set()

    # Frame de animación de la meta
    frame_meta    = [0]
    contador_meta = [0]

    # ─────────────────────────────────────────────────────────────
    # Función interna: loop_juego
    # Propósito: se llama a sí misma cada 16ms (~60fps).
    #            Actualiza todo el estado y redibuja el frame.
    # ─────────────────────────────────────────────────────────────
    def loop_juego():
        if not estado_juego["jugando"]:
            return

        # Actualiza lógica
        actualizar_jugador(matriz)

        for enemigo in enemigos_activos:
            if enemigo["tipo"] == "patrulla":
                actualizar_enemigo_patrulla(enemigo, matriz)
            else:
                actualizar_enemigo_lanzador(enemigo)

        actualizar_proyectiles(matriz)

        # Animación de la meta
        contador_meta[0] += 1
        if contador_meta[0] >= TIEMPO_ANIM_FRAME:
            contador_meta[0] = 0
            frame_meta[0] = (frame_meta[0] + 1) % 7

        # Verifica colisiones y condición de fin
        resultado = verificar_colisiones_jugador(matriz, canvas_juego)

        # Dibuja el frame actual
        dibujar_frame(canvas_juego, canvas_hud, matriz, frame_meta)

        if resultado == "victoria":
            estado_juego["jugando"] = False
            guardar_puntaje(nombre_jugador, estado_juego["puntaje"])
            ventana.after(500, lambda: mostrar_resultado(True, estado_juego["puntaje"]))
        elif resultado == "derrota":
            estado_juego["jugando"] = False
            ventana.after(500, lambda: mostrar_resultado(False, estado_juego["puntaje"]))
        else:
            estado_juego["loop_id"] = ventana.after(16, loop_juego)

    # Arranca el loop
    loop_juego()

 

# -----------------------------------------------------------------
# SECCIÓN 4 — EDITOR DE MAPAS
# -----------------------------------------------------------------
# Constantes del editor
FILAS          = 15
COLUMNAS       = 25
TAM_CELDA      = 32        # píxeles por celda
ANCHO_PANEL    = 200       # ancho del panel de herramientas
ANCHO_GRILLA   = COLUMNAS * TAM_CELDA   # 800px, es el ancho del espacio usable
ALTO_GRILLA    = FILAS    * TAM_CELDA   # 480px, es largo del espacio usable
# Códigos de cada elemento en la matriz, es usadado para calcular puntaje y para guardar el mapa
VACIO          = 0
BLOQUE         = 1
ESCALERA       = 2
TRAMPA         = 3
ENEMIGO_PAT    = 4   # enemigo patrulla
ENEMIGO_LAN    = 5   # enemigo lanzador
INICIO         = 6
META           = 7
# Colores de cada elemento en la cuadrícula, se hace en lista para poder evaluarlo con un for
COLORES_CELDAS = {VACIO: "#1a1a2e",BLOQUE: "#8B5E3C",ESCALERA: "#C8A96E",TRAMPA: "#C0392B",ENEMIGO_PAT: "#8E44AD",ENEMIGO_LAN: "#1A8FC1",INICIO: "#27AE60",META: "#F5C542"}

# Etiquetas visibles en el panel de herramientas, se hace en lista para poder evaluarlo con un for
ETIQUETAS_ELEMENTOS = {VACIO: "Borrador",BLOQUE: "Bloque",ESCALERA: "Escalera",TRAMPA: "Trampa",ENEMIGO_PAT: "Enemigo Patrulla",ENEMIGO_LAN: "Enemigo Lanzador",INICIO: "Inicio Jugador",META: "Meta"}

# Función: crear_matriz_vacia
# Propósito: genera una matriz de FILAS x COLUMNAS llena de ceros que representa el mapa vacío al abrir el editor.
def crear_matriz_vacia():
    matriz = []  #La matriz empieza vacia
    for _ in range(FILAS):  #En cada fila
        fila = []   #Las filas empiezan vacias
        for _ in range(COLUMNAS):  #En cada columna
            fila.append(VACIO)  #Funcion para hacer una lista que contenga todos los espacios de las columnas con la variable vacio(es el borrador)
        matriz.append(fila)  #Funcion para hacer una lista que una todas las filas que contienen las columnas con la variable vacio(es el borrador)
    return matriz
 
# Función: guardar_mapa_archivo
# Propósito: escribe la matriz del mapa en mapas.txt con su nombre
#y autor. Cada fila de la matriz es una línea de númerosseparados por comas.
#Formato en archivo:
#   NOMBRE:The Dungeon by The Killer
#   0,1,1,0,...
#   0,0,2,0,...
#   ---        ← separador entre mapas
def guardar_mapa_archivo(nombre_mapa, matriz):
    # Lee todos los mapas existentes para no sobreescribirlos
    mapas_existentes = leer_todos_los_mapas() #Ejecuta la funcion para hacerlos una lista
 
    # Verifica si ya existe un mapa con ese nombre y lo reemplaza
    encontrado = False
    for i in range(len(mapas_existentes)):  #Iteracion que busca en los mapas uno por uno, si hay uno con el mismo nombre solo remplaza la matriz
        if mapas_existentes[i]["nombre"] == nombre_mapa:
            mapas_existentes[i]["matriz"] = matriz  #Modifica la matriz para guardar los cambios
            encontrado = True  #Indica que si hay una con el mismo nombre
            break  #Rompe la iteracion
    if not encontrado:   #Si no se encuentra
        mapas_existentes.append({"nombre": nombre_mapa, "matriz": matriz})  #Se crea un mapa nuevo y se agrega a la lista
    
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mapas.txt") #Crea una ruta
    # Escribe todos los mapas de vuelta al archivo
    archivo = open(ruta, "w", encoding="utf-8") #Abre el archivo
    for mapa in mapas_existentes: #Por cada mapa en la lista
        archivo.write("NOMBRE:" + mapa["nombre"] + "\n") #Pone el nombre
        for fila in mapa["matriz"]: #Transcribe la matriz por filas
            linea = "" #Reinicia las lineas
            for j in range(len(fila)):
                if j < len(fila) - 1: #Agrega coma
                    linea = linea + str(fila[j]) + ","
                else: #Si no combierte los valores enteros en strings
                    linea = linea + str(fila[j])
            archivo.write(linea + "\n") #Escribe las lineas
        archivo.write("---\n") #Termina el mapa agregado con --- indicando el final del mapa
    archivo.close()
 
# Función: leer_todos_los_mapas
# Propósito: lee mapas.txt y devuelve una lista de diccionarios
# con "nombre" y "matriz" de cada mapa guardado. Si el archivo no existe devuelve lista vacía.
def leer_todos_los_mapas():
    mapas = []
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mapas.txt")#Crea una ruta
    if not os.path.exists(ruta): #veridica que exista un archivo
        return mapas

    archivo = open(ruta, "r", encoding="utf-8") # lee el archivo
    lineas = archivo.readlines() #lee las lineas
    archivo.close()   # Si no existe el archivo, no hay mapas guardados
 
    #Busca los mapas uno por uno
    mapa_actual = None #Empieza sin mapas
    for linea in lineas: #busca en cada linea
        linea = linea.strip() #obtine lo escrito en una linea y borra espacios
        if linea.startswith("NOMBRE:"): #Si empieza con Nombre significa que es un mapa
            mapa_actual = {"nombre": linea[7:], "matriz": []} #Obtiene el nombre y la matriz
        elif linea == "---": #Si encuentra --- significa que leyo todo el mapa
            if mapa_actual is not None: #Si ya registro un mapa
                mapas.append(mapa_actual) #Lo agrega a la lista de mapas
                mapa_actual = None #Marca que esta buscando otro mapa
        elif mapa_actual is not None and linea != "": #Cuando ya no halla mapas
            # Convierte la línea de texto en una lista de enteros cambia "0,1,1,0" a lista de enteros [0, 1, 1, 0]
            fila = []
            for valor in linea.split(","): #por cada coma
                fila.append(int(valor)) #coge el valor entero
            mapa_actual["matriz"].append(fila) #Convierte la matriz en una lista y agrega el valor recien convertido en entero
 
    return mapas
 
# Función: validar_mapa
# Propósito: revisa que la matriz tenga exactamente un INICIOy una META. Devuelve una lista de errores encontrados.
#Si la lista está vacía el mapa es válido.
def validar_mapa(matriz):
    errores = []  #Errores encontrados
    conteo_inicio = 0  #Cuantos inicios hay
    conteo_meta   = 0  #Cuantas metas hay
 
    for fila in matriz:  #Revisa cada fila
        for celda in fila: #Cada columna en cada fila
            if celda == INICIO:  #Verifica si hay inicio en al menos una celda
                conteo_inicio+= 1
            if celda == META:  #Verifica si hay meta en al menos una celda
                conteo_meta+= 1
 
    
    if conteo_inicio == 0:  #Si es 0 solo puso un inicio
        errores.append("Falta el punto de INICIO del jugador.")  #Convierte el texto escrito en la lista
    if conteo_inicio > 1:  #Su es mas de 1 puso mas de un inicio
        errores.append("Solo puede haber un punto de INICIO.") #Convierte el texto escrito en la lista
    if conteo_meta == 0:  #Si es 0 solo puso una meta
        errores.append("Falta la META final.") #Convierte el texto escrito en la lista
    if conteo_meta > 1:  #Su es mas de 1 puso mas de una meta
        errores.append("Solo puede haber una META.") #Convierte el texto escrito en la lista
 
    return errores
 
# Función: calcular_puntaje_mapa
# Propósito: calcula el puntaje base del mapa según sus elementos. Enemigos y trampas suman, bloques y escaleras restan.
def calcular_puntaje_mapa(matriz):
    puntaje = 1000   # Base inicial
    for fila in matriz:  #Verifica cada fila
        for celda in fila:  #Verifica cada celda (columnas en las filas) y asigna puntos o resta dependiendo los elementos
            if celda == ENEMIGO_PAT:
                puntaje = puntaje + 200
            elif celda == ENEMIGO_LAN:
                puntaje = puntaje + 300
            elif celda == TRAMPA:
                puntaje = puntaje + 150
            elif celda == BLOQUE:
                puntaje = puntaje - 10
            elif celda == ESCALERA:
                puntaje = puntaje - 20
    if puntaje < 100:    # Puntaje mínimo para que siempre valga la pena
        puntaje = 100    #Se asigna un 100 minimo por mapa
    return puntaje
 
# Función: mostrar_editor
# Propósito: construye la pantalla del editor de mapas.
# Panel izquierdo con la cuadrícula clickeable y panel derecho con herramientas, nombre y guardado.
def mostrar_editor():
    #Iteracion que limpia la ventana
    for widget in ventana.winfo_children():
        widget.destroy()
    # La ventana del editor es más ancha para acomodar la grilla + panel
    ventana.geometry("1000x600")
 
    # Matriz que representa el estado actual del mapa en edición
    #Se usa una lista de un elemento para poder modificarla desde el editor
    matriz_editor = [crear_matriz_vacia()]
 
    #Elemento actualmente seleccionado en el panel (predeterminado: bloque)
    elemento_seleccionado = [BLOQUE]
 
    # ── Frame principal que divide grilla y panel ──
    frame_principal = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_principal.pack(fill="both", expand=True)
 
    # ── Canvas de la cuadrícula ──
    canvas_grilla = tk.Canvas(frame_principal,width=ANCHO_GRILLA,height=ALTO_GRILLA,bg=COLORES_CELDAS[VACIO], highlightthickness=1,highlightbackground=COLOR_ACENTO)
    canvas_grilla.pack(side="left", padx=(8, 0), pady=8)
 
    # Función interna: dibujar_grilla
    # Redibuja todas las celdas del canvas según la matriz actual
    def dibujar_grilla():
        canvas_grilla.delete("all")  #Elimina lo que habia anteriormente
        for f in range(FILAS): #por cada fila
            for c in range(COLUMNAS): #en cada columna
                #Crea las celdas una por una tomando encuenta el tamaño y su posicion ademas va distribuyendo las cordenadas para la siguiente celda
                x1 = c * TAM_CELDA
                y1 = f * TAM_CELDA
                x2 = x1 + TAM_CELDA
                y2 = y1 + TAM_CELDA
                codigo = matriz_editor[0][f][c]
                color  = COLORES_CELDAS[codigo]  #Usa la listas con los colones, para poder pintar los cuadros recien creados dependiendo del numero
                canvas_grilla.create_rectangle(x1, y1, x2, y2,fill=color,outline="#0a0a0f",width=1)
                # Muestra una letra pequeña para inicio y meta
                if codigo == INICIO: #Verifica que sea el inicio
                    #Modifica la celda para agregar una I
                    canvas_grilla.create_text(x1 + TAM_CELDA // 2, y1 + TAM_CELDA // 2,text="I", fill="white",font=("Courier", 10, "bold"))
                elif codigo == META: #Verifica que sea la Meta
                    #Modifica la celda para agregar una M
                    canvas_grilla.create_text(x1 + TAM_CELDA // 2, y1 + TAM_CELDA // 2,text="M", fill=COLOR_FONDO,font=("Courier", 10, "bold"))
    dibujar_grilla() #Se llama constantemente para ir modificando e ir revisando
 
    # Función interna: pintar_celda
    # Recibe coordenadas del mouse, calcula la celda y la pinta
    # con el elemento seleccionado. Reglas especiales para INICIO
    # y META (solo puede haber uno de cada uno).
    def pintar_celda(event):
        col = event.x // TAM_CELDA   #Obtiene donde en X esta el mouse y divide por el tamaño de la celda para saber si cliqueo bien
        fila = event.y // TAM_CELDA  #Obtiene donde esta Y el mouse y divide por el tamaño de la celda para saber si cliqueo bien
 
        # Verifica que el click esté dentro de los límites
        if col < 0 or col >= COLUMNAS or fila < 0 or fila >= FILAS:
            return
        
        #Obtiene el elemento que se selecciono(Predeterminado:Vacio)
        elem = elemento_seleccionado[0]
 
        #Si es INICIO o META, borra el anterior primero
        if elem == INICIO or elem == META:  #Si el elemento es el inicio o la meta
            for f in range(FILAS):  #Por cada fila
                for c in range(COLUMNAS): #Por cada columna
                    if matriz_editor[0][f][c] == elem: #Busca si ya hay un inicio o meta puesto, lo busca con: [0] siendo el elemento, [f] las filas, [c] columnas, si en alguna lo encuentra
                        matriz_editor[0][f][c] = VACIO #Lo elemina
 
        matriz_editor[0][fila][col] = elem  #Manda el elemto modificado, poniendole un numero, una fila y la columna
        dibujar_grilla() #Ejecuta la funcion de dibujar
 
    # Click y arrastre pintan celdas
    canvas_grilla.bind("<Button-1>", pintar_celda)
    canvas_grilla.bind("<B1-Motion>", pintar_celda)
 
    # ── Panel derecho de herramientas ──
    frame_panel = tk.Frame(frame_principal, bg=COLOR_FONDO, width=220)
    frame_panel.pack(side="left", fill="y", padx=8, pady=8)
    frame_panel.pack_propagate(False)
 
    #Titulo del panel
    tk.Label(frame_panel,text="HERRAMIENTAS",bg=COLOR_FONDO,fg=COLOR_TITULO,font=("Courier", 11, "bold")).pack(pady=(10, 6))
 
    #Decoracion
    tk.Label(frame_panel,text="── ■ ────────── ■ ──",bg=COLOR_FONDO,fg=COLOR_ACENTO,font=FUENTE_PEQUENA).pack(pady=(0, 8))
 
    # Referencia al botón activo para poder resaltarlo
    botones_herramienta = {} #Dependiendo del tipo la lista se le pone un numero
 
    # Función interna: seleccionar_elemento
    # Cambia el elemento activo y resalta su botón en el panel
    def seleccionar_elemento(codigo):
        elemento_seleccionado[0] = codigo
        for cod, btn in botones_herramienta.items():  #Por cada texto y item de la lista de herramientas
            if cod == codigo:  #Si se selecciono se poner en color amarrillo
                btn.config(relief=tk.SOLID, bd=1,fg=COLOR_TITULO,highlightbackground=COLOR_TITULO)
            else:  #Si no en blanco
                btn.config(relief=tk.FLAT, bd=0,fg=COLOR_BOTON)
 
    # Crea un botón por cada elemento
    orden_elementos = [VACIO, BLOQUE, ESCALERA, TRAMPA,
                       ENEMIGO_PAT, ENEMIGO_LAN, INICIO, META]
 
    #Iteracion para ponerle color a las herramientas
    for codigo in orden_elementos:
        color_muestra = COLORES_CELDAS[codigo]
        etiqueta      = ETIQUETAS_ELEMENTOS[codigo]
 
        frame_btn = tk.Frame(frame_panel, bg=COLOR_FONDO)
        frame_btn.pack(fill="x", pady=2, padx=4)
 
        # Cuadrito de color como referencia visual
        tk.Label(frame_btn,bg=color_muestra,width=2,relief=tk.FLAT).pack(side="left", padx=(0, 6))
 
        btn = tk.Button(frame_btn,text=etiqueta, bg=COLOR_FONDO,fg=COLOR_BOTON,font=("Courier", 9),relief=tk.FLAT,bd=0,activebackground=COLOR_FONDO,activeforeground=COLOR_TITULO,cursor="hand2",anchor="w",
        command=lambda c=codigo: seleccionar_elemento(c))
        btn.pack(side="left", fill="x", expand=True)
        botones_herramienta[codigo] = btn
 
    # Marca BLOQUE como seleccionado por defecto
    seleccionar_elemento(BLOQUE)
 
    #Decoracion
    tk.Label(frame_panel,text="── ■ ────────── ■ ──",bg=COLOR_FONDO,fg=COLOR_ACENTO,font=FUENTE_PEQUENA).pack(pady=(12, 8))
 
    # ── Nombre del mapa ──
    tk.Label(frame_panel,text="NOMBRE DEL MAPA",bg=COLOR_FONDO,fg=COLOR_SUBTITULO,font=("Courier", 9, "bold")).pack(anchor="w", padx=6)
    #Diseño
    entry_nombre_mapa = tk.Entry(frame_panel,bg=COLOR_PIXEL_1,fg=COLOR_BOTON,font=("Courier", 10),insertbackground=COLOR_TITULO, relief=tk.FLAT)
    entry_nombre_mapa.pack(fill="x", padx=6, pady=(2, 8))
 
    # ── Checkbox de autor ──
    tk.Label(frame_panel,text="INCLUIR MI NOMBRE",bg=COLOR_FONDO,fg=COLOR_SUBTITULO,font=("Courier", 9, "bold")).pack(anchor="w", padx=6)

    #Checkbox del autor y su diseño
    var_incluir_autor = tk.BooleanVar(value=False)
    chk_autor = tk.Checkbutton(frame_panel,text="Sí, agregar mi nombre",variable=var_incluir_autor,bg=COLOR_FONDO,fg=COLOR_BOTON,selectcolor=COLOR_PIXEL_1,activebackground=COLOR_FONDO,
    activeforeground=COLOR_TITULO,font=("Courier", 9),cursor="hand2")
    chk_autor.pack(anchor="w", padx=6, pady=(2, 12))
 
    # ── Estilo de Texto de error/confirmación ──
    label_mensaje = tk.Label(frame_panel,text="",bg=COLOR_FONDO,fg="#C0392B",font=("Courier", 8),wraplength=180,justify="left")
    label_mensaje.pack(padx=6, pady=(0, 6))
 
    # Frame de botones anclado al fondo del panel
    frame_botones = tk.Frame(frame_panel, bg=COLOR_FONDO)
    frame_botones.pack(side="bottom", fill="x", pady=8)

    # Función interna: intentar_guardar
    # Valida nombre y mapa, construye el nombre completo con autor
    # opcional y llama a guardar_mapa_archivo.
    def intentar_guardar():
        nombre_base = entry_nombre_mapa.get().strip()  #Obtiene lo escrito y borra los espacios en blanco

        if nombre_base == "":  #Se obliga a poner nombre
            #Texto informativo
            label_mensaje.config(text="⚠ El mapa necesita un nombre.",fg="#C0392B")
            return
 
        errores = validar_mapa(matriz_editor[0])  #Se verifican si hay errores
        if errores:  #Si no es una lista vacia
            #Agrega texto con los errores de la lista
            label_mensaje.config(text="⚠ " + errores[0], fg="#C0392B")
            return
 
        # Construye el nombre final con autor opcional
        if var_incluir_autor.get() and nombre_jugador.strip() != "":   #Si hay un nombre de jugador y ya tiene el nombre del mapa
            nombre_final = nombre_base + " by " + nombre_jugador   #Hace un diseño para el nombre
        else:
            nombre_final = nombre_base  #Entrega solo el nombre del mapa
 
        puntaje_base = calcular_puntaje_mapa(matriz_editor[0])
        guardar_mapa_archivo(nombre_final, matriz_editor[0])
        label_mensaje.config(
            text="✔ Mapa guardado!\nPuntaje base: " + str(puntaje_base),
            fg="#27AE60")
 
    # Botón GUARDAR
    #Diseño
    btn_guardar = tk.Button(frame_botones, text="💾  GUARDAR",bg=COLOR_FONDO,fg=COLOR_BOTON,font=("Courier", 11, "bold"),relief=tk.FLAT,bd=0,activebackground=COLOR_FONDO,activeforeground=COLOR_BOTON_HOVER,cursor="hand2",
    command=intentar_guardar)
    btn_guardar.pack(pady=4)
    #Para que alumbre
    aplicar_hover(btn_guardar)
 
    # Botón LIMPIAR
    def limpiar_grilla():
        matriz_editor[0] = crear_matriz_vacia() #Crea una nueva matriz para limpiar todo
        label_mensaje.config(text="")
        dibujar_grilla()  #Redibija
    #Estilo del boton
    btn_limpiar = tk.Button(frame_botones,text="🗑  LIMPIAR",bg=COLOR_FONDO,fg=COLOR_SUBTITULO,font=("Courier", 10),relief=tk.FLAT,bd=0,activebackground=COLOR_FONDO,activeforeground=COLOR_BOTON_HOVER,cursor="hand2",
    command=limpiar_grilla)
    btn_limpiar.pack(pady=4)
    #Diseño de cuando se presiona
    btn_limpiar.bind("<Enter>", lambda e: btn_limpiar.config(fg=COLOR_BOTON_HOVER))
    btn_limpiar.bind("<Leave>", lambda e: btn_limpiar.config(fg=COLOR_SUBTITULO))
 
    #Decoracion
    tk.Label(frame_panel,text="── ■ ────────── ■ ──",bg=COLOR_FONDO,fg=COLOR_ACENTO,font=FUENTE_PEQUENA).pack(pady=(8, 4))
 
    # Botón VOLVER AL MENÚ
    def volver_menu_desde_editor():
        ventana.geometry("800x600")   # Restaura tamaño original
        mostrar_menu()  #Abre el menu
    #Estilo del boton
    btn_volver = tk.Button(frame_botones,text="← VOLVER", bg=COLOR_FONDO,fg=COLOR_SUBTITULO,font=("Courier", 10),relief=tk.FLAT,bd=0,activebackground=COLOR_FONDO,activeforeground=COLOR_BOTON_HOVER,cursor="hand2",
    command=volver_menu_desde_editor)
    btn_volver.pack(pady=4)
    #Diseño de cuando se presiona
    btn_volver.bind("<Enter>", lambda e: btn_volver.config(fg=COLOR_BOTON_HOVER))
    btn_volver.bind("<Leave>", lambda e: btn_volver.config(fg=COLOR_SUBTITULO))
 

# -----------------------------------------------------------------
# SECCIÓN 5 — PUNTAJES
# -----------------------------------------------------------------
# Función: leer_puntajes
# Propósito: lee puntajes.txt y estrae los puntajes guardados en una lista
def leer_puntajes():
    puntajes = []
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "puntajes.txt") #Establece la ruta
    if not os.path.exists(ruta):#Verifica si hay un archivo
        return puntajes #Si no hay retorna nada
    #Si si hay define; 
    archivo = open(ruta, "r", encoding="utf-8") #Abre el archivo
    lineas = archivo.readlines() #Lee las lineas y las copia
    archivo.close() #Cierra el archivo

    for linea in lineas: #Para todas las lineas que se copiaron en del archivo
        linea = linea.strip()  #Lee lo que esta escrito
        if linea == "": #Si no dice nada
            continue #Continua y no ejecuta el 
        partes = linea.split(";") #Corta la coma y lo devuelve en lista ya que cada archivo se ve asi; "Brick Player 1;1500"
        if len(partes) == 2:  #Esto es por si la lista formada tiene mas elementos o menos
            puntajes.append([partes[0], int(partes[1])]) #Hace que la lista tenga el nombre como texto(el primero) y su puntaje como numero

    #Lee la lista creada anteriormente; [[Ana, 500], [Luis, 1200], [Maria, 800]]
    for i in range(len(puntajes)): #Por cada elemento de la lista, recordar que son dos elementos
        for j in range(len(puntajes) - 1 - i): #Lee los elementos de las listas dentro de puntaje
            if puntajes[j][1] < puntajes[j + 1][1]: #El j es el nombnre del jugador y el 1 el puntaje ya que es una lista
                puntajes[j], puntajes[j + 1] = puntajes[j + 1], puntajes[j] #Compara los resultados y obtiene una lista de mayor a menor

    return puntajes

# Función: guardar_puntaje
# Propósito: guarda los puntajes hechos por los jugadores reescrbiendo el archivo
def guardar_puntaje(nombre, puntaje):
    puntajes = leer_puntajes() #Define los puntajes con la funcion para abrir el archivo de puntajes, esto devuelve una lista
    puntajes.append([nombre, puntaje]) #Hace una lista con el nombre y el puntaje recien formado
    #Lee los puntajes dados por la lista devuelta
    for i in range(len(puntajes)): #Por cada elemento de la lista(son listas)
        for j in range(len(puntajes) - 1 - i):#Obtine los elementos de la lista seleccionada de puntajes
            if puntajes[j][1] < puntajes[j + 1][1]: #Compara los jugadores
                puntajes[j], puntajes[j + 1] = puntajes[j + 1], puntajes[j] #Los ordena de mayor a menor
    puntajes = puntajes[:5] #Corta la lista para que solo entren los 5 mejores
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "puntajes.txt") #Establece la ruta
    archivo = open(ruta, "w", encoding="utf-8")#Abre el archivo, lo ejecuta en modo escritura, y el formato
    for entrada in puntajes: #Por cada puntaje de la lista
        archivo.write(entrada[0] + ";" + str(entrada[1]) + "\n") #Lo trascribe
    archivo.close() #Cierra el archivo

# Función: mostrar_puntajes
# Es la funcion que muestra la pantalla donde se encuentran los puntajes
def mostrar_puntajes():
    for widget in ventana.winfo_children(): #Por cada objeto en la ventana
        widget.destroy() #Lo destruye

    #Dimensiones
    ancho = 800
    alto  = 600

    #Canvas del fondo donde se encontraran los puntajes
    canvas_fondo = tk.Canvas(ventana, width=ancho, height=alto, bg=COLOR_FONDO, highlightthickness=0)
    canvas_fondo.place(x=0, y=0)
    dibujar_fondo_pixel(canvas_fondo, ancho, alto)
    canvas_fondo.create_rectangle(0, 0, ancho, 4, fill=COLOR_TITULO, outline="")
    canvas_fondo.create_rectangle(0, alto - 4, ancho, alto, fill=COLOR_TITULO, outline="")

    #Frame para centrar en el canvas y poder poner texto comodamente
    frame_centro = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_centro.place(relx=0.5, rely=0.5, anchor="center")

    #Configuracion del texto del titulo
    label_titulo = tk.Label(frame_centro, text="BRICKBOUND",bg=COLOR_FONDO, fg=COLOR_TITULO, font=FUENTE_TITULO)
    label_titulo.pack(pady=(0, 4))
    #Llama a la funcion parpadeo para darle efectos visuales
    parpadeo_texto(label_titulo, [True])

    #Texto del titulo
    tk.Label(frame_centro, text="MEJORES PUNTAJES",bg=COLOR_FONDO, fg=COLOR_SUBTITULO, font=FUENTE_SUBTITULO).pack(pady=(0, 20))
    tk.Label(frame_centro, text="-- [] ---------------------- [] --",bg=COLOR_FONDO, fg=COLOR_ACENTO, font=FUENTE_PEQUENA).pack(pady=(0, 16))
    
    #Variable de los puntaje
    puntajes = leer_puntajes()

    #Asignacion de puestos se da una medalla dependiendo del puesto
    medallas = ["1.", "2.", "3.", "4.", "5."]
    #Colones de las medallas
    colores_puesto = ["#F5C542", "#C0C0C0", "#CD7F32", COLOR_BOTON, COLOR_BOTON]

    #Condicion simple que lee si hay puntajes si no hay asigna un texto predeterminado, pero si hay los acomoda
    if len(puntajes) == 0:
        tk.Label(frame_centro, text="Aun no hay puntajes registrados.",bg=COLOR_FONDO, fg=COLOR_SUBTITULO, font=("Courier", 12)).pack(pady=20)
    else:
        #Iteracion que asigna un texto dependiendo de la posicion y su medalla
        for i in range(len(puntajes)):
            frame_fila = tk.Frame(frame_centro, bg=COLOR_FONDO)
            frame_fila.pack(fill="x", pady=5)
            tk.Label(frame_fila, text=medallas[i], bg=COLOR_FONDO,fg=colores_puesto[i], font=("Courier", 16, "bold"),width=4).pack(side="left")
            tk.Label(frame_fila, text=puntajes[i][0], bg=COLOR_FONDO,fg=COLOR_BOTON, font=("Courier", 14), width=22, anchor="w").pack(side="left")
            tk.Label(frame_fila, text=str(puntajes[i][1]) + " pts",bg=COLOR_FONDO, fg=colores_puesto[i],font=("Courier", 14, "bold"),width=10, anchor="e").pack(side="left")

    #Decoracion
    tk.Label(frame_centro, text="-- [] ---------------------- [] --",bg=COLOR_FONDO, fg=COLOR_ACENTO, font=FUENTE_PEQUENA).pack(pady=(20, 12))

    #Boton para volver al menu
    btn_volver = tk.Button(frame_centro, text="<- VOLVER",bg=COLOR_FONDO, fg=COLOR_SUBTITULO,font=("Courier", 11), relief=tk.FLAT, bd=0,activebackground=COLOR_FONDO,activeforeground=COLOR_BOTON_HOVER,cursor="hand2", command=mostrar_menu)
    btn_volver.pack()
    btn_volver.bind("<Enter>", lambda e: btn_volver.config(fg=COLOR_BOTON_HOVER))
    btn_volver.bind("<Leave>", lambda e: btn_volver.config(fg=COLOR_SUBTITULO))

    #Pie de pagina
    tk.Label(ventana, text="2026  BRICKBOUND  --  ITCR",bg=COLOR_FONDO, fg=COLOR_ACENTO,font=FUENTE_PEQUENA).place(relx=0.5, rely=0.97, anchor="center")


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


# -----------------------------------------------------------------
# INICIO DEL PROGRAMA
# -----------------------------------------------------------------
ventana = tk.Tk() #Se define la ventana
ventana.title("BrickBound") #El nombre de la ventana
ventana.geometry("800x600") #Las dimenciones de la ventana
ventana.resizable(False, False) #Que no se pueda alargar
ventana.config(bg=COLOR_FONDO) #El color del fondo
 
mostrar_menu() #Se habre primero la pantalla del menu
 
ventana.mainloop() #Loop principal que mantiene la ventana abrierta