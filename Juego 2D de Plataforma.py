import tkinter as tk

# -----------------------------------------------------------------
# BrickBound — main.py
# Curso: Introducción a la Programación LL — ITCR
# Descripción: Archivo principal del juego. Contiene toda la lógica, ventanas y funciones del programa.
# -----------------------------------------------------------------

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
def parpadeo_cursor(label_cursor, estado_visible):
    if estado_visible[0]:
        label_cursor.config(fg=COLOR_TITULO)
    else:
        label_cursor.config(fg=COLOR_FONDO)
    estado_visible[0] = not estado_visible[0]  #Niega el estado para poder intercalar los colores
    label_cursor.after(600, parpadeo_cursor, label_cursor, estado_visible) #Hace un conteo para despues volver a llamar a la funcion

# Función: dibujar cuadrícula de fondo tipo pixel art
# Dibuja una grilla sutil en el canvas de fondo
def dibujar_fondo_pixel(canvas, ancho, alto):
    tamano = 32  # tamaño de cada "pixel" de fondo
    for fila in range(0, alto, tamano):
        for col in range(0, ancho, tamano):
            # Alterna colores para dar textura de cuadrícula sutil
            if (fila // tamano + col // tamano) % 2 == 0:
                color = COLOR_PIXEL_1
            else:
                color = COLOR_PIXEL_2
            canvas.create_rectangle(col, fila, col + tamano, fila + tamano,
                                    fill=color, outline="")

# Función principal: mostrar_menu
# Limpia la ventana y construye la pantalla del menú principal
# Recibe la ventana principal y los callbacks de navegación
def mostrar_menu(ventana, cb_jugar, cb_editor, cb_puntajes):
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
    tk.Label(frame_centro,text="BRICKBOUND",bg=COLOR_FONDO,fg=COLOR_TITULO,font=FUENTE_TITULO).pack(pady=(0, 4))

    # ── Subtítulo con cursor parpadeante ──
    frame_sub = tk.Frame(frame_centro, bg=COLOR_FONDO)
    frame_sub.pack(pady=(0, 40))
    #Texto del subtitulo
    tk.Label(frame_sub,text="2D PLATFORM ADVENTURE",bg=COLOR_FONDO,fg=COLOR_SUBTITULO,font=FUENTE_SUBTITULO).pack(side="left")

    # Cursor tipo terminal que parpadea
    label_cursor = tk.Label(frame_sub,text=" █",bg=COLOR_FONDO,fg=COLOR_TITULO,font=FUENTE_SUBTITULO)
    label_cursor.pack(side="left")
    estado_visible = [True]  # Lista para poder mutar desde la función anidada
    parpadeo_cursor(label_cursor, estado_visible)

    # ── Separador decorativo ──
    tk.Label(frame_centro,text="── ■ ──────────────────── ■ ──",bg=COLOR_FONDO,fg=COLOR_ACENTO,font=FUENTE_PEQUENA).pack(pady=(0, 30))

    # ── Botones del menú ──
    # Cada botón llama a su callback correspondiente al presionar

    # Botón JUGAR
    btn_jugar = tk.Button(frame_centro,text="▶  JUGAR", bg=COLOR_FONDO,fg=COLOR_BOTON,font=FUENTE_BOTON,relief=tk.FLAT,
    bd=0,activebackground=COLOR_FONDO,activeforeground=COLOR_BOTON_HOVER,cursor="hand2",command=cb_jugar)
    btn_jugar.pack(pady=8)
    aplicar_hover(btn_jugar)

    # Botón EDITOR DE MAPAS
    btn_editor = tk.Button(frame_centro,text="✎  EDITOR DE MAPAS",bg=COLOR_FONDO,fg=COLOR_BOTON,font=FUENTE_BOTON,relief=tk.FLAT,
    bd=0,activebackground=COLOR_FONDO,activeforeground=COLOR_BOTON_HOVER,cursor="hand2",command=cb_editor)
    btn_editor.pack(pady=8)
    aplicar_hover(btn_editor)

    # Botón PUNTAJES
    btn_puntajes = tk.Button(frame_centro,text="★  PUNTAJES",bg=COLOR_FONDO,fg=COLOR_BOTON,font=FUENTE_BOTON,relief=tk.FLAT,
    bd=0,activebackground=COLOR_FONDO,activeforeground=COLOR_BOTON_HOVER,cursor="hand2",command=cb_puntajes)
    btn_puntajes.pack(pady=8)
    aplicar_hover(btn_puntajes)

    # Separador antes de Salir
    tk.Label(frame_centro,text="── ■ ──────────────────── ■ ──",bg=COLOR_FONDO,fg=COLOR_ACENTO,font=FUENTE_PEQUENA).pack(pady=(20, 8))

    # Botón SALIR (menos llamativo, color más tenue)
    btn_salir = tk.Button(frame_centro,text="✕  SALIR",bg=COLOR_FONDO,fg=COLOR_SUBTITULO,font=("Courier", 11),relief=tk.FLAT, bd=0,
    activebackground=COLOR_FONDO,activeforeground=COLOR_BOTON_HOVER,cursor="hand2",command=ventana.quit)
    btn_salir.pack(pady=(0, 10))
    #Se hace una logica igual a la de la funcion para hover, solamente que esta es menos llamativa
    btn_salir.bind("<Enter>", lambda e: btn_salir.config(fg=COLOR_BOTON_HOVER))
    btn_salir.bind("<Leave>", lambda e: btn_salir.config(fg=COLOR_SUBTITULO))

    # ── Pie de página ──
    tk.Label(ventana,text="© 2026  BRICKBOUND  —  ITCR  Introducción a la Programación LL",bg=COLOR_FONDO,fg=COLOR_ACENTO,
             font=FUENTE_PEQUENA).place(relx=0.5, rely=0.97, anchor="center")
    
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
# Copia de esta sección va en: Diseño-de-Ventanas/ventana_editor.py
# (Por implementar)
# -----------------------------------------------------------------
 
def mostrar_editor():
    pass  # TODO
 
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