#include <LiquidCrystal.h>

// LCD
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// Coil pins (4 directions)
const int EAST  = 7;    // OUT1 → Austrumi
const int WEST  = 8;    // OUT2 → Rietumi
const int NORTH = 10;   // OUT3 → Ziemeļi
const int SOUTH = A0;   // OUT4 → Dienvidi

// L298N enables
const int ENA = 6;
const int ENB = 9;

// Potentiometer
const int freqPotPin = A2;

const int numSteps = 8;
int currentStep = 0;
float frequency = 1.0;
unsigned long stepDelayMicros = 100000;
unsigned long lastStepMicros = 0;

const byte coilSequence[8][4] = {
      {0, 170, 0, 0},     // WEST (2× power)
      {0, 170, 85, 0},    // WEST + NORTH
      {0, 255, 0, 0},     // NORTH (2× power)
      {85, 170, 0, 0},    // NORTH + EAST
      {170, 85, 0, 0},    // EAST (1× power)
      {170, 0, 0, 85},    // EAST + SOUTH
      {0, 0, 0, 85},      // SOUTH (1× power)
      {0, 85, 0, 170}     // SOUTH + WEST
};

void setup() {
  pinMode(EAST, OUTPUT); pinMode(WEST, OUTPUT);
  pinMode(NORTH, OUTPUT); pinMode(SOUTH, OUTPUT);
  pinMode(ENA, OUTPUT); pinMode(ENB, OUTPUT);
  digitalWrite(ENA, HIGH);
  digitalWrite(ENB, HIGH);

  lcd.begin(16, 2);
  lcd.print("Stepper Rotation");
  delay(1000);
  lcd.clear();

  Serial.begin(9600);
}

void loop() {
  int freqVal = analogRead(freqPotPin);
frequency = map(freqVal, 0, 1023, 10, 200) / 10.0; 
  stepDelayMicros = 1e6 / (frequency * numSteps);

  unsigned long now = micros();
  if (now - lastStepMicros >= stepDelayMicros) {
    lastStepMicros = now;

    analogWrite(EAST,  coilSequence[currentStep][0]);
    analogWrite(WEST,  coilSequence[currentStep][1]);
    analogWrite(NORTH, coilSequence[currentStep][2]);
    analogWrite(SOUTH, coilSequence[currentStep][3]);

    // LCD
    lcd.setCursor(0, 0);
    lcd.print("Freq: ");
    lcd.print(frequency, 1);
    lcd.print(" Hz     ");

    lcd.setCursor(0, 1);
    lcd.print("Step: ");
    lcd.print(currentStep);
    lcd.print("         ");

    Serial.print("Step ");
    Serial.print(currentStep);
    Serial.print(" | Freq: ");
    Serial.print(frequency, 1);
    Serial.print(" Hz | Delay: ");
    Serial.print(stepDelayMicros);
    Serial.println(" us");

    // Next step
    currentStep = (currentStep + 1) % numSteps;
  }
}
