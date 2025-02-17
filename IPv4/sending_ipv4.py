import socket
import time
import os

# Configure Broadcast, Multicast addresses and port
PORT = 5007
CHUNK_SIZE = 1024  # Size of each chunk in bytes
MULTICAST_IP = "224.1.1.1"
BROADCAST_IP = "10.12.1.255"

def send_file(target_ip, file_path, mode="Unicast"):
    file_size = os.path.getsize(file_path)
    total_sent = 0
    start_time = time.time()
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        
        if mode == "Broadcast":
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        with open(file_path, 'rb') as f:
            while chunk := f.read(CHUNK_SIZE):
                sock.sendto(chunk, (target_ip, PORT))
                total_sent += len(chunk)
            print(f"Sent {total_sent}/{file_size} bytes")
        
        end_bytes = b"END"
        sock.sendto(end_bytes, (target_ip, PORT))
        print("Sent END message")
        sock.settimeout(20)

    # Wait for the "FINISH" message back
        finish_received_time = None
        try:
            if mode == "Unicast":
                sock.settimeout(10)
                while True:
                    response, addr = sock.recvfrom(CHUNK_SIZE)
                    if response == b"FINISH":
                        print(f"Received FINISH message from {addr}")
                        break
    
            if mode == "Multicast":
                while True:
                    try:
                        response, addr = sock.recvfrom(CHUNK_SIZE)
                        if response == b"FINISH":
                            finish_received_time = time.time()
                            print(f"Received FINISH message from {addr} after {(finish_received_time - start_time) * 1000:.3f} ms")
                    except socket.timeout:
                        print("Timeout waiting for more FINISH messages")
                        break
    
            if mode == "Broadcast":
                while True:
                    try:
                        response, addr = sock.recvfrom(CHUNK_SIZE)
                        if response == b"FINISH":
                            finish_received_time = time.time()
                            print(f"Received FINISH message from {addr} after {(finish_received_time - start_time) * 1000:.3f} ms")
                    except socket.timeout:
                        print("Timeout waiting for more FINISH messages")
                        break
        except socket.timeout:
            print("Timeout waiting for FINISH message")
    
    end_time = time.time()
    if mode == "Multicast" or mode == "Broadcast":
        end_time = finish_received_time
    duration = end_time - start_time
    bandwidth = total_sent / duration
    print("\n======== RESULT ========")
    print(f"File sent to {target_ip}:{PORT}")
    print(f"Total size: {file_size} bytes")
    print(f"Duration as latency: {duration * 1000:.3f} ms")
    print(f"Bandwidth: {bandwidth:.2f} bytes/second")
    print("========================\n")

def send_unicast():
    target_ip = input("Enter target IPv4 address: ").strip()
    file_path = input("Enter file path to send (Unicast): ").strip()
    send_file(target_ip, file_path, "Unicast")

def send_multicast():
    file_path = input("Enter file path to send (Multicast): ").strip()
    send_file(MULTICAST_IP, file_path, "Multicast")

def send_broadcast():
    file_path = input("Enter file path to send (Broadcast): ").strip()
    send_file(BROADCAST_IP, file_path, "Broadcast")

# Menu for selecting the sending mode
while True:
    print("\n--- Select Sending Mode ---")
    print("1. Unicast (Enter destination IP address)")
    print("2. Multicast (Send to a group of devices)")
    print("3. Broadcast (Send to the entire network)")
    print("4. Exit")

    choice = input("Choose (1/2/3/4): ").strip()

    if choice == "1":
        send_unicast()
    elif choice == "2":
        send_multicast()
    elif choice == "3":
        send_broadcast()
    elif choice == "4":
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please try again!")