import socket
import sys
from struct import unpack


def read(sock, host, port, bool):
    # bind socket to port
    print(f"Starting UDP server on {host} port {port}")
    server_address = (host, port)
    sock.bind(server_address)

    while bool:
        message, address = sock.recvfrom(4096)
        voltage = unpack("3f", message)
        print(f" Recieved {len(message)} bytes \n Voltage: {voltage}")
        return voltage
