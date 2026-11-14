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

- [ ] **Phase 1:** Repo anlegen, erster Commit
- [ ] **Phase 2:** LED blinkt (Upload funktioniert), Ultraschallsensor auslesen
- [ ] **Phase 3:** Servo schwenkt, Arduino sendet `Winkel,Abstand`
- [ ] **Phase 4:** Python-Radarbild am PC
- [ ] **Phase 5:** Halter konstruieren (Fusion-MCP), drucken, montieren
- [ ] **Phase 6:** Auf GitHub hochladen
