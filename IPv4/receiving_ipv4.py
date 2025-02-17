import socket
import struct
import os

HOST = ""  # Listen on all available interfaces
PORT = 5007  # Port to receive data
MULTICAST_IP = "224.1.1.1"  # Multicast group address
CHUNK_SIZE = 1024  # Size of each chunk in bytes

# Create a UDP IPv4 socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Allow address reuse
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the specified port
sock.bind((HOST, PORT))

# Join the multicast group
mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_IP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print(f"Listening for messages on {PORT}...")

total_received = 0
file_path = "received_file_ipv4"

with open(file_path, 'wb') as f:
    while True:
        data, addr = sock.recvfrom(CHUNK_SIZE)

        if data == b"END":
            print(f"Received END message from {addr}")
            sock.sendto(b"FINISH", addr)
            break

        f.write(data)
        total_received += len(data)
        print(f"Received chunk from {addr}, total received: {total_received} bytes")

print(f"File received successfully: {file_path}, Total size: {total_received} bytes")
