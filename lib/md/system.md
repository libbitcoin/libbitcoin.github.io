# libbitcoin-system

libbitcoin-system is the base of the stack. It has no dependency other than the C++20 standard library, and every other library builds on it. It implements Bitcoin's primitives and rules: blocks, transactions, scripts and their execution, its own hash functions and cryptography, keys, addresses and wallets, and encodings and serialization.

## 1. The library

| | |
| - | - |
| Repository | [libbitcoin-system](https://github.com/libbitcoin/libbitcoin-system) |
| Depends on | the C++20 standard library |
| Used by | [libbitcoin-database](database), [libbitcoin-network](network), [libbitcoin-node](node), [libbitcoin-server](server), [libbitcoin-explorer](explorer) |
| Header | `<bitcoin/system.hpp>` |
| Namespace | `libbitcoin::system` |
| Package | `libbitcoin-system` (pkg-config) |
| License | [AGPL with a lesser clause](https://github.com/libbitcoin/libbitcoin-system/blob/master/COPYING) |

## 2. Status

| Gate | Expanded | Coverage |
| ---- | -------- | -------- |
| [![Gate](https://github.com/libbitcoin/libbitcoin-system/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-system/actions/workflows/ci.yml) | [![Expanded](https://github.com/libbitcoin/libbitcoin-system/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-system/actions/workflows/ci-expanded.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-system/master)](https://coveralls.io/github/libbitcoin/libbitcoin-system?branch=master) |

## 3. Documentation

- [System Architecture](../architecture/system/index)
- [Using a library](../developers/index#2-using-a-library)
- [Building](../building/index)
