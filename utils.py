# utils.py
################################################################################
from base64 import b64encode, b64decode                                         # importiert base64 funktionen
################################################################################

def write_file(path, data):                                                     # schreibt text in datei
    with open(path, "w", encoding="utf-8") as f:                                # öffnet datei im textmodus
        f.write(data); print("file saved:", path)                               # schreibt daten und gibt meldung aus

def write_buff(path, data):                                                     # schreibt base64 daten als binärdatei
    with open(path, "wb") as f:                                                 # öffnet datei im binärmodus
        f.write(b64decode(data)); return data                                   # dekodiert und speichert daten

def read_file(path):                                                            # liest textdatei
    with open(path, "r", encoding="utf-8") as f:                                # öffnet datei im lesemodus
        return f.read()                                                         # gibt inhalt zurück

def read_buff(path):                                                            # liest binärdatei und kodiert base64
    with open(path, "rb") as f:                                                 # öffnet datei im binärmodus
        return b64encode(f.read()).decode()                                     # kodiert und gibt als string zurück



