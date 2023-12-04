import socket
import sys
from struct import unpack
from time import sleep

def read(sock, host, port, run):
    # Create a UDP socket
    server_address = ("0.0.0.0", 22)
    sock.bind(server_address)
    try:
        voltage_list = []
        while (len(voltage_list) < 2):


            # Wait for message
            message, address = sock.recvfrom(1024)
            #voltage = unpack('!ff', message )
            #print(f"{voltage}")
            test = "Received voltage 2: 18.00:"
           # print(f"Received {message.decode()}\n")
            voltage = message.decode()
            voltage = voltage.split(":")
            voltage = float(voltage[1])
            voltage_list.append(voltage)

        sleep(0.1)
        return voltage_list, True
    except KeyboardInterrupt:
        sock.close()
        print(f"Sock server closing and game closing")
        return False, False
