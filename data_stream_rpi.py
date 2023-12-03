#!/usr/bin/env python3

import socket
from struct import pack
import ray
import serial

HOST = "0.0.0.0"
PORT = 65000


def read(sock, server_address, bool):
    # will need to add the emg data here
    ray.shutdown()
    ray.init()
    # load our voltage using the
    voltage = ray.get([emg_one.remote(), emg_two.remote()])

    return voltage


@ray.remote
def emg_one(sock, server_address, bool):
    ser = serial.Serial("COM3", baudrate=500000, timeout=1)
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


@ray.remote
def emg_two(sock, server_address, bool):
    # TODO: Need to change the serial port here
    ser = serial.Serial("COM5", baudrate=500000, timeout=1)
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
