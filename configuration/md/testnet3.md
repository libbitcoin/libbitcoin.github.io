# Testnet3

Testnet3 is the long-running public test network, about 5.1 million
blocks.

Save the settings below as `testnet3.cfg` and start the node with it:

```
$ bs -c testnet3.cfg
```

The store is created in a `testnet3` directory under the working
directory, apart from any mainnet store.

```ini
[database]
path = testnet3

[bitcoin]
bip16_activation_time = 1329264000
bip30_deactivate_checkpoint = 0000000023b3a96d3484e5abb3755c413e7d41500f8e2a5c3f0dd01299cd8ef8:21111
bip30_reactivate_height = 486000000
bip34_activation_sample = 100
bip34_activation_threshold = 51
bip34_enforcement_threshold = 75
bip34_freeze = 21111
bip65_freeze = 581885
bip66_freeze = 330776
bip9_bit0_active_checkpoint = 00000000025e930139bac5c6c31a403776da130831ab85be56578f3fa75369bb:770112
bip9_bit1_active_checkpoint = 00000000002b980fcd729daaa248fd9316a5200e9b367f4ff2c42453e84201ca:834624
bip9_bit2_active_checkpoint = 000000000000eb906ab072652b86b05a1afeb95df53ed5c5a63aa3574e1f1b33:2011968
checkpoint = 000000002a936ca763904c3c35fce2f3556c559c0214345d31b1bcebf76acb70:546
genesis_block = 0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4adae5494dffff001d1aa4ae180101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4d04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73ffffffff0100f2052a01000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000
milestone = 0000000000010c0090875c05870eed86761b7cde2c03e69d04e5314f6ff59341:5100000
minimum_work = 000000000000000000000000000000000000000000000b6a51f415a67c0da307

[forks]
difficult = false

[inbound]
bind = 127.0.0.1:18333

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

[table.strong]
expected = 536643888
size = 59030828

[table.candidate]
buckets = 5100001

[table.confirmed]
buckets = 5100001

[table.state]
buckets = 5100001

[table.scan]
buckets = 5100001

[admin]
bind = 0.0.0.0:18080
safe = 0.0.0.0:18043

[native]
bind = 0.0.0.0:18180
safe = 0.0.0.0:18143

[bitcoind]
bind = 0.0.0.0:18280
safe = 0.0.0.0:18243

[electrum]
bind = 0.0.0.0:18380
safe = 0.0.0.0:18343

[bitcoind_zmq]
bind = 0.0.0.0:18680
safe = 0.0.0.0:18643

[btcd]
bind = 0.0.0.0:18780
safe = 0.0.0.0:18743

[sparrow]
bind = 0.0.0.0:18880
safe = 0.0.0.0:18843

[esplora]
bind = 0.0.0.0:18980
safe = 0.0.0.0:18943
```

- `[bitcoin]` replaces the chain parameters: genesis block, soft fork
  activations, checkpoint, milestone and minimum work. The milestone at
  5,100,000 bypasses script validation below it.
- `forks.difficult = false` allows testnet's minimum difficulty blocks.
- `peer.identifier` is the testnet3 network magic, and `[outbound]`
  replaces the mainnet seeds.
- `[wallet]` sets the testnet address and key prefixes.
- `[table.*]` sizes the store for the chain at 5.1 million blocks.
  `node.maximum_concurrency` raises the download window, since testnet blocks
  are small.
- The service sections move each service to the testnet3 ports of the
  port plan, 18043–18980 ([§6](index#6-ports)). A service
  is still off until its `connections` is nonzero.
