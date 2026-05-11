# 🎮 BrickBound — Juego 2D de Plataformas

> Proyecto 1 — Introducción a la Programación LL | ITCR | Primer Semestre 2026

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![Tkinter](https://img.shields.io/badge/UI-Tkinter-orange?style=flat)
![Pygame](https://img.shields.io/badge/Audio-Pygame-green?style=flat)
![Pillow](https://img.shields.io/badge/Sprites-Pillow-yellow?style=flat)
![License](https://img.shields.io/badge/Proyecto-ITCR-red?style=flat)

---

## 📖 Descripción

BrickBound es un videojuego 2D de plataformas desarrollado en Python con Tkinter.
El jugador debe desplazarse desde el punto de inicio hasta la meta final, superando
plataformas, escaleras, enemigos y trampas. Incluye un editor de mapas, sistema de
puntajes persistente y música de fondo.

---

## 🗂️ Estructura del Repositorio

```
Proyecto-1---Juego-2D-de-Plataformas/
│
├── BrickBound.py              # Archivo principal — todo el código del juego
│
├── assets/                    # Sprites y texturas del juego
│   ├── Jugador/               # Spritesheet del personaje (Idle, Run, Jump, Fall, Hit)
│   ├── Enemigo Patrulla/      # Spritesheet del enemigo patrulla
│   ├── Enemigo Lanzador/      # Spritesheet del enemigo lanzador y proyectiles
│   ├── Bloque.png
│   ├── Escalera.png
│   ├── Trampa.png
│   ├── Fondo.png
│   ├── Bandera Meta.png
│   └── Bandera Salida.png
│
├── BrickBound Oficial Song/   # Música del juego
│   ├── New Brick.mp3          # Música del menú (loop global)
│   └── BrakeBrick.mp3         # Música del juego
│
├── mapas.txt                  # Mapas creados por el jugador (generado automáticamente)
└── puntajes.txt               # Top 5 puntajes (generado automáticamente)
```

---

## 🌿 Branches

| Branch | Contenido |
|--------|-----------|
| `main` | Código completo y funcional del juego |
| `Archivos-del-Proyecto` | Assets, sprites y archivos de recursos |
| `Diseño-de-Ventanas` | Copias separadas de cada pantalla del juego |
| `Documentacion` | Documentación del proyecto en PDF |

---

## 🕹️ Cómo Jugar

### Controles
| Tecla | Acción |
|-------|--------|
| `←` / `A` | Mover izquierda |
| `→` / `D` | Mover derecha |
| `Espacio` / `↑` | Saltar |
| `↑` / `W` | Subir escalera |
| `↓` / `S` | Bajar escalera |

### Objetivo
Llegar desde el punto de **inicio** (bandera verde) hasta la **meta** (bandera amarilla)
sin perder las 3 vidas disponibles.

### Sistema de Vidas
- El jugador tiene **3 vidas**
- Cada vida perdida descuenta **300 puntos**
- Trampa → respawn en el inicio
- Enemigo / Proyectil → invencibilidad temporal de ~2 segundos

---

## ✨ Características

- 🗺️ **Mapa predeterminado** — "The Dungeon", siempre disponible
- 🛠️ **Editor de mapas** — creá tus propios niveles con cuadrícula 25×15
- 👾 **2 tipos de enemigos** — patrulla (móvil) y lanzador (proyectiles)
- 🏆 **Top 5 puntajes** — guardados en archivo entre sesiones
- 🎵 **Música** — diferente para menú y juego, con botón para pausar
- 🎨 **Sprites pixel art** — animaciones completas con efecto de daño
- 💾 **Mapas persistentes** — guardados en `mapas.txt`

---

## ⚙️ Requisitos

```bash
Python 3.10+
pip install pillow pygame
```

---

## 🚀 Ejecución

```bash
python BrickBound.py
```

> Asegurate de ejecutarlo desde la carpeta del proyecto para que encuentre
> los archivos `assets/`, `mapas.txt` y `puntajes.txt`.

---

## 🧩 Elementos del Mapa

| Código | Elemento | Efecto en Puntaje |
|--------|----------|-------------------|
| `1` | Bloque | -10 pts |
| `2` | Escalera | -20 pts |
| `3` | Trampa | +150 pts |
| `4` | Enemigo Patrulla | +200 pts |
| `5` | Enemigo Lanzador | +300 pts |
| `6` | Inicio | — |
| `7` | Meta | — |

---

## 📋 Restricciones del Curso

- ❌ No se usan clases (POO)
- ✅ Solo funciones, listas y diccionarios
- ✅ Variables globales justificadas y documentadas

---

## 👤 Autor

**Esteban Sanchez** — ITCR, Introducción a la Programación LL, 2026
