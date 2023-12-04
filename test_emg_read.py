import socket
from struct import unpack

def receive_data(sock):
    while True:
        data, _ = sock.recvfrom(1024)
        value = unpack('!HH', data)
        print(f"Received data: {data.decode()}")

if __name__ == "__main__":
    server_address = ('0.0.0.0', 22)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)

    try:
        receive_data(sock)
    except KeyboardInterrupt:
        sock.close()
        print("Closed socket server")
