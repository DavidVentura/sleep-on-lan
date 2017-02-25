#!/usr/bin/env python3
import socket
import sys

if len(sys.argv) != 2:
    print("Usage: 1 argument: MAC")
    sys.exit(1)

UDP_PORT = 9
MAC = sys.argv[1].replace(":", "")
MAC = MAC[::-1]  # Reverse the MAC address to create a 'sleep' packet

msg = 6 * "FF"
msg = msg + 16 * MAC
msg = bytes.fromhex(msg)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.sendto(msg, ('255.255.255.255', UDP_PORT))
