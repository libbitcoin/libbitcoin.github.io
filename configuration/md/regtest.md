# Regtest

Regtest is a private test chain with minimal difficulty, for local
testing.

These settings have not yet been verified.

Save the settings below as `regtest.cfg` and start the node with it:

```
$ bs -c regtest.cfg
```

The store is created in a `regtest` directory under the working
directory, apart from any mainnet store.

Without a configuration file, `bs -n regtest` creates a store with the same
regtest settings in the `bitcoin` directory. Later runs read the network
from that store, so they need neither `-n` nor a configuration file.

```ini
[database]
path = regtest

[bitcoin]
bip16_activation_time = 1329264000
bip30_deactivate_checkpoint = 0000000000000000000000000000000000000000000000000000000000000000:0
bip30_reactivate_height = 0
bip34_activation_sample = 0
bip34_activation_threshold = 0
bip34_enforcement_threshold = 0
bip34_freeze = 100000000
bip65_freeze = 1351
bip66_freeze = 1251
bip9_bit0_active_checkpoint = 0f9188f13cb7b2c71f2a335e3a4fc328bf5beb436012afca590b1a11466e2206:0
bip9_bit1_active_checkpoint = 0f9188f13cb7b2c71f2a335e3a4fc328bf5beb436012afca590b1a11466e2206:0
bip9_bit2_active_checkpoint = 0f9188f13cb7b2c71f2a335e3a4fc328bf5beb436012afca590b1a11466e2206:0
checkpoint = 0f9188f13cb7b2c71f2a335e3a4fc328bf5beb436012afca590b1a11466e2206:0
genesis_block = 0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4adae5494dffff7f20020000000101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4d04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73ffffffff0100f2052a01000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000
milestone = 0f9188f13cb7b2c71f2a335e3a4fc328bf5beb436012afca590b1a11466e2206:0
minimum_work = 0000000000000000000000000000000000000000000000000000000000000000
proof_of_work_limit = 545259519
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
bind = 127.0.0.1:18444

[outbound]
connections = 0
host_pool_capacity = 0

[manual]
peer = 127.0.0.1:18445

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

# [table.scan]
# buckets = 10001
```

- `[bitcoin]` sets the regtest genesis block and difficulty limit, all
  soft forks active from genesis, and a 150 block subsidy interval.
  There are no checkpoints beyond genesis and no minimum work.
- `forks.retarget = false` disables difficulty retargeting.
- `peer.identifier` is the regtest network magic.
- `[wallet]` sets the regtest address and key prefixes used by the server
  ([Settings Reference](reference#6-wallet)).
- `bs` does not mine, so blocks come from a peer.
- `[outbound]` disables seeding and outbound connections.
- `[manual]` connects to a local node that generates blocks, here on port
  18445 since `bs` listens on 18444.
- `[table.*]` keeps the store small, since the mainnet defaults
  preallocate for the mainnet chain.
- `[table.scan]` is commented out because it enables silent payments
  ([§5.14](index#514-silent-payments)). Uncomment it to index them.
