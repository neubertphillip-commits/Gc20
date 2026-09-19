"""Erzeugt Platzhalterfotos fuer die Galerie-Simulation.

Ohne angeschlossene Kamera gibt es noch keine echten Fotos - diese Funktion
legt beim ersten Start ein paar einfache Bilder an, damit sich Galerie und
der "an Claude senden"-Workflow trotzdem ausprobieren lassen. Beispieldateien
fuer den Dokumentenbrowser liegen dagegen direkt (als Text) unter
assets/sample_docs/ im Repo.
"""

import pygame

from . import config

_SAMPLE_PHOTOS = [
    ("notiz_scan_1.png", (40, 70, 45), "SCAN: Bauplan"),
    ("notiz_scan_2.png", (65, 45, 40), "SCAN: Skizze Gehaeuse"),
]


def ensure_sample_photos() -> None:
    config.PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
    for name, color, label in _SAMPLE_PHOTOS:
        path = config.PHOTOS_DIR / name
        if not path.exists():
            _draw_placeholder_photo(path, color, label)


def _draw_placeholder_photo(path, color, label) -> None:
    surface = pygame.Surface((320, 240))
    surface.fill(color)
    pygame.draw.rect(surface, (255, 255, 255), surface.get_rect(), width=2)
    font = pygame.font.SysFont(None, 16)
    text = font.render(label, True, (255, 255, 255))
    surface.blit(text, (10, 10))
    pygame.image.save(surface, str(path))
