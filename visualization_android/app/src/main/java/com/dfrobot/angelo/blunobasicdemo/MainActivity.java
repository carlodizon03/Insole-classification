package com.dfrobot.angelo.blunobasicdemo;

import android.annotation.SuppressLint;
import android.annotation.TargetApi;
import android.bluetooth.BluetoothGattService;
import android.content.Context;
import android.content.SharedPreferences;
import android.os.Build;
import android.os.Bundle;
import android.content.Intent;
import android.os.SystemClock;
import android.text.TextUtils;
import android.util.ArrayMap;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.Chronometer;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.ScrollView;
import android.widget.TextView;

import java.util.Arrays;
import java.util.Map;
import java.util.Random;

import ca.hss.heatmaplib.HeatMap;

public class MainActivity<getBundle> extends BlunoLibrary {
	private Button StartButton;
	private Button StopButton;
	private Button ConnectButton;
	private ImageButton RestartButton;
	private Button buttonScan;
	private Chronometer mChronometer;
	private TextView scanStatus;


	private TextView sensorView1;
	private TextView sensorView4;
	private TextView sensorView5;
	private TextView sensorView6;

	private TextView sensorView1R;
	private TextView sensorView4R;
	private TextView sensorView5R;
	private TextView sensorView6R;

	private HeatMap heatMap1;
	private HeatMap heatMap2;


	private long laststop;
	private boolean running;
	private String sending="1";

	public String recDataString = new String();
//	private StringBuilder recDataString = new StringBuilder();


	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		onCreateProcess();														//onCreate Process by BlunoLibrary


		//serialBegin(115200);													//set the Uart Baudrate on BLE chip to 115200

		StartButton = (Button) findViewById(R.id.start_button);
		StopButton = (Button) findViewById(R.id.stop_button);
		ConnectButton = (Button) findViewById(R.id.connected_button);
		RestartButton = (ImageButton) findViewById(R.id.re_button);
		mChronometer = (Chronometer) findViewById(R.id.chronometer);
		scanStatus = (TextView) findViewById(R.id.scanStatus);

		sensorView1 = (TextView) findViewById(R.id.sensorView1);
		sensorView4 = (TextView) findViewById(R.id.sensorView4);
		sensorView5 = (TextView) findViewById(R.id.sensorView5);
		sensorView6 = (TextView) findViewById(R.id.sensorView6);

		sensorView1R = (TextView) findViewById(R.id.sensorView1R);
		sensorView4R = (TextView) findViewById(R.id.sensorView4R);
		sensorView5R = (TextView) findViewById(R.id.sensorView5R);
		sensorView6R = (TextView) findViewById(R.id.sensorView6R);


		heatMap1 = (HeatMap) findViewById(R.id.heatmap1);
		heatMap2 = (HeatMap) findViewById(R.id.heatmap2);


		//start button
		StartButton.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				if (!running) {
					mChronometer.setBase(SystemClock.elapsedRealtime() - laststop);
					mChronometer.start();
					running = true;
//                    StartButton.setEnabled(false);
//                    StopButton.setEnabled(true);


				}

				serialSend("1");

			}
		});

		//stop button
		StopButton.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				if (running) {
					mChronometer.stop();
					laststop = SystemClock.elapsedRealtime() - mChronometer.getBase();
					running = false;
//                    StopButton.setEnabled(false);
//                    StartButton.setEnabled(true);

					//stop  getting data
//					serialSend("8");
//					onStop();


				}
			}
		});

		//Connect Button
		ConnectButton.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				buttonScanOnClickProcess();

			}
		});

//		DisconnectButton.setOnClickListener(new View.OnClickListener()
//		{
//			@Override
//			public void onClick(View v) {
//								onStop();
//
//
//				}
//		});

		//reset button
		RestartButton.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				mChronometer.stop();
				mChronometer.setBase(SystemClock.elapsedRealtime());
				laststop = 0;
//                StartButton.setEnabled(true);
//                StopButton.setEnabled(true);

				//stop  getting data
				onStop();

				//clear and refresh the display Heatmap
				heatMap1.forceRefresh();
				heatMap1.clearData();

				heatMap2.forceRefresh();
				heatMap2.clearData();
			}
		});
	}

	protected void onResume(){
		super.onResume();
		System.out.println("BlUNOActivity onResume");
		onResumeProcess();														//onResume Process by BlunoLibrary
	}



	@Override
	protected void onActivityResult(int requestCode, int resultCode, Intent data) {
		onActivityResultProcess(requestCode, resultCode, data);					//onActivityResult Process by BlunoLibrary
		super.onActivityResult(requestCode, resultCode, data);
	}

	@Override
	protected void onPause() {
		super.onPause();
		onPauseProcess();														//onPause Process by BlunoLibrary
	}

	protected void onStop() {
		super.onStop();
		onStopProcess();														//onStop Process by BlunoLibrary
	}

	@Override
	protected void onDestroy() {
		super.onDestroy();
		onDestroyProcess();														//onDestroy Process by BlunoLibrary
	}

	@Override
	public void onConectionStateChange(connectionStateEnum theConnectionState) {//Once connection state changes, this function will be called
		switch (theConnectionState) {											//Four connection state
			case isConnected:
//			buttonScan.setText("Connected");
				scanStatus.setText("Connected");
						//send the data to the BLUNO
				break;
			case isConnecting:
//			buttonScan.setText("Connecting");
				scanStatus.setText("Connecting");
				break;
			case isToScan:
//			buttonScan.setText("Scan");
				scanStatus.setText("Status");
				break;
			case isScanning:
//			buttonScan.setText("Scanning");
				scanStatus.setText("Scanning");
				break;
			case isDisconnecting:
//			buttonScan.setText("isDisconnecting");
				scanStatus.setText("isDisconnecting");
				break;
			default:
				break;
		}
	}

	@Override
	public void onSerialReceived(String theString) {							//Once connection data received, this function will be called
		// TODO Auto-generated method stub
		recDataString += theString;                        //keep appending to string until E

		int endRight = recDataString.indexOf("ER");               	//determine end of line
		if (endRight == 13 ) {                                          //make sure there data before E
			String dataInPrint = recDataString.substring(1, endRight);
			int dataLength = dataInPrint.length();                //get length of data received
			System.out.println("DATA: " + dataInPrint);
			System.out.println("String Length: " + String.valueOf(dataLength));
//
			if (recDataString.charAt(0) == 'R'){                //get sensor looking for start with S
				String sensor1 = recDataString.substring(1, 4);  //assume that each sensor has 3 position + tabs (not for last sensor)
				String sensor4 = recDataString.substring(4, 7);		//This sensor receiving should be fix (s1, s4, s5, s6) from Arduino code
				String sensor5 = recDataString.substring(7, 10);
				String sensor6 = recDataString.substring(10, 13);

				sensorView1R.setText(" Sensor1: " + sensor1 );		//display the value sensor below heatmap
				sensorView4R.setText(" Sensor4: " + sensor4 );
				sensorView5R.setText(" Sensor5: " + sensor5 );
				sensorView6R.setText(" Sensor6: " + sensor6 );



				//right foot
				double value1 = Double.parseDouble(sensor6);
				double value2 = Double.parseDouble(sensor4);
				double value3 = Double.parseDouble(sensor5);
				double value4 = Double.parseDouble(sensor1);

				analogRight(value1,value2,value3,value4);
//				//split data for each sensor by comma
//
//				String dataInPrint = recDataString.substring(recDataString.indexOf("R")+1, endRight);   //extract string
//				System.out.println("DATA: " + dataInPrint);
//
//				String[] parts = dataInPrint.split(",");
//				double[] values = new double[4];
//
//				//using for loop to parse data to double
//				for (int i=1; i<parts.length;i++){
//					values[i] = Double.parseDouble(parts[i]);
//				}
//				sensorView1R.setText("Sensor1: " + values[0]);
//				sensorView4R.setText("Sensor4: " + values[1]);
//				sensorView5R.setText("Sensor5: " + values[2]);
//				sensorView6R.setText("Sensor6: " + values[3]);
//
//				analogRight(values[3],values[1],values[2],values[0]);
			}
			recDataString = "";		 //clear all string data

		}

		//Left side  start Letter with 'L'
		// L000111222333EL
		int endLeft = recDataString.indexOf("EL");               	//determine end of line
		if (endLeft == 13 ) {                                          //make sure there data before E
			String dataInPrint = recDataString.substring(1, endLeft);   //extract string
//			serialReceivedText.setText("Received: " + dataInPrint);
			int dataLength = dataInPrint.length();                //get length of data received
			System.out.println("DATA: " + dataInPrint);
			System.out.println("String Length: " + String.valueOf(dataLength));



			if (recDataString.charAt(0) == 'L') {                //get sensor looking for start with S
				String sensor1 = recDataString.substring(1, 4);  //assume that each sensor has 3 position + tabs (not for last sensor)
				String sensor4 = recDataString.substring(4, 7);		//This sensor receiving should be fix (s1, s4, s5, s6) from Arduino code
				String sensor5 = recDataString.substring(7, 10);
				String sensor6 = recDataString.substring(10, 13);

				sensorView1.setText(" Sensor1: " + sensor1 );		//display the value sensor below heatmap
				sensorView4.setText(" Sensor4: " + sensor4 );
				sensorView5.setText(" Sensor5: " + sensor5 );
				sensorView6.setText(" Sensor6: " + sensor6 );

				//left foot
				double value1 = Double.parseDouble(sensor4);
				double value2 = Double.parseDouble(sensor6);
				double value3 = Double.parseDouble(sensor1);
				double value4 = Double.parseDouble(sensor5);

				analogLeft(value1,value2,value3,value4);

//				String dataInPrint = recDataString.substring(recDataString.indexOf("L")+1, endLeft);   //extract string
//				System.out.println("DATA: " + dataInPrint);
//				//split data for each sensor by comma
//				String[] parts = dataInPrint.split(",");
//				double[] values = new double[4];

//				//using for loop to parse data to double
//				for (int i=1; i<parts.length;i++){
//					values[i] = Double.parseDouble(parts[i]);
//				}
//				sensorView1.setText("Sensor1: " + values[0]);
//				sensorView4.setText("Sensor4: " + values[1]);
//				sensorView5.setText("Sensor5: " + values[2]);
//				sensorView6.setText("Sensor6: " + values[3]);
//
//				analogLeft(values[1],values[3],values[0],values[2]);
			}
			recDataString = "";

		}





	}


	//	@TargetApi(Build.VERSION_CODES.KITKAT)
	public void analogRight(double value1, double value2,double value3,double value4){ 							//test just value1 in one position
		//Set the range that you want the heat maps gradient to cover
		heatMap2.setMinimum(0);
		heatMap2.setMaximum(100);

		//make the colour gradient from yellow to red
		Map<Float, Integer> colorStops = new ArrayMap<>();
		colorStops.put(0.3f, 0xFFDACF03);
		colorStops.put(0.4f, 0xFFDA7203);
		colorStops.put(1.0f, 0xFFDA031C);
		heatMap2.setColorStops(colorStops);

		//For Heatmap
		//add location sensor data to the map with random value
		float x1 = 0.35f;
		float y1 = 0.25f;
		float x2 = 0.65f;
		float y2 = 0.3f;
		float x3 = 0.35f;
		float y3 = 0.90f;
		float x4 = 0.65f;
		float y4 = 0.90f;

		HeatMap.DataPoint point1 = new HeatMap.DataPoint(x1, y1, value1);
		heatMap2.addData(point1);

		HeatMap.DataPoint point2 = new HeatMap.DataPoint(x2, y2, value2);
		heatMap2.addData(point2);

		HeatMap.DataPoint point3 = new HeatMap.DataPoint(x3, y3, value3);
		heatMap2.addData(point3);

		HeatMap.DataPoint point4 = new HeatMap.DataPoint(x4, y4, value4);
		heatMap2.addData(point4);

		heatMap2.forceRefresh();


	}

	public void analogLeft(double value1, double value2,double value3,double value4){ 							//test just value1 in one position
		//Set the range that you want the heat maps gradient to cover
		heatMap1.setMinimum(0);
		heatMap1.setMaximum(100);

		//make the colour gradient from yellow to red
		Map<Float, Integer> colorStops = new ArrayMap<>();
		colorStops.put(0.3f, 0xFFDACF03);
		colorStops.put(0.4f, 0xFFDA7203);
		colorStops.put(1.0f, 0xFFDA031C);
		heatMap1.setColorStops(colorStops);

		//For Heatmap
		//add location sensor data to the map with random value
		float x1 = 0.35f;
		float y1 = 0.3f;
		float x2 = 0.65f;
		float y2 = 0.25f;
		float x3 = 0.35f;
		float y3 = 0.90f;
		float x4 = 0.65f;
		float y4 = 0.90f;

		HeatMap.DataPoint point1 = new HeatMap.DataPoint(x1, y1, value1);
		heatMap1.addData(point1);

		HeatMap.DataPoint point2 = new HeatMap.DataPoint(x2, y2, value2);
		heatMap1.addData(point2);

		HeatMap.DataPoint point3 = new HeatMap.DataPoint(x3, y3, value3);
		heatMap1.addData(point3);

		HeatMap.DataPoint point4 = new HeatMap.DataPoint(x4, y4, value4);
		heatMap1.addData(point4);

		heatMap1.forceRefresh();



	}


}