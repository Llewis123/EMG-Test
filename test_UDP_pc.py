#!/usr/bin/env python3
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import socket
import sys
from struct import unpack

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
host, port = '0.0.0.0', 22


print(f'Starting UDP server on {host} port {port}')
sock.bind(server_address)
fig, ax = plt.subplots()
line, = ax.plot([], [], label='Live Data')
# Set up the initialization function
def init():
    ax.set_xlim(0, 100)  # Set the x-axis limit
    ax.set_ylim(0, 100)  # Set the y-axis limit
    return line,

# Set up the update function
def update(frame):
    message, address = sock.recvfrom(1024)
    if message:
        # Wait for message

        voltage = message.decode()
        voltage = voltage.split(":")
        voltage = float(voltage[1])
        #voltage = unpack('!ff', message )
        #print(f"{voltage}")
        #test = "Received voltage 2: 18.00:"
        #print(f"Received {message.decode()}\n")
    return line,

# Create the animation
ani = FuncAnimation(fig, update, frames=range(100), init_func=init, blit=True)

# Show the plot
plt.show()
