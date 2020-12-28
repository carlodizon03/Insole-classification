#include "I2Cdev.h"
#include "MPU6050.h"
#include <SimpleTimer.h>

/**
 *  Define which insole will be programmed here
 *  
 *  Options:
 *  
 *  RIGHT_INSOLE 
 *  LEFT_INSOLE
 */
#define LEFT_INSOLE

SimpleTimer Timer;
int timer_id;
int prompt_counter = 3;
int prompt_timer_id;
/**
 *  Uncomment this line if you are gonna use accelerometer
 *  Comment if there is no connected accelerometer
 */
#define WITH_ACCEL

#if defined(WITH_ACCEL)
  MPU6050 accel;
  int16_t ax, ay, az;
  #define OUTPUT_READABLE_accel
#endif

// GND/5V is the left most pin facing the top of insole
int s1_p1 = A0;
int s2_p4 = A1;
int s3_p5 = A2;
int s4_p6= A3;
String s1_data;
String s2_data;
String s3_data;
String s4_data;

String visualization_data;
/*
 * Ending flag to be switched by timer callback
 */
bool isEnd = false;

/*
 * Timer callback to switch the Ending flag
 */
void setEndFlag()
{
  isEnd = true;
}

/**
 * Sending Modes
 *  0 - data collection
 *  1 - visualization
 *  8 - non-sending mode
 */
int sending_mode = 3;  

String dataCollection_endFlag= "S";

#if defined(RIGHT_INSOLE)
  String visualisation_prefix = "R";
  String visualization_suffix = "ER";
#elif defined(LEFT_INSOLE)
  String visualisation_prefix = "L";
  String visualization_suffix = "EL";
#endif

void setTimerInterval_(int interval, int *timer_id)
{
  timer_id = Timer.setInterval(interval,sendEndFlag);
}

void sendEndFlag()
{
  if (sending_mode == 0)
  {
    Serial.println();
    Serial.println(dataCollection_endFlag);
    isEnd = false;
    Timer.disable(timer_id);
    Timer.enable(prompt_timer_id);
    
  }
}

void prompt()
{
  if(sending_mode == 0)
  {
    if(prompt_counter == 3)
    {
      Serial.print("Make a whole step and back in ");
    }
    Serial.print(prompt_counter);Serial.print(".....");
    prompt_counter--;
    if(prompt_counter == 0 )
    {
      Serial.println();
      prompt_counter = 3;
      Timer.enable(timer_id); 
      Timer.disable(prompt_timer_id);
      
    }
  }
}

void sendVisualizationData()
{
  if (sending_mode == 1)
  {
    Serial.print(visualization_data);
    delay(100);
    Serial.flush();
    visualization_data = "";
  }
}
void setup() {
  pinMode(s1_p1, INPUT_PULLUP);
  pinMode(s2_p4, INPUT_PULLUP);
  pinMode(s3_p5, INPUT_PULLUP);
  pinMode(s4_p6, INPUT_PULLUP);
  Serial.begin(115200);
  
  #if defined(WITH_ACCEL)
    accel.initialize();
    Serial.println(accel.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
//  
//    Serial.println("Updating internal sensor offsets...");
//
//    Serial.print(accel.getXAccelOffset()); Serial.print("\t"); 
//    Serial.print(accel.getYAccelOffset()); Serial.print("\t"); 
//    Serial.print(accel.getZAccelOffset()); Serial.print("\t"); 
//    
//    Serial.print("\n");
//    accel.setXAccelOffset(-2305);
//    accel.setYAccelOffset(-2783);
//    accel.setZAccelOffset(2976);
//    Serial.print(accel.getXAccelOffset()); Serial.print("\t"); // -76
//    Serial.print(accel.getYAccelOffset()); Serial.print("\t"); // -2359
//    Serial.print(accel.getZAccelOffset()); Serial.print("\t"); // 1688
  #endif
  setTimerInterval_(2000, &timer_id);
  prompt_timer_id = Timer.setInterval(1000, prompt);
  Timer.disable(timer_id);
  Timer.disable(prompt_timer_id);
  
  Serial.println("Press: ");
  Serial.println("0 for data collection");
  Serial.println("1 for visualization");
  Serial.println("8 for- non-sending mode");

}

void loop() {

  if(Serial.available()>0)
  {
    char data = Serial.read();

    if(data == '0')
    { 
      visualization_data="";
      Serial.flush();
      sending_mode = 0;
      Timer.enable(timer_id);
    }
    else if(data == '1')
    {
      Serial.flush();
      sending_mode = 1;
      Timer.disable(timer_id);
    }
    else if(data == '2'){
      Serial.flush();
      Timer.deleteTimer(timer_id);
      setTimerInterval_(10, &timer_id);
      Timer.enable(timer_id);
    }
    else if(data == '3'){
      Serial.flush();
      Timer.deleteTimer(timer_id);
      setTimerInterval_(500, &timer_id);
      Timer.enable(timer_id);
    }
    else if(data == '4'){
      Serial.flush();
      Timer.deleteTimer(timer_id);
      setTimerInterval_(1000, &timer_id);
      Timer.enable(timer_id);
    }
    else if(data == '5'){
      Serial.flush();
      Timer.deleteTimer(timer_id);
      setTimerInterval_(1500, &timer_id);
      Timer.enable(timer_id);
    }
    else if(data == '6'){
      Serial.flush();
      Timer.deleteTimer(timer_id);
      setTimerInterval_(2000, &timer_id);
      Timer.enable(timer_id);
    }
    else if(data == '7'){
      Serial.flush();
      Timer.deleteTimer(timer_id);
      setTimerInterval_(2500, &timer_id);
      Timer.enable(timer_id);
    }
    else if(data == '8'){
      Serial.flush();
      Timer.disable(timer_id);
      Timer.disable(prompt_timer_id);
      sending_mode = 3;
    }
  }
  Timer.run();
  if(sending_mode == 0)
  {
    if(Timer.isEnabled(timer_id))
    {
      
      sendData();
      if(isEnd)
      {
        sendEndFlag();
      }
    }
    
  }
  if(sending_mode == 1)
  {
    getVisualizationData();
    sendVisualizationData();
  }

  
}

String make3Digits(int val){
  if(val <100){
    if (val > 9) {
       String new_val = "0" + (String) val;
       return new_val;
    }
    else if(val < 10) {
        String new_val = "00" + (String) val;
        return new_val;
    }
 
  }
  else {
    return "100";  
  }
}

void getVisualizationData()
{
    visualization_data += visualisation_prefix;
    visualization_data+= make3Digits(map(analogRead(s1_p1),1023,500,0,100));
    visualization_data+= make3Digits(map(analogRead(s2_p4),1023,500,0,100));
    visualization_data+= make3Digits(map(analogRead(s3_p5),1023,500,0,100));
    visualization_data+= make3Digits(map(analogRead(s4_p6),1023,500,0,100));
    visualization_data+= visualization_suffix;
}
void sendData()
{ 
  String data = "";
  #if defined(WITH_ACCEL)
    accel.getAcceleration(&ax,&ay,&az);
    data += ax;
    data += ',';
    data += ay;
    data += ',';
    data += az;
    data += ',';
  #endif
  int a = map(analogRead(s1_p1),1023,500,0,100);
  int b = map(analogRead(s2_p4),1023,500,0,100);
  int c = map(analogRead(s3_p5),1023,500,0,100);
  int d = map(analogRead(s4_p6),1023,500,0,100);
  data += (a)<100 ? a :100;
  data += ',';
  data += (b)<100 ? b :100;
  data += ',';
  data += (c)<100 ? c :100;
  data += ',';
  data += (d)<100 ? d :100;
  Serial.println(data);
}
