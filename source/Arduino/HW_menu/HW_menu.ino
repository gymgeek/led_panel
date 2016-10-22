long lastRead = 0;
long lastBlink = 0;
long blinkState = 0;
const int pins[8] = {10, 11, 12, 13, A0, A1, A2, A3};
int states[4][4] = {{0, 0, 0, 0},
                    {0, 0, 0, 0},
                    {0, 0, 0, 0},
                    {0, 0, 0, 0}};

#include <Keypad.h>

const byte ROWS = 4; 
const byte COLS = 4; 
char hexaKeys[ROWS][COLS] = {
  {'B','C','D','A'},
  {'F','G','H','E'},
  {'J','K','L','I'},
  {'M','N','O','P'}
};
byte rowPins[ROWS] = {5, 4, 3, 2}; 
byte colPins[COLS] = {9, 8, 7, 6}; 
Keypad customKeypad = Keypad( makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 


void setup() {
  Serial.begin(9600);
 for(int i = 0; i < sizeof(pins)/sizeof(int); i++) {
  pinMode(pins[i], OUTPUT);
  digitalWrite(pins[i], 0);
 }
  lastRead = millis();
}


void loop() {
  for(int ro = 0; ro < 4; ro++){
    oneRow(ro);
    for(int col = 0; col < 4; col++){
      if(states[ro][col] == 2) {
        digitalWrite(pins[4+col], blinkState);
      }
      else {
        digitalWrite(pins[4+col], !states[ro][col]);
      }
    }
    check();
   while(lastRead + 7 > millis()){    
   }
   lastRead = millis();
  }

}

void oneRow(int row){
  for(int i = 0; i < 4; i++){
    digitalWrite(pins[i], 0);

  }
   for(int i = 0; i < 4; i++){
  
    digitalWrite(pins[4+i], 1);
  }
  digitalWrite(pins[row], 1);
}

void check() {
  char customKey = customKeypad.getKey();
  
  if (customKey){
    Serial.print(customKey);
  }

  if(lastBlink + 500 < millis()){
    blinkState = (blinkState+1)%2;
    lastBlink = millis();
  }
  if(Serial.available()> 1){
    int recv = Serial.read()-65;
    int stat = Serial.read()-65;

    if(!(recv>= 0 && recv <=16)){
      Serial.flush();
      return;
    }
    states[int(recv/4)][3-(recv%4)] = stat;
    return;   
      
    
  }
}







