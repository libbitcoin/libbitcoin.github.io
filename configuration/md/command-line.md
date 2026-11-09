# Command Line

## 1. Options

All options, grouped by purpose:

| Group | Option | Purpose |
| ----- | ------ | ------- |
| Configuration | `-c`, `--config <path>` | Read settings from a configuration file |
| | `-n`, `--net <network>` | Select the network (`mainnet`, `testnet3`, `testnet4`, `testnet5`, `regtest` or `signet`), by default the configured `bitcoin.network` (`mainnet`) |
| Prompts | `-a`, `--accept` | Accept startup prompts without interaction |
| Information | `-h`, `--help` | Display command line options |
| | `-s`, `--settings` | Display the settings in effect, with their descriptions and defaults ([Displaying settings](file#2-displaying-settings)) |
| | `-v`, `--version` | Display version information |
| | `-w`, `--hardware` | Display hardware compatibility (CPU features, GPU) |
| Store | `-m`, `--make` | Create a new store in the configured directory, without running |
| | `-b`, `--backup` | Snapshot the store (also available live from the console) |
| | `-r`, `--restore` | Restore from the most recent snapshot |
| Service | `-d`, `--daemon <value>` | Install (`true`) or uninstall (`false`) as a daemon/service |
| | `-u`, `--user <credential>` | Daemon logon credential (defaults to the system account) |
| Store scans | `-i`, `--information` | Display store information |
| | `-f`, `--flags` | Display all fork flag transitions |
| | `-k`, `--buckets` | Display hashmap bucket fill |
| | `-l`, `--collisions` | Display hashmap collision statistics (time consuming) |

The store directory is named for the network (`mainnet`, `testnet4` and
so on). It is under the working directory, or under `database.path` when
that is configured: `path = bitcoin` puts the mainnet store in
`bitcoin/mainnet`. `bs` creates the store if it does not exist, and `-m`
creates it without running. Every run selects the network, by `-n` or by
`bitcoin.network` in a configuration file. Without either, `bs` uses the
`mainnet` store.

The log files and the peer address cache (`hosts.cache`) are written by default
to the working directory and are not separated by network, so run each
network from its own working directory.

The network can be set in the configuration file instead of by `-n`:

```ini
[bitcoin]
network = testnet4
```

```
$ bs --config bs.cfg
```

Display command line help:

```
$ bs -h

Usage: bs [-abfhiklmrsvw] [--config value] [--daemon value] [--net value]
[--user value]

Info: Runs a full node bitcoin server.

Options (named):

-a [--accept]        Accept startup prompts without interaction.
-b [--backup]        Backup to a snapshot (can also do live).
-c [--config]        Specify path to a configuration settings file.
-d [--daemon]        Install ('true') or uninstall ('false') as a daemon.
-f [--flags]         Scan and display all flag transitions.
-h [--help]          Display command line options.
-i [--information]   Scan and display store information.
-k [--buckets]       Scan and display hashmap bucket fill.
-l [--collisions]    Scan and show hashmap collision stats (may SIGKILL).
-m [--make]          Make new store in configured directory.
-n [--net]           Specify the network
                     (mainnet|testnet3|testnet4|regtest|signet|testnet5), defaults
                     to the configured network.
-r [--restore]       Restore from most recent snapshot.
-s [--settings]      Display all configuration settings.
-u [--user]          Daemon logon credential, defaults to system account.
-v [--version]       Display version information.
-w [--hardware]      Display hardware compatibility.
```

Display version information:

```
$ bs --version
Version Information...
secp256k1............ internal
tls.................. internal tls 1.3
libbitcoin-system.... 4.0.10444 8a3cb4da
libbitcoin-database.. 4.0.4814 167d381a
libbitcoin-network... 4.0.7428 dd3e7777
libbitcoin-node...... 4.0.4343 efadf0b5
libbitcoin-server.... 4.0.3513 71a3750f
compiled schema...... 4.0.29
```

Display hardware compatibility:

```
$ bs --hardware
Hardware configuration (x64)...
aesni....... platform:1 compiled:1.
vaes........ platform:1 compiled:1.
shani....... platform:1 compiled:1.
sha512...... platform:0 compiled:0.
sse41....... platform:1 compiled:1.
avx2........ platform:1 compiled:1.
avx512...... platform:1 compiled:1.
avxifma..... platform:0 compiled:0.
avx512ifma.. platform:1 compiled:1.
cuda........ platform:1 compiled:1.
cuda ecc.... platform:1 enabled:0.
```

`platform` shows whether the machine supports a feature and `compiled`
whether this build uses it. A build does not have to be compiled for the
hardware it runs on, though in many cases doing so significantly
improves performance. Do not compile options that the hardware does not
support, as the build will not run. The largest gains in initial block
download come from `shani` (or `sha2` on Arm), and otherwise from
`avx`.

CUDA (GPU) support is compiled by default, except on macOS. `cuda ecc`
reports whether the GPU's error correcting code (ECC) memory is enabled,
which is set in your own environment. ECC is recommended but not
required when using the GPU. When enabled it provides the same memory
reliability as the main processor (see
[GPU error correction](performance#gpu-error-correction)).

## 2. The running console

Commands typed into a running `bs` console (press `<enter>` after the character):

| Key | Action |
| --- | ------ |
| `m` | Menu of options and toggles |
| `c` | Close the node (graceful shutdown, same as `<ctrl> c`) |
| `b` | Backup the store (live snapshot) |
| `h` | Hold network communication |
| `g` | Go network communication |
| `i` | Info about the store |
| `e` | Errors in the store |
| `w` | Work distribution |
| `z` | Clear a disk-full condition (not required, automatically clears with sufficient space) |

Log on/off typed into a running `bs` console (press `<enter>` after the character):

| Key | Digit | Level |
| --- | ----- | ----- |
| `a` | `.0` | Application |
| `n` | `.1` | News: startup, progress and notable events |
| `s` | `.2` | Sessions: connect and accept |
| `p` | `.3` | Protocols |
| `x` | `.4` | Proxies: sockets and channels |
| `r` | `.5` | Remote peer behavior |
| `f` | `.6` | Own node fault |
| `q` | `.7` | Quitting: connections and other components stopping |
| `o` | `.8` | Objects: lifetime tracking (debug builds only) |
| `v` | `.9` | Verbose detail |

Each log entry shows its level as a digit after the timestamp, for
example `.6` on a fault.
