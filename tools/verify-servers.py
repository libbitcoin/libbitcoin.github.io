#!/usr/bin/env python3
"""Verify the community servers' P2P and ZMQ (clear and CurveZMQ) endpoints.

P2P passes when the peer answers a version message with its own version and a
verack on the network's magic. ZMQ passes when the ZMTP handshake completes;
a secure port is probed with the published server public key, so a wrong key
fails. Requires pyzmq with curve support. Exit status is the failure count.
"""

import hashlib
import os
import socket
import struct
import sys
import time

import zmq

HOSTS = {
    "wormer.libbitcoin.net": ">XrBaljAIXUrrCt(y^(i-@2mUY-4]lj=:DSoFWns",
    "carmine.libbitcoin.net": "ihZy(J.QWwNe(L9uUMyI8GH0<vW=kHJ9PLdBle8:",
}

# network: (magic, p2p port, zmq clear port, zmq secure port)
NETWORKS = {
    "mainnet": (3652501241, 8333, 8380, 8343),
    "testnet3": (118034699, 18333, 18380, 18343),
    "testnet4": (675223068, 48333, 48380, 48343),
    "testnet5": (1163282758, 18353, 58380, 58343),
}

TIMEOUT = 10
PROTOCOL = 70016


def checksum(payload):
    return hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]


def message(magic, command, payload=b""):
    return struct.pack("<I12sI", magic, command.encode(), len(payload)) + checksum(payload) + payload


def version_payload():
    address = struct.pack("<Q", 0) + bytes(10) + b"\xff\xff" + bytes(4) + struct.pack(">H", 0)
    agent = b"/verify-servers/"
    return (struct.pack("<iQq", PROTOCOL, 0, int(time.time())) + address + address +
            os.urandom(8) + bytes([len(agent)]) + agent + struct.pack("<i?", 0, False))


def receive(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise ConnectionError("closed by peer")
        data += chunk
    return data


def varint(data, offset):
    prefix = data[offset]
    if prefix < 0xfd:
        return prefix, offset + 1
    width = {0xfd: 2, 0xfe: 4, 0xff: 8}[prefix]
    return int.from_bytes(data[offset + 1:offset + 1 + width], "little"), offset + 1 + width


def probe_p2p(host, port, magic):
    with socket.create_connection((host, port), TIMEOUT) as sock:
        sock.settimeout(TIMEOUT)
        sock.sendall(message(magic, "version", version_payload()))
        detail, verack = None, False
        while detail is None or not verack:
            got, command, size, check = struct.unpack("<I12sI4s", receive(sock, 24))
            if got != magic:
                raise ValueError("magic %08x" % got)
            payload = receive(sock, size)
            if checksum(payload) != check:
                raise ValueError("bad checksum")
            command = command.rstrip(b"\0").decode()
            if command == "version":
                protocol = struct.unpack_from("<i", payload)[0]
                length, offset = varint(payload, 80)
                agent = payload[offset:offset + length].decode(errors="replace")
                height = struct.unpack_from("<i", payload, offset + length)[0]
                detail = "%s protocol %d height %d" % (agent, protocol, height)
                sock.sendall(message(magic, "verack"))
            elif command == "verack":
                verack = True
        return detail


def probe_zmq(context, host, port, server_key=None):
    sock = context.socket(zmq.SUB)
    sock.setsockopt(zmq.LINGER, 0)
    if server_key:
        public, secret = zmq.curve_keypair()
        sock.curve_publickey = public
        sock.curve_secretkey = secret
        sock.curve_serverkey = server_key.encode()
    monitor = sock.get_monitor_socket(zmq.EVENT_ALL)
    try:
        sock.connect("tcp://%s:%d" % (host, port))
        deadline = time.time() + TIMEOUT
        while time.time() < deadline:
            if not monitor.poll(250):
                continue
            event = zmq.utils.monitor.recv_monitor_message(monitor)["event"]
            if event == zmq.EVENT_HANDSHAKE_SUCCEEDED:
                return "handshake"
            if event in (zmq.EVENT_HANDSHAKE_FAILED_PROTOCOL, zmq.EVENT_HANDSHAKE_FAILED_AUTH,
                         zmq.EVENT_HANDSHAKE_FAILED_NO_DETAIL):
                raise ValueError("handshake failed (%s)" % zmq.Event(event).name)
        raise TimeoutError("no handshake")
    finally:
        sock.disable_monitor()
        monitor.close()
        sock.close()


def main():
    import zmq.utils.monitor  # noqa: F401
    if not zmq.has("curve"):
        sys.exit("pyzmq lacks curve support")
    context = zmq.Context()
    failures = 0
    for host, key in HOSTS.items():
        for network, (magic, p2p, clear, secure) in NETWORKS.items():
            probes = [
                ("p2p", p2p, lambda: probe_p2p(host, p2p, magic)),
                ("zmq clear", clear, lambda: probe_zmq(context, host, clear)),
                ("zmq secure", secure, lambda: probe_zmq(context, host, secure, key)),
            ]
            for name, port, probe in probes:
                try:
                    result = "ok    " + probe()
                except Exception as error:
                    result = "FAIL  %s" % (error or type(error).__name__)
                    failures += 1
                print("%-24s %-9s %-11s %5d  %s" % (host, network, name, port, result), flush=True)
    context.term()
    sys.exit(failures)


if __name__ == "__main__":
    main()
