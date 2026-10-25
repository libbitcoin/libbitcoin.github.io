# bs Configuration

## 1. Quick start

The executable is `bs` (`bs.exe` on Windows), and the examples run the
same on Linux, macOS and Windows. `bs` runs with built-in mainnet
defaults. No configuration file is read unless `--config` is given.

Run with defaults. The store is created in a `bitcoin` directory under
the current directory if it does not exist.

```
$ bs
```

With a configuration file:

```
$ bs --config bs.cfg
```

---

## 2. Command line

All options, grouped by purpose:

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

Display command line help:

```
$ bs -h

Usage: bs [-abfhiklnrsvw] [--config value] [--daemon value] [--user
value]

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
-n [--newstore]      Create new store in configured directory.
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
boost................ 1.91.0
secp256k1............ internal
openssl (tls)........ internal tls 1.3
libbitcoin-system.... 4.0.10255 63f7b348
libbitcoin-database.. 4.0.4703 10e63cfe
libbitcoin-network... 4.0.7306 1feceb44
libbitcoin-node...... 4.0.4262 74e460da
libbitcoin-server.... 4.0.3334 996bec9f
compiled schema...... 4.0.16
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
download come from `shani` (or `crypto` on Arm), and otherwise from
`avx`.

CUDA (GPU) support is compiled by default, except on macOS. `cuda ecc`
reports whether the GPU's error correcting code (ECC) memory is enabled,
which is set in your own environment. ECC is recommended but not
required when using the GPU. When enabled it provides the same memory
reliability as the main processor.

---

## 3. The running console

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

---

## 4. The configuration file

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

---

## 5. Common setups

### 5.1 Sync to a height and stop

```ini
[node]
maximum_height = 900,000
```

`bs` will not download a block above that height.

### 5.2 Milestone sync

A milestone is a block you have previously validated and therefore know
to be valid, which implies that all preceding blocks are valid. A
milestone sync verifies the identity of the milestone block and all of
its ancestors, and validates the blocks above it. The default milestone
is block 950,000. The milestone and pruning are fixed when the store is
created (§10).

```ini
[bitcoin]
milestone = 000000000000000000010b93c9ea1c29fea277383f0f7d1f26de8b5802e885ff:950000
```

Pruning reduces download and store size under a milestone sync. With
`node.limited_blocks`, blocks under the milestone are downloaded and stored
without their input scripts and witnesses, and the node serves only
blocks above the milestone to peers.

```ini
[node]
limited_blocks = true
```

### 5.3 Full validation

To validate every block, set the milestone to the genesis block when
creating the store (§10):

```ini
[bitcoin]
milestone = 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f:0
```

### 5.4 Checkpoints

Checkpoints are consensus checks, and removing them is a hard fork.
However, to do so set a checkpoint to the genesis block:

```ini
[bitcoin]
checkpoint = 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f:0
```

### 5.5 Admin site

`bs` serves its own administrative site, which also utilizes its native
REST interface. Here both are limited to the local machine:

```ini
[admin]
bind = 127.0.0.1:8080
bind = [::1]:8080
connections = 10

[native]
bind = 127.0.0.1:8180
bind = [::1]:8180
connections = 10
```

To view the admin site open `http://localhost:8080` in a browser. Its pages
are admin REST queries rendered as HTML, the default for a browser request.
The same paths return data when JSON is requested, with `format=json` or an
`Accept: application/json` header.

To serve a custom admin site from a directory instead of the embedded site,
set `admin.path`. A request for `/` returns `admin.default`
(`index.html`).

The admin interface is libbitcoin's own, and provides:

- HTTP and websocket on each port. Over a websocket, each frame is one
  request path, and `log_subscribe` and `event_subscribe` stream the
  node's log and events.
- TLS on its `safe` addresses (§7.2), with optional client certificates.
- Credentials (§7.3), restricted by REST method names.

### 5.6 Block explorer

The native REST interface serves the block explorer. Here it is limited
to the local machine:

```ini
[native]
bind = 127.0.0.1:8180
bind = [::1]:8180
connections = 10
```

To view the block explorer open `http://localhost:8180` in a browser.

The explorer is the native REST interface rendered as HTML, the default for a
browser request. The same paths return each result in any of four formats,
chosen with `format=` or the `Accept` header:

| Format | Media type | Result |
| ------ | ---------- | ------ |
| `html` | `text/html` | The explorer page |
| `json` | `application/json` | JSON |
| `text` | `text/plain` | Hex encoded bytes |
| `data` | `application/octet-stream` | Raw bytes |

For example, the genesis block header as JSON:

```
http://localhost:8180/v1/block/height/0/header?format=json
```

returns:

```json
{
    "hash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
    "version": 1,
    "previous": "0000000000000000000000000000000000000000000000000000000000000000",
    "merkle_root": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
    "timestamp": 1231006505,
    "bits": 486604799,
    "nonce": 2083236893
}
```

The full native REST map, under `http://localhost:8180`. In block paths,
`{block}` is `hash/{block hash}` or `height/{height}`. The method name is
the one used in credential method lists (§7.3).

| Path | Method | Result |
| ---- | ------ | ------ |
| `/v1/configuration` | `configuration` | Server configuration |
| `/v1/top` | `top` | Top confirmed height |
| `/v1/top/subscribe` | `top_subscribe` | Top height notifications (websocket) |
| `/v1/block/{block}` | `block` | Block |
| `/v1/block/{block}/header` | `block_header` | Block header |
| `/v1/block/{block}/header/context` | `block_header_context` | Header validation context |
| `/v1/block/{block}/details` | `block_details` | Block details |
| `/v1/block/{block}/txs` | `block_txs` | All transactions of the block |
| `/v1/block/{block}/tx/{position}` | `block_tx` | Transaction at a position in the block |
| `/v1/block/{block}/filter/{type}` | `block_filter` | Client filter |
| `/v1/block/{block}/filter/{type}/hash` | `block_filter_hash` | Client filter hash |
| `/v1/block/{block}/filter/{type}/header` | `block_filter_header` | Client filter header |
| `/v1/block/subscribe` | `block_subscribe` | Block notifications (websocket) |
| `/v1/tx/{tx hash}` | `tx` | Transaction |
| `/v1/tx/{tx hash}/header` | `tx_header` | Header of the confirming block |
| `/v1/tx/{tx hash}/details` | `tx_details` | Transaction details |
| `/v1/tx/subscribe` | `tx_subscribe` | Transaction notifications (websocket) |
| `/v1/input/{tx hash}` | `inputs` | All inputs of the transaction |
| `/v1/input/{tx hash}/{index}` | `input` | Input |
| `/v1/input/{tx hash}/{index}/script` | `input_script` | Input script |
| `/v1/input/{tx hash}/{index}/witness` | `input_witness` | Input witness |
| `/v1/output/{tx hash}` | `outputs` | All outputs of the transaction |
| `/v1/output/{tx hash}/{index}` | `output` | Output |
| `/v1/output/{tx hash}/{index}/script` | `output_script` | Output script |
| `/v1/output/{tx hash}/{index}/spender` | `output_spender` | Confirmed spender of the output |
| `/v1/output/{tx hash}/{index}/spenders` | `output_spenders` | All spenders of the output |
| `/v1/output/{tx hash}/{index}/subscribe` | `output_subscribe` | Spend notifications (websocket) |
| `/v1/address/{script hash}` | `address` | All history of an output script |
| `/v1/address/{script hash}/confirmed` | `address_confirmed` | Confirmed history |
| `/v1/address/{script hash}/unconfirmed` | `address_unconfirmed` | Unconfirmed history |
| `/v1/address/{script hash}/balance` | `address_balance` | Confirmed balance |
| `/v1/address/{script hash}/subscribe` | `address_subscribe` | History notifications (websocket) |

Query options, besides `format`:

| Option | Applies to | Purpose |
| ------ | ---------- | ------- |
| `witness=false` | block, transaction and input paths | Omit witness data |
| `turbo=false` | address paths | Run the query on one thread instead of all (see `database.turbo`) |
| `stop=true` | subscribe paths | End the subscription |

To serve a custom block explorer from a directory instead of the embedded
site, set `native.path`. A request for `/` returns `native.default`
(`index.html`).

The native interface is libbitcoin's own, and provides:

- HTTP and websocket on each port. Over a websocket, each frame is one
  request path, and the `subscribe` paths (top, block, transaction,
  output and address) push notifications.
- Data, text, JSON and HTML formats for each path.
- TLS on its `safe` addresses (§7.2), with optional client certificates.
- Credentials (§7.3), restricted by REST method names.

### 5.7 Electrum server

Electrum on its assigned ports (§6), clear and secure (§7.2):

```ini
[electrum]
bind = 0.0.0.0:8580
safe = 0.0.0.0:8543
connections = 100
cert_path = server.pem
key_path = server.key
```

Beyond the standard Electrum transports (TCP and TLS), `bs` provides:

- HTTP and websocket on the same ports. Subscriptions need a full duplex
  transport (TCP or websocket), so an HTTP connection's subscriptions
  are held until it upgrades to a websocket.
- Client certificates on its `safe` addresses (§7.2).
- Credentials (§7.3), restricted by RPC method names. A credential
  refuses raw TCP clients.

### 5.8 Bitcoind RPC

The RPC interface listens on its default port, 8280, here limited to
the local machine.

```ini
[bitcoind]
bind = 127.0.0.1:8280
bind = [::1]:8280
connections = 10
credential = user:password
```

A credential may end with a list of the methods it permits (§7.3), here
three RPC methods and the matching REST block request:

```ini
[bitcoind]
credential = reader:password:getblockcount,getblockhash,getblock,block
```

Beyond the standard bitcoind interfaces (JSON-RPC over HTTP, and REST),
`bs` provides:

- JSON-RPC over websocket and raw TCP on the same ports.
- TLS on its `safe` addresses (§7.2), with optional client certificates.
- Credentials (§7.3) for REST as well as RPC, restricted by RPC and REST
  method names, which are distinct. A credential refuses raw TCP clients.

### 5.9 BTCD RPC

The btcd RPC interface listens on its default port, 8480, here limited
to the local machine:

```ini
[btcd]
bind = 127.0.0.1:8480
bind = [::1]:8480
connections = 10
credential = user:password
```

The BTCD interface is the Bitcoind RPC interface (§5.8) with btcd's
methods added. Unlike btcd's own implementation, the methods it inherits
behave exactly as they do in `[bitcoind]`.

A websocket or raw TCP client may authenticate after connecting, with
btcd's `authenticate` method. A failed `authenticate` closes the
connection. A request for a method the credential does not permit returns
an invalid parameters error.

Beyond the standard btcd transports (HTTP and websocket, with TLS),
`bs` provides:

- JSON-RPC over raw TCP on the same ports.
- Client certificates on its `safe` addresses (§7.2).
- Credentials (§7.3), restricted by RPC method names. Raw TCP clients
  authenticate with `authenticate`.

### 5.10 ZMQ notifications

ZMQ publishes on its default port, 8380, here limited to the local
machine.

```ini
[bitcoind_zmq]
bind = 127.0.0.1:8380
bind = [::1]:8380
connections = 10
```

Beyond the standard bitcoind notifications, `bs` provides CurveZMQ on its
`safe` addresses (§7.2): encrypted notifications, optionally only to
the client keys listed in `bitcoind_zmq.cert`.

### 5.11 Esplora REST

The Esplora REST interface, on its assigned port:

```ini
[esplora]
bind = 0.0.0.0:8780
connections = 100
```

To serve existing Esplora clients, bind it to the port they expect
instead (§6). `esplora.maximum_history` limits the entries returned for
one address.

Beyond the standard Esplora REST interface, `bs` provides:

- Websocket on the same ports. Each frame is one request path, and a
  request with a body (a broadcast) follows the path with a newline and
  the body.
- TLS on its `safe` addresses (§7.2), with optional client certificates.
- Credentials (§7.3), restricted by REST method names.

### 5.12 Client filters (BIP157/158)

```ini
[node]
provide_filters = true

[table.filter_bk]
buckets = 950001

[table.filter_tx]
buckets = 950001
```

Client filters are enabled when the store is created (§10). Any count
above 0 on both tables enables the client filters index. The value
given initializes the index to entries for that many blocks, but the index
grows as required.

### 5.13 Disable the address index

The address index is disabled when the store is created (§10):

```ini
[table.outs]
buckets = 0
```

### 5.14 Silent payments

Silent payments are indexed from `node.silent_start_height`, and never below
taproot activation, so 0 indexes from there. The start height is fixed when
the store is created (§10). The index is served to Sparrow
by the `[sparrow]` service, the Electrum protocol with silent payment
extensions:

```ini
[node]
silent_start_height = 0

[sparrow]
bind = 0.0.0.0:8680
safe = 0.0.0.0:8643
connections = 100
cert_path = server.pem
key_path = server.key
```

The Sparrow interface is the Electrum interface with silent payment and
block statistics methods added, and provides the same transports and
security as `[electrum]` (§5.7).

### 5.15 Tor

Outbound through Tor's SOCKS5 proxy, inbound through a Tor hidden service
(`HiddenServiceDir` and `HiddenServicePort` in `torrc`) pointing at the node's
listening port, and onion address gossip:

```ini
[outbound]
socks = 127.0.0.1:9050
seed = <first seed onion address>.onion:8333
seed = <second seed onion address>.onion:8333

[inbound]
self = <hidden service onion address>.onion:8333

[peer]
gossip_tor = true
```

`inbound.self` advertises the hidden service address to peers, so they can
connect to the node over Tor. Seeds are connected through the proxy, so the default seeds work where Tor
can reach them. An onion-only node lists onion seeds.

`outbound.socks` proxies the outbound session and its seeds. Manual peers
([5.17](#517-fixed-peers)) use their own `manual.socks`. Each takes an optional
`username` and `password`.

### 5.16 I2P

Outbound through the SOCKS5 proxy pointed at an I2P router's SOCKS port,
inbound through the router's SAM bridge, and I2P address gossip. The
destination key file is created if it does not exist, and the I2P address
derived from it is advertised to peers, so `inbound.self` is not needed:

```ini
[outbound]
socks = 127.0.0.1:4447
seed = <first seed destination>.b32.i2p
seed = <second seed destination>.b32.i2p

[inbound]
sam = 127.0.0.1:7656
key_path = i2p.key

[peer]
gossip_i2p = true
```

Seeds are connected through the proxy, which reaches only I2P destinations,
so an I2P node lists I2P seeds. I2P has no ports, so none is given.

`outbound.socks` proxies the outbound session and its seeds. Manual peers
([5.17](#517-fixed-peers)) use their own `manual.socks`. Each takes an optional
`username` and `password`.

### 5.17 Fixed peers

```ini
[manual]
peer = 192.168.0.10:8333
peer = 192.168.0.11:8333

[outbound]
connections = 0

[inbound]
connections = 0
```

Manual peers are automatically reconnected after a delay
(`network.retry_timeout_seconds`) when they drop.
`outbound.connections = 0` disables the outbound session, which otherwise
connects to peers from the address pool, and `inbound.connections = 0`
disables the inbound session, which otherwise accepts peers that connect to
the node. The node then exchanges only with the peers listed.

### 5.18 Peer services and policy

What the node provides to and requires of its peers, and its transaction
policy:

```ini
[node]
limited_blocks  = true      # pruned blocks
provide_blocks  = true      # provides blocks
require_blocks  = true      # requires blocks
provide_witness = true      # provides witnesses (bip144)
require_witness = true      # requires witnesses (bip144)
provide_filters = false     # serves client filters (bip157)
provide_privacy = true      # opportunistic encryption (bip324)
delay_inbound = true
fee_estimate_horizon = 0
minimum_fee_rate = 0.000001
```

- `node.limited_blocks` prunes blocks under the milestone (§5.2), and the
  node then serves only blocks above it.
- `node.provide_filters` also requires the client filter tables (§5.12).
- `node.delay_inbound` refuses inbound peers, and client services other
  than `[admin]` and `[native]`, until the chain is current.
- `node.fee_estimate_horizon` is the number of recent blocks used for fee
  estimates, at most 1,008 (one week). `0` disables fee estimation.
- `node.minimum_fee_rate` is the lowest fee rate, in BTC per thousand
  virtual bytes, of an unconfirmed transaction the node accepts. It is
  also reported to clients as the relay fee.

Which peer messages the node sends and accepts:

```ini
[peer]
enable_relay = true         # in/out transaction announcements
enable_alert = false        # send/log alert messages (no send option)
enable_reject = false       # send/log reject messages
enable_compact = true       # in/out compact block announcements
enable_address = true       # in/out address messages (false disables address v1 and v2)
enable_address_v2 = true    # in/out address v2 messages (drops down to v1 if gossip is IP only)
enable_witness_tx = true    # in/out wtxid for tx announcements
enable_memory_pool = true   # respond to mempool message with full pool
enable_not_found = true     # send not_found messages (vs. dropping peer for requesting what we don't have)
```

### 5.19 Outbound bindings

By default the operating system chooses the network adapter of each
outbound connection from its routing table, and with several adapters it
normally uses only one. Binding outbound connections to adapter addresses
restricts them to those adapters, and spreads them across the adapters
to combine their bandwidth:

```ini
[outbound]
bind = 192.168.0.20
bind = 192.168.0.21
connections = 100
```

- Each outbound connection slot is assigned one binding in turn, so here
  each adapter carries 50 connections. A slot always reconnects on its
  own adapter, so the split holds for as long as the node runs.
- Give the address without a port. The operating system assigns the
  source port.
- An IPv4 binding connects only to IPv4 peers, and an IPv6 binding only
  to IPv6 peers. List one address per adapter to balance by adapter.
- Seed connections use `outbound.bind`. Manual peers use `manual.bind`,
  assigned in the order the peers are listed.
- Through a SOCKS5 proxy, the binding applies to the connection to the
  proxy.
- The slots of an adapter that is down stay idle and retry until it
  returns.

Outbound bindings do not affect inbound connections, which are accepted
on the `inbound.bind` addresses. Inbound defaults to `0.0.0.0:8333`, and
accepts connections on every IPv4 adapter. To accept peers only on the same adapters, bind
inbound to the same addresses:

```ini
[inbound]
bind = 192.168.0.20:8333
bind = 192.168.0.21:8333
```

Whether a bound connection actually leaves through its adapter depends on
the operating system:

- **Windows** routes a connection through the adapter that owns its
  bound address. The bindings are sufficient.
- **macOS** scopes the route lookup to the adapter that owns the bound
  address. The bindings are sufficient.
- **Linux** routes by destination and ignores the bound address, so every
  connection leaves through the adapter of the preferred default route.
  Each adapter needs its own routing table and a rule that selects it by
  source address.

For two Linux adapters on one subnet, `eth0` at 192.168.0.20 and `eth1`
at 192.168.0.21, with gateway 192.168.0.1:

```
$ sudo ip route add default via 192.168.0.1 dev eth0 table 100
$ sudo ip route add default via 192.168.0.1 dev eth1 table 200
$ sudo ip rule add from 192.168.0.20 lookup 100
$ sudo ip rule add from 192.168.0.21 lookup 200
$ sudo sysctl -w net.ipv4.conf.all.arp_filter=1 net.ipv4.conf.all.arp_ignore=1 net.ipv4.conf.all.arp_announce=2
```

All five lines are required. The tables and rules send each connection
out through its bound adapter. The last line makes each adapter answer
only for its own address, so that replies also arrive on that adapter.
Adapters on separate networks need only the tables and rules, each with
its own gateway. Confirm the route of a bound address with:

```
$ ip route get 1.1.1.1 from 192.168.0.21
```

These commands do not persist across a reboot. Add the same tables and
rules to the distribution's network configuration (netplan,
systemd-networkd or NetworkManager).

Adapters on one subnet share its gateway, so their combined bandwidth is
also limited by the gateway's uplink.

---

## 6. Ports

Every service has an assigned port on each chain, clear and secure. A
service listens only on the addresses given by its `bind` and `safe`
settings (§7.1), so the examples on this page give them explicitly.

The P2P network uses its convention on each chain, so peers find the
node without configuration. Each libbitcoin service uses its own block,
`8N80` for clear connections and `8N43` for secure (TLS), so that `bs` can run
beside `bitcoind`, Electrum servers and Esplora on one machine without
conflict.

| Service | Section | Clear | Secure |
| ------- | ------- | ----- | ------ |
| P2P network | `[inbound]` | 8333 | 8333 |
| Admin web | `[admin]` | 8080 | 8043 |
| Native web and REST | `[native]` | 8180 | 8143 |
| Bitcoind RPC and REST | `[bitcoind]` | 8280 | 8243 |
| Bitcoind ZMQ | `[bitcoind_zmq]` | 8380 | 8343 |
| BTCD RPC | `[btcd]` | 8480 | 8443 |
| Electrum | `[electrum]` | 8580 | 8543 |
| Sparrow | `[sparrow]` | 8680 | 8643 |
| Esplora REST | `[esplora]` | 8780 | 8743 |

P2P has no separate secure port. BIP324 encryption is negotiated on the
same port, and offered when `node.provide_privacy` is set. ZMQ's secure
port uses CurveZMQ.

On the test chains the service ports move by a fixed offset, and the P2P
port follows its network's convention:

| Chain | Service offset | Services | P2P |
| ----- | -------------- | -------- | --- |
| mainnet | 0 | 8043–8780 | 8333 |
| testnet3 | +10000 | 18043–18780 | 18333 |
| regtest | +20000 | 28043–28780 | 18444 |
| signet | +30000 | 38043–38780 | 38333 |
| testnet4 | +40000 | 48043–48780 | 48333 |

To use a service as a drop-in replacement, bind it to the port its
clients expect instead:

```ini
[bitcoind]
bind = 127.0.0.1:8332
bind = [::1]:8332

[btcd]
safe = 127.0.0.1:8334
safe = [::1]:8334

[electrum]
bind = 0.0.0.0:50001
safe = 0.0.0.0:50002

[esplora]
bind = 127.0.0.1:3000
bind = [::1]:3000
```

A section may list several `bind` and `safe` lines, and listens on all
of them. This Electrum server accepts clients on its default ports and
on the conventional ones, over IPv4 and IPv6:

```ini
[electrum]
bind = 0.0.0.0:8580
bind = [::]:8580
bind = 0.0.0.0:50001
bind = [::]:50001
safe = 0.0.0.0:8543
safe = [::]:8543
safe = 0.0.0.0:50002
safe = [::]:50002
connections = 100
cert_path = server.pem
key_path = server.key
```

And this RPC interface listens on the local machine and on one private
network address only:

```ini
[bitcoind]
bind = 127.0.0.1:8280
bind = [::1]:8280
bind = 192.168.0.10:8280
connections = 10
credential = user:password
```

---

## 7. Settings shared by every service

The client services (`[admin]`, `[native]`, `[bitcoind]`, `[electrum]`,
`[btcd]`, `[sparrow]` and `[esplora]`) share these settings.
`[bitcoind_zmq]` shares the listening settings, and secures its
connections using CurveZMQ rather than TLS (§7.2).

### 7.1 Listening

A service runs only when it has somewhere to listen and is allowed
connections:

| Setting | Purpose |
| ------- | ------- |
| `bind` | Address and port for clear connections. Multiple allowed. |
| `safe` | Address and port for secure connections. Multiple allowed. |
| `connections` | Maximum concurrent connections. `0` disables the service. |

An address of `0.0.0.0` (or `[::]` for IPv6) listens on all interfaces,
and `127.0.0.1` (or `[::1]` for IPv6) on the local machine only. Client
services other than `[admin]` and `[native]` wait until the chain is
current before accepting connections (`node.delay_inbound`).

### 7.2 Secure connections

A `safe` address serves TLS, and requires a server certificate and its
private key. Without both, the service does not listen on its `safe`
addresses.

| Setting | Purpose |
| ------- | ------- |
| `cert_path` | Server certificate file (PEM). |
| `key_path` | Server private key file (PEM). |
| `key_pass` | Password of an encrypted private key, if any. |
| `cert_auth` | Directory of certificate authority files (PEM). When set, clients must present a certificate issued by one of them. |

The same certificate and key may be used by every service. For example,
`[admin]` over TLS only:

```ini
[admin]
safe = 127.0.0.1:8043
safe = [::1]:8043
connections = 10
cert_path = server.pem
key_path = server.key
```

ZMQ uses CurveZMQ instead of TLS. Its `safe` addresses require the
server's secret key (`bitcoind_zmq.key`, Z85 encoded), and each
`bitcoind_zmq.cert` line authorizes one client public key. With no `cert`
lines, any client may connect.

### 7.3 Authentication

Every client service except `[bitcoind_zmq]` has:

| Setting | Purpose |
| ------- | ------- |
| `credential` | A `user:password` for HTTP Basic authentication ([RFC 7617](https://www.rfc-editor.org/rfc/rfc7617.txt), [RFC 9110 §11](https://www.rfc-editor.org/rfc/rfc9110.txt)). Multiple allowed. When any is set, every request must present one of them. Basic authentication is not encrypted, so it is exposed unless the connection is secure. |

`[bitcoind]`, `[btcd]`, `[electrum]` and `[sparrow]` accept raw TCP,
HTTP and websocket clients on the same port. Raw TCP carries no HTTP
headers, so when a credential is set, a raw TCP connection is closed at
its first request, except by `[btcd]`, whose clients authenticate in-band
(§5.9). To restrict raw TCP clients, require client
certificates (`cert_auth`) instead.

A credential may end with a list of the methods it permits,
`user:password:method,...`. A request for any other method is refused,
with HTTP 403 or by closing a websocket. JSON-RPC interfaces use their
RPC method names, such as `getblock` or `blockchain.headers.subscribe`.
REST interfaces use these names, one for each kind of request path:

| Section | REST method names |
| ------- | ----------------- |
| `[bitcoind]` | chain_information, block, block_txs, block_hash, block_headers, block_filter, block_filter_headers, block_part, block_spent_tx_outputs, deployment_info, get_utxos, mempool, mempool_information, tx |
| `[native]` | configuration, top, top_subscribe, block, block_header, block_header_context, block_details, block_tx, block_txs, block_filter, block_filter_hash, block_filter_header, block_subscribe, tx, tx_header, tx_details, tx_subscribe, inputs, input, input_script, input_witness, outputs, output, output_script, output_spender, output_spenders, output_subscribe, address, address_confirmed, address_unconfirmed, address_balance, address_subscribe |
| `[esplora]` | blocks, block, block_header, block_height, block_status, block_txid, block_txids, block_txs, tip_hash, tip_height, tx, tx_status, tx_merkle_proof, tx_merkleblock_proof, tx_outspend, tx_outspends, address, address_txs, address_txs_chain, address_txs_mempool, address_utxo, mempool, mempool_txids, mempool_recent, fee_estimates, broadcast, broadcast_package |
| `[admin]` | log_subscribe, event_subscribe |

### 7.4 HTTP services

`[admin]`, `[native]`, `[bitcoind]`, `[btcd]` and `[esplora]` are HTTP
services, and also have:

| Setting | Purpose |
| ------- | ------- |
| `host` | Allowed `Host` header values ([RFC 9110 §7.2](https://www.rfc-editor.org/rfc/rfc9110.txt)). Multiple allowed. |
| `origin` | Allowed `Origin` header values for cross-origin requests ([RFC 6454](https://www.rfc-editor.org/rfc/rfc6454.txt)). Multiple allowed. |
| `allow_opaque_origin` | Allow requests with an opaque origin ([RFC 6454 §7.3](https://www.rfc-editor.org/rfc/rfc6454.txt)), such as from a page opened as a local file. |

### 7.5 Limits

Each service has the limits that apply to its protocol. They apply to
each connection separately.

#### Time

| Setting | Purpose |
| ------- | ------- |
| `inactivity_minutes` | A connection that has received nothing for this long is closed. This is also the HTTP keep-alive period. Sending does not count as activity. `0` disables it. |
| `expiration_minutes` | A connection is closed this long after it opened, whether or not it is active. `0` disables it. |
| `connect_timeout_seconds` | Time allowed for a new connection to complete its transport layer handshake (TLS, or ZMTP for ZMQ) before it is dropped. Application layer handshakes, such as Electrum version negotiation, are not covered. Each connection's limit is chosen at random between half and all of this value, so that many clients do not time out together. `0` uses `network.connect_timeout_seconds`, which defaults to 5 seconds. |

#### Throughput

| Setting | Purpose |
| ------- | ------- |
| `rate_limit` | Maximum send rate of a connection, in bytes per second. The limit is continuous, not a cliff: each send is paced by its size, so a connection is slowed to the rate rather than cut off at a quota. Sends are delayed, not dropped, and throttling never disconnects a client. A client that requests faster than its responses drain is bounded by `maximum_backlog`. This protects against denial of service by bounding the rate at which one client can draw data from the server. `network.rate_limit` applies the same limit to every connection. When both are set the lower applies, and `0` leaves the other in effect (both `0` is unlimited). |
| `maximum_backlog` | Maximum bytes of responses waiting to be sent to a connection, such as to a client that reads slower than it asks. A connection that exceeds it is closed. ZMQ instead drops the notifications that do not fit. This protects against denial of service by bounding the memory a client that does not read can hold on the server. |

#### Memory

| Setting | Purpose |
| ------- | ------- |
| `maximum_request` | Largest request accepted, in bytes, by every service: an HTTP body, a websocket message, an Electrum JSON-RPC message, a ZMQ frame, or a P2P message (`[inbound]`, `[outbound]` and `[manual]`). A larger request closes the connection. This protects against denial of service by bounding the memory a client can make the server allocate. |
| `minimum_buffer` | Buffer memory a connection keeps for reading requests, and for writing JSON responses. A buffer expanded beyond this by a large request or response is trimmed back to this size once it is idle. |
| `maximum_buffer` | Size of the buffer a JSON response is written through. A larger response is sent in pieces of this size, so it limits the memory per connection, not the response size. |

---

## 8. Performance settings

The defaults suit most machines. These are the settings that most affect
sync and query speed.

### 8.1 Processor

| Setting | Default | Purpose |
| ------- | ------- | ------- |
| `network.threads` | `0` | Threads that run the network: peer and client connections. `0` uses one per hardware thread, at most 32. |
| `node.threads` | `0` | Threads that validate blocks. `0` uses one per hardware thread, which is two per core on a processor with hyperthreading (SMT). |
| `node.thread_priority` | `true` | Run validation threads at high priority, ahead of other programs. `false` leaves them at normal priority. |
| `node.memory_priority` | `true` | Keep the process at normal memory priority. `false` lowers it, so the operating system reclaims its memory first. |
| `database.turbo` | `true` | Allow a single client query to use all processors, so large queries return sooner. |

### 8.2 Signature verification and silent payment indexing

When a sufficient GPU is available, signatures are verified, and silent
payment transactions indexed, in batches on the GPU, which is much faster
than on a CPU. Run
`bs -w` to see whether a GPU is available, and which processor features
apply.

| Setting | Default | Purpose |
| ------- | ------- | ------- |
| `node.use_gpu` | `true` | Use the GPU when one is available, for signature verification, silent payment indexing and silent payment scans. |
| `node.batch_verify` | `1,000,000` | Signatures verified in each GPU batch. `0` disables GPU verification. |
| `node.batch_silent` | `1,000,000` | Silent payment transactions indexed in each GPU batch. `0` disables GPU indexing. |
| `database.gpu_scan_minimum` | `65,536` | Smallest silent payment scan, in transactions, sent to the GPU. Smaller scans run on the CPU, where they return sooner. |

### 8.3 Network

| Setting | Default | Purpose |
| ------- | ------- | ------- |
| `node.maximum_concurrency` | `50,000` | Blocks downloaded concurrently. Blocks arrive out of order, and this window lets download run ahead of validation. `0` is unlimited. |
| `outbound.connections` | `100` | Outgoing peer connections while syncing. More peers may be required to saturate a high bandwidth network connection. |
| `outbound.current_connections` | `10` | Outgoing peer connections once the chain is current, when fewer are needed. `0` keeps `outbound.connections`. |

---

## 9. Store table sizing (`[table.*]`)

The `[table.*]` settings are advanced and generally do not need to be
changed. Each table has some of `buckets`, `expected`, `size` and
`rate`, and the defaults are sized for mainnet at 950,000 blocks.

The common changes are:

- disabling the address index ([5.13](#513-disable-the-address-index));
- enabling client filters ([5.12](#512-client-filters-bip157158));
- sizing for a test chain, as on the [Testnet3](testnet3),
  [Testnet4](testnet4), [Signet](signet) and [Regtest](regtest) pages.

`bs -k` and `bs -l` report bucket fill and collisions on an existing
store.

### 9.1 Bucket autotuning

The hashmap tables (`header`, `tx`, `ins`, `outs`, `pool` and `wtxid`)
derive their bucket count from their `expected` entry count and the
installed memory, unless `buckets` is configured. The ratio of entries to
buckets is the load factor. More buckets shorten searches but enlarge
the table heads, which must generally be held in memory during initial
sync.

| Installed memory | Load factor | Address index (`outs`) |
| ---------------- | ----------- | ---------------------- |
| 8 GB or less | 7.5 | 50 |
| 32 GB or more | 2.5 | 5 |

Between 8 and 32 GB the load factor falls in proportion to the memory.
So a store created on a smaller machine uses less memory for its heads,
and one created on a larger machine searches faster. A configured
`buckets` value replaces the derived count, and `0` disables an optional
table.

---

## 10. Settings fixed at store creation

Some settings are captured in the store when it is created, in its
envelope, and govern that store from then on. The general rules are that
hashmap bucket counts cannot be changed (would require table rewrites),
optional indexation cannot be altered (would result in hidden gaps), and
consensus rules cannot be modified (would result in an inconsistent
chain).

Each time `bs` opens an existing store (or restores one), it compares the
captured values with the configuration. Where a setting differs, the
store's value is used for that run, and the configured value is ignored.
The configuration file is not changed. Each overridden setting is logged
by name:

```
Database envelope [milestone] overrides configuration.
```

The captured settings are:

| Section | Settings |
| ------- | -------- |
| `[bitcoin]` | the chain parameters, soft fork activations and the milestone |
| `[forks]` | all |
| `[database]` | `interval_depth` |
| `[table.*]` | `buckets` of `header`, `tx`, `ins`, `outs`, `duplicate`, `pool` and `wtxid`, and whether client filters are enabled |
| `[node]` | `limited_blocks` and `silent_start_height` |

A different top checkpoint is logged but not replaced, and client filters
cannot be added to a store created without them. To change any of these
settings, create a new store. The setups that depend on
them, from milestone sync and pruning to disabling the address index,
take effect only on a new store.

---

## 11. Settings Reference

Every setting, by section, with its description and default, is on the
[Settings Reference](reference) page.

Settings for the test chains are on their own pages:
[Testnet3](testnet3), [Testnet4](testnet4), [Signet](signet) and [Regtest](regtest).
