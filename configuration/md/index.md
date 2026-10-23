# bs Configuration

This page is an outline in progress. Section headings are the page
structure; bullets are what each section will cover; code blocks are
candidate examples. Open questions are collected at the end.

---

## 1. Quick start

- `bs` runs with built-in mainnet defaults; no configuration file is read
  unless `--config` is given.
- First run: create the store, then start.

```sh
bs --newstore          # create a new store in ./bitcoin
bs                     # run with defaults
```

- With a configuration file:

```sh
bs --config bs.cfg --newstore
bs --config bs.cfg
```

---

## 2. Command line

All options, grouped by purpose (from `bs --help`):

| Group | Option | Purpose |
| ----- | ------ | ------- |
| Configuration | `-c`, `--config <path>` | Read settings from a configuration file |
| Prompts | `-a`, `--accept` | Accept startup prompts without interaction |
| Information | `-h`, `--help` | Display command line options |
| | `-s`, `--settings` | Display all configuration settings (with any `--config` applied) |
| | `-v`, `--version` | Display version information |
| | `-w`, `--hardware` | Display hardware compatibility (CPU features, GPU) |
| Store | `-n`, `--newstore` | Create a new store in the configured directory |
| | `-b`, `--backup` | Snapshot the store (also available live from the console) |
| | `-r`, `--restore` | Restore from the most recent snapshot |
| Service | `-d`, `--daemon <value>` | Install (`true`) or uninstall (`false`) as a daemon/service |
| | `-u`, `--user <credential>` | Daemon logon credential (defaults to the system account) |
| Store scans | `-i`, `--information` | Display store information |
| | `-f`, `--flags` | Display all fork flag transitions |
| | `-k`, `--buckets` | Display hashmap bucket fill |
| | `-l`, `--collisions` | Display hashmap collision statistics (time consuming) |

Examples to include:

```sh
bs -c bs.cfg -s | less     # check what a config file actually sets
bs -c bs.cfg -w            # will this machine use the GPU / SIMD paths?
bs -c bs.cfg -b            # snapshot a stopped store
bs -c bs.cfg -r            # recover after an unclean shutdown
bs -c bs.cfg -i            # store sizes and table information
bs -c bs.cfg -d true       # install as a service
```

- Note that every action option takes the same `--config`, since the
  store location comes from `[database] path`.

---

## 3. The running console

- Keys typed into a running `bs` (press `m` for the menu):

| Key | Action |
| --- | ------ |
| `m` | Menu of options and toggles |
| `c` | Close the node (graceful shutdown; same as Ctrl-C) |
| `b` | Backup the store (live snapshot) |
| `h` / `g` | Hold / go network communication |
| `i` | Info about the store |
| `e` | Errors in the store |
| `w` | Work distribution |
| `z` | Zeroize a disk-full error (after freeing space) |

- Log toggles at runtime: `a`pplication, `n`ews, `s`ession, `p`rotocol,
  `x` proxy, `r`emote, `f`ault, `q`uitting, `o`bjects, `v`erbose.
- Shutdown: after "== shutdown ==" the process waits at "Press <enter>
  to exit".

---

## 4. The configuration file

- Format: INI style, `[section]` headers, `name = value`, `#` comments.
- Multi-valued settings repeat the line (`bind`, `safe`, `seed`, `peer`,
  `checkpoint`, `credential`, `blacklist`, `whitelist`, `host`, `origin`).
- Command line options are not settings; settings are only in the file.
- Section map:

| Area | Sections |
| ---- | -------- |
| Logging | `[log]` |
| Store | `[database]`, `[table.*]` |
| Chain | `[bitcoin]`, `[forks]`, `[wallet]` |
| Node | `[node]` |
| Peer network | `[network]`, `[peer]`, `[outbound]`, `[inbound]`, `[manual]` |
| Client services | `[admin]`, `[native]`, `[bitcoind]`, `[bitcoind_zmq]`, `[btcd]`, `[electrum]`, `[sparrow]`, `[esplora]`, `[stratum_v1]`, `[stratum_v2]` |

- Most users touch `[log]`, `[database]`, `[node]` and one or two service
  sections; `[bitcoin]`, `[forks]` and `[table.*]` are left at defaults.

Minimal file:

```ini
[database]
path = /data/bitcoin

[log]
path = /data/log
```

---

## 5. Common setups

Each a short paragraph and a config fragment.

### 5.1 Sync to a height and stop

```ini
[node]
maximum_height = 900000
```

- `bs` idles at the stop height with the store open; close with `c`.

### 5.2 Milestone sync

- What `[bitcoin] milestone` does (bypass script validation up to a
  trusted block) and that the default milestone is 950,000.

```ini
[bitcoin]
milestone = 000000000000000000010b93c9ea1c29fea277383f0f7d1f26de8b5802e885ff:950000
```

### 5.3 Electrum server

```ini
[electrum]
bind = 0.0.0.0:50001
safe = 0.0.0.0:50002
connections = 100
cert_path = /etc/bs/server.pem
key_path = /etc/bs/server.key
```

### 5.4 bitcoind-compatible RPC

```ini
[bitcoind]
bind = 127.0.0.1:8332
connections = 10
credential = user:password
```

### 5.5 ZMQ notifications

```ini
[bitcoind_zmq]
bind = 127.0.0.1:28332
connections = 10
```

### 5.6 Esplora REST

### 5.7 Admin and native web pages

### 5.8 Client filters (BIP157/158)

```ini
[node]
provide_filters = true

[table.filter_bk]
buckets = ...

[table.filter_tx]
buckets = ...
```

### 5.9 Silent payments

```ini
[node]
silent_start_height = 709632
```

### 5.10 Privacy networks

- Outbound over Tor (`[outbound] socks`), inbound over I2P
  (`[inbound] sam`, `key_path`), address gossip (`[peer] gossip_tor`,
  `gossip_i2p`), opportunistic encryption (`[node] provide_privacy`).

### 5.11 Fixed peers

```ini
[manual]
peer = 192.168.0.10:8333
peer = 192.168.0.11:8333

[outbound]
connections = 0
```

### 5.12 Without the address index

```ini
[table.outs]
buckets = 0
```

---

## 6. Settings shared by every service

- One table of the settings every client service section has, with what
  each does: `bind`, `safe` (TLS), `connections` (0 = disabled),
  `cert_path` / `key_path` / `key_pass` / `cert_auth`, `credential`,
  `host`, `origin`, `allow_opaque_origin`, `inactivity_minutes`,
  `expiration_minutes`, `connect_timeout_seconds`, `rate_limit`,
  `maximum_request`, `maximum_backlog`, `minimum_buffer`,
  `maximum_buffer`.
- The rule: a service is off until it has a `bind` (or `safe`) and a
  nonzero `connections`.
- `node.delay_inbound`: client services (except admin and native) do not
  accept connections until the chain is current.

---

## 7. Performance settings

- `[node] threads`, `thread_priority`, `memory_priority`.
- `[node] use_gpu`, `batch_verify`, `batch_silent`, `cpu_batch_verify`,
  `cpu_batch_silent`; check with `bs -w`.
- `[node] maximum_concurrency` (download window).
- `[database] turbo`.
- `[outbound] connections` during sync, `current_connections` after.

---

## 8. Store table sizing (`[table.*]`)

- Each table has `buckets`, `expected`, `size`, `rate`. Defaults are
  sized for mainnet at 950,000 blocks; derived values are shown by
  `bs --settings`.
- When to change them: disabling the address index, enabling filters,
  testnet or regtest, a smaller disk.
- `bs -k` / `bs -l` to check bucket fill and collisions on an existing
  store.

---

## 9. Reference

- Link to (or embed) the full `bs --settings` output, every setting with
  its description and default, grouped by section.

---

## Open questions

1. **Other chains.** There is no testnet/regtest switch; the parser is
   built with mainnet defaults (`console/main.cpp:113`). Is the intended
   usage a full set of `[bitcoin]`/`[forks]`/`[wallet]`/`[peer]`
   overrides (descriptions say "use … for testnet")? If so, ship sample
   files per chain?
2. **Relative paths.** Are `[database] path`, `[log] path` and other
   paths relative to the working directory or the config file?
3. **Daemon on Linux/macOS.** `--daemon` is implemented for Windows
   services; the source has TODOs for systemd and launchd. Document as
   Windows-only for now, with a sample systemd unit for Linux?
4. **Environment variable.** Loading the config path from the
   environment is commented out (`src/parser.cpp:2726`). Leave
   undocumented?
5. **Existing docs.** `docs/configuration.md` and `data/bs.cfg` in the
   server repo use old section names (`[web]`, `[explore]`,
   `[socket]`). Replace them with this page, or point them here?
6. **Ports.** The commented-out default binds in `src/parser.cpp:98-109`
   use 8080–8680. Use those ports in the examples, or the conventional
   ones (50001/50002 Electrum, 8332 RPC, 28332 ZMQ)?
7. **Filter table sizing.** What bucket counts to recommend for
   `[table.filter_bk]` and `[table.filter_tx]` when enabling filters?
8. **Where it lives.** A single page (`configuration.html`) under a
   "Server" menu item, or a section with one page per area?
