import socket
import time
import os
import struct

# IPv6 Configuration
PORT = 5007
CHUNK_SIZE = 1024  # Size of each chunk in bytes
MULTICAST_IPV6 = "ff02::1234"
INTERFACE_NAME = "eth0"  # Replace with your actual interface name
INTERFACE_INDEX = socket.if_nametoindex(INTERFACE_NAME)

def send_file(target_ip, file_path, mode="Unicast"):
    file_size = os.path.getsize(file_path)
    total_sent = 0
    start_time = time.time()  # Start time when file sending begins
    
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
        # Configure socket options for multicast if needed
        if mode == "Multicast":
            sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 2)  # TTL = 2
            sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_IF, INTERFACE_INDEX)
        
        # Send the file in chunks
        with open(file_path, 'rb') as f:
            while chunk := f.read(CHUNK_SIZE):
                sock.sendto(chunk, (target_ip, PORT))
                total_sent += len(chunk)
            print(f"Sent {total_sent}/{file_size} bytes")
        
        # Send an END message to indicate file transmission is complete
        sock.sendto(b"END", (target_ip, PORT))
        print("Sent END message")
        
        # Wait for FINISH response(s)
        sock.settimeout(10)
        finish_received_count = 0
        last_finish_time = 0  # Variable to track the time of the last FINISH response
        
        # Check for MULTICAST/ANYCAST responses
        if mode == "Unicast":
            # Expect only one FINISH response
            try:
                while True:
                    response, addr = sock.recvfrom(CHUNK_SIZE)
                    if response == b"FINISH":
                        elapsed = time.time() - start_time
                        print(f"Received FINISH message from {addr} after {elapsed * 1000:.3f} ms")
                        last_finish_time = elapsed  # Update last_finish_time with the latest FINISH response time
                        break
            except socket.timeout:
                print("Timeout waiting for FINISH message")
        else:
            # For Multicast or Anycast, expect multiple FINISH responses until timeout
            try:
                while True:
                    response, addr = sock.recvfrom(CHUNK_SIZE)
                    if response == b"FINISH":
                        elapsed = time.time() - start_time
                        print(f"Received FINISH message from {addr} after {elapsed * 1000:.3f} ms")
                        last_finish_time = elapsed  # Update last_finish_time with the latest FINISH response time
                        finish_received_count += 1
            except socket.timeout:
                print(f"Timeout waiting for FINISH messages, received {finish_received_count} responses")
        
        # Calculate the total duration using the last FINISH message received
        finish_time = time.time()  # Time when the last FINISH message was received
        duration = last_finish_time  # Use the time of the last FINISH message to calculate the duration
        
        # Calculate bandwidth
        bandwidth = total_sent / duration
        
        print("\n======== RESULT ========")
        print(f"File sent to {target_ip}:{PORT}")
        print(f"Total size: {file_size} bytes")
        print(f"Duration (latency): {duration * 1000:.3f} ms")  # Duration should be the latency to the last FINISH message
        print(f"Bandwidth: {bandwidth:.2f} bytes/second")
        print("========================\n")

def send_unicast():
    target_ip = input("Enter target IPv6 address: ").strip()
    file_path = input("Enter file path to send (Unicast): ").strip()
    send_file(target_ip, file_path, "Unicast")

def send_multicast():
    file_path = input("Enter file path to send (Multicast): ").strip()
    send_file(MULTICAST_IPV6, file_path, "Multicast")

def send_anycast():
    target_ip = input("Enter Anycast IPv6 address (simulated using Unicast): ").strip()
    file_path = input("Enter file path to send (Anycast): ").strip()
    send_file(target_ip, file_path, "Anycast")

# Menu for selecting the sending mode
while True:
    print("\n--- Select Sending Mode ---")
    print("1. Unicast (Enter destination IPv6 address)")
    print("2. Multicast (Send to a group of devices)")
    print("3. Anycast (Simulated using Unicast)")
    print("4. Exit")
    
    choice = input("Choose (1/2/3/4): ").strip()
    if choice == "1":
        send_unicast()
    elif choice == "2":
        send_multicast()
    elif choice == "3":
        send_anycast()
    elif choice == "4":
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please try again!")
