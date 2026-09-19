"""Claude-Assistent-Screen (Kap. 9.4).

Simuliert den "Scan & Frag"-Workflow: Auf dem echten Geraet wuerde ein
frisches Kamerafoto gesendet, hier stattdessen ein bestehendes Foto aus der
Galerie oder ein Dokument aus dem Dateibrowser - damit sich der komplette
Ablauf schon ohne Kamera-Hardware testen laesst. Ohne installiertes
`anthropic`-Paket oder ohne ANTHROPIC_API_KEY zeigt der Screen einen
Hinweis statt abzustuerzen.
"""

import base64
import textwrap
import threading

import pygame

from . import base
from .. import config

try:
    import anthropic
except ImportError:  # anthropic ist optional, siehe requirements.txt
    anthropic = None


def _wrap(text, width):
    lines = []
    for paragraph in text.splitlines() or [""]:
        lines.extend(textwrap.wrap(paragraph, width) or [""])
    return lines


class ClaudeChatScreen(base.Screen):
    STATE_MENU = "menu"
    STATE_TYPING = "typing"
    STATE_WAITING = "waiting"
    STATE_RESULT = "result"

    def __init__(self, app):
        super().__init__(app)
        self.state = self.STATE_MENU
        self.query = ""
        self.response_text = ""
        self.error = None
        self.font = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_SMALL)
        self._client = None

    def ask_about_image(self, image_path):
        self._send(image_path=image_path, text="Was siehst du auf diesem Bild?")

    def ask_about_document(self, doc_path):
        text = doc_path.read_text(encoding="utf-8", errors="replace")
        self._send(image_path=None, text=f"Fasse dieses Dokument kurz zusammen:\n\n{text[:4000]}")

    def handle_key(self, event):
        if self.state == self.STATE_MENU:
            if event.key == pygame.K_t:
                self.state = self.STATE_TYPING
                self.query = ""
            return

        if self.state == self.STATE_TYPING:
            if event.key == pygame.K_RETURN and self.query.strip():
                self._send(image_path=None, text=self.query)
            elif event.key == pygame.K_BACKSPACE:
                self.query = self.query[:-1]
            elif event.key == pygame.K_ESCAPE:
                self.state = self.STATE_MENU
            elif event.unicode and event.unicode.isprintable():
                self.query += event.unicode
            return

        if self.state == self.STATE_RESULT:
            if event.key in (pygame.K_BACKSPACE, pygame.K_ESCAPE, pygame.K_RETURN):
                self.state = self.STATE_MENU

    def _send(self, image_path, text):
        self.state = self.STATE_WAITING
        self.error = None
        self.response_text = ""
        # Netzwerk-Aufruf laeuft im Hintergrund-Thread, damit die pygame-
        # Eventloop waehrend der Anfrage nicht einfriert.
        threading.Thread(target=self._call_claude, args=(image_path, text), daemon=True).start()

    def _call_claude(self, image_path, text):
        try:
            client = self._get_client()
            content = []
            if image_path is not None:
                data = base64.standard_b64encode(image_path.read_bytes()).decode("utf-8")
                content.append(
                    {
                        "type": "image",
                        "source": {"type": "base64", "media_type": "image/png", "data": data},
                    }
                )
            content.append({"type": "text", "text": text})

            response = client.beta.messages.create(
                model=config.ANTHROPIC_MODEL,
                max_tokens=1024,
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
                output_config={"effort": "low"},
                messages=[{"role": "user", "content": content}],
            )
            self.response_text = (
                "".join(block.text for block in response.content if block.type == "text")
                or "(keine Textantwort erhalten)"
            )
        except Exception as exc:  # wird dem Nutzer angezeigt, nicht verschluckt
            self.error = f"Fehler: {exc}"
        finally:
            self.state = self.STATE_RESULT

    def _get_client(self):
        if anthropic is None:
            raise RuntimeError("anthropic-Paket fehlt (pip install anthropic)")
        if self._client is None:
            # Liest ANTHROPIC_API_KEY automatisch aus der Umgebung (siehe README.md)
            self._client = anthropic.Anthropic()
        return self._client

    def draw(self, surface):
        if self.state == self.STATE_MENU:
            lines = [
                "CLAUDE-ASSISTENT",
                "",
                "In Galerie/Dateien: Taste 'C'",
                "  -> Scan & Frag (sendet Foto/Dokument)",
                "",
                "T = Freitext-Frage eintippen",
                "F1 = zurueck zum Hauptmenue",
            ]
        elif self.state == self.STATE_TYPING:
            lines = ["Frage eingeben, ENTER=senden, ESC=abbrechen", "", "> " + self.query]
        elif self.state == self.STATE_WAITING:
            lines = ["Sende Anfrage an Claude...", "(benoetigt WLAN + ANTHROPIC_API_KEY)"]
        else:
            lines = ["Fehler:", *_wrap(self.error, 58)] if self.error else _wrap(
                self.response_text, 58
            )
            lines += ["", "ENTER/ESC=zurueck zum Claude-Menue"]

        for i, line in enumerate(lines[:14]):
            surf = self.font.render(line, True, config.FG_COLOR)
            surface.blit(surf, (4, 4 + i * 14))
