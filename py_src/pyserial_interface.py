"""
Serial communication to write graphs
Packet example: 'a007z'
    where a is the servo id
    007 is the servo position
    z is the end of packet signal
"""

import serial
import time
import csv
from numpy import interp

class GraphTranslator:

    def __init__(self, arduino_port, servo_range):
        self.s = serial.Serial(arduino_port, 9600)
        self.servo_range = servo_range

    def readGraphCSV(self, file_name):
        graph = [[], [], []]
        
        try:
            with open(file_name, 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    graph[0].append(int(row[0]))
                    graph[1].append(int(row[1]))
                    graph[2].append(int(row[2]))
        except IOError as e:
            print("Error reading file: " + str(e))
    
        print('Loaded graph: ')
        print(graph)
        return graph

    def convertGraphToServoPositions(self, graph):
        converted_graph = [[], [], []]
        a_range = [min(graph[1]), max(graph[1])]
        print(a_range)
        b_range = [min(graph[2]), max(graph[2])]
        print(b_range)        

        for value in graph[1]:
            converted_graph[1].append(interp(value, a_range, self.servo_range))
        for value in graph[2]:
            converted_graph[2].append(interp(value, b_range, self.servo_range))
       
        print('Converted graph: ')
        print(converted_graph) 
        return converted_graph    

    def writeGraphToArduino(self, converted_graph):
        for x in range(0, len(graph[0])):
            self.writePacketToArduino('a', converted_graph[1][x])
            self.writePacketToArduino('b', converted_graph[2][x])
            time.sleep(5)

    def writePacketToArduino(self, motor, position):
        print ('Writing motor ' + motor + ' to ' + str(position))
        
        # Convert the position int
        position = str(position)
        while len(position) < 3:
            position = '0' + position
    
        self.s.write(motor)
        self.s.write(position[0])
        self.s.write(position[1])
        self.s.write(position[2])
        self.s.write('z')
    
    def shutDown(self):
        self.s.close()

if __name__ == '__main__':
    arduino_port = '/dev/cu.usbmodem1421'
    servo_range = [0, 90]
    terminate = False
    gt = GraphTranslator(arduino_port, servo_range)

    while terminate == False:
        instruction = raw_input('Enter csv file name or \'exit\':  ')
        if instruction == 'exit':
            gt.shutDown()
            terminate = True
        else:
            graph = gt.readGraphCSV(instruction)
            servo_mapped_graph = gt.convertGraphToServoPositions(graph)
            gt.writeGraphToArduino(servo_mapped_graph)
