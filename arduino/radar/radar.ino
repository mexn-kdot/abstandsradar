// Radar: Servo schwenkt den Ultraschallsensor hin und her, bei jedem Winkel
// wird gemessen und eine Zeile "Winkel,Abstand" an den PC geschickt.
//
// Beispiel-Ausgabe:   45,103.2     (45°, 103,2 cm)
//                     48,-1        (48°, kein Echo)
//
// Verdrahtung (Arduino Mega), Plan: docs/verdrahtung-radar.html
//   HC-SR04 VCC  -> 5V          HC-SR04 Trig -> Pin 6
//   HC-SR04 GND  -> GND         HC-SR04 Echo -> Pin 7
//   Servo orange (Signal) -> Pin 9
//   Servo rot  (+5 V)     -> + Schiene Steckbrett (Powerbank USB 2)
//   Servo braun (GND)     -> - Schiene Steckbrett, Schiene mit Mega-GND verbunden

#include <Servo.h>  // Fertige Bibliothek, gehört zur Arduino-Software dazu

const int TRIG_PIN  = 6;
const int ECHO_PIN  = 7;
const int SERVO_PIN = 9;

const float SCHALL_CM_PRO_US = 0.0343;
const unsigned long TIMEOUT_US = 30000;

// Schwenkbereich und Schrittweite in Grad
const int WINKEL_MIN = 0;
const int WINKEL_MAX = 180;
const int SCHRITT    = 3;

// Wartezeit nach jedem Schritt, damit der Servo steht, bevor gemessen wird
const int BERUHIGEN_MS = 25;

Servo servo;            // ein Servo-"Objekt": steht für den echten Servo
int winkel = WINKEL_MIN;
int richtung = +1;      // +1 = aufwärts schwenken, -1 = abwärts

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  servo.attach(SERVO_PIN);
  servo.write(winkel);
  delay(500);           // Servo in Startposition fahren lassen
}

void loop() {
  servo.write(winkel);
  delay(BERUHIGEN_MS);

  float abstand = messeMedianCm();

  // Eine Zeile "Winkel,Abstand" senden – dieses Format liest pc/radar.py
  Serial.print(winkel);
  Serial.print(",");
  if (abstand < 0) {
    Serial.println(-1);
  } else {
    Serial.println(abstand, 1);
  }

  // Nächster Winkel; am Rand die Richtung umdrehen (Pendelbewegung)
  winkel += richtung * SCHRITT;
  if (winkel >= WINKEL_MAX) { winkel = WINKEL_MAX; richtung = -1; }
  if (winkel <= WINKEL_MIN) { winkel = WINKEL_MIN; richtung = +1; }
}

// Misst dreimal und nimmt den mittleren Wert (Median).
// Ein einzelner Ausreißer fällt dadurch einfach raus – anders als beim
// Mittelwert, wo er das Ergebnis verfälschen würde.
float messeMedianCm() {
  float a = messeAbstandCm(); delay(5);
  float b = messeAbstandCm(); delay(5);
  float c = messeAbstandCm();

  // Median von drei Werten: der, der weder der größte noch der kleinste ist
  if ((a <= b && b <= c) || (c <= b && b <= a)) return b;
  if ((b <= a && a <= c) || (c <= a && a <= b)) return a;
  return c;
}

// Einzelmessung wie in ultraschall_test: Abstand in cm, oder -1 ohne Echo.
float messeAbstandCm() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  unsigned long laufzeit = pulseIn(ECHO_PIN, HIGH, TIMEOUT_US);
  if (laufzeit == 0) {
    return -1;
  }
  return laufzeit * SCHALL_CM_PRO_US / 2.0;
}
