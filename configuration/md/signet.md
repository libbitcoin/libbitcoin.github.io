# Signet

Signet is a public test network whose blocks are signed by its operators
instead of being mined competitively, so it produces blocks steadily, about
321,000 to date.

Save the settings below as `signet.cfg` and start the node with it:

```
$ bs -c signet.cfg
```

The store is created in a `signet` directory under the working directory,
apart from any mainnet store.

```ini
[database]
path = signet

[bitcoin]
bip16_activation_time = 1329264000
bip30_deactivate_checkpoint = 00000086d6b2636cb2a392d45edc4ec544a10024d30141c9adf4bfd9de533b53:1
bip30_reactivate_height = 486000000
bip34_activation_sample = 100
bip34_activation_threshold = 51
bip34_enforcement_threshold = 75
bip34_freeze = 1
bip65_freeze = 1
bip66_freeze = 1
bip9_bit0_active_checkpoint = 00000086d6b2636cb2a392d45edc4ec544a10024d30141c9adf4bfd9de533b53:1
bip9_bit1_active_checkpoint = 00000086d6b2636cb2a392d45edc4ec544a10024d30141c9adf4bfd9de533b53:1
bip9_bit2_active_checkpoint = 00000086d6b2636cb2a392d45edc4ec544a10024d30141c9adf4bfd9de533b53:1
checkpoint = 00000008819873e925422c1ff0f99f7cc9bbb232af63a077a480a3633bee1ef6:0
genesis_block = 0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a008f4d5fae77031e8ad222030101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4d04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73ffffffff0100f2052a01000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000
milestone = 00000002a5e0ba0498f1e9f4591af0b66b63c654665efe65206fd0ae7bbaf923:321295
minimum_work = 00000000000000000000000000000000000000000000000000001090e9dc1520
proof_of_work_limit = 503543726
signet_challenge = 1 [03ad5e0edad18cb1f0fc0d28a3d4f1f3e445640337489abb10404f2d1e086be430] [0359ef5021964fe22d6f8e05b2463c9540ce96883fe3b278760f048f5189f2e6c4] 2 checkmultisig

[forks]
signet = true

[peer]
identifier = 1087308554

[wallet]
hd_private_prefix = 70615956
hd_public_prefix = 70617039
p2kh_prefix = 111
p2sh_prefix = 196
silent_prefix = tsp
wif_prefix = 239
witness_prefix = tb

[inbound]
bind = 127.0.0.1:38333

[outbound]
seed = seed.signet.bitcoin.sprovoost.nl:38333
seed = seed.signet.achownodes.xyz:38333

[table.header]
expected = 330000

[table.txs]
buckets = 330001

[table.candidate]
buckets = 330001

[table.confirmed]
buckets = 330001

[table.state]
buckets = 330001

# [table.scan]
# buckets = 330001
```

- `[bitcoin]` replaces the chain parameters: genesis block, soft fork
  activations, checkpoint, milestone, minimum work and proof of work limit.
- `bitcoin.signet_challenge` is the script that each block's signature must
  satisfy, here a 1 of 2 multisig of the signet operators.
- `forks.signet` requires the block signatures (BIP325).
- `peer.identifier` is the signet network magic.
- `[outbound]` replaces the mainnet seeds.
- `[wallet]` sets the testnet address and key prefixes used by the server
  ([Settings Reference](reference#6-wallet)).
- `[table.*]` sizes the chain-height tables for about 330,000 blocks.
- `[table.scan]` is commented out because it enables silent payments
  ([§5.14](index#514-silent-payments)). Uncomment it to index them.
