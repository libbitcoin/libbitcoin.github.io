# libbitcoin-node

The node combines network and store, to download, validate, and index the blockchain and unconfirmed transactions. Blocks are downloaded and validated concurrently, while a sequence of chasers advances the chain in order.

## 1. The library

| | |
| - | - |
| Repository | [libbitcoin-node](https://github.com/libbitcoin/libbitcoin-node) |
| Depends on | [libbitcoin-database](database), [libbitcoin-network](network) |
| Used by | [libbitcoin-server](server) |
| Header | `<bitcoin/node.hpp>` |
| Namespace | `libbitcoin::node` |
| Package | `libbitcoin-node` (pkg-config) |
| License | [AGPL with a lesser clause](https://github.com/libbitcoin/libbitcoin-node/blob/master/COPYING) |

## 2. Status

| Gate | Expanded | Coverage |
| ---- | -------- | -------- |
| [![Gate](https://github.com/libbitcoin/libbitcoin-node/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-node/actions/workflows/ci.yml) | [![Expanded](https://github.com/libbitcoin/libbitcoin-node/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-node/actions/workflows/ci-expanded.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-node/master)](https://coveralls.io/github/libbitcoin/libbitcoin-node?branch=master) |

## 3. Documentation

- [Node Architecture](../architecture/node/index)
- [Using a library](../developers/index#2-using-a-library)
- [Building](../building/index)
