# Build status

The current status of the libbitcoin builds, tests, releases and packages.

## 1. Continuous integration

| Repository | Gate | Expanded | Coverage |
| ---------- | ---- | -------- | -------- |
| [libbitcoin-system](https://github.com/libbitcoin/libbitcoin-system) | [![Gate](https://github.com/libbitcoin/libbitcoin-system/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-system/actions/workflows/ci.yml) | [![Expanded](https://github.com/libbitcoin/libbitcoin-system/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-system/actions/workflows/ci-expanded.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-system/master)](https://coveralls.io/github/libbitcoin/libbitcoin-system?branch=master) |
| [libbitcoin-database](https://github.com/libbitcoin/libbitcoin-database) | [![Gate](https://github.com/libbitcoin/libbitcoin-database/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-database/actions/workflows/ci.yml) | [![Expanded](https://github.com/libbitcoin/libbitcoin-database/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-database/actions/workflows/ci-expanded.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-database/master)](https://coveralls.io/github/libbitcoin/libbitcoin-database?branch=master) |
| [libbitcoin-network](https://github.com/libbitcoin/libbitcoin-network) | [![Gate](https://github.com/libbitcoin/libbitcoin-network/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-network/actions/workflows/ci.yml) | [![Expanded](https://github.com/libbitcoin/libbitcoin-network/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-network/actions/workflows/ci-expanded.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-network/master)](https://coveralls.io/github/libbitcoin/libbitcoin-network?branch=master) |
| [libbitcoin-node](https://github.com/libbitcoin/libbitcoin-node) | [![Gate](https://github.com/libbitcoin/libbitcoin-node/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-node/actions/workflows/ci.yml) | [![Expanded](https://github.com/libbitcoin/libbitcoin-node/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-node/actions/workflows/ci-expanded.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-node/master)](https://coveralls.io/github/libbitcoin/libbitcoin-node?branch=master) |
| [libbitcoin-server](https://github.com/libbitcoin/libbitcoin-server) | [![Gate](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/ci.yml) | [![Expanded](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/ci-expanded.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-server/master)](https://coveralls.io/github/libbitcoin/libbitcoin-server?branch=master) |
| [libbitcoin-explorer](https://github.com/libbitcoin/libbitcoin-explorer) | [![Gate](https://github.com/libbitcoin/libbitcoin-explorer/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-explorer/actions/workflows/ci.yml) | [![Expanded](https://github.com/libbitcoin/libbitcoin-explorer/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-explorer/actions/workflows/ci-expanded.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-explorer/master)](https://coveralls.io/github/libbitcoin/libbitcoin-explorer?branch=master) |
| [libbitcoin-build](https://github.com/libbitcoin/libbitcoin-build) | [![Gate](https://github.com/libbitcoin/libbitcoin-build/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-build/actions/workflows/ci.yml) | | |

See [Test Architecture](../architecture/test/index).

## 2. Releases

| Workflow | Status |
| -------- | ------ |
| Release Build (`manual-release.yml`) | [![Release Build](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/manual-release.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/manual-release.yml) |

See [Release builds](../architecture/build/release) and
[Deterministic builds](../architecture/build/deterministic).

## 3. Packaging

| Workflow | Status |
| -------- | ------ |
| Package Release (`package-release.yml`) | [![Package Release](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/package-release.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/package-release.yml) |

| Package | Distribution | Latest |
| ------- | ------------ | ------ |
| deb | apt repository | |
| Homebrew formula | tap | [![Homebrew](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fraw.githubusercontent.com%2Flibbitcoin%2Fhomebrew-tap%2Fmain%2FFormula%2Flibbitcoin-server.rb&search=version%20%22%28%5B%5E%22%5D%2B%29%22&replace=%241&label=tap)](https://github.com/libbitcoin/homebrew-tap) |
| winget | `winget-pkgs` | [![winget](https://img.shields.io/winget/v/Libbitcoin.Server)](https://github.com/microsoft/winget-pkgs/tree/master/manifests/l/Libbitcoin/Server) |
| Docker image | `ghcr.io` | |
| Umbrel app | app store | [![Umbrel](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fgetumbrel%2Fumbrel-apps%2Fmaster%2Fbitcoin-server%2Fumbrel-app.yml&query=%24.version&label=umbrel)](https://github.com/getumbrel/umbrel-apps/tree/master/bitcoin-server) |
| StartOS package | registry | |

See [Packaging](../architecture/build/packaging).
