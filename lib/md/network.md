# libbitcoin-network

libbitcoin-network is asynchronous networking for the Bitcoin peer-to-peer protocol and for client services: HTTP, WebSocket, JSON-RPC, TLS and ZeroMQ. It provides the connection lifecycle, the wire encodings and the threading model, and leaves the behavior of a node or server to the libraries that derive from its types.

## 1. The library

| | |
| - | - |
| Repository | [libbitcoin-network](https://github.com/libbitcoin/libbitcoin-network) |
| Depends on | [libbitcoin-system](system) |
| Used by | [libbitcoin-node](node) |
| Header | `<bitcoin/network.hpp>` |
| Namespace | `libbitcoin::network` |
| Package | `libbitcoin-network` (pkg-config) |
| License | [AGPL with a lesser clause](https://github.com/libbitcoin/libbitcoin-network/blob/master/COPYING) |

## 2. Status

| Gate | Expanded | Coverage |
| ---- | -------- | -------- |
| [![Gate](https://github.com/libbitcoin/libbitcoin-network/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-network/actions/workflows/ci.yml) | [![Expanded](https://github.com/libbitcoin/libbitcoin-network/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-network/actions/workflows/ci-expanded.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-network/master)](https://coveralls.io/github/libbitcoin/libbitcoin-network?branch=master) |

## 3. Documentation

- [Network Architecture](../architecture/network/index)
- [Using a library](../developers/index#2-using-a-library)
- [Building](../building/index)
