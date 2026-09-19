"""Startet die Cyberdeck-UI-Simulation auf dem Laptop.

Zeigt, wie das Hauptmenue und die vier Apps (Kap. 8/9 in PROJEKTPLAN.md)
spaeter auf dem echten Display aussehen und sich bedienen werden - noch
ohne jede Hardware. Siehe README.md fuer Setup und Tastenbelegung.
"""

import pygame

from cyberdeck.app import CyberdeckApp
from cyberdeck.sample_data import ensure_sample_photos


def main():
    pygame.init()
    ensure_sample_photos()
    CyberdeckApp().run()


if __name__ == "__main__":
    main()
