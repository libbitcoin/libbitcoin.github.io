# Build status

The current status of the libbitcoin builds, tests, releases and packages.

## 1. Continuous integration

The current master of each repository: the check-in gate (`ci.yml`), the
expanded matrix (`ci-expanded.yml`) and line coverage
([Test Architecture](../architecture/test/index)).

| Repository | Gate | Expanded | Coverage |
| ---------- | ---- | -------- | -------- |
| [libbitcoin-system](https://github.com/libbitcoin/libbitcoin-system) | [![Gate](https://github.com/libbitcoin/libbitcoin-system/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-system/actions/workflows/ci.yml) | [![Expanded](https://github.com/libbitcoin/libbitcoin-system/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-system/actions/workflows/ci-expanded.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-system/master)](https://coveralls.io/github/libbitcoin/libbitcoin-system?branch=master) |
| [libbitcoin-database](https://github.com/libbitcoin/libbitcoin-database) | [![Gate](https://github.com/libbitcoin/libbitcoin-database/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-database/actions/workflows/ci.yml) | [![Expanded](https://github.com/libbitcoin/libbitcoin-database/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-database/actions/workflows/ci-expanded.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-database/master)](https://coveralls.io/github/libbitcoin/libbitcoin-database?branch=master) |
| [libbitcoin-network](https://github.com/libbitcoin/libbitcoin-network) | [![Gate](https://github.com/libbitcoin/libbitcoin-network/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-network/actions/workflows/ci.yml) | [![Expanded](https://github.com/libbitcoin/libbitcoin-network/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-network/actions/workflows/ci-expanded.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-network/master)](https://coveralls.io/github/libbitcoin/libbitcoin-network?branch=master) |
| [libbitcoin-node](https://github.com/libbitcoin/libbitcoin-node) | [![Gate](https://github.com/libbitcoin/libbitcoin-node/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-node/actions/workflows/ci.yml) | [![Expanded](https://github.com/libbitcoin/libbitcoin-node/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-node/actions/workflows/ci-expanded.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-node/master)](https://coveralls.io/github/libbitcoin/libbitcoin-node?branch=master) |
| [libbitcoin-server](https://github.com/libbitcoin/libbitcoin-server) | [![Gate](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/ci.yml) | [![Expanded](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/ci-expanded.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-server/master)](https://coveralls.io/github/libbitcoin/libbitcoin-server?branch=master) |
| [libbitcoin-explorer](https://github.com/libbitcoin/libbitcoin-explorer) | [![Gate](https://github.com/libbitcoin/libbitcoin-explorer/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-explorer/actions/workflows/ci.yml) | [![Expanded](https://github.com/libbitcoin/libbitcoin-explorer/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-explorer/actions/workflows/ci-expanded.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-explorer/master)](https://coveralls.io/github/libbitcoin/libbitcoin-explorer?branch=master) |
| [libbitcoin-build](https://github.com/libbitcoin/libbitcoin-build) | [![Gate](https://github.com/libbitcoin/libbitcoin-build/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-build/actions/workflows/ci.yml) | | |

## 2. Release builds

| Workflow | Status |
| -------- | ------ |
| Release Build (`manual-release.yml`) | [![Release Build](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/manual-release.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/manual-release.yml) |
| Latest release | [![Release](https://img.shields.io/github/v/release/libbitcoin/libbitcoin-server?include_prereleases)](https://github.com/libbitcoin/libbitcoin-server/releases) |

| Platform | Architecture | Builds | Status |
| -------- | ------------ | ------ | ------ |
| Linux | x64 | baseline, shani, avxifma, avx512ifma | ✔ |
| Linux | arm64 | baseline, crypto, sha3 | ✔ |
| Linux (musl) | x64 | baseline, shani, avxifma, avx512ifma | ✔ |
| Linux (musl) | arm64 | baseline, crypto, sha3 | WIP |
| macOS | x64, arm64 | one per architecture | ✔ |
| Windows | x64 | baseline, shani, avxifma, avx512ifma | ✔ |
| Windows | arm64 | baseline, crypto, sha3 | ✔ |

See [Release builds](../architecture/build/release).

## 3. Packages

| Workflow | Status |
| -------- | ------ |
| Package Release (`package-release.yml`) | [![Package Release](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/package-release.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/package-release.yml) |

| Package | Built | Distribution |
| ------- | ----- | ------------ |
| deb | ✔ | WIP (apt repository) |
| Homebrew formula | ✔ | WIP (tap) |
| winget | ✔ | WIP (`winget-pkgs`) |
| Docker image | ✔ | ✔ (`ghcr.io`) |
| Umbrel app | ✔ | WIP (app store) |
| StartOS package | ✔ | WIP (registry) |

See [Packaging](../architecture/build/packaging).

## 4. Reproducible builds

| Method | Libbitcoin | Bitcoin Core |
| ------ | ---------- | ------------ |
| Double Build (two independent builders) | WIP (`bs-linux-x64`, `selector-linux-x64`) | No target |
| Guix | WIP (Linux, macOS, Windows) | ✔ (Linux, macOS, Windows) |

See [Deterministic builds](../architecture/build/deterministic).

## 5. Notes

- ✔: in place and working.
- WIP: being added.
- No target: no documented process.

Badges show the most recent run of each workflow.
