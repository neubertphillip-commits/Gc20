class Screen:
    """Gemeinsame Basis fuer alle Screens der Kiosk-App (Kap. 8 PROJEKTPLAN.md)."""

    def __init__(self, app):
        self.app = app

    def on_enter(self):
        """Wird jedes Mal aufgerufen, wenn der Screen aktiv wird."""

    def on_exit(self):
        """Wird beim Verlassen des Screens aufgerufen."""

    def handle_key(self, event):
        raise NotImplementedError

    def update(self, dt):
        pass

    def draw(self, surface):
        raise NotImplementedError
