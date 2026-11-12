# Testnet5

Testnet5 is a public test network defined by
[BIP 95](https://github.com/bitcoin/bips/blob/master/bip-0095.md), to
replace testnet4. It runs mainnet consensus with none of the testnet
exceptions: no minimum difficulty blocks, a higher minimum difficulty,
and every soft fork, including the five rules of BIP 54, active from
block 1.

## Deployment status

| Item | Status |
| ---- | ------ |
| [BIP 95](https://github.com/bitcoin/bips/blob/master/bip-0095.md) | Draft (version 0.3.0) |
| Genesis block | Not yet mined; the BIP 95 placeholder is used below |
| Network | Not yet started; no DNS seeds |
| `bs` | `-n testnet5`, with the defaults below; not yet released |
| [Community servers](public) | Ports assigned ([Ports](#ports)), not yet serving |

The genesis block, checkpoint and milestone below change when the
testnet5 genesis block is mined, and a store made with the placeholder
must then be made again.

Start the node on testnet5:

```
$ bs -n testnet5
```

`-n testnet5` applies the built-in testnet5 defaults below, and keeps its files
in a `testnet5` directory under the working directory (or `folders.root`),
apart from any other network's: the store in `testnet5/store`, and the log
files and the peer address cache (`peers.cache`) in `testnet5`. Every run
selects the network the same way. Without `-n testnet5`, `bs` uses the
`mainnet` directory.

## Defaults

These are the settings in which the testnet5 defaults differ from mainnet, as
displayed by `bs -n testnet5 --settings`. The derived bucket counts of the
other tables also differ, as do the service ports ([Ports](#ports)).

```ini
[bitcoin]
network = testnet5
bip16_activation_time = 1329264000
bip34_activation_sample = 0
bip34_activation_threshold = 0
bip34_enforcement_threshold = 0
bip34_freeze = 0
bip54_coinbase_start = 4294967295
bip54_sigops_start = 4294967295
bip54_timespan_start = 4294967295
bip54_timewarp_start = 4294967295
bip54_txsize_start = 4294967295
bip65_freeze = 0
bip66_freeze = 0
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
checkpoint = 000000000001bd3ade1e24d07c1a3677d4868c34f2f1696fa419e3b9f061b1e0:0
genesis_block = 00401c200000000000000000000000000000000000000000000000000000000000000000de48bbaa869592873fc4e5042f2931f9b42bb7e8ddeccd373df845d80983409b9663e96af8ff071b9916ba730101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff5b04ffff001d01044c52323032362d31312d3033203937343334332030303030303030303030303030303030303030306138366436646132633135363364303836363864396563313863636535386362386338363564346133316338ffffffff0100f2052a010000000a6a089763e96a0000000000000000
milestone = 000000000001bd3ade1e24d07c1a3677d4868c34f2f1696fa419e3b9f061b1e0:0
minimum_work = 0000000000000000000000000000000000000000000000000000000000000000
proof_of_work_limit = 437256191

[peer]
identifier = 1163282758

[wallet]
hd_private_prefix = 70615956
hd_public_prefix = 70617039
p2kh_prefix = 111
p2sh_prefix = 196
silent_prefix = tsp
wif_prefix = 239
witness_prefix = tb

[inbound]
bind = 0.0.0.0:18353

[outbound]
connect_batch_size = 10
connections = 50

[node]
maximum_concurrency = 100000

[table.header]
expected = 156456
size = 17835984

[table.txs]
buckets = 150001
size = 604424

[table.tx]
expected = 14810011
size = 9478407

[table.ins]
expected = 33127580
size = 17226342

[table.outs]
expected = 57089349
size = 5138041

[table.input]
size = 87852864

[table.output]
size = 20343818

[table.candidate]
buckets = 150001

[table.confirmed]
buckets = 150001

[table.state]
buckets = 150001

[table.scan]
buckets = 150001
```

- `[bitcoin]` replaces the chain parameters, with soft forks active from
  block 1, and BIP 54 active without signaling.
- `bitcoin.proof_of_work_limit` is `0x1a0fffff`, a higher minimum
  difficulty than mainnet's.
- `peer.identifier` is the testnet5 network magic (`FIVE`).
- `[outbound]` has no seeds, so the node finds no peers by itself. Name
  peers in `[manual]` (see [Configuration](#configuration)).
- `[wallet]` sets the testnet address and key prefixes used by the server
  ([Settings Reference](reference#6-wallet)).
- `[table.*]` sizes the store as for testnet4, at 150,000 blocks.
- `node.maximum_concurrency` raises the download window, since testnet
  blocks are small.

The `[forks]` settings are those of mainnet: `forks.difficult = true`
(no minimum difficulty blocks), and `forks.time_warp_patch` and
`forks.block_storm_patch` off, since BIP 54 replaces the testnet4 rules.

## Configuration

A configuration file is needed only to change a default. With no seeds,
testnet5 needs at least one peer named in `[manual]`. The block explorer
is off by default, and the admin console is served locally by default, on
port 58080. This recommended file connects to a peer and serves the block
explorer locally:

```ini
[bitcoin]
network = testnet5

[manual]
peer = <host>:18353

[native]
bind = 127.0.0.1
connections = 10
```

Save it as `testnet5.cfg` and start the node with it:

```
$ bs -c testnet5.cfg
```

`bitcoin.network` in the file selects the network, so `-n` is not needed.
The store is the same `testnet5` store.

## Ports

On testnet5, each service listens by default on its
mainnet port plus 50,000 ([Conventional Ports](ports)):

| Service | Section | Clear | Secure |
| ------- | ------- | ----- | ------ |
| P2P network | `[inbound]` | 18353 | 18353 |
| Admin web | `[admin]` | 58080 | 58043 |
| Native web and REST | `[native]` | 58180 | 58143 |
| Bitcoind RPC and REST | `[bitcoind]` | 58280 | 58243 |
| ZMQ | `[zmq]` | 58380 | 58343 |
| BTCD RPC | `[btcd]` | 58480 | 58443 |
| Electrum | `[electrum]` | 58580 | 58543 |
| Sparrow | `[sparrow]` | 58680 | 58643 |
| Esplora | `[esplora]` | 58780 | 58743 |
| Stratum v1 | `[stratum_v1]` | 58880 | 58843 |
| Stratum v2 | `[stratum_v2]` | 58980 | – |
