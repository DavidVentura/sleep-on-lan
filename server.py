#!/usr/bin/env python3
import socket
import myutil
from multiprocessing import Process


def handle_data(data):
    print(data)
    if data == "SLEEP":
        # myutil.suspend()
        pass


def listen_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 9))
    while True:
        msg, _ = sock.recvfrom(1024)
        res = myutil.parse_magic_packet(msg)
        handle_data(res)


def listen_tcp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 7777))
    sock.listen(1)
    while True:
        conn, _ = sock.accept()
        data = conn.recv(4096)
        if not data:
            continue
        data = data.decode("utf-8").split("\r\n")
        path = data[0].split(" ")[1].lstrip("/")
        conn.send(b"HTTP/1.1 200 OK\n\n\n")
        conn.close()
        handle_data(path)


if __name__ == '__main__':
    p = Process(target=listen_udp)
    p.start()
    q = Process(target=listen_tcp)
    q.start()
    p.join()
    q.join()
