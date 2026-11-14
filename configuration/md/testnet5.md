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
| Genesis block | Mined 2026-11-14 05:03 UTC, committing to mainnet block 975,744; hash `00000000000008c1637e7d3252dc1c333d4546fd6fff6a474b200d674a91d497` ([BIP 95 parameters](https://github.com/bitcoin/bips/pull/2356), pending merge) |
| Network | Live; no DNS seeds |
| `bs` | `-n testnet5`, with the defaults below; not yet released |
| [Community servers](public) | Serving testnet5 |

A store made with the BIP 95 placeholder genesis block, or on the
rehearsal bootstrap chain that preceded the network, must be made again.

Start the node on testnet5:

```
$ bs -n testnet5
```

`-n testnet5` applies the built-in testnet5 defaults below, and keeps its files
in a `testnet5` directory under the working directory (or `folders.root`),
apart from any other network's: the store in `testnet5/store`, and the log
files and the peer address cache (`peers.cache`) in `testnet5`. Every run
selects the network the same way. Without `-n testnet5`,
`bitcoin.network = testnet5`, or the testnet5 genesis block in
`bitcoin.genesis_block`, `bs` uses mainnet defaults and the `mainnet`
directory.

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
checkpoint = 00000000000008c1637e7d3252dc1c333d4546fd6fff6a474b200d674a91d497:0
genesis_block = 00c0302200000000000000000000000000000000000000000000000000000000000000008de2a6b556ecb56779c34481ede767f09b2ae214f37ab1ad34085b5cb699588c91ebf76affff0f1a31913d650101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff5b04ffff001d01044c52323032362d31312d3134203937353734342030303030303030303030303030303030303030313233653236383165326638326163646362393433306131356565633234636338356234303036393164343739ffffffff0100f2052a010000000a6a0895ebf76a0200000000000000
milestone = 00000000000008c1637e7d3252dc1c333d4546fd6fff6a474b200d674a91d497:0
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
