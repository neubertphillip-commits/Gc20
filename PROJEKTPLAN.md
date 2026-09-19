# Cyberdeck-Projekt: Casio-Taschenrechner (fx-CG20 / fx-CG50) + Raspberry Pi Zero 2 W

Planungsdokument für den Umbau eines Casio-Grafikrechner-Gehäuses (im Text
"GC-20"/"GC-50" genannt, gemeint sind vermutlich die **fx-CG20** bzw.
**fx-CG50** aus Casios Prizm-Serie – das sind die Modelle mit großem
Farbdisplay und vollem Tasten-Layout, die genug Volumen für einen Umbau
bieten) zu einem funktionsfähigen Mini-Cyberdeck auf Basis eines
**Raspberry Pi Zero 2 W**.

> Hinweis: Falls tatsächlich andere Modelle gemeint sind (z. B. reine
> Schulrechner ohne Grafikdisplay), bitte kurz Bescheid geben – die
> Kernaussagen (Platzproblem, Tastatur-Matrix, Stromversorgung) bleiben
> gleich, aber die genauen Maße im Kapitel 2 müssten angepasst werden.

## 1. Zieldefinition

- Voll funktionsfähiger Mini-Computer im Gehäuse eines Casio-Taschenrechners
- **Bedienung wie im Original**: Ein Hauptmenü mit Icons/Menüpunkten,
  Navigation per Pfeiltasten + EXE, genau wie beim originalen Casio-OS –
  keine "PC-artige" Fensterverwaltung (siehe Kap. 8)
- Vier Kernanwendungen über das Hauptmenü erreichbar:
  1. **Taschenrechner** – die originale Funktionalität des Geräts bleibt
     vollständig erhalten
  2. **Galerie** – Fotos ansehen, die mit der rückseitigen Kamera
     aufgenommen wurden
  3. **Dokumentenbrowser** – Text-/Markdown-/PDF-Dateien auf der SD-Karte
     durchsuchen und anzeigen
  4. **Claude-Assistent** – direkte Anbindung an die Claude-API, u. a. um
     mit der Kamera fotografierte Dokumente/Notizen auswerten zu lassen
- Akkubetrieb, Ladung über USB-C
- Raspberry Pi OS Lite (Terminal) oder minimaler Desktop, Fokus auf
  Retro-/Terminal-Ästhetik statt Vollwertigkeit
- Wenn möglich: Originaltastatur des Rechners als Eingabegerät weiterverwenden
  (das ist der optisch und thematisch spannendste Teil des Umbaus)
- Akkubetrieb, Ladung über USB-C
- **Kamera** für Foto/Video bzw. Webcam-Funktion (z. B. für Videocalls,
  QR-Codes scannen, einfache Bildverarbeitung) – siehe Kap. 7
- Nice-to-have: Original-Batteriefach als Ladeport/Schalter-Attrappe nutzen

## 2. Gehäusewahl: fx-CG20 vs. fx-CG50

| Merkmal | fx-CG20 | fx-CG50 |
|---|---|---|
| Display | 3,16" Farb-LCD | 3,2" Farb-LCD, etwas höher aufgelöst (384×216) |
| Gehäuse | baugleiche Plattform, minimal älter | neuere Revision, Platinen-Layout etwas kompakter |
| Verfügbarkeit gebraucht | günstiger (oft < 20 €) | etwas teurer, aber noch verbreitet |
| Innenvolumen | praktisch identisch | praktisch identisch |

**Empfehlung:** Nimm das Modell, das du günstiger/defekt bekommst – ideal ist
ein Exemplar mit **kaputtem Display oder Wasserschaden**, bei dem Tastatur
und Gehäuse aber intakt sind. Für den Umbau selbst macht es keinen
nennenswerten Unterschied.

**Vor dem Kauf/Zerlegen unbedingt selbst nachmessen** (Hersteller-Datenblätter
nennen nur die Displaydiagonale, keine Innenmaße):
- Außenmaße mit Schieblehre
- Innenhöhe im Bereich des Batteriefachs (dort ist meist am meisten Platz)
- Position und Dicke der Tastaturmatrix-Platine

## 3. Platzproblem – der eigentliche Knackpunkt

Der Pi Zero 2 W ist mit **65 × 30 × ~5 mm** klein, aber die Casio-Gehäuse
sind für eine extrem flache Platine (Single-Layer, ASIC-Chip) ausgelegt,
nicht für eine "dicke" Platine mit SD-Karten-Slot, USB-Buchsen und
Antennenbereich. Realistische Engpässe:

1. **Bauhöhe**: Pi Zero 2 W + aufgelötete Stiftleisten/Kabel + microSD-Karte
   ragt oft höher als der freie Innenraum. → Buchsen ggf. flach anlöten,
   microSD nicht seitlich abstehen lassen (Adapter mit Rückseiten-Slot oder
   fliegende Verkabelung direkt an die eMMC/SD-Pads, falls vorhanden).
2. **Antenne**: Der Pi Zero 2 W hat eine kleine PCB-Antenne oben links –
   die sollte nicht direkt unter/neben Metall (Batteriekontakte!) liegen,
   sonst leidet WLAN/BT-Reichweite spürbar (wichtig, da die Claude-Anbindung
   ohne WLAN nicht funktioniert).
   sonst leidet WLAN/BT-Reichweite spürbar.
3. **Display-Anschluss**: Ein kleines Display (siehe Kap. 5) braucht meist
   einen FPC- oder Pfostenstecker, der zusätzliche Höhe braucht.
4. **Akku**: LiPo-Pouch-Zellen sind flach und lassen sich gut in
   Freiräumen (z. B. wo früher 4×AAA-Batterien saßen) unterbringen.
5. **Kamera-Kabel**: Das CSI-Flachbandkabel zum Pi Zero ist sehr kurz und
   knickempfindlich – bei rückseitiger Montage (siehe Kap. 7) muss es quer
   durchs Gehäuse zur Rückschale geführt werden, ohne die Hauptplatine oder
   die Tastaturmatrix zu blockieren.
   knickempfindlich – die Kameraplatine muss nah am Pi verbaut werden bzw.
   ein längeres/dünneres Zero-Kamerakabel eingeplant werden (siehe Kap. 7).

Realistischer Ansatz: Nicht versuchen, alles "unsichtbar" reinzuquetschen,
sondern **Gehäuse minimal modifizieren** (Rückseite an einer Stelle
aufdicken/3D-gedrucktes Zwischenteil einsetzen), statt an der Elektronik zu
sparen. Das ist bei den meisten Cyberdeck-Umbauten dieser Größenordnung
üblich und ehrlicher als "es passt gerade so".

## 4. Stückliste (BOM)

| Komponente | Vorschlag | Hinweis |
|---|---|---|
| SBC | Raspberry Pi Zero 2 W | WLAN/BT integriert, für Claude-Anbindung zwingend nötig |
| Speicher | microSD 32–64 GB (A1/A2) | hochwertige Karte, Platz für OS + Fotos + Dokumente |
| Display | 2,4"–3,5" SPI-TFT (z. B. Waveshare, ILI9341/ST7789) oder das Original-LCD, falls ansteuerbar | Original-LCD ansteuern ist sehr aufwendig (proprietärer Controller, kaum dokumentiert) → **Empfehlung: kleines SPI-TFT einbauen**, das ungefähr in die alte Displayöffnung passt |
| Tastatur | Original-Tastenmatrix + eigener Matrix-Scanner (z. B. über GPIO + Software wie `matrix-keyboard`/Custom-Python-Daemon, oder ein kleiner Mikrocontroller wie ATtiny/Pi Pico als USB-HID-Keyboard-Adapter) | siehe Kap. 6 |
| Strom | LiPo-Akku 1000–2000 mAh + Lade-/Boost-Platine (z. B. PiSugar 2/3 für Zero, oder TP4056 + separater 5V-Boost-Converter) | PiSugar ist am wartungsärmsten (Laden, Boost, Ein/Aus-Knopf in einem) |
| Kamera | Raspberry Pi Camera Module 3 (Autofokus) oder kompaktere/günstigere Alternative (z. B. Arducam-Mini-Modul mit OV5647/IMX219) | braucht das **Pi-Zero-spezifische CSI-Kabel** (schmalerer 22-auf-15-Pin-Stecker als beim normalen Pi) – rückseitig montiert, siehe Kap. 7 |
| Audio (optional) | kleiner I2S-DAC/Verstärker (z. B. MAX98357A) + Mini-Lautsprecher | Pi Zero hat keinen analogen Audio-Ausgang |
| Kühlung | keine aktive Kühlung nötig, ggf. dünnes Kupfer-Shim auf dem SoC | Pi Zero 2 W wird bei Dauerlast (Kamera + Netzwerk) handwarm |
| Sonstiges | dünne JST-Kabel, Kapton-Tape, ggf. 3D-gedrucktes Halterahmen für Display/Pi/Kamera | FDM-Druck reicht |

Geschätzte Hardware-Kosten (ohne vorhandene Werkzeuge): **70–110 €**, je
nachdem ob PiSugar (teurer, aber komfortabel) oder Eigenbau-Powerbank-Lösung,
und welches Kameramodul gewählt wird. Dazu kommen **laufende Kosten für die
Claude-API** (siehe Kap. 9.4) – die fallen nur bei tatsächlicher Nutzung an,
nicht im Standby.
| SBC | Raspberry Pi Zero 2 W | WLAN/BT integriert |
| Speicher | microSD 32–64 GB (A1/A2) | hochwertige Karte, Lite-OS reicht klein |
| Display | 2,4"–3,5" SPI-TFT (z. B. Waveshare, ILI9341/ST7789) oder das Original-LCD, falls ansteuerbar | Original-LCD ansteuern ist sehr aufwendig (proprietärer Controller, kaum dokumentiert) → **Empfehlung: kleines SPI-TFT einbauen**, das ungefähr in die alte Displayöffnung passt |
| Tastatur | Original-Tastenmatrix + eigener Matrix-Scanner (z. B. über GPIO + Software wie `matrix-keyboard`/Custom-Python-Daemon, oder ein kleiner Mikrocontroller wie ATtiny/Pi Pico als USB-HID-Keyboard-Adapter) | siehe Kap. 6 |
| Strom | LiPo-Akku 1000–2000 mAh + Lade-/Boost-Platine (z. B. PiSugar 2/3 für Zero, oder TP4056 + separater 5V-Boost-Converter) | PiSugar ist am wartungsärmsten (Laden, Boost, Ein/Aus-Knopf in einem) |
| Kamera | Raspberry Pi Camera Module 3 (Autofokus) oder kompaktere/günstigere Alternative (z. B. Arducam-Mini-Modul mit OV5647/IMX219) | braucht das **Pi-Zero-spezifische CSI-Kabel** (schmalerer 22-auf-15-Pin-Stecker als beim normalen Pi) – siehe Kap. 7 |
| Audio (optional) | kleiner I2S-DAC/Verstärker (z. B. MAX98357A) + Mini-Lautsprecher | Pi Zero hat keinen analogen Audio-Ausgang |
| Kühlung | keine aktive Kühlung nötig, ggf. dünnes Kupfer-Shim auf dem SoC | Pi Zero 2 W wird bei Dauerlast handwarm |
| Sonstiges | dünne JST-Kabel, Kapton-Tape, ggf. 3D-gedrucktes Halterahmen für Display/Pi/Kamera | FDM-Druck reicht |

Geschätzte Kosten (ohne vorhandene Werkzeuge): **70–110 €**, je nachdem ob
PiSugar (teurer, aber komfortabel) oder Eigenbau-Powerbank-Lösung, und
welches Kameramodul gewählt wird.

## 5. Display-Optionen

1. **Original-LCD weiterverwenden** – theoretisch am stimmigsten, praktisch
   fast nie sinnvoll: Der Controller ist proprietär und nirgends öffentlich
   dokumentiert, ein Reverse-Engineering würde den Rahmen des Projekts
   sprengen.
2. **Kleines SPI-TFT (empfohlen)** – z. B. 2,8"–3,5" ILI9341/ST7789-Displays
   sind günstig, gut von Raspberry Pi OS unterstützt (fbtft/DRM-Treiber) und
   lassen sich mit wenig Aufwand hinter die alte Displayöffnung setzen
   (ggf. Öffnung leicht anpassen).
3. **E-Ink** – stromsparend, aber zu träge für ein interaktives Menü und für
   den Kamera-/Galerie-Anwendungsfall ungeeignet (kein Live-Preview beim
   Fotografieren) – daher hier nicht empfohlen.
3. **E-Ink** – stromsparend, aber zu träge für ein interaktives Terminal;
   höchstens als sekundäres Status-Display sinnvoll.

## 6. Tastatur: Original-Matrix vs. Fertiglösung

Die Casio-Tastatur ist eine klassische **Zeilen/Spalten-Matrix** (Membran auf
Flex-Folie, kontaktiert über eine Folienleiste). Zwei realistische Wege:

**A) Matrix selbst auslesen (aufwendiger, aber authentischer)**
- Folienstecker der Tastatur auf Pinbelegung durchmessen (Multimeter,
  Durchgangsprüfung an jeder Kombination)
- Matrix an GPIOs des Pi Zero anschließen, per Software abfragen
  (z. B. Python mit `RPi.GPIO`/`gpiozero`, oder besser: ein günstiger
  Mikrocontroller wie **Raspberry Pi Pico** oder **Pro Micro (ATmega32U4)**
  dazwischen, der die Matrix scannt und sich dem Pi Zero als **USB-HID-
  Tastatur** meldet – entkoppelt Timing-Probleme vom Hauptsystem und ist die
  in der Cyberdeck-Szene übliche Lösung)
- Tastenbelegung (Zahlen, Funktionstasten, Cursor) per Keymap auf sinnvolle
  Terminal-/Anwendungstasten legen (z. B. SHIFT+Zahl → Sonderzeichen,
  EXE → Enter, ALPHA → Buchstabenebene für Texteingabe, MENU → zurück zum
  Hauptmenü)
  Terminal-Tasten legen (z. B. SHIFT+Zahl → Sonderzeichen, EXE → Enter)

**B) Fertige Mini-Tastatur einbauen (einfacher, weniger "Original")**
- z. B. ausgeschlachtete BlackBerry-Tastatur oder ein fertiges I2C/USB-
  Tastaturmodul (wie es viele kleine Cyberdecks nutzen)
- Deutlich schnellerer Weg, wenn dir die Original-Optik weniger wichtig ist
  als "es funktioniert bald"

**Empfehlung:** Variante A mit Pi Pico als USB-HID-Adapter – guter Kompromiss
aus Aufwand und Ergebnis, und der Pico kostet nur ein paar Euro.

## 7. Kamera-Integration

Der Pi Zero 2 W hat einen eigenen, kleineren **CSI-Kameraanschluss** (nicht
kompatibel mit dem Standard-Kamerakabel des "großen" Pi) – dafür braucht man
ein **Pi-Zero-Kamerakabel** (gibt es in mehreren Längen, z. B. 15 cm),
zusätzlich zum eigentlichen Kameramodul.

**Modulwahl:**
1. **Raspberry Pi Camera Module 3** – aktuelle, offiziell unterstützte Wahl
   mit Autofokus, aber Platine/Gehäuse etwas größer.
2. **Kompaktere Drittanbieter-Module** (z. B. Arducam-Mini-Boards mit
   OV5647/IMX219-Sensor) – kleinere Grundfläche, oft ohne Gehäuse, dadurch
   leichter in einer 3D-gedruckten Halterung unterzubringen. Für dieses
   Projekt aufgrund des begrenzten Platzes eher zu empfehlen als Modul 3.

**Platzierung im Gehäuse** – zwei sinnvolle Varianten:
- **Frontseitig, oberhalb des Displays** (Webcam-Stil): gute Wahl, wenn die
  Kamera hauptsächlich für Videocalls/Selfie-Nutzung gedacht ist. Erfordert
  eine kleine Bohrung/Öffnung im oberen Gehäuserand, dort ist bei den
  Prizm-Gehäusen meist ohnehin schon wenig Elektronik verbaut (guter
  Freiraum in der Nähe der oberen Displaykante).
- **Rückseitig** (Foto-Kamera-Stil): bessere Bildqualität für "richtige"
  Fotos, aber unpraktisch, wenn man während der Nutzung gleichzeitig aufs
  Display schaut. Erfordert eine Öffnung in der Rückschale.

**Empfehlung:** Frontseitig oberhalb des Displays, analog zur Webcam an
einem Laptop – passt am besten zur "Terminal/Cyberdeck"-Nutzung.

**Software:** `libcamera`/`rpicam-apps` (in aktuellem Raspberry Pi OS
enthalten), z. B. `rpicam-still`/`rpicam-vid` für Fotos/Video; für
Videocalls oder eigene Anwendungen lässt sich der Kamera-Stream auch per
`v4l2` in andere Tools einspeisen.

**Zu beachten:**
- Kamera-Kabel ist die zusätzliche Zwangsbedingung aus Kap. 3, Punkt 5 –
  Kameraposition und Pi-Zero-Position im Gehäuse aufeinander abstimmen,
  bevor die 3D-Halterung konstruiert wird.
- Zusätzlicher Stromverbrauch bei aktiver Kamera/Videostreaming –
  bei der Akkukapazität (Kap. 4) etwas Puffer einplanen (z. B. eher
  2000 mAh statt 1000 mAh, wenn Video-Streaming ein häufiger Use-Case ist).
- Kleine Blendöffnung im Gehäuse so groß wie nötig, aber so klein wie
  möglich schneiden – Streulicht/Kratzer auf der Linse vermeiden.

## 8. Software-Stack

- **Raspberry Pi OS Lite (64-bit)** als Basis
- Boot direkt in ein Terminal-UI, z. B.:
  - `tmux` + Shell als "Startbildschirm"
  - oder ein Retro-Menü (z. B. selbstgeschriebenes `dialog`/`whiptail`-Menü,
    oder Tools wie `bashtop`, `cool-retro-term` falls X11 doch läuft)
- WLAN/Bluetooth vorkonfigurieren (`raspi-config` headless per
  `wpa_supplicant.conf`/NetworkManager)
- Display-Treiber (fbcp-ili9341 oder passenden DRM-Treiber je nach TFT)
- USB-HID-Tastatur (falls Variante A/Pico) braucht keinen Treiber – wird
  vom Kernel als normale Tastatur erkannt
- Kamera-Support über `libcamera`/`rpicam-apps` (siehe Kap. 7)

## 9. Mechanischer Bauablauf (grober Fahrplan)

1. Spender-Rechner zerlegen, alle Teile fotografieren/dokumentieren
   (Reihenfolge der Schrauben, Kabelwege)
2. Innenmaße final vermessen, 3D-Halterung für Pi Zero + TFT + Kamera + Akku
   konstruieren (Fusion360/FreeCAD reicht) und drucken
3. Tastaturmatrix durchmessen und Pinbelegung dokumentieren
4. Elektronik "auf dem Tisch" aufbauen und komplett testen (Pi Zero, TFT,
   Kamera, Pico-Tastaturadapter, Akku/Lade-Platine), **bevor** irgendetwas
   verklebt wird
5. Software-Image vorbereiten und durchtesten
6. Erst dann alles ins Gehäuse einbauen, Kabel fixieren, Gehäuse schließen
7. Finaler Test, Nacharbeiten an Tastenbelegung/Software

## 10. Risiken / Stolpersteine

- **Zeitaufwand für Tastatur-Matrix** wird häufig unterschätzt – hier
  realistisch mehrere Abende einplanen
- **WLAN-Reichweite** kann durch die metallische Batteriefach-Umgebung
  leiden – Antenne des Pi Zero möglichst frei/außen positionieren
  (Kunststoffbereich, kein Metall in der Nähe)
- **Akkusicherheit**: LiPo nur mit passender Lade-/Schutzschaltung
  verwenden, nicht direkt an den Pi hängen
- **Kamera-Kabel** ist die zerbrechlichste Verbindung im ganzen Aufbau –
  beim Einbau nicht knicken/quetschen, Zugentlastung einplanen
- **Gehäuse-Modifikation** (Fräsen/Dremeln für USB-C-Ladebuchse,
  Kamera-Öffnung, ggf. microSD-Zugang) ist optisch der schwierigste Teil –
  lieber einmal mehr Maß nehmen als zweimal schneiden

## 11. Nächste konkrete Schritte

- [ ] Exakte Modellbezeichnung des Spendergeräts bestätigen (fx-CG20 oder
      fx-CG50, ggf. Foto/Rückseite prüfen)
- [ ] Gerät besorgen (idealerweise defektes Display, funktionierende Tasten)
- [ ] Zerlegen, Innenraum vermessen und fotografieren
- [ ] Kameramodul und -position festlegen (Kap. 7) – beeinflusst die
      3D-Halterung und die Position des Pi Zero direkt
- [ ] BOM final bestellen (Kap. 4)
- [ ] Mit Kap. 6/Variante A (Tastaturmatrix) als ersten elektronischen
      Meilenstein starten – das ist der unsicherste Teil und sollte zuerst
      geklärt werden
