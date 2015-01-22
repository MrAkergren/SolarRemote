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
 
  Serial.begin(9600);
}

void loop() { 
  int x;
  x = analogRead (0);                  // Read the analog value for buttons
  
  if (x < 100) {                       // Right button is pressed
    lcd.setCursor(0,1);
    lcd.print ("Right ");
    Serial.println("run r"); 
  }
  else if (x < 200) {                  // Up button is pressed
    lcd.setCursor(0,1);
    lcd.print ("Up    ");
    Serial.println("run u");
    //Serial.write("run u");
    //Serial.write("\r");
  }
  else if (x < 450){                   // Down button is pressed
    lcd.setCursor(0,1);
    lcd.print ("Down  ");
    Serial.println("run d");
  }
  else if (x < 680){                   // Left button is pressed
    lcd.setCursor(0,1);
    lcd.print ("Left  ");
    Serial.println("run l");
  }
  else if (x < 1000){                   // Select button is pressed
    lcd.setCursor(0,1);
    lcd.print ("Select"); 
  }
  
  if (x != 1023) { //x == 1023 if no button is pressed
    delay(300);  //wait 300ms until input
  }
}
