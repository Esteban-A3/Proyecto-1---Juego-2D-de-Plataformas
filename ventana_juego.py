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
        estado_juego["vidas"] -= 1
        estado_juego["puntaje"] -= PUNTAJE_PENALIZACION
        if estado_juego["puntaje"] < 0:
            estado_juego["puntaje"] = 0
        if estado_juego["vidas"] <= 0:
            return "derrota"
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
    canvas_hud.create_text(20, ALTO_HUD // 2,text="BRICKBOUND",fill=COLOR_TITULO,font=("Courier", 16, "bold"),anchor="w")

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

    #Llama a la funcion para poner la musica que se ejecuta en el juego
    tocar_musica_juego()

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
    canvas_hud = tk.Canvas(ventana, width=ANCHO_JUEGO, height=ALTO_HUD,bg=COLOR_FONDO, highlightthickness=0)
    canvas_hud.pack()

    #Boton para la musica
    btn_musica = tk.Button(ventana,text="♪ MUSICA",bg=COLOR_FONDO,fg=COLOR_SUBTITULO,font=("Courier", 9),relief=tk.FLAT, bd=0,activebackground=COLOR_FONDO,activeforeground=COLOR_TITULO,cursor="hand2",command=alternar_musica)
    btn_musica.place(relx=0.50, rely=0.02, anchor="center")

    # ── Marco retro alrededor del área de juego ──
    frame_juego = tk.Frame(ventana, bg=COLOR_TITULO, padx=3, pady=3)
    frame_juego.pack()



    # ── Canvas del juego ──
    canvas_juego = tk.Canvas(frame_juego, width=ANCHO_JUEGO, height=ALTO_JUEGO,bg=COLOR_FONDO, highlightthickness=0)
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

 