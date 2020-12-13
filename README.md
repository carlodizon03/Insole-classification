# Bluno Workflow Instructions

* Bluno will not send any data upon start up, it will just wait for command before starting the operation.
* To start the bluno sending data, from the mobile app you need to send any of 3 character to choose the mode described below: 
  1)  **"0"**  - is for **visualization mode**, when bluno received this character it will start sending data on  **visualization mode** with the following format:
      **R000111222333ER**
     or
     **L000111222333EL**
  2)  **"1"**  - is for **data collection mode**, when bluno received  this character it will start sending data on  **data collection mode** with the following format:
  
        **S,**  
          x,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,...,n<sub>t-1</sub>  
          y,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,...,n<sub>t-1</sub>  
          z,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,...,n<sub>t-1</sub>  
          a,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,...,n<sub>t-1</sub>  
          b,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,...,n<sub>t-1</sub>  
          c,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,...,n<sub>t-1</sub>  
          d,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,n<sub>t</sub>,...,n<sub>t-1</sub>  
        **E**
        
        **S** - indicates the Start of the data block.  
        **x** - indicates the row for the accelerometer x-axis.  
        **y** - indicates the row for the accelerometer y-axis.  
        **z** - indicates the row for the accelerometer z-axis.  
        **a** - indicates the sensor 1 of the insole.  
        **b** - indicates the sensor 4 of the insole.
        **c** - indicates the sensor 5 of the insole.
        **d** - indicates the sensor 6 of the insole.
        **t** - indicates the nth time the sample was read. 
        
   3)  **"2"** - is a **Non-Sending mode**. This simply stops the bluno to send any data.
   
        ### **NOTE:** The number of samples is highly dependent on Timer interval. So use the best interval, I suggest 1500ms for a complete movement. The Timer Interval can be set using commands described below:
        
 ### Changing the timer interval.
 
 * From the mobile app you need to send any of the following commands:
    1) **"2"** - sets the timer interval to 100 ms which is the fastest. 
    2) **"3"** - sets the timer interval to 500 ms.
    3) **"4"** - sets the timer interval to 1000 ms.
    4) **"5"** - sets the timer interval to 1500 ms.
    6) **"6"** - sets the timer interval to 2000 ms.
    7) **"7"** - sets the timer inter val to 2500 which is the slowest.
 
### Stop sending data.

* From the mobile app you need to send the following command:
  1) **"8"** - stops the timer and change the sending mode to **Non-Sending Mode**
        
        
