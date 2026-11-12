# libbitcoin-explorer

libbitcoin-explorer is the library of **Bitcoin Explorer** (`bx`), a command line tool built directly on libbitcoin-system. Each command is generated from one model that declares its name, options, arguments, configuration settings and help text.

## 1. The library

| | |
| - | - |
| Repository | [libbitcoin-explorer](https://github.com/libbitcoin/libbitcoin-explorer) |
| Depends on | [libbitcoin-system](system) |
| Used by | `bx` (Bitcoin Explorer) |
| Header | `<bitcoin/explorer.hpp>` |
| Namespace | `libbitcoin::explorer` |
| Package | `libbitcoin-explorer` (pkg-config) |
| License | [AGPL with a lesser clause](https://github.com/libbitcoin/libbitcoin-explorer/blob/master/COPYING) |

## 2. Status

| Gate | Expanded | Coverage |
| ---- | -------- | -------- |
| [![Gate](https://github.com/libbitcoin/libbitcoin-explorer/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-explorer/actions/workflows/ci.yml) | [![Expanded](https://github.com/libbitcoin/libbitcoin-explorer/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-explorer/actions/workflows/ci-expanded.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-explorer/master)](https://coveralls.io/github/libbitcoin/libbitcoin-explorer?branch=master) |

## 3. Documentation

- [Explorer Architecture](../architecture/explorer/index)
- [BX Commands](../client/commands) and [BX Settings](../configuration/bx)
- [Using a library](../developers/index#2-using-a-library)
- [Building](../building/index)
