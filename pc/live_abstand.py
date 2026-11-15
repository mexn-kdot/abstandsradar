# Live-Anzeige: Zeichnet den Abstand vom Ultraschallsensor als laufende Kurve.
#
# Voraussetzung: Auf dem Arduino läuft arduino/ultraschall_test.
# Der Arduino schickt Zeilen wie "Abstand: 101.3 cm" über USB (COM4).
# Dieses Programm liest die Zeilen, holt die Zahl heraus und zeichnet sie.
#
# Starten:   python pc/live_abstand.py
# Beenden:   Fenster schließen
#
# Wichtig: Der COM-Port kann immer nur von EINEM Programm gleichzeitig benutzt
# werden. Serieller Monitor/Plotter der Arduino IDE also vorher schließen.

import re
import time
from collections import deque

import matplotlib.pyplot as plt
import serial  # Paket "pyserial"
from matplotlib.animation import FuncAnimation

# --- Einstellungen -----------------------------------------------------------
PORT = "COM4"          # Hier hängt der Mega (siehe Geräte-Manager)
BAUD = 9600            # Muss zu Serial.begin(9600) im Arduino-Programm passen
FENSTER_S = 20         # So viele Sekunden zeigt die Kurve rückwirkend
MAX_ABSTAND_CM = 200   # Obergrenze der y-Achse

# Sucht in einer Zeile nach einer Zahl wie "101.3" (regulärer Ausdruck)
ZAHL = re.compile(r"Abstand:\s*([\d.]+)")

# --- Verbindung öffnen -------------------------------------------------------
# timeout=0: readline() wartet nicht, sondern gibt sofort zurück, was da ist.
verbindung = serial.Serial(PORT, BAUD, timeout=0)
# Beim Öffnen startet der Arduino neu. Alte Daten im Puffer verwerfen.
time.sleep(2)
verbindung.reset_input_buffer()

# deque = Liste mit fester Maximallänge: Alte Werte fallen hinten raus.
zeiten = deque(maxlen=FENSTER_S * 10)
abstaende = deque(maxlen=FENSTER_S * 10)
startzeit = time.time()
puffer = ""  # sammelt angefangene Zeilen, bis das Zeilenende kommt

# --- Diagramm vorbereiten ----------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.5))
fig.canvas.manager.set_window_title("Abstandsradar – Live-Abstand")
linie, = ax.plot([], [], color="#2a7de1", linewidth=2)
anzeige = ax.text(0.98, 0.92, "", transform=ax.transAxes, ha="right",
                  fontsize=22, fontweight="bold", color="#2a7de1")
ax.set_xlabel("Zeit [s]")
ax.set_ylabel("Abstand [cm]")
ax.set_ylim(0, MAX_ABSTAND_CM)
ax.grid(True, alpha=0.3)


def aktualisieren(_frame):
    """Wird ca. 10x pro Sekunde aufgerufen: neue Daten lesen, Kurve neu zeichnen."""
    global puffer

    # Alles abholen, was seit dem letzten Aufruf angekommen ist
    puffer += verbindung.read(verbindung.in_waiting or 1).decode(errors="ignore")

    # Nur vollständige Zeilen auswerten; der Rest bleibt im Puffer
    *zeilen, puffer = puffer.split("\n")
    for zeile in zeilen:
        treffer = ZAHL.search(zeile)
        jetzt = time.time() - startzeit
        if treffer:
            zeiten.append(jetzt)
            abstaende.append(float(treffer.group(1)))
            anzeige.set_text(f"{abstaende[-1]:.1f} cm")
        elif "kein Echo" in zeile:
            anzeige.set_text("kein Echo")

    # Kurve und x-Achse nachführen
    linie.set_data(zeiten, abstaende)
    if zeiten:
        rechts = max(zeiten[-1], FENSTER_S)
        ax.set_xlim(rechts - FENSTER_S, rechts)
    return linie, anzeige


# FuncAnimation ruft aktualisieren() alle 100 ms auf
animation = FuncAnimation(fig, aktualisieren, interval=100, cache_frame_data=False)
plt.tight_layout()
plt.show()  # blockiert, bis das Fenster geschlossen wird

verbindung.close()
