# Abstandsradar

Ein Ultraschallsensor auf einem Servo schwenkt von 0° bis 180° und misst dabei den Abstand zu Hindernissen. Ein Python-Programm am PC zeichnet daraus live ein Radarbild.

## Aufbau

```
[Arduino Mega 2560]  --USB (seriell)-->  [PC: Python]
 Servo SG90 schwenkt 0–180°               liest Zeilen "Winkel,Abstand"
 HC-SR04 misst Abstand                    zeichnet Radarbild
 sendet z. B. "45,120"
```

## Ordnerstruktur

| Ordner | Inhalt | Sprache/Werkzeug |
|---|---|---|
| `arduino/` | Programm für das Board | C++ (Arduino IDE) |
| `pc/` | Radar-Anzeige | Python |
| `halter/` | 3D-Druck-Halter Sensor ↔ Servo, Fusion-Skripte und STL | Fusion (per MCP) |

Die Ordner entstehen, sobald es dort den ersten Inhalt gibt – Git speichert keine leeren Ordner.

## Hardware

- Elegoo Mega 2560 (Most Complete Starter Kit)
- Ultraschallsensor HC-SR04
- Servo SG90
- 3D-gedruckter Halter (Ender-3 V3 SE)

## Fahrplan

- [x] **Phase 1:** Repo anlegen, erster Commit
- [x] **Phase 2:** LED blinkt (Upload funktioniert), Ultraschallsensor auslesen – Verdrahtung: `docs/verdrahtung-ultraschall.html`
- [x] **Phase 3:** Servo schwenkt, Arduino sendet `Winkel,Abstand` – Verdrahtung: `docs/verdrahtung-radar.html`, Programm: `arduino/radar`
- [x] **Phase 4:** Python-Radarbild am PC – `python pc/radar.py` (Live-Kurve ohne Servo: `pc/live_abstand.py`)
- [x] **Phase 5:** Halter konstruieren (Fusion-MCP), drucken, montieren
  - [x] Konstruktion in Fusion, Datei „Halloween_Elektronikgehäuse“ (v3), Komponenten `Deckel_Radar` und `Sensorhalter`. Richtungen: vorne = Schallwandler, hinten = Kabelschlitz.
  - [x] `halter/Deckel_Radar.stl`: neuer Deckel für die Kiste, gleiche 4 × M3 wie der alte. SG90 hängt im Ausschnitt (Welle in Deckelmitte), Laschen oben auf, 1 Schraube M2 direkt in den 3-mm-Deckel (Kernloch 1,7 durchgehend). Kabelnut fürs Servokabel, Kabelschlitz hinten mittig (7 mm, zum Rand offen) für die Sensorkabel. Druck: flache Unterseite aufs Bett (Einbaulage), ca. 31 g.
  - [x] `halter/Sensorhalter.stl`: Winkel mit Horntasche quer (Doppelarm 32 mm) und Hornschraube von oben (Senkung Ø 5). HC-SR04 kopfüber auf 4 Buchsen, Schrauben M1,6, Stiftleiste oben, Kabel als Schlaufe frei. Druck: Horntasche aufs Bett, ca. 6,5 g.
  - [x] Gedruckt und montiert. Die Bohrungen für den Sensor passten nicht, deshalb ist der HC-SR04 aufgeklebt. Für einen Nachdruck den Lochabstand am eigenen Sensor nachmessen.
- [x] **Phase 6:** Auf GitHub hochladen – https://github.com/mexn-kdot/abstandsradar

## Ideen für später

- **TF-Luna statt HC-SR04:** Einpunkt-LiDAR mit Laser-Laufzeitmessung. Reichweite bis 8 m, Strahl nur ca. 2° breit statt 15–30°, Preis ca. 20–40 €. Damit wird das Radarbild deutlich schärfer, Kanten erscheinen als Kanten. Anschluss mit 4 Kabeln über UART an `Serial1` des Mega (5V, GND, TX, RX). Servo und `pc/radar.py` bleiben, neu sind die Messfunktion in `arduino/radar` und ein angepasster Sensorhalter. Schwächen: direkte Sonne, Glas und Spiegel.
- **Autarker Betrieb mit LCD1602 aus dem Kit:** „Skyline“-Anzeige des Radars direkt auf dem Display, ohne PC.
- **Flieger-Tracker:** eigenes Projekt, ausgearbeitet im Claude-Doc „Idee: Flieger-Tracker mit Kamera“.
