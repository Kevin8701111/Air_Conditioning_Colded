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

cold_swnsor = serial.Serial()

def arduino_connect():
    global cold_swnsor
    try:
        cold_swnsor = serial.Serial("COM8", 9600, timeout=1)
        time.sleep(2.5)
    except:
        print("arduino plugin error")
    time.sleep(1)

while(1):
    if(cold_swnsor.is_open):
        response = cold_swnsor.readline()
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
