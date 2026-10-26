# Bitcoind ZMQ

The bitcoind ZMQ interface is a drop-in for the ZeroMQ notifications of
bitcoind, published on the `[bitcoind_zmq]` binding (default port 8380).
Any ZeroMQ `SUB` socket can subscribe.

## 1. Topics

| Topic | Body | Published for |
| ----- | ---- | ------------- |
| [`hashblock`](#hashblock) | Block hash | Each confirmed block |
| [`hashtx`](#hashtx) | Transaction hash | Each transaction of a confirmed or disconnected block, and each pool transaction |
| [`rawblock`](#rawblock) | Block | Each confirmed block |
| [`rawtx`](#rawtx) | Transaction | Each transaction of a confirmed or disconnected block, and each pool transaction |
| [`sequence`](#sequence) | Hash and event | Each confirmed or disconnected block, and each pool transaction |

## 2. Calling pattern

### 2.1 Enabling

The service starts only with both an address and a connection limit:

```ini
[bitcoind_zmq]
bind = 127.0.0.1:8380
bind = [::1]:8380
connections = 10
```

Notifications begin once the node is current. Before that, connections
are refused while `node.delay_inbound` is set (the default).

### 2.2 Subscribing

Every topic is published on every address of the binding, so one socket
can subscribe to any of them. bitcoind instead binds an address for each
topic, set by its `-zmqpub` options.

A subscription is a topic prefix. The empty prefix subscribes to every
topic, and `raw` to both `rawblock` and `rawtx`. Topics with no
subscription are not sent. Cancelling a prefix stops every topic it
matches, even one also matched by another subscription.

`bitcoind_zmq.maximum_subscriptions` (default 100) limits the subscribe
commands of one connection. Each counts, and each cancel releases one.
Exceeding it closes the connection.

### 2.3 Messages

Each notification is a message of three frames:

| Frame | Content |
| ----- | ------- |
| 1 | The topic, such as `hashblock` |
| 2 | The body |
| 3 | The sequence number, 4 bytes, little-endian |

Each topic has its own sequence number on each connection. It starts at 0
when the connection subscribes, and increases by one for each message of
that topic.

```python
import zmq

socket = zmq.Context().socket(zmq.SUB)
socket.connect("tcp://localhost:8380")
socket.setsockopt(zmq.SUBSCRIBE, b"hashblock")

while True:
    topic, body, sequence = socket.recv_multipart()
    print(topic.decode(), body.hex(), int.from_bytes(sequence, "little"))
```

```
hashblock 00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048 0
hashblock 000000006a625f06636b8bb6ac7b960a8d03705d1ace08b1a19da3fdcc99ddbd 1
```

### 2.4 Backlog

`bitcoind_zmq.maximum_backlog` (default 32 MB) bounds the notifications
waiting to be sent to one connection. A notification that does not fit is
dropped, and the connection is kept. A drop leaves a gap in that topic's
sequence numbers, which is how a subscriber detects it.

### 2.5 CurveZMQ

The `safe` addresses (default port 8343) use CurveZMQ, enabled by the
server's secret key:

```ini
[bitcoind_zmq]
safe = 127.0.0.1:8343
key = <server secret key, Z85>
cert = <client public key, Z85>
connections = 10
```

Generate a key pair with any CurveZMQ tool, such as
`zmq.curve_keypair()` in Python, set the secret key as `key`, and give
clients the public key. Each `cert` authorizes one client public key, and
with no `cert` any client is allowed. The configuration parser reads `#`
as a comment, so use a key that does not contain it.

```python
import zmq

socket = zmq.Context().socket(zmq.SUB)
socket.curve_serverkey = b"<server public key>"
socket.curve_publickey, socket.curve_secretkey = zmq.curve_keypair()
socket.connect("tcp://localhost:8343")
socket.setsockopt(zmq.SUBSCRIBE, b"")
```

A client whose key is not listed is refused with a ZAP status of 400, as
in libzmq. The `bind` addresses never use CurveZMQ.

## 3. Blocks

### hashblock

The hash of each block added to the confirmed chain, 32 bytes, in the
usual reversed (display) order.

```
hashblock 00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048 0
```

Disconnected blocks are not published here (see [`sequence`](#sequence)).

### rawblock

Each block added to the confirmed chain, in wire format with witness
data.

Disconnected blocks are not published here.

## 4. Transactions

### hashtx

The hash of each transaction, 32 bytes, in the usual reversed (display)
order, published for:

- each transaction of a block added to the confirmed chain, before the
  block's `hashblock`;
- each transaction of a block removed from the confirmed chain;
- each transaction accepted to the memory pool.

A transaction of a removed block that returns to the pool is published
again as a pool transaction.

### rawtx

Each transaction, in wire format with witness data, published for the
same events as [`hashtx`](#hashtx).

## 5. Sequence

### sequence

Changes to the confirmed chain and the memory pool, in one ordered
stream. The body is a hash, in the usual reversed (display) order,
followed by a label:

| Label | Event | Body |
| ----- | ----- | ---- |
| `C` | Block added to the confirmed chain | Block hash, `C` (33 bytes) |
| `D` | Block removed from the confirmed chain | Block hash, `D` (33 bytes) |
| `A` | Transaction accepted to the memory pool | Transaction hash, `A`, pool sequence (41 bytes) |
| `R` | Transaction removed from the memory pool | Transaction hash, `R`, pool sequence (41 bytes) |

bitcoind sends `R` for a transaction removed from its pool for a reason
other than confirmation, such as eviction, expiry, replacement or a
confirmed conflict. `bs` does not evict, expire or replace transactions,
so the only removal `R` covers is a transaction made unconfirmable by a
confirmed conflict, for which `R` is not yet sent.

The pool sequence is 8 bytes, little-endian. It counts the `A`
notifications of the connection, and is not bitcoind's
`mempool_sequence`.

In a reorganization, each removed block is published with `D` from the
top down, then each added block with `C` from the fork up.
