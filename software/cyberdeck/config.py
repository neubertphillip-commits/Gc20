"""Zentrale Konstanten fuer die Cyberdeck-UI-Simulation.

DISPLAY_WIDTH/HEIGHT entsprechen ungefaehr der Aufloesung des geplanten
SPI-TFT (Kap. 5 in PROJEKTPLAN.md). Alle Screens zeichnen auf eine Surface
in genau dieser Groesse; main.py skaliert sie fuers Laptop-Fenster hoch.
Wird spaeter das echte Display angeschlossen, aendert sich nur SCALE (auf 1)
und die Fenstergroesse - das Layout der Screens bleibt unveraendert.
"""

import pathlib

DISPLAY_WIDTH = 384
DISPLAY_HEIGHT = 216
SCALE = 3
FPS = 30

BG_COLOR = (12, 14, 18)
FG_COLOR = (210, 230, 210)
ACCENT_COLOR = (90, 200, 120)
DIM_COLOR = (90, 100, 90)
ERROR_COLOR = (220, 90, 90)

ASSETS_DIR = pathlib.Path(__file__).parent / "assets"
DOCS_DIR = ASSETS_DIR / "sample_docs"
PHOTOS_DIR = ASSETS_DIR / "sample_photos"

FONT_NAME = None  # Standard-Systemfont; spaeter ggf. gegen einen Retro-Font tauschen
FONT_SIZE_SMALL = 8
FONT_SIZE_NORMAL = 10
FONT_SIZE_LARGE = 14

ANTHROPIC_MODEL = "claude-opus-5"
