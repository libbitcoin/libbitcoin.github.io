# Interfaces

`bs` serves each interface on its own port, with its own credentials and
certificates. The [interfaces page](../interfaces.html) shows the coverage
of every interface, and how each method compares with its reference
implementation. These pages document the methods of each interface:
how to call them, with examples and their responses.

| Interface | Section | Default port |
| --------- | ------- | ------------ |
| [Native REST](native) | `[native]` | 8180, secure 8143 |
| [Bitcoind REST](bitcoind-rest) | `[bitcoind]` | 8280, secure 8243 |

To enable an interface, and to secure it, see
[Configuration](../configuration/index).
