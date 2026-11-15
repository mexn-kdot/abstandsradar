# Radarbild: Zeichnet die Messungen des schwenkenden Sensors als Radar.
#
# Voraussetzung: Auf dem Arduino läuft arduino/radar.
# Der Arduino schickt Zeilen wie "45,103.2" (Winkel in Grad, Abstand in cm),
# "-1" als Abstand heißt: kein Echo.
#
# Starten:   python pc/radar.py
# Beenden:   Fenster schließen
#
# Wie bei live_abstand.py gilt: COM4 kann nur ein Programm gleichzeitig nutzen.

import math
import time

import matplotlib.pyplot as plt
import serial
from matplotlib.animation import FuncAnimation

# --- Einstellungen -----------------------------------------------------------
PORT = "COM4"
BAUD = 9600
REICHWEITE_CM = 200     # Radius des Radarbilds
NACHLEUCHTEN_S = 8      # So lange bleiben Punkte sichtbar und verblassen dabei
SPIEGELN = False        # True, falls links und rechts im Bild vertauscht sind

GRUEN = "#39ff7a"
HINTERGRUND = "#06140b"

# --- Verbindung --------------------------------------------------------------
verbindung = serial.Serial(PORT, BAUD, timeout=0)
time.sleep(2)                    # Arduino startet beim Öffnen neu
verbindung.reset_input_buffer()

# Pro Winkel nur die jeweils neueste Messung merken:
#   messungen[winkel] = (abstand_cm, zeitpunkt)
# Ein dict (Wörterbuch) ist wie eine Tabelle mit Schlüssel -> Wert.
messungen = {}
aktueller_winkel = 0
puffer = ""

# --- Diagramm vorbereiten ----------------------------------------------------
fig = plt.figure(figsize=(10, 6), facecolor=HINTERGRUND)
fig.canvas.manager.set_window_title("Abstandsradar")
ax = fig.add_subplot(projection="polar", facecolor=HINTERGRUND)  # Polarkoordinaten!
ax.set_thetamin(0)               # nur Halbkreis 0°–180°
ax.set_thetamax(180)
if SPIEGELN:
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location("W")
ax.set_ylim(0, REICHWEITE_CM)
ax.set_rticks(range(50, REICHWEITE_CM + 1, 50))
ax.tick_params(colors=GRUEN, labelsize=9)
ax.grid(color=GRUEN, alpha=0.25)
ax.spines["polar"].set_color(GRUEN)
fig.text(0.5, 0.92, "Abstandsradar", ha="center", color=GRUEN, fontsize=14)
# Halbkreis groß ins Fenster ziehen (Werte sind Anteile der Fensterfläche)
fig.subplots_adjust(left=0.05, right=0.95, bottom=-0.5, top=1.4)

punkte = ax.scatter([], [], s=28, color=GRUEN, edgecolors="none")
strahl, = ax.plot([], [], color=GRUEN, linewidth=2)
anzeige = fig.text(0.02, 0.95, "", ha="left", va="top", color=GRUEN,
                   fontsize=13, family="monospace")


def zeile_auswerten(zeile):
    """Macht aus "45,103.2" die Zahlen 45 und 103.2 und speichert sie."""
    global aktueller_winkel
    teile = zeile.strip().split(",")
    if len(teile) != 2:
        return                     # z. B. halbe Zeile beim Start: ignorieren
    try:
        winkel = int(teile[0])
        abstand = float(teile[1])
    except ValueError:
        return
    aktueller_winkel = winkel
    if 0 < abstand <= REICHWEITE_CM:
        messungen[winkel] = (abstand, time.time())
    else:
        messungen.pop(winkel, None)  # kein Echo / zu weit: alten Punkt löschen
    text = f"{abstand:5.1f} cm" if abstand > 0 else " kein Echo"
    anzeige.set_text(f"Winkel {winkel:3d}°   Abstand {text}")


def aktualisieren(_frame):
    global puffer
    puffer += verbindung.read(verbindung.in_waiting or 1).decode(errors="ignore")
    *zeilen, puffer = puffer.split("\n")
    for zeile in zeilen:
        zeile_auswerten(zeile)

    # Alte Punkte entfernen, die übrigen nach Alter verblassen lassen
    jetzt = time.time()
    for w in [w for w, (_, t) in messungen.items() if jetzt - t > NACHLEUCHTEN_S]:
        del messungen[w]

    winkel_rad, abstaende, farben = [], [], []
    for w, (d, t) in messungen.items():
        winkel_rad.append(math.radians(w))       # matplotlib rechnet im Bogenmaß
        abstaende.append(d)
        helligkeit = 1 - (jetzt - t) / NACHLEUCHTEN_S
        farben.append((0.22, 1.0, 0.48, max(helligkeit, 0.05)))  # RGBA

    if winkel_rad:
        punkte.set_offsets(list(zip(winkel_rad, abstaende)))
        punkte.set_facecolors(farben)
    else:
        punkte.set_offsets([[0, 0]])
        punkte.set_facecolors([(0, 0, 0, 0)])

    # Der "Radarstrahl": Linie vom Mittelpunkt in aktueller Richtung
    w = math.radians(aktueller_winkel)
    strahl.set_data([w, w], [0, REICHWEITE_CM])
    return punkte, strahl, anzeige


animation = FuncAnimation(fig, aktualisieren, interval=50, cache_frame_data=False)
plt.show()
verbindung.close()
