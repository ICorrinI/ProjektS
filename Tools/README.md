# PNG zu nummeriertem Pixel-Array

Dieses Python-Skript liest ein PNG-Bild ein und wandelt es in ein 2D-Array von Zahlen um. Jede Farbe im Bild wird automatisch erkannt und mit einer eindeutigen Zahl versehen.

## Features

- Dynamische Farberkennung: Neue Farben werden automatisch durchnummeriert.
- Unterstützt beliebige Bildgrößen (z.B. 16x16, 32x32, 128x16, etc.).
- Liefert sowohl das nummerierte Array als auch die Zuordnung Farbe → Zahl.

## Installation

1. Stelle sicher, dass Python 3 installiert ist.
2. Installiere die benötigte Bibliothek Pillow:

```bash
pip install pillow numpy
```