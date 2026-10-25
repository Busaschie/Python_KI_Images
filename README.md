# Python_KI_Images

Python-Toolkit zur KI-gestützten Erzeugung und Auswahl von Bildern und Videos.

## Überblick

Das Projekt generiert Bilder per Prompt, wählt die besten Ergebnisse aus und erzeugt daraus Videos.

## Projektstruktur

```text
├── imagen.py   # Bildgenerierung
├── vidgen.py   # Videogenerierung
├── curate.py   # Auswahl/Kuratierung der Ergebnisse
├── props.py    # Konfiguration/Parameter
├── utils.py    # Hilfsfunktionen
├── prompts/    # Prompt-Vorlagen
└── .env        # API-Schlüssel (lokal, nicht committen!)
```

## Installation

```bash
git clone https://github.com/Busaschie/Python_KI_Images.git
cd Python_KI_Images
python -m venv .venv
# Windows: .venv\Scripts\activate | Linux/macOS: source .venv/bin/activate
```

Benötigte Pakete installieren und in der `.env` den API-Schlüssel des verwendeten Bild-/Video-Dienstes eintragen.

## Nutzung

```bash
python imagen.py   # Bilder erzeugen
python curate.py   # Ergebnisse auswählen
python vidgen.py   # Video erzeugen
```

## Sicherheit

Die `.env` darf keine echten Schlüssel im öffentlichen Repository enthalten. Schlüssel widerrufen/erneuern, falls sie bereits committet wurden, und `.env` in `.gitignore` aufnehmen.
