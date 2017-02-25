#!/usr/bin/env python3

import socket
import platform
from subprocess import check_output, Popen

INVALID = "INVALID"
WAKE = "WAKE"
SLEEP = "SLEEP"
OTHERS = "OTHERS"


def parse_magic_packet(packet):
    frame = packet[0:6].hex()
    macs = set()
    for _ in range(0, 16):
        packet = packet[6:]
        mac = packet[:6].hex()
        macs.add(mac)

    if frame != "ff"*6 or len(macs) != 1:
        return INVALID

    mac = list(macs)[0].lower()
    if mac in MACS:
        return WAKE

    if mac[::-1] in MACS:
        return SLEEP

    return OTHERS


def get_windows_macs():
    import re
    out = check_output(["ipconfig", "/all"]).decode("ascii").split("\n")
    match_mac = r"\s(?P<mac>[0-9a-f-]{17})\s"
    ret = []
    for line in out:
        matches = re.search(match_mac, line, flags=re.IGNORECASE)
        if matches:
            ret.append(matches.group("mac").replace("-", "").lower())
    return ret


def get_linux_macs():
    import netifaces
    ret = []
    ifaces = netifaces.interfaces()
    ifaces.remove('lo')
    for i in ifaces:
        addresses = netifaces.ifaddresses(i)[netifaces.AF_LINK]
        ret.append(addresses[0]['addr'].replace(":", "")).lower()
    return ret


def get_macs():
    if platform.system() == 'Windows':
        return get_windows_macs()
    else:
        return get_linux_macs()


def suspend():
    if platform.system() == 'Windows':
        Popen(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
    else:
        Popen(["systemctl", "suspend"])


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 9))
MACS = get_macs()

while True:
    msg, addr = sock.recvfrom(1024)
    res = parse_magic_packet(msg)
    print(res)
    if res == "SLEEP":
        suspend()
