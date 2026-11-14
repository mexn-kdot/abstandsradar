// Ultraschall-Test: Liest den HC-SR04 aus und schickt den Abstand an den PC.
//
// Verdrahtung (Arduino Mega):
//   HC-SR04 VCC  -> 5V
//   HC-SR04 GND  -> GND
//   HC-SR04 Trig -> Pin 6
//   HC-SR04 Echo -> Pin 7
//
// Messprinzip: Trig bekommt einen 10-µs-Impuls, der Sensor sendet einen
// 40-kHz-Ultraschallburst. Echo ist so lange HIGH, bis das Echo zurück ist.
// Laufzeit (hin und zurück) * Schallgeschwindigkeit / 2 = Abstand.

const int TRIG_PIN = 6;
const int ECHO_PIN = 7;

// Schallgeschwindigkeit bei ~20 °C: 343 m/s = 0,0343 cm/µs
const float SCHALL_CM_PRO_US = 0.0343;

// Länger als 30 ms warten wir nicht auf ein Echo (entspricht ~5 m).
// Der Sensor schafft zuverlässig nur ca. 2 cm bis 4 m.
const unsigned long TIMEOUT_US = 30000;

void setup() {
  Serial.begin(9600);  // Serielle Verbindung zum PC, 9600 Baud
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  Serial.println("Ultraschall-Test gestartet");
}

void loop() {
  float abstand = messeAbstandCm();

  if (abstand < 0) {
    Serial.println("kein Echo (nichts im Bereich)");
  } else {
    Serial.print("Abstand: ");
    Serial.print(abstand, 1);  // eine Nachkommastelle
    Serial.println(" cm");
  }

  delay(200);  // 5 Messungen pro Sekunde
}

// Gibt den Abstand in cm zurück, oder -1, wenn kein Echo kam.
float messeAbstandCm() {
  // Sauberen 10-µs-Triggerimpuls erzeugen
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Dauer messen, die Echo HIGH ist (0 = Timeout)
  unsigned long laufzeit = pulseIn(ECHO_PIN, HIGH, TIMEOUT_US);
  if (laufzeit == 0) {
    return -1;
  }
  return laufzeit * SCHALL_CM_PRO_US / 2.0;
}
