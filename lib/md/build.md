# libbitcoin-build

libbitcoin-build generates the build, CI and install files of the libbitcoin
repositories from one XML manifest, so that they stay consistent across the
three build systems (autotools, CMake and Visual Studio) and across the
repositories. It is a maintainer tool: everything it generates is committed
to each repository, so building a library or `bs` does not require it.

## 1. The tool

| | |
| - | - |
| Repository | [libbitcoin-build](https://github.com/libbitcoin/libbitcoin-build) |
| Generates for | [libbitcoin-system](system), [libbitcoin-database](database), [libbitcoin-network](network), [libbitcoin-node](node), [libbitcoin-server](server), [libbitcoin-explorer](explorer) |
| Manifest | `version4.xml` |
| Templates | [iMatix GSL](https://github.com/zeromq/gsl) |
| Run | `generate4.sh` (`generate4.cmd` on Windows) |
| License | [AGPL with a lesser clause](https://github.com/libbitcoin/libbitcoin-build/blob/master/COPYING) |

## 2. Status

| Gate |
| ---- |
| [![Gate](https://github.com/libbitcoin/libbitcoin-build/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-build/actions/workflows/ci.yml) |

## 3. Documentation

- [libbitcoin-build](../building/libbitcoin-build)
- [Build Architecture](../architecture/build/index)
- [Building](../building/index)
