"""
This was the final code used in the writing to the data, I
used multiprocessing to get all of my money's worth out of the raspberry pi
one core for one process,
two cores for recieving data and sending to socket at the same time for one sensor
"""


import serial
import multiprocessing
from struct import pack
import time
import socket

def read_serial(serial_port, output_queue):

    # read from serial port
    ser = serial.Serial(serial_port, baudrate=500000, timeout=1)
    try:
        while True:
            data = ser.readline().decode("utf-8").strip()
            # put in the output queue
            output_queue.put(data)
    except KeyboardInterrupt:
        ser.close()
        print(f"Closed serial port: {serial_port}")

def send_to_socket(output_queue, server_address):
    # open our socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        while True:
            # grab data from queue
            data = output_queue.get()
            # send data
            print(f"Sending data: {data}")
            message = pack('!H', float(data))
            sock.sendto(message, server_address)
    except KeyboardInterrupt:
        sock.close()
        print("Closed socket")

if __name__ == "__main__":
    serial_port1 = "/dev/ttyUSB0"
    serial_port2 = "/dev/ttyUSB1"
    server_address = ('10.245.193.9', 22)

    # START our multiprocessing
    queue1 = multiprocessing.Queue()
    queue2 = multiprocessing.Queue()

    process_serial1 = multiprocessing.Process(target=read_serial, args=(serial_port1, queue1))
    process_serial2 = multiprocessing.Process(target=read_serial, args=(serial_port2, queue2))
    process_socket1 = multiprocessing.Process(target=send_to_socket, args=(queue1, server_address))
    process_socket2 = multiprocessing.Process(target=send_to_socket, args=(queue2, server_address))

    process_serial1.start()
    process_serial2.start()
    process_socket1.start()
    process_socket2.start()
    # start our processes - wait for them to start at same time
    try:
        process_serial1.join()
        process_serial2.join()
        process_socket1.join()
        process_socket2.join()
    except KeyboardInterrupt:
        print("Processes finished")
