"""
Serial communication to write graphs
Packet example: 'a007z'
    where a is the servo id
    007 is the servo position
    z is the end of packet signal
"""

import serial
import time

arduino_port = '/dev/cu.usbmodem1421'
ser = serial.Serial(arduino_port, 9600)

i = 0
while i < 5:
    # Get some graph data here

    # Convert the graph data to servo mapping here

    # Write a servo position packet to the Arduino
    ser.write('a')
    ser.write('1')
    ser.write('2')
    ser.write('7')
    ser.write('z')
    time.sleep(3)
    i+=1

ser.close()
