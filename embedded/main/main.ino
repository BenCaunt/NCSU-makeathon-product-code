#include <Servo.h>

const int PEDAL_PIN = D1;
const int SERVO_RECYCLE_PIN = D8;
const int SERVO_TRASH_PIN = D7;

const int time_to_close_ms = 4 * 1000;
const unsigned long debounce_time_ms = 400;  // Debounce time in milliseconds

Servo recycle;
Servo trash;
const int recycle_close = 73;
const int trash_close = 0;
const int recycle_open = 30;
const int trash_open = 45;

bool is_bin_closed = true;
unsigned long time_of_bin_close = 0;
unsigned long last_debounce_time = 0;  // Last time the pedal input was toggled
int last_pedal_state = LOW;            // Last known state of the pedal
int pedal_state = LOW;                 // Current state of the pedal

void setup() {
  Serial.begin(9600);
  pinMode(PEDAL_PIN, INPUT);
  recycle.attach(SERVO_RECYCLE_PIN);
  trash.attach(SERVO_TRASH_PIN);
  recycle.write(recycle_close);
  trash.write(trash_close);
}

void loop() {
  int reading = digitalRead(PEDAL_PIN);

  // If the switch changed, due to noise or pressing:
  if (reading != last_pedal_state) {
    last_debounce_time = millis();
  }

  if ((millis() - last_debounce_time) > debounce_time_ms) {
    // If the pedal state has changed:
    if (reading != pedal_state) {
      pedal_state = reading;

      // Only take action if the new pedal state is HIGH
      if (pedal_state == HIGH) {
        Serial.println("PEDAL_PRESSED");
      }
    }
  }

  last_pedal_state = reading;

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    openBin(command);
  }

  if (!is_bin_closed && millis() - time_of_bin_close >= time_to_close_ms) {
    recycle.write(recycle_close);
    trash.write(trash_close);
    is_bin_closed = true;
  }
}

void openBin(String binType) {
  Serial.println(binType);
  if (binType == "RECYCLE") {
    recycle.write(recycle_open);
  } else if (binType == "TRASH") {
    trash.write(trash_open);
  }
  time_of_bin_close = millis();
  is_bin_closed = false;
}
