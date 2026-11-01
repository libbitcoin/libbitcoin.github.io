# Packages

There are three ways to get Bitcoin Server (`bs`):

| Way | From | See |
| --- | ---- | --- |
| Package | A package manager, which installs and updates `bs` | §1 |
| Download | A signed build from the libbitcoin-server releases page | [Download BS](../download/index) |
| Build | The source, built on the machine that runs it, or for others | [Quick Start](../start/index), [Building](../building/index) |

## 1. Package managers

| Manager | Platform | Install |
| ------- | -------- | ------- |
| apt (deb) | Linux x64, arm64 | `sudo apt install ./libbitcoin-server_<version>_<arch>.deb` |
| Homebrew | macOS x64, arm64 | `brew install --formula ./libbitcoin-server.rb` |
| winget | Windows x64, arm64 | `winget install --manifest <directory of the manifests>`, or run the installer |
| Docker | Linux x64, arm64 | `docker run -v <data directory>:/data -p 8333:8333 -p 8080:8080 -p 8180:8180 ghcr.io/libbitcoin/libbitcoin-server:<version>` |
| Umbrel | umbrelOS x64, arm64 | Install the `bitcoin-server` app |
| StartOS | StartOS 0.4 x64, arm64 | Sideload `bitcoin-server` (`.s9pk`) |

The deb, the formula, the winget manifests, the Windows installers, the
Umbrel app and the StartOS packages are assets of each release, and the
image is in the GitHub container registry. The deb, the Windows installer
and the image use the best variant of `bs` the processor supports
([Packaging](../architecture/build/packaging)).
