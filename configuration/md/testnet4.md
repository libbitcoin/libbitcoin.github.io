# Testnet4

Testnet4 is the newest public test network, about 150,000 blocks.

Start the node on testnet4:

```
$ bs -n testnet4
```

`-n testnet4` applies the built-in testnet4 defaults below, and keeps the store
in a `testnet4` directory under the working directory, apart from any mainnet
store. Every run selects the network the same way. Without `-n testnet4`,
`bs` uses the `mainnet` store.

The log files and the peer address cache (`hosts.cache`) are written by default
to the working directory and are not separated by network, so run each
network from its own working directory.

## Defaults

These are the settings in which the testnet4 defaults differ from mainnet, as
displayed by `bs -n testnet4 --settings`. The derived bucket counts of the
other tables also differ, as do the service ports ([Ports](#ports)).

```ini
[bitcoin]
network = testnet4
bip16_activation_time = 1329264000
bip34_activation_sample = 0
bip34_activation_threshold = 0
bip34_enforcement_threshold = 0
bip34_freeze = 0
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
checkpoint = 00000000da84f2bafbbc53dee25a72ae507ff4914b867c565be350b0da8bf043:0
genesis_block = 0100000000000000000000000000000000000000000000000000000000000000000000004e7b2b9128fe0291db0693af2ae418b767e657cd407e80cb1434221eaea7a07a046f3566ffff001dbb0c78170101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff5504ffff001d01044c4c30332f4d61792f323032342030303030303030303030303030303030303030303165626435386332343439373062336161396437383362623030313031316662653865613865393865303065ffffffff0100f2052a010000002321000000000000000000000000000000000000000000000000000000000000000000ac00000000
milestone = 0000000002368b1e4ee27e2e85676ae6f9f9e69579b29093e9a82c170bf7cf8a:123613
minimum_work = 000000000000000000000000000000000000000000000b6a51f415a67c0da307

[forks]
block_storm_patch = true
difficult = false
time_warp_patch = true

[peer]
identifier = 675223068

[wallet]
hd_private_prefix = 70615956
hd_public_prefix = 70617039
p2kh_prefix = 111
p2sh_prefix = 196
silent_prefix = tsp
wif_prefix = 239
witness_prefix = tb

[inbound]
bind = 0.0.0.0:48333

[outbound]
seed = seed.testnet4.bitcoin.sprovoost.nl:48333
seed = seed.testnet4.wiz.biz:48333
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
  block 1.
- `forks.time_warp_patch` enables the testnet4 time warp rule.
- `forks.block_storm_patch` enables the testnet4 block storm rule.
- `forks.difficult = false` enables testnet's minimum difficulty blocks.
- `peer.identifier` is the testnet4 network magic.
- `[outbound]` replaces the mainnet seeds.
- `[wallet]` sets the testnet address and key prefixes used by the server
  ([Settings Reference](reference#6-wallet)).
- `[table.*]` sizes the store for the chain at 150,000 blocks.
- `node.maximum_concurrency` raises the download window, since testnet
  blocks are small.

## Configuration

A configuration file is needed only to change a default. Network
operation needs none, but the admin console and block explorer are off by
default. This recommended file serves both locally:

```ini
[bitcoin]
network = testnet4

[admin]
bind = 127.0.0.1:48080
connections = 10

[native]
bind = 127.0.0.1:48180
connections = 10
```

Save it as `testnet4.cfg` and start the node with it:

```
$ bs -c testnet4.cfg
```

`bitcoin.network` in the file selects the network, so `-n` is not needed.
The store is the same `testnet4` store.

## Ports

On testnet4, each service listens by default on its
mainnet port plus 40,000 ([Conventional Ports](ports)):

| Service | Section | Clear | Secure |
| ------- | ------- | ----- | ------ |
| P2P network | `[inbound]` | 48333 | 48333 |
| Admin web | `[admin]` | 48080 | 48043 |
| Native web and REST | `[native]` | 48180 | 48143 |
| Bitcoind RPC and REST | `[bitcoind]` | 48280 | 48243 |
| Bitcoind ZMQ | `[bitcoind_zmq]` | 48380 | 48343 |
| BTCD RPC | `[btcd]` | 48480 | 48443 |
| Electrum | `[electrum]` | 48580 | 48543 |
| Sparrow | `[sparrow]` | 48680 | 48643 |
| Esplora | `[esplora]` | 48780 | 48743 |
| Stratum v1 | `[stratum_v1]` | 48880 | 48843 |
| Stratum v2 | `[stratum_v2]` | 48980 | – |
