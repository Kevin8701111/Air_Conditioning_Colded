#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

import serial, time
import json
import datetime
from serial import SerialException
import paho.mqtt.client as mqtt

# MQTT setup data
MQTT_SERVER = "10.20.0.19"
MQTT_PORT = 1883
MQTT_TOPIC = "air-conditioner-vent"

cold_sensor = serial.Serial()

while(1):
	if(cold_sensor.is_open):
		send_status = 0
		response = cold_sensor.readline()
		response = response.decode('ascii')
		print(response)
#		response = '{"Temperature" : "30.5", "Humidity" : "100"}'
		try:
			data = json.loads(str(response))
			Temperature = data["Temperature"]
			Humidity = data["Humidity"]
			Temperature = float(Temperature)
#			print(Temperature, type(Temperature), Humidity, type(Humidity))
			send_status = 1
		except:
			send_status = 0
		print('------------------------------------------------------')
		if (send_status == 1):
			try:
				# MQTT connection
				mqtt_conn = mqtt.Client()
				mqtt_conn.connect(MQTT_SERVER, MQTT_PORT)
				mqtt_conn.publish(MQTT_TOPIC, response)
				now = datetime.datetime.now()
				print('MQTT To Server OK ! -->' , now)
			except:
				print('MQTT To Server Error !')
		print('------------------------------------------------------')
		time.sleep(1)
	else:
		try:
			cold_sensor = serial.Serial('COM30', 9600, timeout=1)
			time.sleep(2.5)
		except:
			cold_sensor = serial.Serial()
		time.sleep(1)
