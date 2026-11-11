# Testnet3

Testnet3 is a long-running public test network, about 5.1 million
blocks.

Start the node on testnet3:

```
$ bs -n testnet3
```

`-n testnet3` applies the built-in testnet3 defaults below, and keeps its files
in a `testnet3` directory under the working directory (or `folders.root`),
apart from any other network's: the store in `testnet3/store`, and the log
files and the peer address cache (`peers.cache`) in `testnet3`. Every run
selects the network the same way. Without `-n testnet3`, `bs` uses the
`mainnet` directory.

## Defaults

These are the settings in which the testnet3 defaults differ from mainnet, as
displayed by `bs -n testnet3 --settings`. The derived bucket counts of the
other tables also differ, as do the service ports ([Ports](#ports)).

```ini
[bitcoin]
network = testnet3
bip16_activation_time = 1329264000
bip34_activation_sample = 100
bip34_activation_threshold = 51
bip34_enforcement_threshold = 75
bip34_freeze = 21111
bip65_freeze = 581885
bip66_freeze = 330776
bip9_bit0_start = 1456790400
bip9_bit0_threshold = 1512
bip9_bit1_start = 1462060800
bip9_bit1_threshold = 1512
bip9_bit1_timeout = 1493596800
bip9_bit2_activation_height = 0
bip9_bit2_threshold = 1512
checkpoint = 000000002a936ca763904c3c35fce2f3556c559c0214345d31b1bcebf76acb70:546
genesis_block = 0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4adae5494dffff001d1aa4ae180101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4d04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73ffffffff0100f2052a01000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000
milestone = 0000000000000093bcb68c03a9a168ae252572d348a2eaeba2cdf9231d73206f:2500000
minimum_work = 000000000000000000000000000000000000000000000b6a51f415a67c0da307

[forks]
difficult = false

[inbound]
bind = 0.0.0.0:18333

[peer]
identifier = 118034699

[wallet]
hd_private_prefix = 70615956
hd_public_prefix = 70617039
p2kh_prefix = 111
p2sh_prefix = 196
silent_prefix = tsp
wif_prefix = 239
witness_prefix = tb

[outbound]
seed = testnet-seed.bitcoin.jonasschnelli.ch:18333
seed = seed.tbtc.petertodd.net:18333
seed = seed.testnet.bitcoin.sprovoost.nl:18333
connections = 50
connect_batch_size = 10

[node]
maximum_concurrency = 1000000

[table.header]
expected = 5158746
size = 588097044

[table.txs]
buckets = 5100001
size = 21874552

[table.tx]
expected = 536643888
size = 343452088

[table.ins]
expected = 598161444
size = 311043951

[table.outs]
expected = 1166697559
size = 105002780

[table.input]
size = 981182034

[table.output]
size = 600719803

[table.candidate]
buckets = 5100001

[table.confirmed]
buckets = 5100001

[table.state]
buckets = 5100001

[table.scan]
buckets = 5100001
```

- `[bitcoin]` replaces the chain parameters: genesis block, soft fork
  activations, checkpoint, milestone and minimum work.
- `forks.difficult = false` enables testnet's minimum difficulty blocks.
- `peer.identifier` is the testnet3 network magic.
- `[outbound]` replaces the mainnet seeds.
- `[wallet]` sets the testnet address and key prefixes used by the server
  ([Settings Reference](reference#6-wallet)).
- `[table.*]` sizes the store for the chain at 5.1 million blocks.
- `node.maximum_concurrency` raises the download window, since testnet
  blocks are small.

## Configuration

A configuration file is needed only to change a default. Network
operation needs none, but the admin console and block explorer are off by
default. This recommended file serves both locally:

```ini
[bitcoin]
network = testnet3

[admin]
bind = 127.0.0.1:18080
connections = 10

[native]
bind = 127.0.0.1:18180
connections = 10
```

Save it as `testnet3.cfg` and start the node with it:

```
$ bs -c testnet3.cfg
```

`bitcoin.network` in the file selects the network, so `-n` is not needed.
The store is the same `testnet3` store.

## Ports

On testnet3, each service listens by default on its
mainnet port plus 10,000 ([Conventional Ports](ports)):

| Service | Section | Clear | Secure |
| ------- | ------- | ----- | ------ |
| P2P network | `[inbound]` | 18333 | 18333 |
| Admin web | `[admin]` | 18080 | 18043 |
| Native web and REST | `[native]` | 18180 | 18143 |
| Bitcoind RPC and REST | `[bitcoind]` | 18280 | 18243 |
| ZMQ | `[zmq]` | 18380 | 18343 |
| BTCD RPC | `[btcd]` | 18480 | 18443 |
| Electrum | `[electrum]` | 18580 | 18543 |
| Sparrow | `[sparrow]` | 18680 | 18643 |
| Esplora | `[esplora]` | 18780 | 18743 |
| Stratum v1 | `[stratum_v1]` | 18880 | 18843 |
| Stratum v2 | `[stratum_v2]` | 18980 | – |
