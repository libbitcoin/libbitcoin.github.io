# Build status

The current status of the libbitcoin builds, tests, releases and packages.
Builds is the number of jobs in each workflow's build matrices.

## 1. Continuous integration

The gate builds and tests each repository on every push and pull request,
across its platforms and build systems, and reports test coverage to
[Coveralls](https://coveralls.io/github/libbitcoin).
Across all repositories, a run builds libbitcoin-system 120 times,
libbitcoin-database 60, libbitcoin-network 80, libbitcoin-node 40,
libbitcoin-server 20, and libbitcoin-explorer 20. Tests are run only for
the last repository in each build.

| Workflow | Trigger |
| -------- | ------- |
| Continuous Integration (`ci.yml`) | Push, pull request or manual |

| Repository | Status | Coverage | Libraries | Builds |
| ---------- | ------ | -------- | --------: | -----: |
| [libbitcoin-system](https://github.com/libbitcoin/libbitcoin-system) | [![Gate](https://github.com/libbitcoin/libbitcoin-system/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-system/actions/workflows/ci.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-system/master)](https://coveralls.io/github/libbitcoin/libbitcoin-system?branch=master) | 1 | 20 |
| [libbitcoin-database](https://github.com/libbitcoin/libbitcoin-database) | [![Gate](https://github.com/libbitcoin/libbitcoin-database/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-database/actions/workflows/ci.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-database/master)](https://coveralls.io/github/libbitcoin/libbitcoin-database?branch=master) | 2 | 20 |
| [libbitcoin-network](https://github.com/libbitcoin/libbitcoin-network) | [![Gate](https://github.com/libbitcoin/libbitcoin-network/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-network/actions/workflows/ci.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-network/master)](https://coveralls.io/github/libbitcoin/libbitcoin-network?branch=master) | 2 | 20 |
| [libbitcoin-node](https://github.com/libbitcoin/libbitcoin-node) | [![Gate](https://github.com/libbitcoin/libbitcoin-node/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-node/actions/workflows/ci.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-node/master)](https://coveralls.io/github/libbitcoin/libbitcoin-node?branch=master) | 4 | 20 |
| [libbitcoin-server](https://github.com/libbitcoin/libbitcoin-server) | [![Gate](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/ci.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-server/master)](https://coveralls.io/github/libbitcoin/libbitcoin-server?branch=master) | 5 | 20 |
| [libbitcoin-explorer](https://github.com/libbitcoin/libbitcoin-explorer) | [![Gate](https://github.com/libbitcoin/libbitcoin-explorer/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-explorer/actions/workflows/ci.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-explorer/master)](https://coveralls.io/github/libbitcoin/libbitcoin-explorer?branch=master) | 3 | 20 |
| [libbitcoin-build](https://github.com/libbitcoin/libbitcoin-build) | [![Gate](https://github.com/libbitcoin/libbitcoin-build/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-build/actions/workflows/ci.yml) | |  | 2 |

See [Test Architecture](../architecture/test/index).

## 2. Expanded continuous integration

The expanded matrix is run on demand. It covers every compiler in all
combinations of debug or release and static or shared, and adds the
constant-time and cross-architecture tests. libbitcoin-system and
libbitcoin-explorer each run 4 additional constant-time test builds.
Across all repositories, a run builds libbitcoin-system 674 times,
libbitcoin-database 333, libbitcoin-network 448, libbitcoin-node 222,
libbitcoin-server 111, and libbitcoin-explorer 115. Tests are run only for
the last repository in each build.

| Workflow | Trigger |
| -------- | ------- |
| Expanded Continuous Integration (`ci-expanded.yml`) | Manual |

| Repository | Status | Libraries | Builds |
| ---------- | ------ | --------: | -----: |
| [libbitcoin-system](https://github.com/libbitcoin/libbitcoin-system) | [![Expanded](https://github.com/libbitcoin/libbitcoin-system/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-system/actions/workflows/ci-expanded.yml) | 1 | 115 |
| [libbitcoin-database](https://github.com/libbitcoin/libbitcoin-database) | [![Expanded](https://github.com/libbitcoin/libbitcoin-database/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-database/actions/workflows/ci-expanded.yml) | 2 | 111 |
| [libbitcoin-network](https://github.com/libbitcoin/libbitcoin-network) | [![Expanded](https://github.com/libbitcoin/libbitcoin-network/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-network/actions/workflows/ci-expanded.yml) | 2 | 111 |
| [libbitcoin-node](https://github.com/libbitcoin/libbitcoin-node) | [![Expanded](https://github.com/libbitcoin/libbitcoin-node/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-node/actions/workflows/ci-expanded.yml) | 4 | 111 |
| [libbitcoin-server](https://github.com/libbitcoin/libbitcoin-server) | [![Expanded](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/ci-expanded.yml) | 5 | 111 |
| [libbitcoin-explorer](https://github.com/libbitcoin/libbitcoin-explorer) | [![Expanded](https://github.com/libbitcoin/libbitcoin-explorer/actions/workflows/ci-expanded.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-explorer/actions/workflows/ci-expanded.yml) | 3 | 115 |
| [libbitcoin-build](https://github.com/libbitcoin/libbitcoin-build) | | | |

## 3. Releases

The release workflow builds, from the version tags, `bs` (libbitcoin-server
and the four libraries it depends on) and `selector` (built on
libbitcoin-system). It builds each target twice and compares the results,
then signs the files and publishes them as a draft release. Builds counts
both builds of each target, and the toolchain and SDK jobs.

| Workflow | Status | Libraries | Builds |
| -------- | ------ | --------: | -----: |
| Release Build (`manual-release.yml`) | [![Release Build](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/manual-release.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/manual-release.yml) | 5 | 98 |

See [Release builds](../architecture/build/release) and
[Deterministic builds](../architecture/build/deterministic).

## 4. Packaging

The packaging workflow packages the signed builds of a published release
for each package manager, as a container image and as node platform apps.
The image is pushed to the container registry and the other packages are
attached to the release.

| Workflow | Status | Builds |
| -------- | ------ | -----: |
| Package Release (`package-release.yml`) | [![Package Release](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/package-release.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/package-release.yml) | 6 |

See [Packaging](../architecture/build/packaging).

## 5. Deployment

The distribution workflow submits the packages of a published release to
their distribution repositories. Latest shows the version each one
currently offers.

| Workflow | Status |
| -------- | ------ |
| Distribute Release (`distribute.yml`) | [![Distribute Release](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/distribute.yml/badge.svg)](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/distribute.yml) |

| Package | Latest | Distribution |
| ------- | ------ | ------------ |
| Docker image | [![Docker](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fgithub.com%2Flibbitcoin%2Flibbitcoin-server%2Fpkgs%2Fcontainer%2Flibbitcoin-server&search=%5C%3Ftag%3D%28%5Cd%5B%5E%22%5D%2A%29%22&replace=%241&label=ghcr)](https://github.com/libbitcoin/libbitcoin-server/pkgs/container/libbitcoin-server) | `ghcr.io` |
| deb | [![apt](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fraw.githubusercontent.com%2Flibbitcoin%2Fapt%2Fmain%2Fdists%2Fstable%2Fmain%2Fbinary-amd64%2FPackages&search=Version%3A%20%28%5CS%2B%29&replace=%241&label=apt)](https://github.com/libbitcoin/apt) | apt repository |
| Homebrew formula | [![Homebrew](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fraw.githubusercontent.com%2Flibbitcoin%2Fhomebrew-tap%2Fmain%2FFormula%2Flibbitcoin-server.rb&search=version%20%22%28%5B%5E%22%5D%2B%29%22&replace=%241&label=tap)](https://github.com/libbitcoin/homebrew-tap) | tap |
| winget | [![winget](https://img.shields.io/winget/v/Libbitcoin.Server)](https://github.com/microsoft/winget-pkgs/tree/master/manifests/l/Libbitcoin/Server) | `winget-pkgs` |
| Umbrel app | [![Umbrel](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fgetumbrel%2Fumbrel-apps%2Fmaster%2Fbitcoin-server%2Fumbrel-app.yml&query=%24.version&label=umbrel)](https://github.com/getumbrel/umbrel-apps/tree/master/bitcoin-server) | app store |
| StartOS package | [![StartOS](https://img.shields.io/badge/startos-resource%20not%20found-red)](https://marketplace.start9.com/?id=bitcoin-server) | registry |

See [Distribution](../architecture/build/packaging#4-distribution).

<style>
.scroller table { table-layout: fixed; width: 100%; }
.scroller th { box-sizing: border-box; }
.scroller th:first-child { width: 43%; }
.scroller th:nth-child(2):not(:last-child) { width: 34%; }
.scroller th:nth-child(2):nth-last-child(4) { width: 22%; }
</style>
