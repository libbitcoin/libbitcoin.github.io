# Interfaces

`bs` serves each interface on its own port, with its own credentials and
certificates. The [interfaces page](../interfaces.html) shows the coverage
of every interface, and how each method compares with its reference
implementation. These pages document the methods of each interface:
how to call them, with examples and their responses.

| Interface | Section | Default port |
| --------- | ------- | ------------ |
| [Admin Console](admin) | `[admin]` | 8080, secure 8043 |
| [Native REST](native) | `[native]` | 8180, secure 8143 |
| [Bitcoin P2P](p2p) | `[inbound]`, `[outbound]`, `[manual]` | 8333 |
| [Bitcoind REST](bitcoind-rest) | `[bitcoind]` | 8280, secure 8243 |
| [Bitcoind ZMQ](zeromq) | `[bitcoind_zmq]` | 8380, secure 8343 |
| [Esplora REST](esplora) | `[esplora]` | 8780, secure 8743 |

To enable an interface, and to secure it, see
[Configuration](../configuration/index).
