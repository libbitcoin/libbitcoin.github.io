# Regtest

Regtest is a private test chain with minimal difficulty, for local
testing.

These settings have not yet been verified.

Start the node on regtest:

```
$ bs -n regtest
```

`-n regtest` applies the built-in regtest defaults below, and keeps the store
in a `regtest` directory under the working directory, apart from any mainnet
store. Every run selects the network the same way. Without `-n regtest`,
`bs` uses the `mainnet` store.

The log files and the peer address cache (`hosts.cache`) are written by default
to the working directory and are not separated by network, so run each
network from its own working directory.

## Defaults

These are the settings in which the regtest defaults differ from mainnet, as
displayed by `bs -n regtest --settings`. The derived bucket counts of the
other tables also differ, as do the service ports ([Ports](#ports)).

```ini
[bitcoin]
network = regtest
bip16_activation_time = 1329264000
bip34_activation_sample = 0
bip34_activation_threshold = 0
bip34_enforcement_threshold = 0
bip34_freeze = 100000000
bip54_coinbase_start = 4294967295
bip54_sigops_start = 4294967295
bip54_timespan_start = 4294967295
bip54_timewarp_start = 4294967295
bip54_txsize_start = 4294967295
bip65_freeze = 1351
bip66_freeze = 1251
bip9_activation_period = 0
bip9_bit0_start = 4294967295
bip9_bit0_threshold = 0
bip9_bit0_timeout = 0
bip9_bit1_start = 4294967295
bip9_bit1_threshold = 0
bip9_bit1_timeout = 0
bip9_bit2_activation_height = 0
bip9_bit2_speedy_trial = false
bip9_bit2_start = 4294967295
bip9_bit2_threshold = 0
bip9_bit2_timeout = 0
genesis_block = 0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4adae5494dffff7f20020000000101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4d04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73ffffffff0100f2052a01000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000
milestone = 0f9188f13cb7b2c71f2a335e3a4fc328bf5beb436012afca590b1a11466e2206:0
minimum_work = 0000000000000000000000000000000000000000000000000000000000000000
proof_of_work_limit = 545259519
retargeting_interval_seconds = 86400
subsidy_interval = 150

[forks]
retarget = false

[peer]
identifier = 3669344250

[wallet]
hd_private_prefix = 70615956
hd_public_prefix = 70617039
p2kh_prefix = 111
p2sh_prefix = 196
silent_prefix = tsp
wif_prefix = 239
witness_prefix = bcrt

[inbound]
bind = 0.0.0.0:18444

[outbound]
connections = 0
host_pool_capacity = 0

[table.header]
expected = 10000
size = 0

[table.txs]
buckets = 10001
size = 0

[table.tx]
expected = 100000
size = 0

[table.ins]
expected = 200000
size = 0

[table.outs]
expected = 300000
size = 0

[table.input]
size = 0

[table.output]
size = 0

[table.candidate]
buckets = 10001

[table.confirmed]
buckets = 10001

[table.state]
buckets = 10001

[table.scan]
buckets = 10001
```

- `[bitcoin]` sets the regtest genesis block and difficulty limit, all
  soft forks active from genesis, and a 150 block subsidy interval.
  There are no checkpoints and no minimum work.
- `forks.retarget = false` disables difficulty retargeting.
- `peer.identifier` is the regtest network magic.
- `[wallet]` sets the regtest address and key prefixes used by the server
  ([Settings Reference](reference#6-wallet)).
- `[outbound]` disables seeding and outbound connections.
- `[table.*]` keeps the store small, since the mainnet defaults
  preallocate for the mainnet chain.

## Configuration

A configuration file is needed only to change a default. `bs` does not
mine, and the regtest defaults make no outbound connections, so blocks
come from a local node that generates them. This recommended file
connects to one on port 18445, since `bs` listens on 18444, and serves the
admin console and block explorer locally, which are off by default:

```ini
[bitcoin]
network = regtest

[manual]
peer = 127.0.0.1:18445

[admin]
bind = 127.0.0.1:28080
connections = 10

[native]
bind = 127.0.0.1:28180
connections = 10
```

Save it as `regtest.cfg` and start the node with it:

```
$ bs -c regtest.cfg
```

`bitcoin.network` in the file selects the network, so `-n` is not needed.
The store is the same `regtest` store.

## Ports

On regtest, each service listens by default on its
mainnet port plus 20,000 ([Conventional Ports](ports)):

| Service | Section | Clear | Secure |
| ------- | ------- | ----- | ------ |
| P2P network | `[inbound]` | 18444 | 18444 |
| Admin web | `[admin]` | 28080 | 28043 |
| Native web and REST | `[native]` | 28180 | 28143 |
| Bitcoind RPC and REST | `[bitcoind]` | 28280 | 28243 |
| ZMQ | `[zmq]` | 28380 | 28343 |
| BTCD RPC | `[btcd]` | 28480 | 28443 |
| Electrum | `[electrum]` | 28580 | 28543 |
| Sparrow | `[sparrow]` | 28680 | 28643 |
| Esplora | `[esplora]` | 28780 | 28743 |
| Stratum v1 | `[stratum_v1]` | 28880 | 28843 |
| Stratum v2 | `[stratum_v2]` | 28980 | – |
