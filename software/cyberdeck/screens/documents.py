import pygame

from . import base
from .. import config


class DocumentsScreen(base.Screen):
    """Dateiliste + einfacher Text-Pager (Kap. 9.3). PDF-Rendering ist hier
    bewusst noch nicht enthalten - das kommt erst mit PyMuPDF/pdftoppm auf
    der echten Hardware, sobald ein erster Software-Stand steht."""

    VISIBLE_LINES = 12

    def __init__(self, app):
        super().__init__(app)
        self.files = sorted(p for p in config.DOCS_DIR.glob("*") if p.is_file())
        self.selected = 0
        self.viewing = False
        self.scroll = 0
        self.lines = []
        self.font = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_SMALL)

    def on_enter(self):
        self.viewing = False

    def handle_key(self, event):
        if not self.files:
            return

        if self.viewing:
            if event.key in (pygame.K_BACKSPACE, pygame.K_ESCAPE):
                self.viewing = False
            elif event.key == pygame.K_DOWN:
                self.scroll = min(self.scroll + 1, max(0, len(self.lines) - self.VISIBLE_LINES))
            elif event.key == pygame.K_UP:
                self.scroll = max(self.scroll - 1, 0)
            elif event.key == pygame.K_c:
                # Simuliert "Frage Claude zu diesem Dokument" aus Kap. 9.3/9.4
                self.app.screens["claude"].ask_about_document(self.files[self.selected])
                self.app.go_to("claude")
            return

        if event.key == pygame.K_DOWN:
            self.selected = min(self.selected + 1, len(self.files) - 1)
        elif event.key == pygame.K_UP:
            self.selected = max(self.selected - 1, 0)
        elif event.key == pygame.K_RETURN:
            self._open_selected()

    def _open_selected(self):
        path = self.files[self.selected]
        text = path.read_text(encoding="utf-8", errors="replace")
        self.lines = text.splitlines() or [""]
        self.scroll = 0
        self.viewing = True

    def draw(self, surface):
        if not self.files:
            text = self.font.render("Keine Dateien vorhanden", True, config.DIM_COLOR)
            surface.blit(text, (10, 10))
            return

        if self.viewing:
            visible = self.lines[self.scroll : self.scroll + self.VISIBLE_LINES]
            for i, line in enumerate(visible):
                surf = self.font.render(line[:60], True, config.FG_COLOR)
                surface.blit(surf, (4, 4 + i * 14))
            hint = self.font.render(
                "Pfeil hoch/runter=Scroll, ENTF/ESC=zurueck, C=Claude",
                True,
                config.DIM_COLOR,
            )
            surface.blit(hint, (4, config.DISPLAY_HEIGHT - 14))
            return

        for i, path in enumerate(self.files):
            color = config.ACCENT_COLOR if i == self.selected else config.FG_COLOR
            surf = self.font.render(path.name, True, color)
            surface.blit(surf, (6, 6 + i * 16))

        hint = self.font.render("Pfeiltasten, ENTER=oeffnen, F1=MENU", True, config.DIM_COLOR)
        surface.blit(hint, (4, config.DISPLAY_HEIGHT - 14))
