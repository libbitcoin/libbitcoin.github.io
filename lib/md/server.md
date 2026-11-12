# libbitcoin-server

libbitcoin-server extends the full node with client interfaces: native REST, Electrum, bitcoind JSON-RPC and REST, ZeroMQ and others, each a network service that queries the store and pushes notifications from chain events. It builds **Bitcoin Server** (`bs`).

## 1. The library

| | |
| - | - |
| Repository | [libbitcoin-server](https://github.com/libbitcoin/libbitcoin-server) |
| Depends on | [libbitcoin-node](node) |
| Used by | `bs` (Bitcoin Server) |
| Header | `<bitcoin/server.hpp>` |
| Namespace | `libbitcoin::server` |
| Package | `libbitcoin-server` (pkg-config) |
| License | [AGPL with a lesser clause](https://github.com/libbitcoin/libbitcoin-server/blob/master/COPYING) |

## 2. Status

| Gate | Expanded | Coverage |
| ---- | -------- | -------- |
| [![Gate](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/ci.yml) | [![Expanded](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/ci-expanded.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-server/master)](https://coveralls.io/github/libbitcoin/libbitcoin-server?branch=master) |

## 3. Documentation

- [Server Architecture](../architecture/server/index)
- [Download BS](../download/index) and [Quick Start](../start/index)
- [BS Interfaces](../interfaces/index)
- [Configuration](../configuration/index)
- [Using a library](../developers/index#2-using-a-library)
- [Building](../building/index)
