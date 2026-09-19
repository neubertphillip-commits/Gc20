# Cyberdeck-UI-Simulation

Läuft auf einem normalen Laptop (Windows/Mac/Linux) und zeigt, wie das
Hauptmenü und die vier Apps aus Kap. 8/9 von [`../PROJEKTPLAN.md`](../PROJEKTPLAN.md)
später auf dem eingebauten Display aussehen und sich bedienen lassen werden –
komplett ohne Casio-Gehäuse, Pi Zero oder Kamera.

## Setup

```bash
cd software
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Ohne das `anthropic`-Paket startet die Simulation trotzdem – nur der
Claude-Screen zeigt dann eine Fehlermeldung statt einer echten Antwort.

## Tastenbelegung (Laptop-Tastatur simuliert die spätere Original-Tastatur)

| Taste | Bedeutung |
|---|---|
| Pfeiltasten | Navigation |
| Enter | EXE (bestätigen/öffnen) |
| Rücktaste | Zeichen löschen bzw. eine Ebene zurück |
| Entf | Eingabe/Ansicht zurücksetzen (im Rechner) |
| Esc | Im Hauptmenü: Simulation beenden. In einer App: zurück/abbrechen |
| **F1** | Original-Taste **MENU** – von überall sofort zurück ins Hauptmenü |
| **C** (in Galerie/Dateien) | "Scan & Frag": aktuelles Foto/Dokument an Claude senden |
| **T** (im Claude-Screen) | Freitext-Frage eintippen |

### Rechner-Screen (zusätzlich zu den obigen Tasten)

| Taste | Bedeutung |
|---|---|
| Buchstaben/Zahlen/Operatoren tippen | Ausdruck eingeben, z. B. `sin(30)`, `2pi`, `5!`, `sqrt(16)` |
| **F2** | Grad/Radiant umschalten (Anzeige oben rechts) |
| **F3** | letztes Ergebnis (`ans`) in den Ausdruck einfügen |
| **F4** / **F5** / **F6** | Speicher M+ / MR (`mem` einfügen) / MC (löschen) |
| **F7** | Graph-Modus: `y = f(x)` eingeben und plotten |
| Pfeiltasten (im Graph-Plot) | Ansicht verschieben (Pan) |
| **+** / **-** (im Graph-Plot) | Rein-/Rauszoomen |

Unterstützte Funktionen: `sin cos tan asin acos atan sinh cosh tanh asinh
acosh atanh log ln log2 sqrt cbrt root(n,x) abs fact npr ncr`, Konstanten
`pi e`, sowie `ans`/`mem`. **Nicht enthalten** (bewusst außerhalb des
Rahmens dieses Prototyps, vergleichbar mit dem CAS-Umfang mancher
TI-84-Nachbauten wie [OpenCalc](https://github.com/CoryPearl/opencalc)):
Gleichungslöser, Matrizen, komplexe Zahlen, symbolisches Ableiten/
Integrieren, Wertetabellen.

## Claude-Anbindung testen

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python main.py
```

Dann in der Galerie ein Foto öffnen und **C** drücken, oder im
Claude-Screen mit **T** eine eigene Frage eintippen. Ohne WLAN/API-Key
zeigt der Screen einen Fehler statt abzustürzen – das entspricht dem in
Kap. 9.4/12 beschriebenen Verhalten auf dem echten Gerät.

## Was hier bewusst noch fehlt

- **Echte Tastenmatrix**: Die Simulation nutzt die Laptop-Tastatur 1:1.
  Sobald die Original-Tastenbelegung (Kap. 6) feststeht, wird nur die
  Zuordnung Taste → Aktion angepasst – die Screens selbst bleiben gleich.
- **PDF-Anzeige**: Der Dokumentenbrowser zeigt aktuell nur Text/Markdown.
  PDF-Rendering (PyMuPDF/`pdftoppm`, Kap. 9.3) kommt erst dazu, wenn ein
  konkreter Anwendungsfall dafür ansteht.
- **Echte Fotos**: Die Galerie zeigt generierte Platzhalterbilder statt
  echter Kamerafotos (noch keine Kamera verbaut).

## Architektur

```
main.py                     Einstiegspunkt
cyberdeck/
  config.py                 Displaygröße, Farben, Fonts, Claude-Modell
  app.py                    Kiosk-Loop, Screen-Verwaltung, Tastenrouting
  sample_data.py            Platzhalterfotos fürs Ausprobieren
  screens/
    menu.py                 Hauptmenü (Kap. 8)
    calculator.py           Taschenrechner (Kap. 9.1)
    gallery.py               Galerie (Kap. 9.2)
    documents.py             Dokumentenbrowser (Kap. 9.3)
    claude_chat.py            Claude-Assistent / "Scan & Frag" (Kap. 9.4)
  assets/
    sample_docs/             Beispieltexte für den Dateibrowser
    sample_photos/           wird beim ersten Start automatisch befüllt
```

Diese Struktur ist bewusst so gehalten, dass sie später direkt auf dem
Pi Zero 2 W weiterläuft: Aus `pygame`-Fenster wird `pygame` im
Framebuffer/KMS-Modus, aus Laptop-Tastatur wird der Pico-USB-HID-Adapter
(Kap. 6) – die Screens und die Menü-Logik ändern sich dafür nicht.
