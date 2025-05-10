const int buttonPins[4] = {2, 3, 4, 5};   // Button input pins
const int ledPins[4] = {6, 8, 10, 12};    // LED output pins
const int buzzerPin = 7;                  // Buzzer pin

bool wasPressed[4] = {false, false, false, false}; // Button state tracking

void setup() {
  for (int i = 0; i < 4; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);   // Buttons use internal pull-ups
    pinMode(ledPins[i], OUTPUT);            // LEDs as output
    digitalWrite(ledPins[i], LOW);          // Ensure LEDs start OFF
  }

  pinMode(buzzerPin, OUTPUT);               // Buzzer output
  digitalWrite(buzzerPin, LOW);             // Ensure buzzer is OFF at start
}

void loop() {
  for (int i = 0; i < 4; i++) {
    bool isPressed = (digitalRead(buttonPins[i]) == LOW);

    if (isPressed && !wasPressed[i]) {
      // Just pressed: turn on LED and beep
      digitalWrite(ledPins[i], HIGH);
      digitalWrite(buzzerPin, HIGH);
      delay(100);  // Short beep
      digitalWrite(buzzerPin, LOW);
    } else if (!isPressed && wasPressed[i]) {
      // Just released: turn off LED
      digitalWrite(ledPins[i], LOW);
    }

    wasPressed[i] = isPressed; // Update state
  }
}
