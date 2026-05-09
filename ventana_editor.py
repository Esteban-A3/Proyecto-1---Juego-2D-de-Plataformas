# ═════════════════════════════════════════════════════════════════
# BrickBound — ventana_editor.py
# Branch: Diseño-de-Ventanas
# Descripción: Copia de la Sección 4 del archivo principal.
#              Editor de mapas con cuadrícula 25x15 clickeable,
#              panel de herramientas, validación y guardado.
# ═════════════════════════════════════════════════════════════════

import tkinter as tk

# ─────────────────────────────────────────────────────────────────
# Constantes del editor
# ─────────────────────────────────────────────────────────────────
FILAS          = 15
COLUMNAS       = 25
TAM_CELDA      = 32
ANCHO_PANEL    = 220
ANCHO_GRILLA   = COLUMNAS * TAM_CELDA
ALTO_GRILLA    = FILAS    * TAM_CELDA

# Códigos de cada elemento en la matriz
VACIO          = 0
BLOQUE         = 1
ESCALERA       = 2
TRAMPA         = 3
ENEMIGO_PAT    = 4
ENEMIGO_LAN    = 5
INICIO         = 6
META           = 7

# Colores de cada elemento en la cuadrícula
COLORES_CELDAS = {
    VACIO      : "#1a1a2e",
    BLOQUE     : "#8B5E3C",
    ESCALERA   : "#C8A96E",
    TRAMPA     : "#C0392B",
    ENEMIGO_PAT: "#8E44AD",
    ENEMIGO_LAN: "#1A8FC1",
    INICIO     : "#27AE60",
    META       : "#F5C542",
}

ETIQUETAS_ELEMENTOS = {
    VACIO      : "Borrador",
    BLOQUE     : "Bloque",
    ESCALERA   : "Escalera",
    TRAMPA     : "Trampa",
    ENEMIGO_PAT: "Enemigo Patrulla",
    ENEMIGO_LAN: "Enemigo Lanzador",
    INICIO     : "Inicio Jugador",
    META       : "Meta",
}

# ─────────────────────────────────────────────────────────────────
# Función: crear_matriz_vacia
# Propósito: genera una matriz de FILAS x COLUMNAS llena de ceros
#            que representa el mapa vacío al abrir el editor.
# ─────────────────────────────────────────────────────────────────
def crear_matriz_vacia():
    matriz = []
    for _ in range(FILAS):
        fila = []
        for _ in range(COLUMNAS):
            fila.append(VACIO)
        matriz.append(fila)
    return matriz

# ─────────────────────────────────────────────────────────────────
# Función: leer_todos_los_mapas
# Propósito: lee mapas.txt y devuelve una lista de diccionarios
#            con "nombre" y "matriz" de cada mapa guardado.
#            Si el archivo no existe devuelve lista vacía.
# ─────────────────────────────────────────────────────────────────
def leer_todos_los_mapas():
    mapas = []
    try:
        archivo = open("mapas.txt", "r", encoding="utf-8")
        lineas = archivo.readlines()
        archivo.close()
    except:
        return mapas

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
            fila = []
            for valor in linea.split(","):
                fila.append(int(valor))
            mapa_actual["matriz"].append(fila)

    return mapas

# ─────────────────────────────────────────────────────────────────
# Función: guardar_mapa_archivo
# Propósito: escribe la matriz del mapa en mapas.txt con su nombre
#            y autor. Si ya existe un mapa con ese nombre lo
#            reemplaza, si no lo agrega al final.
# Formato en archivo:
#   NOMBRE:The Dungeon by The Killer
#   0,1,1,0,...
#   ---
# ─────────────────────────────────────────────────────────────────
def guardar_mapa_archivo(nombre_mapa, matriz):
    mapas_existentes = leer_todos_los_mapas()

    encontrado = False
    for i in range(len(mapas_existentes)):
        if mapas_existentes[i]["nombre"] == nombre_mapa:
            mapas_existentes[i]["matriz"] = matriz
            encontrado = True
            break

    if not encontrado:
        mapas_existentes.append({"nombre": nombre_mapa, "matriz": matriz})

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

# ─────────────────────────────────────────────────────────────────
# Función: validar_mapa
# Propósito: revisa que la matriz tenga exactamente un INICIO
#            y una META. Devuelve lista de errores encontrados.
# ─────────────────────────────────────────────────────────────────
def validar_mapa(matriz):
    errores = []
    conteo_inicio = 0
    conteo_meta   = 0

    for fila in matriz:
        for celda in fila:
            if celda == INICIO:
                conteo_inicio = conteo_inicio + 1
            if celda == META:
                conteo_meta = conteo_meta + 1

    if conteo_inicio == 0:
        errores.append("Falta el punto de INICIO del jugador.")
    if conteo_inicio > 1:
        errores.append("Solo puede haber un punto de INICIO.")
    if conteo_meta == 0:
        errores.append("Falta la META final.")
    if conteo_meta > 1:
        errores.append("Solo puede haber una META.")

    return errores

# ─────────────────────────────────────────────────────────────────
# Función: calcular_puntaje_mapa
# Propósito: calcula el puntaje base del mapa según sus elementos.
#            Enemigos y trampas suman, bloques y escaleras restan.
# ─────────────────────────────────────────────────────────────────
def calcular_puntaje_mapa(matriz):
    puntaje = 1000
    for fila in matriz:
        for celda in fila:
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
    if puntaje < 100:
        puntaje = 100
    return puntaje

# ─────────────────────────────────────────────────────────────────
# Función: mostrar_editor
# Propósito: construye la pantalla del editor de mapas.
#            Panel izquierdo con la cuadrícula clickeable y
#            panel derecho con herramientas, nombre y guardado.
# Nota: en el archivo principal usa la variable global
#       nombre_jugador para el autor del mapa.
# ─────────────────────────────────────────────────────────────────
def mostrar_editor():
    # En el archivo principal aquí se limpia la ventana y se
    # cambia la geometría a 1000x600
    # ventana.geometry("1000x600")

    matriz_editor = [crear_matriz_vacia()]
    elemento_seleccionado = [BLOQUE]

    # ── Frame principal ──
    frame_principal = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_principal.pack(fill="both", expand=True)

    # ── Canvas de la cuadrícula ──
    canvas_grilla = tk.Canvas(frame_principal,
                              width=ANCHO_GRILLA,
                              height=ALTO_GRILLA,
                              bg=COLORES_CELDAS[VACIO],
                              highlightthickness=1,
                              highlightbackground=COLOR_ACENTO)
    canvas_grilla.pack(side="left", padx=(8, 0), pady=8)

    def dibujar_grilla():
        canvas_grilla.delete("all")
        for f in range(FILAS):
            for c in range(COLUMNAS):
                x1 = c * TAM_CELDA
                y1 = f * TAM_CELDA
                x2 = x1 + TAM_CELDA
                y2 = y1 + TAM_CELDA
                codigo = matriz_editor[0][f][c]
                color  = COLORES_CELDAS[codigo]
                canvas_grilla.create_rectangle(x1, y1, x2, y2,
                                               fill=color,
                                               outline="#0a0a0f",
                                               width=1)
                if codigo == INICIO:
                    canvas_grilla.create_text(x1 + TAM_CELDA // 2,
                                              y1 + TAM_CELDA // 2,
                                              text="I", fill="white",
                                              font=("Courier", 10, "bold"))
                elif codigo == META:
                    canvas_grilla.create_text(x1 + TAM_CELDA // 2,
                                              y1 + TAM_CELDA // 2,
                                              text="M", fill=COLOR_FONDO,
                                              font=("Courier", 10, "bold"))

    dibujar_grilla()

    def pintar_celda(event):
        col  = event.x // TAM_CELDA
        fila = event.y // TAM_CELDA
        if col < 0 or col >= COLUMNAS or fila < 0 or fila >= FILAS:
            return
        elem = elemento_seleccionado[0]
        # Si es INICIO o META borra el anterior para que solo haya uno
        if elem == INICIO or elem == META:
            for f in range(FILAS):
                for c in range(COLUMNAS):
                    if matriz_editor[0][f][c] == elem:
                        matriz_editor[0][f][c] = VACIO
        matriz_editor[0][fila][col] = elem
        dibujar_grilla()

    canvas_grilla.bind("<Button-1>", pintar_celda)
    canvas_grilla.bind("<B1-Motion>", pintar_celda)

    # ── Panel derecho ──
    frame_panel = tk.Frame(frame_principal, bg=COLOR_FONDO, width=ANCHO_PANEL)
    frame_panel.pack(side="left", fill="y", padx=8, pady=8)
    frame_panel.pack_propagate(False)

    tk.Label(frame_panel,
             text="HERRAMIENTAS",
             bg=COLOR_FONDO,
             fg=COLOR_TITULO,
             font=("Courier", 11, "bold")).pack(pady=(10, 6))

    tk.Label(frame_panel,
             text="── ■ ────────── ■ ──",
             bg=COLOR_FONDO,
             fg=COLOR_ACENTO,
             font=FUENTE_PEQUENA).pack(pady=(0, 8))

    botones_herramienta = {}

    def seleccionar_elemento(codigo):
        elemento_seleccionado[0] = codigo
        for cod, btn in botones_herramienta.items():
            if cod == codigo:
                btn.config(relief=tk.SOLID, bd=1, fg=COLOR_TITULO)
            else:
                btn.config(relief=tk.FLAT, bd=0, fg=COLOR_BOTON)

    orden_elementos = [VACIO, BLOQUE, ESCALERA, TRAMPA,
                       ENEMIGO_PAT, ENEMIGO_LAN, INICIO, META]

    for codigo in orden_elementos:
        frame_btn = tk.Frame(frame_panel, bg=COLOR_FONDO)
        frame_btn.pack(fill="x", pady=2, padx=4)
        tk.Label(frame_btn,
                 bg=COLORES_CELDAS[codigo],
                 width=2,
                 relief=tk.FLAT).pack(side="left", padx=(0, 6))
        btn = tk.Button(frame_btn,
                        text=ETIQUETAS_ELEMENTOS[codigo],
                        bg=COLOR_FONDO,
                        fg=COLOR_BOTON,
                        font=("Courier", 9),
                        relief=tk.FLAT,
                        bd=0,
                        activebackground=COLOR_FONDO,
                        activeforeground=COLOR_TITULO,
                        cursor="hand2",
                        anchor="w",
                        command=lambda c=codigo: seleccionar_elemento(c))
        btn.pack(side="left", fill="x", expand=True)
        botones_herramienta[codigo] = btn

    seleccionar_elemento(BLOQUE)

    tk.Label(frame_panel,
             text="── ■ ────────── ■ ──",
             bg=COLOR_FONDO,
             fg=COLOR_ACENTO,
             font=FUENTE_PEQUENA).pack(pady=(12, 8))

    # ── Nombre del mapa ──
    tk.Label(frame_panel,
             text="NOMBRE DEL MAPA",
             bg=COLOR_FONDO,
             fg=COLOR_SUBTITULO,
             font=("Courier", 9, "bold")).pack(anchor="w", padx=6)

    entry_nombre_mapa = tk.Entry(frame_panel,
                                 bg=COLOR_PIXEL_1,
                                 fg=COLOR_BOTON,
                                 font=("Courier", 10),
                                 insertbackground=COLOR_TITULO,
                                 relief=tk.FLAT)
    entry_nombre_mapa.pack(fill="x", padx=6, pady=(2, 8))

    # ── Checkbox autor ──
    tk.Label(frame_panel,
             text="INCLUIR MI NOMBRE",
             bg=COLOR_FONDO,
             fg=COLOR_SUBTITULO,
             font=("Courier", 9, "bold")).pack(anchor="w", padx=6)

    var_incluir_autor = tk.BooleanVar(value=False)
    tk.Checkbutton(frame_panel,
                   text="Sí, agregar mi nombre",
                   variable=var_incluir_autor,
                   bg=COLOR_FONDO,
                   fg=COLOR_BOTON,
                   selectcolor=COLOR_PIXEL_1,
                   activebackground=COLOR_FONDO,
                   activeforeground=COLOR_TITULO,
                   font=("Courier", 9),
                   cursor="hand2").pack(anchor="w", padx=6, pady=(2, 8))

    # ── Mensaje de error o confirmación ──
    label_mensaje = tk.Label(frame_panel,
                             text="",
                             bg=COLOR_FONDO,
                             fg="#C0392B",
                             font=("Courier", 8),
                             wraplength=180,
                             justify="left")
    label_mensaje.pack(padx=6, pady=(0, 6))

    # ── Botones al fondo ──
    frame_botones = tk.Frame(frame_panel, bg=COLOR_FONDO)
    frame_botones.pack(side="bottom", fill="x", pady=8)

    def intentar_guardar():
        nombre_base = entry_nombre_mapa.get().strip()
        if nombre_base == "":
            label_mensaje.config(text="⚠ El mapa necesita un nombre.", fg="#C0392B")
            return
        errores = validar_mapa(matriz_editor[0])
        if errores:
            label_mensaje.config(text="⚠ " + errores[0], fg="#C0392B")
            return
        if var_incluir_autor.get() and nombre_jugador.strip() != "":
            nombre_final = nombre_base + " by " + nombre_jugador
        else:
            nombre_final = nombre_base
        puntaje_base = calcular_puntaje_mapa(matriz_editor[0])
        guardar_mapa_archivo(nombre_final, matriz_editor[0])
        label_mensaje.config(
            text="✔ Guardado!\nPuntaje base: " + str(puntaje_base),
            fg="#27AE60")

    def limpiar_grilla():
        matriz_editor[0] = crear_matriz_vacia()
        label_mensaje.config(text="")
        dibujar_grilla()

    def volver_menu_desde_editor():
        ventana.geometry("800x600")
        mostrar_menu()

    btn_guardar = tk.Button(frame_botones,
                            text="💾  GUARDAR",
                            bg=COLOR_FONDO, fg=COLOR_BOTON,
                            font=("Courier", 11, "bold"),
                            relief=tk.FLAT, bd=0,
                            activebackground=COLOR_FONDO,
                            activeforeground=COLOR_BOTON_HOVER,
                            cursor="hand2",
                            command=intentar_guardar)
    btn_guardar.pack(pady=4)
    aplicar_hover(btn_guardar)

    btn_limpiar = tk.Button(frame_botones,
                            text="🗑  LIMPIAR",
                            bg=COLOR_FONDO, fg=COLOR_SUBTITULO,
                            font=("Courier", 10),
                            relief=tk.FLAT, bd=0,
                            activebackground=COLOR_FONDO,
                            activeforeground=COLOR_BOTON_HOVER,
                            cursor="hand2",
                            command=limpiar_grilla)
    btn_limpiar.pack(pady=4)
    btn_limpiar.bind("<Enter>", lambda e: btn_limpiar.config(fg=COLOR_BOTON_HOVER))
    btn_limpiar.bind("<Leave>", lambda e: btn_limpiar.config(fg=COLOR_SUBTITULO))

    tk.Label(frame_botones,
             text="── ■ ────────── ■ ──",
             bg=COLOR_FONDO,
             fg=COLOR_ACENTO,
             font=FUENTE_PEQUENA).pack(pady=(4, 4))

    btn_volver = tk.Button(frame_botones,
                           text="← VOLVER",
                           bg=COLOR_FONDO, fg=COLOR_SUBTITULO,
                           font=("Courier", 10),
                           relief=tk.FLAT, bd=0,
                           activebackground=COLOR_FONDO,
                           activeforeground=COLOR_BOTON_HOVER,
                           cursor="hand2",
                           command=volver_menu_desde_editor)
    btn_volver.pack(pady=4)
    btn_volver.bind("<Enter>", lambda e: btn_volver.config(fg=COLOR_BOTON_HOVER))
    btn_volver.bind("<Leave>", lambda e: btn_volver.config(fg=COLOR_SUBTITULO))