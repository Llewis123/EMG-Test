#!/usr/bin/env python3

import multiprocessing as mp
import socket
from struct import pack

import serial

HOST = "10.245.193.9"
PORT = 22




def emg_one(sock, server_address, bool):
    ser = serial.Serial("/dev/ttyUSB0", baudrate=500000, timeout=1)
    try:
        while bool:
            # read our emg_voltage
            voltage = ser.readline().decode("utf-8").strip()
            # print for testing
            print(f" Recieved: {voltage}")
            message = pack("3f", voltage)
            sock.sendto(message, server_address)

    except KeyboardInterrupt:
        # close serial
        ser.close()
        print("Closed serial port")



def emg_two(sock, server_address, bool):
    # TODO: Need to change the serial port here
    ser = serial.Serial("/dev/ttyUSB1", baudrate=500000, timeout=1)
    try:
        while bool:
            # read our emg_voltage
            voltage = ser.readline().decode("utf-8").strip()
            # print for testing
            print(f" Recieved: {voltage}")
            message = pack("3f", voltage)
            sock.sendto(message, server_address)

    except KeyboardInterrupt:
        # close serial
        ser.close()
        print("Closed serial port")


def read(sock, server_address, bool):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (HOST, PORT)
    # will need to add the emg data here
    voltage1 = mp.Process(target=emg_one(), args=(sock,server_address,True))
    voltage2 = mp.Process(target=emg_two(), args=(sock,server_address,True))
    # load our voltage using the
    voltage1.start()
    voltage2.start()

    voltage1.join()
    voltage2.join()
    print(f"Processes finished")

    return 0

