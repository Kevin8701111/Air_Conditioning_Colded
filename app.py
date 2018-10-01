#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

import serial, time
import json
import datetime
from serial import SerialException
import paho.mqtt.client as mqtt
# usbid version only for 1.0.3
from usbid.device import usb_roots

# MQTT setup data
MQTT_SERVER = "10.20.0.19"
MQTT_PORT = 1883
MQTT_TOPIC = "air-conditioner-vent"

cold_sensor = serial.Serial()

def arduino_connect():
	global cold_sensor
	cold_sensor_tty = ""
	for usb_id in range(1, 10):
		try:
			usb_info = usb_roots()[1][1][usb_id]
		except:
			usb_info = " "
		if (usb_info != " "):
			if (usb_info.idVendor == "067b" and usb_info.idProduct == "2303"):
				cold_sensor_tty = usb_info.tty
				print("cold_sensor_tty -->" + cold_sensor_tty)
			else:
				print("arduino plugin error")
		if (cold_sensor_tty != ""):
			break
	try:
		cold_sensor = serial.Serial('/dev/' + cold_sensor_tty, 9600, timeout=1)
		time.sleep(2.5)
	except:
		cold_sensor = serial.Serial()
	time.sleep(1)

while(1):
	if(cold_sensor.is_open):
		response = cold_sensor.readline()
		response = response.decode('ascii')
		print(response)
		if (response != ""):
			print('------------------------------------------------------')
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
	else:
		arduino_connect()
