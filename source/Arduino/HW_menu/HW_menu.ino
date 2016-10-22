long lastRead = 0;
long lastBlink = 0;
long blinkState = 0;

#include <WS2812.h>
int states[16] = {0, 0, 0, 0,0, 0, 0, 0,0, 0, 0, 0,0, 0, 0, 0,};

WS2812 LED(16); 
cRGB LedOn;
cRGB LedOff;

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
  LED.setOutput(10);
 
  Serial.begin(9600);

  lastRead = millis();
  LedOn.r = 0;
  LedOn.g = 0;
  LedOn.b = 255;
  for(int i = 0; i < 16; i++) {
      LED.set_crgb_at(i, LedOff);
  }
  LED.sync();
}


void loop() {
  for(int i = 0; i < 16; i++){    
      if(states[i] == 2) {
        if(blinkState){
            setLed(i, LedOn);
        }else {
            setLed(i, LedOff);
        }
         
      }
      else {
         if(states[i]){
            setLed(i, LedOn);
        }else {
            setLed(i, LedOff);
        }
      }
  }
    LED.sync();
    check();
   while(lastRead + 7 > millis()){    
   }
   lastRead = millis();
  

}
void setLed(int ledPos, cRGB ledVal) {
  switch(ledPos){ 
    case 0: // wiimote 1
      LED.set_crgb_at(0, ledVal);
      break;
    case 1: //hra B
      LED.set_crgb_at(4, ledVal);
      break;
    case 2: //hra C
      LED.set_crgb_at(5, ledVal);
      break;
    case 3: //hra D
      LED.set_crgb_at(6, ledVal);
      break;
    case 4://wiimote 2
      LED.set_crgb_at(1, ledVal);
      break;
    case 5: //hraF
      LED.set_crgb_at(7, ledVal);
      break;
    case 6://hra G
      LED.set_crgb_at(8, ledVal);
      break;
    case 7://hra H
      LED.set_crgb_at(9, ledVal);
      break;
    case 8://kalibrace infra
      LED.set_crgb_at(2, ledVal);
      break;
    case 9://hra J
      LED.set_crgb_at(10, ledVal);
      break;
    case 10: //hra K
      LED.set_crgb_at(11, ledVal);
      break;
    case 11: //hra L
      LED.set_crgb_at(12, ledVal);
      break;
    case 12://cancel
      LED.set_crgb_at(3, ledVal);
      break;
    case 13://hra N
      LED.set_crgb_at(13, ledVal);
      break;
    case 14://hra O
      LED.set_crgb_at(14, ledVal);
      break;
    case 15://hra P
      LED.set_crgb_at(15, ledVal);
      break;
   
    
  }
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
    states[recv] = stat;
    return;   
      
    
  }
}







