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

MPU6050 accel;
int16_t ax, ay, az;
#define OUTPUT_READABLE_accel


// GND/5V is the left most pin facing the top of insole
int s1_p1 = A0;
int s2_p4 = A1;
int s3_p5 = A2;
int s4_p6= A3;
String s1_data;
String s2_data;
String s3_data;
String s4_data;
String accel_x;
String accel_y;
String accel_z;
String visualization_data;
/*
 * Sending flag to be switched by timer callback
 */
bool isSend = false;

/*
 * Timer callback to switch the sending flag
 */
void setSendFlag()
{
  isSend = true;
}

/**
 * Sending Modes
 *  0 - data collection
 *  1 - visualization
 *  3 - non-sending mode
 */
int sending_mode = 3;  

String dataCollection_prefix = "S";
String dataCollection_suffix = "E";

#if defined(RIGHT_INSOLE)
  String visualisation_prefix = "R";
  String visualization_suffix = "ER";
#elif defined(LEFT_INSOLE)
  String visualisation_prefix = "L";
  String visualization_suffix = "EL";
#endif



void setTimerInterval_(int interval, int *timer_id)
{
  timer_id = Timer.setInterval(interval,setSendFlag);
}
void sendDataCollectionData()
{
  if (sending_mode == 0)
  {
    Timer.disable(timer_id);
    Serial.println(dataCollection_prefix);
    Serial.print("x");
    Serial.println(accel_x);
    Serial.print("y");
    Serial.println(accel_y);
    Serial.print("z");
    Serial.println(accel_z);
    Serial.print("a");
    Serial.println(s1_data);
    Serial.print("b");
    Serial.println(s2_data);
    Serial.print("c");
    Serial.println(s3_data);
    Serial.print("d");
    Serial.println(s4_data);
    Serial.println(dataCollection_suffix);
    accel_x = "";
    accel_y = "";
    accel_z = "";
    s1_data = "";
    s2_data = "";
    s3_data = "";
    s4_data = "";
    isSend = false;
    Timer.enable(timer_id); 
  }
}
void sendVisualizationData()
{
  if (sending_mode == 1)
  {
    Serial.print(visualisation_prefix);
    Serial.print(visualization_data);
    Serial.println(visualization_suffix);
    visualization_data = "";
  }
}
void setup() {
  pinMode(s1_p1, INPUT_PULLUP);
  pinMode(s2_p4, INPUT_PULLUP);
  pinMode(s3_p5, INPUT_PULLUP);
  pinMode(s4_p6, INPUT_PULLUP);
  Serial.begin(115200);
  accel.initialize();
  Serial.println(accel.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");

  Serial.println("Updating internal sensor offsets...");

  Serial.print(accel.getXAccelOffset()); Serial.print("\t"); // -76
  Serial.print(accel.getYAccelOffset()); Serial.print("\t"); // -2359
  Serial.print(accel.getZAccelOffset()); Serial.print("\t"); // 1688
  
  Serial.print("\n");
  accel.setXAccelOffset(-937);
  accel.setYAccelOffset(-2561);
  accel.setZAccelOffset(1419);
  Serial.print(accel.getXAccelOffset()); Serial.print("\t"); // -76
  Serial.print(accel.getYAccelOffset()); Serial.print("\t"); // -2359
  Serial.print(accel.getZAccelOffset()); Serial.print("\t"); // 1688

  setTimerInterval_(100, &timer_id);
  Timer.disable(timer_id);
}

void loop() {

  if(Serial.available()>0)
  {
    int data = Serial.read();

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
      setTimerInterval_(100, &timer_id);
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
      sending_mode = 3;
    }
  }

  if(sending_mode == 0)
  {
    Timer.run();
    getAllData();
    if(isSend)
    {
      sendDataCollectionData();
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
  else{
    return "100";  
  }
  
}

void getVisualizationData()
{
  
    visualization_data+= make3Digits(map(analogRead(s1_p1),1023,500,0,100));
    visualization_data+= make3Digits(map(analogRead(s2_p4),1023,500,0,100));
    visualization_data+= make3Digits(map(analogRead(s3_p5),1023,500,0,100));
    visualization_data+= make3Digits(map(analogRead(s4_p6),1023,500,0,100));

}
void getAllData()
{ 
  accel.getAcceleration(&ax,&ay,&az);
  accel_x += ax;
  accel_y += ay;
  accel_z += az;
  s1_data += map(analogRead(s1_p1),1023,500,0,100);
  s2_data += map(analogRead(s2_p4),1023,500,0,100);
  s3_data += map(analogRead(s3_p5),1023,500,0,100);
  s4_data += map(analogRead(s4_p6),1023,500,0,100);
  accel_x += ",";
  accel_y += ",";
  accel_z += ",";
  s1_data += ",";
  s2_data += ",";
  s3_data += ",";
  s4_data += ",";
}
