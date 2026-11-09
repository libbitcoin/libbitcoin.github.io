# Configuration File

## 1. The configuration file

Paths take the platform's form, for example `/data/bitcoin` or
`D:\bitcoin`. A relative path is relative to the working directory,
not to the configuration file.

Integer values may use commas as thousands separators, for example
`node.maximum_height = 900,000`.

Section map:

| Area | Sections |
| ---- | -------- |
| Logging | `[log]` |
| Store | `[database]`, `[table.*]` |
| Chain | `[bitcoin]`, `[forks]`, `[wallet]` |
| Node | `[node]` |
| P2P network | `[network]`, `[peer]`, `[outbound]`, `[inbound]`, `[manual]` |
| Client-server | `[admin]`, `[native]`, `[bitcoind]`, `[bitcoind_zmq]`, `[btcd]`, `[electrum]`, `[sparrow]`, `[esplora]` |

Simple example config file:

```ini
[database]
path = bitcoin

[log]
path = log
```

The same settings can be written without section headers, by prefixing
each name with its section:

```ini
database.path = bitcoin
log.path = log
```

## 2. Displaying settings

`bs -s` (`--settings`) prints every setting with the value in effect for
that run, each under its section and preceded by its description and
default. The values are the selected network's defaults, the values
derived from them (such as table bucket counts, [Bucket autotuning](store#2-bucket-autotuning)),
and any configured value, which is marked `# configured`. Combine it with
`-c` to see what a configuration file does, and with `-n` to see a
network's values:

```
$ bs -c bs.cfg -s
```

```ini
[node]
# Maximum block height to populate, defaults to '0' (unlimited).
maximum_height = 900000 # configured

[table.header]
# The number of buckets in the header table head, derived from expected and memory, defaults to '385181'.
buckets = 385181
```

A setting with no value, such as an unset list, is printed commented out.
Settings captured by an existing store ([Settings fixed at store creation](store#3-settings-fixed-at-store-creation))
are shown as configured; the store's values replace them when the store
opens.
