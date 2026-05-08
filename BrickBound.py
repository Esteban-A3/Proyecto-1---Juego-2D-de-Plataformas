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
# Propósito: si el jugador no tiene nombre le pide uno
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
# Copia de esta sección va en: Diseño-de-Ventanas/ventana_seleccion_mapa.py
# (Por implementar)
# -----------------------------------------------------------------
 
def mostrar_seleccion_mapa():
    pass  # TODO
 
# -----------------------------------------------------------------
# SECCIÓN 3 — JUEGO
# Copia de esta sección va en: Diseño-de-Ventanas/ventana_juego.py
# (Por implementar)
# -----------------------------------------------------------------
 
def mostrar_juego():
    pass  # TODO
 
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
# Propósito: genera una matriz de FILAS x COLUMNAS llena de ceros
#            que representa el mapa vacío al abrir el editor.
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
    mapas_existentes = leer_todos_los_mapas()
 
    # Verifica si ya existe un mapa con ese nombre y lo reemplaza
    encontrado = False
    for i in range(len(mapas_existentes)):  #Iteracion que busca en los mapas uno por uno, si hay uno con el mismo nombre solo remplaza la matriz
        if mapas_existentes[i]["nombre"] == nombre_mapa:
            mapas_existentes[i]["matriz"] = matriz  #Modifica la matriz para guardar los cambios
            encontrado = True  #Indica que si hay una con el mismo nombre
            break  #Rompe la iteracion
    if not encontrado:   #Si no se encuentra
        mapas_existentes.append({"nombre": nombre_mapa, "matriz": matriz})  #Se crea un mapa nuevo y se agrega a la lista
 
    # Escribe todos los mapas de vuelta al archivo
    archivo = open("mapas.txt", "w", encoding="utf-8")
    for mapa in mapas_existentes:
        archivo.write("NOMBRE:" + mapa["nombre"] + "\n")
        for fila in mapa["matriz"]:
            linea = ""
            for j in range(len(fila)):
                if j < len(fila) - 1:
                    linea = linea + str(fila[j]) + ","
                else:
                    linea = linea + str(fila[j])
            archivo.write(linea + "\n")
        archivo.write("---\n")
    archivo.close()
 
# Función: leer_todos_los_mapas
# Propósito: lee mapas.txt y devuelve una lista de diccionarios
# con "nombre" y "matriz" de cada mapa guardado. Si el archivo no existe devuelve lista vacía.

def leer_todos_los_mapas():
    mapas = [] #Se empieza con la lista vacia
    try:
        archivo = open("mapas.txt", "r", encoding="utf-8")
        lineas = archivo.readlines()   #Extrae lo escrito en el archivo
        archivo.close()  #Cierra el archivo
    except:
        return mapas   # Si no existe el archivo, no hay mapas guardados
 
    mapa_actual = None
    for linea in lineas:
        linea = linea.strip()
        if linea.startswith("NOMBRE:"):
            mapa_actual = {"nombre": linea[7:], "matriz": []}
        elif linea == "---":
            if mapa_actual is not None:
                mapas.append(mapa_actual)
                mapa_actual = None
        elif mapa_actual is not None and linea != "":
            # Convierte la línea de texto en una lista de enteros
            fila = []
            for valor in linea.split(","):
                fila.append(int(valor))
            mapa_actual["matriz"].append(fila)
 
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
# Copia de esta sección va en: Diseño-de-Ventanas/ventana_puntajes.py
# Excepción: leer/escribir puntajes usa un archivo externo puntajes.txt
# -----------------------------------------------------------------
 
def mostrar_puntajes():
    pass  # TODO
 
# -----------------------------------------------------------------
# SECCIÓN 6 — RESULTADO FINAL
# Copia de esta sección va en: Diseño-de-Ventanas/ventana_resultado.py
# (Por implementar)
# -----------------------------------------------------------------
 
def mostrar_resultado():
    pass  # TODO
 
# -----------------------------------------------------------------
# INICIO DEL PROGRAMA
# -----------------------------------------------------------------
 
ventana = tk.Tk()
ventana.title("BrickBound")
ventana.geometry("800x600")
ventana.resizable(False, False)
ventana.config(bg=COLOR_FONDO)
 
mostrar_menu()
 
ventana.mainloop()