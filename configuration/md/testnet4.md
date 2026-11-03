# Testnet4

Testnet4 is the newest public test network, about 150,000 blocks.

Save the settings below as `testnet4.cfg` and start the node with it:

```
$ bs -c testnet4.cfg
```

The store is created in a `testnet4` directory under the working
directory, apart from any mainnet store.

Without a configuration file, `bs -n testnet4` creates a store with the same
testnet4 settings in the `bitcoin` directory. Later runs read the network
from that store, so they need neither `-n` nor a configuration file.

```ini
[database]
path = testnet4

[bitcoin]
network = testnet4
bip16_activation_time = 1329264000
bip34_activation_sample = 100
bip34_activation_threshold = 51
bip34_enforcement_threshold = 75
bip34_freeze = 1
bip65_freeze = 1
bip66_freeze = 1
bip9_activation_period = 0
bip9_bit0_active_checkpoint = 0000000012982b6d5f621229286b880e909984df669c2afabb102ce311b13f28:1
bip9_bit0_start = 0
bip9_bit0_threshold = 0
bip9_bit0_timeout = 0
bip9_bit1_active_checkpoint = 0000000012982b6d5f621229286b880e909984df669c2afabb102ce311b13f28:1
bip9_bit1_start = 0
bip9_bit1_threshold = 0
bip9_bit1_timeout = 0
bip9_bit2_activation_height = 0
bip9_bit2_active_checkpoint = 0000000012982b6d5f621229286b880e909984df669c2afabb102ce311b13f28:1
bip9_bit2_speedy_trial = false
bip9_bit2_start = 0
bip9_bit2_threshold = 0
bip9_bit2_timeout = 0
checkpoint = 00000000da84f2bafbbc53dee25a72ae507ff4914b867c565be350b0da8bf043:0
genesis_block = 0100000000000000000000000000000000000000000000000000000000000000000000004e7b2b9128fe0291db0693af2ae418b767e657cd407e80cb1434221eaea7a07a046f3566ffff001dbb0c78170101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff5504ffff001d01044c4c30332f4d61792f323032342030303030303030303030303030303030303030303165626435386332343439373062336161396437383362623030313031316662653865613865393865303065ffffffff0100f2052a010000002321000000000000000000000000000000000000000000000000000000000000000000ac00000000
milestone = 0000000000d9877342754dea8ec1eb24631517d38e3443c370465ee53a8b7434:150000
minimum_work = 0000000000000000000000000000000000000000000009a0fe15d0177d086304

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
bind = 127.0.0.1:48333

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

# [table.scan]
# buckets = 150001
```

- `bitcoin.network` selects the testnet4 defaults, including the service
  ports ([Ports](#ports)).
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
- `[table.scan]` is commented out because it enables silent payments
  ([§5.14](index#514-silent-payments)). Uncomment it to index them.
- `node.maximum_concurrency` raises the download window, since testnet
  blocks are small.

## Ports

With `bitcoin.network = testnet4`, each service listens by default on its
mainnet port plus 40,000 ([Ports](index#6-ports)):

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
