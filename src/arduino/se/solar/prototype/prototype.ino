// 87876 LCD Shield för Arduino
// 16x2 tecken och knappar
// Kjell & Company 

// include the library code:
#include <LiquidCrystal.h>

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);   // initialize the library with the numbers of the interface pins

void setup() {
  lcd.begin(16, 2);                      // set up the LCD's number of columns and rows
  lcd.clear();                           // Clear LCD
  lcd.setCursor(0,0);                    // Set cursor to x=0 and y=0
  lcd.print("LCD Key Shield");           // Print text on LCD
  lcd.setCursor(0,1);
  lcd.print("Op. SolarRemote");
  delay(3000);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Press any Key:");
 
  SerialUSB.begin(38400);     //Serial init

}

int x;
int lastCmd;

//char run_r[] = "run r";
//char run_s[] = "run stop";
//byte row[] = {'\r'};

//byte run_r[] = {'r','u','n',' ','r'};
//byte run_s[] = {'r','u','n',' ','s','t','o','p'};

String run_r ="run r";
String run_s ="run stop";
String row = "\r";

uint8_t run_r1[run_r.length()];
run_r.getBytes(run_r1, message.length()+1);

uint8_t run_s1[run_s.length()];
run_s.getBytes(run_s1, message.length()+1);
  
void loop() { 
  x = analogRead (0);                  // Read the analog value for buttons
  
  if (x == 1023 && lastCmd < 900) {      //no button is pressed
    if (abs(lastCmd-x) > 2) {
      SerialUSB.write(run_s1, sizeof(run_s));
      SerialUSB.write(row, sizeof(row));
    }
    delay(300);
  }  
  if (x < 100) {                       // Right button is pressed
    lcd.setCursor(0,1);
    lcd.print ("Right ");
    if (abs(lastCmd-x) > 2) {
      SerialUSB.write(run_r1, sizeof(run_r));
      SerialUSB.write(row, sizeof(row));
    } 
  }
  else if (x < 200) {                  // Up button is pressed
    lcd.setCursor(0,1);
    lcd.print ("Up    ");
    if (abs(lastCmd-x) > 2) {
      SerialUSB.print("run u");
      SerialUSB.print("\r");
    }
  }
  else if (x < 450){                   // Down button is pressed
    lcd.setCursor(0,1);
    lcd.print ("Down  ");
    SerialUSB.println(x);
    if (abs(lastCmd-x) > 2) {
      SerialUSB.print("run d");
      SerialUSB.print("\r");
    }
  }
  else if (x < 680){                   // Left button is pressed
    lcd.setCursor(0,1);
    lcd.print ("Left  ");
    if (abs(lastCmd-x) > 2) {
      SerialUSB.print("run l");
      SerialUSB.print("\r");
    }
  }
  else if (x < 1000){                   // Select button is pressed
    lcd.setCursor(0,1);
    lcd.print ("Select"); 
    if (abs(lastCmd-x) > 2) {
      SerialUSB.write("\n");
    }
  }
  
  if (x != 1023) { //x == 1023 if no button is pressed
    delay(300);  //wait 300ms until input
  }
  
  lastCmd = x;
}

