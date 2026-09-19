import pygame

from . import base
from .. import config
from ..sample_data import ensure_sample_photos


class GalleryScreen(base.Screen):
    """Thumbnail-Raster + Vollbildansicht (Kap. 9.2). Die Fotos sind hier
    generierte Platzhalter, da noch keine Kamera angeschlossen ist."""

    THUMB_SIZE = (90, 68)
    COLS = 3

    def __init__(self, app):
        super().__init__(app)
        ensure_sample_photos()
        self.photos = sorted(config.PHOTOS_DIR.glob("*.png"))
        self.thumbnails = [
            pygame.transform.smoothscale(pygame.image.load(str(p)).convert(), self.THUMB_SIZE)
            for p in self.photos
        ]
        self.selected = 0
        self.viewing = False
        self.font = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_SMALL)

    def on_enter(self):
        self.viewing = False

    def handle_key(self, event):
        if not self.photos:
            return

        if self.viewing:
            if event.key in (pygame.K_RETURN, pygame.K_BACKSPACE, pygame.K_ESCAPE):
                self.viewing = False
            elif event.key == pygame.K_c:
                # Simuliert den "Scan & Frag"-Kurzbefehl aus Kap. 9.2/9.4
                self.app.screens["claude"].ask_about_image(self.photos[self.selected])
                self.app.go_to("claude")
            return

        if event.key == pygame.K_RIGHT:
            self.selected = min(self.selected + 1, len(self.photos) - 1)
        elif event.key == pygame.K_LEFT:
            self.selected = max(self.selected - 1, 0)
        elif event.key == pygame.K_DOWN:
            self.selected = min(self.selected + self.COLS, len(self.photos) - 1)
        elif event.key == pygame.K_UP:
            self.selected = max(self.selected - self.COLS, 0)
        elif event.key == pygame.K_RETURN:
            self.viewing = True

    def draw(self, surface):
        if not self.photos:
            text = self.font.render("Keine Fotos vorhanden", True, config.DIM_COLOR)
            surface.blit(text, (10, 10))
            return

        if self.viewing:
            img = pygame.transform.smoothscale(
                pygame.image.load(str(self.photos[self.selected])).convert(),
                (config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT - 16),
            )
            surface.blit(img, (0, 0))
            hint = self.font.render(
                "ENTER/ESC=zurueck  C=an Claude senden", True, (255, 255, 255)
            )
            surface.blit(hint, (4, config.DISPLAY_HEIGHT - 14))
            return

        margin = 6
        for i, thumb in enumerate(self.thumbnails):
            col = i % self.COLS
            row = i // self.COLS
            x = margin + col * (self.THUMB_SIZE[0] + margin)
            y = margin + row * (self.THUMB_SIZE[1] + margin)
            surface.blit(thumb, (x, y))
            if i == self.selected:
                pygame.draw.rect(
                    surface,
                    config.ACCENT_COLOR,
                    (x - 2, y - 2, self.THUMB_SIZE[0] + 4, self.THUMB_SIZE[1] + 4),
                    width=2,
                )

        hint = self.font.render("Pfeiltasten, ENTER=oeffnen, F1=MENU", True, config.DIM_COLOR)
        surface.blit(hint, (4, config.DISPLAY_HEIGHT - 14))
