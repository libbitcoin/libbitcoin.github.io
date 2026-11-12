# libbitcoin-database

libbitcoin-database is the store. It holds the blockchain and unconfirmed transactions in memory-mapped tables, built from append-only bodies published by small heads, and provides the queries over them.

## 1. The library

| | |
| - | - |
| Repository | [libbitcoin-database](https://github.com/libbitcoin/libbitcoin-database) |
| Depends on | [libbitcoin-system](system) |
| Used by | [libbitcoin-node](node) |
| Header | `<bitcoin/database.hpp>` |
| Namespace | `libbitcoin::database` |
| Package | `libbitcoin-database` (pkg-config) |
| License | [AGPL with a lesser clause](https://github.com/libbitcoin/libbitcoin-database/blob/master/COPYING) |

## 2. Status

| Gate | Expanded | Coverage |
| ---- | -------- | -------- |
| [![Gate](https://github.com/libbitcoin/libbitcoin-database/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-database/actions/workflows/ci.yml) | [![Expanded](https://github.com/libbitcoin/libbitcoin-database/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-database/actions/workflows/ci-expanded.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-database/master)](https://coveralls.io/github/libbitcoin/libbitcoin-database?branch=master) |

## 3. Documentation

- [Database Architecture](../architecture/database/index)
- [Using a library](../developers/index#2-using-a-library)
- [Building](../building/index)
