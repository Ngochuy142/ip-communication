import socket
import struct
import os

MULTICAST_IPV6 = "ff02::1234"
PORT = 5007
INTERFACE_NAME = "eth0"
INTERFACE_INDEX = socket.if_nametoindex(INTERFACE_NAME)
CHUNK_SIZE = 1024  # Size of each chunk in bytes

# Create a UDP IPv6 socket
sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Allow port reuse
try:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
except AttributeError:
    print("SO_REUSEPORT is not available on this system.")

# Bind the socket to receive data (accepting both Multicast and Unicast)
sock.bind(("", PORT))

# Join the Multicast group
group = socket.inet_pton(socket.AF_INET6, MULTICAST_IPV6)
mreq = group + struct.pack("@I", INTERFACE_INDEX)
sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

print(f"Listening for messages on {PORT}...")

total_received = 0
file_path = "received_file_ipv6"
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