# Interfaces

`bs` serves each interface on its own port, with its own credentials and
certificates. The [interfaces page](../interfaces.html) shows the coverage
of every interface, and how each method compares with its reference
implementation. These pages document the methods of each interface:
how to call them, with examples and their responses.

| Interface | Section | Port | Secure port | Protocols |
| --------- | ------- | ---- | ----------- | --------- |
| [Admin Console](admin) | `[admin]` | 8080 | 8043 | HTTP/S, WS/S |
| [Native REST](native) | `[native]` | 8180 | 8143 | HTTP/S, WS/S |
| [Electrum](electrum) | `[electrum]` | 8580 | 8543 | TCP/S, HTTP/S, WS/S |
| [Bitcoin P2P](p2p) | `[inbound]` | 8333 |  | P2P/S |
| [Bitcoind REST](bitcoind-rest) | `[bitcoind]` | 8280 | 8243 | HTTP/S |
| [Bitcoind ZMQ](zeromq) | `[bitcoind_zmq]` | 8380 | 8343 | ZMTP/S |
| [Esplora REST](esplora) | `[esplora]` | 8780 | 8743 | HTTP/S, WS/S |

Each interface reaches all of its protocols on one port, and their secure
forms (TLS, or CurveZMQ for ZMTPS) on another. P2P serves P2P and P2PS
(BIP324) on one port.

To enable an interface, and to secure it, see
[Configuration](../configuration/index).
