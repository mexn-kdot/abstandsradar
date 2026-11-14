// Blink-Test: Prüft, ob das Hochladen aufs Board funktioniert.
//
// Benutzt die eingebaute LED "L" auf dem Board (Pin 13), es muss also nichts
// verdrahtet werden. Viele Boards blinken ab Werk schon im Sekundentakt –
// deshalb blinkt dieses Programm in einem eigenen Muster: zweimal kurz, dann
// Pause. Siehst du das Doppelblitzen, läuft DEIN Programm.

// setup() läuft genau einmal nach dem Einschalten bzw. nach dem Hochladen.
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);  // Pin 13 als Ausgang schalten
}

// loop() läuft danach endlos immer wieder von vorn – wie ein SPS-Zyklus.
void loop() {
  blitz();
  blitz();
  delay(1000);  // 1 Sekunde Pause (Angabe in Millisekunden)
}

// Eine eigene Funktion: LED kurz an, dann kurz aus.
void blitz() {
  digitalWrite(LED_BUILTIN, HIGH);  // LED an (5 V auf den Pin)
  delay(100);
  digitalWrite(LED_BUILTIN, LOW);   // LED aus (0 V)
  delay(150);
}
