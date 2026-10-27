# Quick Start

From source to a synced node serving wallets and a block explorer.
Bitcoin Server (`bs`) is the libbitcoin server, and runs the same on Linux, macOS and
Windows.

## 1. Build

To use a published build instead, see [Download](../download/index), and
continue from §2.

On Linux or macOS, a release build installed under `~/libbitcoin`,
optimized for this machine:

```
$ git clone https://github.com/libbitcoin/libbitcoin-server
$ cd libbitcoin-server
$ ./builds/gnu/install-gnu.sh --prefix=$HOME/libbitcoin --build-boost --build-config=release --build-link=static --hardware-optimized
```

The result is `~/libbitcoin/bin/bs`. On Windows, see
[Building on Windows](../building/windows). For build choices, see
[Building](../building/index).

> **Portability:** a build with `--hardware-optimized` runs only on CPUs
> that have every instruction set extension of the machine it was built
> on. To build for other machines, omit it, and enable only the
> extensions they all have (see [Hardware options](../building/options#2-hardware-options)).

## 2. Sync

```
$ bs
```

With no configuration, `bs` syncs mainnet into a `bitcoin` store in the
current directory, creating it if it does not exist. Progress is logged
to the console. To stop, type `c` and `<enter>`, or press `<ctrl> c`. A
restart resumes where it stopped.

The time a sync takes and the space its store needs are shown on the
[Sync](../sync.html) and [Footprint](../footprint.html) pages.

## 3. Serve

Each interface is enabled by an address and a connection limit. This
configuration serves the admin console and the block explorer locally,
and Electrum wallets on the network:

```ini
[database]
path = bitcoin

[admin]
bind = 127.0.0.1:8080
connections = 10

[native]
bind = 127.0.0.1:8180
connections = 10

[electrum]
bind = 0.0.0.0:8580
connections = 100
```

```
$ bs --config bs.cfg
```

| Interface | Address |
| --------- | ------- |
| Admin console | `http://localhost:8080` in a browser |
| Block explorer | `http://localhost:8180` in a browser |
| Electrum, Sparrow | The server's address and port 8580, without SSL |

The admin console and the block explorer are available at once, and
show the sync's progress. The other interfaces accept connections once
the node is current.

## 4. Next

- [Configuration](../configuration/index): common setups, such as
  milestone sync, TLS, credentials and test networks.
- [Interfaces](../interfaces/index): every interface, its methods and
  examples.
- [Building](../building/index): platforms, build options and hardware
  optimizations.
