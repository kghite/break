"""
Serial communication to write graphs
"""

import serial
import time

arduino_port = '/dev/cu.usbmodem1421'
ser = serial.Serial(arduino_port, 9600)

i = 0
while i < 5:
    # Get some graph data here

    # Convert the graph data to servo mapping here

    # Write to the Arduino
    ser.write('5') # Test
    time.sleep(3)
    i+=1

ser.close()
