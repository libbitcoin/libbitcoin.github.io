# Settings Reference

`bs --settings` displays every setting in its section, each with a
comment giving its description and default, followed by its configured
value. With `--config`, a setting configured to other than its default is
marked by a comment. The sections below are the defaults, grouped by
area.

## 1. `[log]`

Logging: which kinds of events are logged (unless changed at the console), and where log files are written.

```ini
[log]
# Enable application logging, defaults to 'true'.
application = true
# Enable local fault logging, defaults to 'true'.
fault = true
# The maximum byte size of each pair of rotated log files, defaults to '1000000'.
maximum_size = 1000000
# Enable news logging, defaults to 'true'.
news = true
# The log files directory, defaults to empty.
path =
# Enable protocol logging, defaults to 'false'.
protocol = false
# Enable proxy logging, defaults to 'false'.
proxy = false
# Enable quitting logging, defaults to 'false'.
quitting = false
# Enable remote fault logging, defaults to 'true'.
remote = true
# Enable session logging, defaults to 'true'.
session = true
# Path to a directory containing windows symbols (.pdb) files, defaults to empty.
symbols =
# Enable verbose logging, defaults to 'false'.
verbose = false
```

## 2. `[database]`

The store: its directory and store-wide options.

```ini
[database]
# Minimum transactions for a silent payment scan to use the GPU, defaults to '65536'.
gpu_scan_minimum = 65536
# The interval depth for merkle proof optimization, defaults to '11'.
interval_depth = 11
# Save unconfirmable block state (prevents revalidation), defaults to 'true'.
mark_unconfirmable = true
# The blockchain database directory, defaults to 'bitcoin'.
path = bitcoin
# Allow individual non-validation queries to use all CPUs, defaults to 'true'.
turbo = true
```

## 3. Store tables (`[table.*]`)

The sizing of each store table. These are advanced settings and are rarely changed (§9).

```ini
[table.candidate]
# The number of buckets provisioned in the candidate table head, defaults to '950001'.
buckets = 950001
# The percentage expansion of the candidate table head, defaults to '1'.
rate = 1

[table.confirmed]
# The number of buckets provisioned in the confirmed table head, defaults to '950001'.
buckets = 950001
# The percentage expansion of the confirmed table head, defaults to '1'.
rate = 1

[table.duplicate]
# The minimum number of buckets in the duplicate table head, defaults to '1024'.
buckets = 1024
# The expected element count of the duplicate table, defaults to '0'.
expected = 0
# The percentage expansion of the duplicate table, defaults to '1'.
rate = 1
# The minimum allocation of the duplicate table body, defaults to '0'.
size = 0

[table.ecdsa]
# The percentage expansion of each batch_ecdsa table body, defaults to '1'.
rate = 1
# The minimum allocation of each batch_ecdsa table body, defaults to '0'.
size = 0

[table.filter_bk]
# The number of buckets in the filter_bk table head, defaults to '0' (0 disables).
buckets = 0
# The percentage expansion of the filter_bk table body, defaults to '1'.
rate = 1
# The minimum allocation of the filter_bk table body, defaults to '0'.
size = 0

[table.filter_tx]
# The number of buckets in the filter_tx table head, defaults to '0' (0 disables).
buckets = 0
# The percentage expansion of the filter_tx table body, defaults to '1'.
rate = 1
# The minimum allocation of the filter_tx table body, defaults to '0'.
size = 0

[table.header]
# The number of buckets in the header table head, dynamic default.
buckets = 385181
# The expected element count of the header table, defaults to '962953'.
expected = 962953
# The percentage expansion of the header table body, defaults to '1'.
rate = 1
# The minimum allocation of the header table body, defaults to '124220679'.
size = 124220679

[table.input]
# The percentage expansion of the input table body, defaults to '1'.
rate = 1
# The minimum allocation of the input table body, defaults to '67269346'.
size = 67269346

[table.ins]
# The number of buckets in the ins table head, dynamic default.
buckets = 1345386900
# The expected element count of the ins table, defaults to '3363467251'.
expected = 3363467251
# The percentage expansion of the ins table body, defaults to '1'.
rate = 1
# The minimum allocation of the ins table body, defaults to '1749002971'.
size = 1749002971

[table.output]
# The percentage expansion of the output table body, defaults to '1'.
rate = 1
# The minimum allocation of the output table body, defaults to '1278023220'.
size = 1278023220

[table.outs]
# The number of buckets in the outs table head, dynamic default (0 disables address index).
buckets = 748385817
# The expected element count of the outs table, defaults to '3741929086'.
expected = 3741929086
# The percentage expansion of the outs table body, defaults to '1'.
rate = 1
# The minimum allocation of the outs table body, defaults to '336773618'.
size = 336773618

[table.pool]
# The number of buckets in the pool table head, dynamic default (0 disables).
buckets = 4000000
# The expected element count of the pool table, defaults to '10000000'.
expected = 10000000
# The percentage expansion of the pool table body, defaults to '1'.
rate = 1
# The minimum allocation of the pool table body, defaults to '0'.
size = 0

[table.presilent]
# The percentage expansion of each batch_presilent table body, defaults to '1'.
rate = 1
# The minimum allocation of each batch_presilent table body, defaults to '0'.
size = 0

[table.prevalid]
# The percentage expansion of each batch_prevalid table body, defaults to '1'.
rate = 1
# The minimum allocation of each batch_prevalid table body, defaults to '0'.
size = 0

[table.prevout]
# The minimum number of buckets in the prevout table head, defaults to '0'.
buckets = 0
# The percentage expansion of the prevout table, defaults to '1'.
rate = 1
# The minimum allocation of the prevout table body, defaults to '0'.
size = 0

[table.scan]
# The number of buckets provisioned in the scan table head, defaults to '950001'.
buckets = 950001
# The percentage expansion of the scan table body, defaults to '1'.
rate = 1
# The minimum allocation of the scan table body, defaults to '0'.
size = 0

[table.schnorr]
# The percentage expansion of each batch_schnorr table body, defaults to '1'.
rate = 1
# The minimum allocation of each batch_schnorr table body, defaults to '0'.
size = 0

[table.silent]
# The percentage expansion of each batch_silent table body, defaults to '1'.
rate = 1
# The minimum allocation of each batch_silent table body, defaults to '0'.
size = 0

[table.spends]
# The percentage expansion of the spends table body, defaults to '1'.
rate = 1
# The minimum allocation of the spends table body, defaults to '0'.
size = 0

[table.state]
# The number of buckets provisioned in the state table head, defaults to '950001'.
buckets = 950001
# The percentage expansion of the state table head, defaults to '1'.
rate = 1

[table.strong]
# The number of buckets provisioned in the strong table head, defaults to '1359871695'.
buckets = 1359871695
# The percentage expansion of the strong table head, defaults to '1'.
rate = 1

[table.tx]
# The number of buckets in the tx table head, dynamic default.
buckets = 543948678
# The expected element count of the tx table, defaults to '1359871695'.
expected = 1359871695
# The percentage expansion of the tx table body, defaults to '1'.
rate = 1
# The minimum allocation of the tx table body, defaults to '870317885'.
size = 870317885

[table.txs]
# The number of buckets in the txs table head, defaults to '950001'.
buckets = 950001
# The percentage expansion of the txs table body, defaults to '1'.
rate = 1
# The minimum allocation of the txs table body, defaults to '54471017'.
size = 54471017

[table.wtxid]
# The number of buckets in the wtxid table head, dynamic default (0 disables).
buckets = 4000000
# The expected element count of the wtxid table, defaults to '10000000'.
expected = 10000000
# The percentage expansion of the wtxid table body, defaults to '1'.
rate = 1
# The minimum allocation of the wtxid table body, defaults to '0'.
size = 0
```

## 4. `[bitcoin]`

Chain parameters: genesis block, soft fork activation, checkpoints, milestone and minimum work. The defaults are mainnet, and change only for another chain.

```ini
[bitcoin]
# The activation time for bip16 in unix time, defaults to '1333238400'.
bip16_activation_time = 1333238400
# The hash:height checkpoint for bip30 deactivation, defaults to '000000000000024b89b42a942fe0d9fea3bb44ab7bd1b19115dd6a759c0808b8:227931'.
bip30_deactivate_checkpoint = 000000000000024b89b42a942fe0d9fea3bb44ab7bd1b19115dd6a759c0808b8:227931
# The height for bip30 reactivation, defaults to '1983702'.
bip30_reactivate_height = 1983702
# The number of blocks considered for bip34 style soft fork activation, defaults to '1000'.
bip34_activation_sample = 1000
# The number of new version blocks required for bip34 style soft fork activation, defaults to '750'.
bip34_activation_threshold = 750
# The number of new version blocks required for bip34 style soft fork enforcement, defaults to '950'.
bip34_enforcement_threshold = 950
# The block height to freeze the bip34 softfork for bip90, defaults to '227931'.
bip34_freeze = 227931
# The block height to freeze the bip65 softfork for bip90, defaults to '388381'.
bip65_freeze = 388381
# The block height to freeze the bip66 softfork for bip90, defaults to '363725'.
bip66_freeze = 363725
# The hash:height checkpoint for bip9 bit0 activation, defaults to '000000000000000004a1b34462cb8aeebd5799177f7a29cf28f2d1961716b5b5:419328'.
bip9_bit0_active_checkpoint = 000000000000000004a1b34462cb8aeebd5799177f7a29cf28f2d1961716b5b5:419328
# The hash:height checkpoint for bip9 bit1 activation, defaults to '0000000000000000001c8018d9cb3b742ef25114f27563e3fc4a1902167f9893:481824'.
bip9_bit1_active_checkpoint = 0000000000000000001c8018d9cb3b742ef25114f27563e3fc4a1902167f9893:481824
# The hash:height checkpoint for bip9 bit2 activation, defaults to '0000000000000000000687bca986194dc2c1f949318629b44bb54ec0a94d8244:709632'.
bip9_bit2_active_checkpoint = 0000000000000000000687bca986194dc2c1f949318629b44bb54ec0a94d8244:709632
# The target block period, defaults to '600'.
block_spacing_seconds = 600
# The blockchain checkpoints, defaults to the consensus set.
checkpoint = 00000000000000004d9b4ef50f0f9d686fd69db2e03af35a100370c64632a983:295000
checkpoint = 0000000000000001ae8c72a0b0c301f67e3afca10e819efa9041e458e9bd7e40:279000
checkpoint = 000000000000003887df1f29024b06fc2200b55f8af8f35453d7be294df2d214:250000
checkpoint = 00000000000001c108384350f74090433e7fcf79a606b8e797f065b130575932:225430
checkpoint = 00000000000001b4f4b433e81ee46494af945cf96014816a4e2370f11b23df4e:216116
checkpoint = 000000000000048b95347e83192f69cf0366076336c639f9b7228e9ba171342e:210000
checkpoint = 000000000000059f452a5f7340de6682a977387c17010ff6e6c3bd83ca8b1317:193000
checkpoint = 000000000000099e61ea72015e79632f216fe6cb33d7899acb35b75c8303b763:168000
checkpoint = 00000000000005b12ffd4cd315cd34ffd4a594f430ac814c91184a0d42d2b0fe:134444
checkpoint = 00000000000291ce28027faea320c8d2b054b2e0fe44a773f3eefb151d6bdc97:105000
checkpoint = 0000000000573993a3c9e41ce34471c079dcf5f52a0e824a81e7f953b8661a20:74000
checkpoint = 000000002dd5588a74784eaa7ab0507a18ad16a236e7b1ce69f00d7ddfb5d0a6:33333
checkpoint = 0000000069e244f73d78e8fd29ba2fd2ed618bd6fa2ee92559f542fdb26e7c1d:11111
# The hexadecimal encoding of the genesis block, defaults to mainnet.
genesis_block = 0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c0101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4d04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73ffffffff0100f2052a01000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000
# The initial block subsidy, defaults to '50'.
initial_block_subsidy_bitcoin = 50
# A block presumed to be valid but not required to be present, defaults to '000000000000000000010b93c9ea1c29fea277383f0f7d1f26de8b5802e885ff:950000'.
milestone = 000000000000000000010b93c9ea1c29fea277383f0f7d1f26de8b5802e885ff:950000
# The minimum work for any branch to be considered valid, defaults to '000000000000000000000000000000000000000052b2559353df4117b7348b64'.
minimum_work = 000000000000000000000000000000000000000052b2559353df4117b7348b64
# The proof of work limit, defaults to '486604799'.
proof_of_work_limit = 486604799
# The difficulty retargeting factor, defaults to '4'.
retargeting_factor = 4
# The difficulty retargeting period, defaults to '1209600'.
retargeting_interval_seconds = 1209600
# The subsidy halving period, defaults to '210000'.
subsidy_interval = 210000
# The future timestamp allowance, defaults to '7200'.
timestamp_limit_seconds = 7200
```

## 5. `[forks]`

The consensus rules enforced. The defaults are mainnet.

```ini
[forks]
# Add check-sequence-verify op code, defaults to 'true' (soft fork).
bip112 = true
# Use median time past for locktime, defaults to 'true' (soft fork).
bip113 = true
# Segregated witness consensus layer, defaults to 'true' (soft fork).
bip141 = true
# Witness version 0 (segwit), defaults to 'true' (soft fork).
bip143 = true
# Prevent dummy value malleability, defaults to 'true' (soft fork).
bip147 = true
# Add pay-to-script-hash processing, defaults to 'true' (soft fork).
bip16 = true
# Disallow collision of unspent transaction hashes, defaults to 'true' (soft fork).
bip30 = true
# Require coinbase input includes block height, defaults to 'true' (soft fork).
bip34 = true
# Witness version 1 (taproot), defaults to 'true' (soft fork).
bip341 = true
# Validation of taproot script, defaults to 'true' (soft fork).
bip342 = true
# Finite monetary supply, defaults to 'true' (soft fork).
bip42 = true
# Add check-locktime-verify op code, defaults to 'true' (soft fork).
bip65 = true
# Require strict signature encoding, defaults to 'true' (soft fork).
bip66 = true
# Add relative locktime enforcement, defaults to 'true' (soft fork).
bip68 = true
# Assume bip34, bip65, and bip66 activation if enabled, defaults to 'true' (hard fork).
bip90 = true
# Assume block_storm_patch activation if enabled, defaults to 'false' (testnet4).
block_storm_patch = false
# Require difficult blocks, defaults to 'true' (use false for testnet).
difficult = true
# Fix target overflow for very low difficulty, defaults to 'false' (litecoin).
ltc_retarget_overflow_patch = false
# Use scrypt hashing for proof of work, defaults to 'false' (litecoin).
ltc_scrypt_proof_of_work = false
# Fix time warp bug, defaults to 'false' (litecoin).
ltc_time_warp_patch = false
# Retarget difficulty, defaults to 'true' (use false for regtest).
retarget = true
# Assume time_warp_patch activation if enabled, defaults to 'false' (testnet4).
time_warp_patch = false
```

## 6. `[wallet]`

Address and key prefixes, which the server uses to read and write
addresses, keys and descriptors in client requests and responses:

- The Bitcoind and BTCD interfaces use all of them, for addresses, keys
  and descriptors.
- The Electrum and Esplora interfaces use the address prefixes.
- The Sparrow interface uses the silent payment prefix.

They do not affect the node or the store. The defaults are mainnet, and a
test chain sets its own, as on the [Testnet3](testnet3),
[Testnet4](testnet4), [Signet](signet) and [Regtest](regtest) pages.

```ini
[wallet]
# The extended private key prefix, defaults to '76066276' (use '70615956' for testnet).
hd_private_prefix = 76066276
# The extended public key prefix, defaults to '76067358' (use '70617039' for testnet).
hd_public_prefix = 76067358
# The pay-to-public-key-hash address prefix, defaults to '0' (use '111' for testnet).
p2kh_prefix = 0
# The pay-to-script-hash address prefix, defaults to '5' (use '196' for testnet).
p2sh_prefix = 5
# The silent payment address prefix, defaults to 'sp' (use 'tsp' for testnet).
silent_prefix = sp
# The wallet import format prefix, defaults to '128' (use '239' for testnet).
wif_prefix = 128
# The witness address prefix, defaults to 'bc' (use 'tb' for testnet).
witness_prefix = bc
```

## 7. `[node]`

The node: validation threads, batching and GPU use, the download window, fee policy, and what is served to peers.

```ini
[node]
# Allowable underperformance standard deviation, defaults to '1.5' (0 disables).
allowed_deviation = 1.5
# Limit of per channel cached peer block and tx announcements, to avoid replay, defaults to '42'.
announcement_cache = 42
# Count of silent payment transactions to index in each batch, defaults to '1000000' (0 disables).
batch_silent = 1000000
# Count of signatures to verify in each batch, defaults to '1000000' (0 disables).
batch_verify = 1000000
# Maximum percent of a compact block not pooled to fill it, defaults to '50'.
compact_missing_percent = 50
# Time to await a compact block fill before downloading the block, defaults to '10' (0 disables).
compact_timeout_seconds = 10
# Time from present that blocks are considered current, defaults to '1440' (0 disables).
currency_window_minutes = 1440
# Block inbound peer/client (excluding admin/native) until current, defaults to 'true'.
delay_inbound = true
# Fee estimation horizon, limited to 1008, defaults to '0' (0 disables).
fee_estimate_horizon = 0
# Limit block service to recent blocks, defaults to 'false'.
limited_blocks = false
# Maximum number of blocks to download concurrently, defaults to '50000' (0 disables).
maximum_concurrency = 50000
# Maximum block height to populate, defaults to '0' (unlimited).
maximum_height = 0
# Set the process to high memory priority, defaults to 'true'.
memory_priority = true
# Minimum fee rate increment for conflicting tx acceptance, defaults to '0.0'.
minimum_bump_rate = 0.0
# Minimum fee rate for non-conflicting tx acceptance, defaults to '0.000001'.
minimum_fee_rate = 0.000001
# Serve blocks to network connections, defaults to 'true'.
provide_blocks = true
# Serve client filters to network connections, defaults to 'false'.
provide_filters = false
# Provide opportunistic connection encryption, defaults to 'false'.
provide_privacy = false
# Serve witness data to network connections, defaults to 'true'.
provide_witness = true
# Require block service of outbound connections, defaults to 'true'.
require_blocks = true
# Require witness service of outbound connections, defaults to 'true'.
require_witness = true
# Sampling period for drop of stalled channels, defaults to '10' (0 disables).
sample_period_seconds = 10
# Minimum height of silent payment indexation, defaults to '4294967295'.
silent_start_height = 4294967295
# Set validation threads to high processing priority, defaults to 'true'.
thread_priority = true
# The number of threads in the validation threadpool, defaults to '0' (hardware threads).
threads = 0
# Use the GPU where available, defaults to 'true'.
use_gpu = true
```

## 8. `[network]`

Settings shared by all P2P connections: threads, connection timing, send rate, and address allow and deny lists.

```ini
[network]
# IP address to disallow, allows all others, multiple allowed.
#blacklist =
# The time limit for connection establishment, defaults to '5'.
connect_timeout_seconds = 5
# The per channel send rate limit in bytes per second, defaults to '0' (unlimited).
rate_limit = 0
# The time delay for failed connection retry, defaults to '1'.
retry_timeout_seconds = 1
# The minimum number of threads in the network threadpool, defaults to '0' (hardware threads, at most 32).
threads = 0
# IP address to allow, prohibits all others, multiple allowed.
#whitelist =
```

## 9. `[peer]`

The P2P protocol: version range, supported messages, address gossip, and the network identifier.

```ini
[peer]
# The lower bound for address selection divisor, defaults to '5'.
address_lower = 5
# The upper bound for address selection divisor, defaults to '10'.
address_upper = 10
# The time between ping messages, defaults to '10' (0 disables).
channel_heartbeat_minutes = 10
# Enable address gossip, defaults to 'true'.
enable_address = true
# Enable privacy network (Tor and I2P) address gossip, defaults to 'true'.
enable_address_v2 = true
# Enable alert messages, defaults to 'false'.
enable_alert = false
# Enable compact block messages, defaults to 'true'.
enable_compact = true
# Enable memory pool messages, defaults to 'false'.
enable_memory_pool = false
# Enable not found messages, defaults to 'true'.
enable_not_found = true
# Enable reject messages, defaults to 'false'.
enable_reject = false
# Enable transaction relay, defaults to 'true'.
enable_relay = true
# Enable witness transaction identifier relay, defaults to 'false'.
enable_witness_tx = false
# Gossip i2p addresses, defaults to 'false'.
gossip_i2p = false
# Gossip internet protocol version 4 (IPv4) addresses, defaults to 'true'.
gossip_ipv4 = true
# Gossip internet protocol version 6 (IPv6) addresses, defaults to 'false'.
gossip_ipv6 = false
# Gossip tor (onion) addresses, defaults to 'false'.
gossip_tor = false
# The time limit to complete the connection handshake, defaults to '15' (0 disables).
handshake_timeout_seconds = 15
# The magic number for message headers, defaults to '3652501241'.
identifier = 3652501241
# The advertised services that cause a peer to be dropped, defaults to '268435632'.
invalid_services = 268435632
# The maximum allowable channel clock skew, defaults to '120'.
maximum_skew_minutes = 120
# The peer address cache file directory, defaults to empty.
path =
# The maximum network protocol version, defaults to '70016'.
protocol_maximum = 70016
# The minimum network protocol version, defaults to '31800'.
protocol_minimum = 31800
# The node user agent string, defaults to '/libbitcoin:4.0.10255/'.
user_agent = /libbitcoin:4.0.10255/
# Validate the checksum of network messages, defaults to 'false'.
validate_checksum = false
```

## 10. `[outbound]`

Connections the node makes to peers: count, seeds, the address pool, and a SOCKS proxy.

```ini
[outbound]
# IP address to bind outbound connections, multiple allowed, defaults to empty.
#bind =
# The number of concurrent attempts to establish one connection, defaults to '5'.
connect_batch_size = 5
# The time limit for connection establishment, defaults to '0' (network controls).
connect_timeout_seconds = 0
# The target number of outgoing network connections, defaults to '100'.
connections = 100
# The target number of outgoing connections when current, defaults to '10' (0 disables).
current_connections = 10
# The age limit for any connection, defaults to '60' (0 disables).
expiration_minutes = 60
# The maximum number of peer hosts in the pool, defaults to '10000'.
host_pool_capacity = 10000
# The inactivity time limit for any connection, defaults to '10' (0 disables).
inactivity_minutes = 10
# The maximum write backlog of a channel, defaults to '1048576'.
maximum_backlog = 1048576
# The maximum allowed request size, defaults to '4000000'.
maximum_request = 4000000
# The minimum retained read buffer size, defaults to '4096'.
minimum_buffer = 4096
# The socks5 proxy password (optional).
password =
# The send rate limit in bytes per second, defaults to '0' (network controls).
rate_limit = 0
# A seed node for initializing the host pool, multiple allowed.
seed = seed.bitcoin.sipa.be:8333
seed = dnsseed.bluematt.me:8333
seed = seed.bitcoin.jonasschnelli.ch:8333
seed = seed.btc.petertodd.net:8333
seed = seed.bitcoin.sprovoost.nl:8333
seed = dnsseed.emzy.de:8333
seed = seed.bitcoin.wiz.biz:8333
seed = seed.mainnet.achownodes.xyz:8333
# The time limit for obtaining seed connections and addresses, defaults to '30'.
seeding_timeout_seconds = 30
# The socks5 proxy endpoint (port required).
socks = localhost
# The socks5 proxy username (optional).
username =
```

## 11. `[inbound]`

Connections peers make to the node: listening addresses, count, and I2P.

```ini
[inbound]
# IP address to bind for listening, multiple allowed, defaults to '0.0.0.0:8333' (all IPv4).
bind = 0.0.0.0:8333
# The time limit for connection establishment, defaults to '0' (network controls).
connect_timeout_seconds = 0
# The target number of incoming network connections, defaults to '100'.
connections = 100
# Allow connections from the node to itself, defaults to 'false'.
enable_loopback = false
# The age limit for any connection, defaults to '60' (0 disables).
expiration_minutes = 60
# The inactivity time limit for any connection, defaults to '10' (0 disables).
inactivity_minutes = 10
# The i2p destination private key file path, created if not existing.
key_path =
# The maximum write backlog of a channel, defaults to '1048576'.
maximum_backlog = 1048576
# The maximum allowed request size, defaults to '4000000'.
maximum_request = 4000000
# The minimum retained read buffer size, defaults to '4096'.
minimum_buffer = 4096
# The sam bridge password (optional).
password =
# The send rate limit in bytes per second, defaults to '0' (network controls).
rate_limit = 0
# The i2p sam bridge endpoint (port required).
sam = localhost
# Address to advertise, multiple allowed.
#self =
# The sam bridge username (optional).
username =
```

## 12. `[manual]`

Persistent connections to specific peers.

```ini
[manual]
# IP address to bind manual connections, multiple allowed, defaults to empty.
#bind =
# The time limit for connection establishment, defaults to '0' (network controls).
connect_timeout_seconds = 0
# The age limit for any connection, defaults to '60' (0 disables, will attempt reconnect).
expiration_minutes = 60
# The inactivity time limit for any connection, defaults to '10' (0 disables, will attempt reconnect).
inactivity_minutes = 10
# The maximum write backlog of a channel, defaults to '1048576'.
maximum_backlog = 1048576
# The maximum allowed request size, defaults to '4000000'.
maximum_request = 4000000
# The minimum retained read buffer size, defaults to '4096'.
minimum_buffer = 4096
# The socks5 proxy password (optional).
password =
# A persistent peer node, multiple allowed.
#peer =
# The send rate limit in bytes per second, defaults to '0' (network controls).
rate_limit = 0
# The socks5 proxy endpoint (port required).
socks = localhost
# The socks5 proxy username (optional).
username =
```

## 13. `[admin]`

The administrative web and websocket interface.

```ini
[admin]
# Allow requests from opaque origin (see CORS), defaults to 'false'.
allow_opaque_origin = false
# IP address to bind, multiple allowed, defaults to empty (disabled).
#bind =
# The trusted client certificate directory (*.PEM), enables client authentication.
cert_auth =
# The path to the server certificate file (.PEM), defaults to empty.
cert_path =
# The time limit for connection establishment, defaults to '0' (network controls).
connect_timeout_seconds = 0
# The required maximum number of connections, defaults to '0'.
connections = 0
# The path of the default source page, defaults to 'index.html'.
default = index.html
# The maximum connection duration, defaults to '60'.
expiration_minutes = 60
# The host name (http verification), multiple allowed, defaults to empty (disabled).
#host =
# The idle timeout (http keep-alive), defaults to '10'.
inactivity_minutes = 10
# The password to decrypt the server private key file (.PEM), optional.
key_pass =
# The path to the server private key file (.PEM), defaults to empty.
key_path =
# The maximum write backlog of a channel, defaults to '10485760'.
maximum_backlog = 10485760
# The maximum json response buffer size, defaults to '65536'.
maximum_buffer = 65536
# The maximum allowed request size, defaults to '4000000'.
maximum_request = 4000000
# The minimum retained read buffer size, defaults to '4096'.
minimum_buffer = 4096
# The allowed origin (see CORS), multiple allowed, defaults to empty (disabled).
#origin =
# The required root path of source files to be served, defaults to empty.
path =
# The send rate limit in bytes per second, defaults to '0' (network controls).
rate_limit = 0
# IP address to secure bind, multiple allowed, defaults to empty (disabled).
#safe =
# The server name (http header), defaults to 'libbitcoin/4'.
server = libbitcoin/4
```

## 14. `[native]`

The native libbitcoin REST and websocket interface, and its web pages.

```ini
[native]
# Allow requests from opaque origin (see CORS), defaults to 'false'.
allow_opaque_origin = false
# IP address to bind, multiple allowed, defaults to empty (disabled).
#bind =
# The trusted client certificate directory (*.PEM), enables client authentication.
cert_auth =
# The path to the server certificate file (.PEM), defaults to empty.
cert_path =
# The time limit for connection establishment, defaults to '0' (network controls).
connect_timeout_seconds = 0
# The required maximum number of connections, defaults to '0'.
connections = 0
# The path of the default source page, defaults to 'index.html'.
default = index.html
# The maximum connection duration, defaults to '60'.
expiration_minutes = 60
# The host name (http verification), multiple allowed, defaults to empty (disabled).
#host =
# The idle timeout (http keep-alive), defaults to '10'.
inactivity_minutes = 10
# The password to decrypt the server private key file (.PEM), optional.
key_pass =
# The path to the server private key file (.PEM), defaults to empty.
key_path =
# The maximum write backlog of a channel, defaults to '1048576'.
maximum_backlog = 1048576
# The maximum json response buffer size, defaults to '65536'.
maximum_buffer = 65536
# The maximum allowed request size, defaults to '4000000'.
maximum_request = 4000000
# The minimum retained read buffer size, defaults to '4096'.
minimum_buffer = 4096
# The allowed origin (see CORS), multiple allowed, defaults to empty (disabled).
#origin =
# The required root path of source files to be served, defaults to empty.
path =
# The send rate limit in bytes per second, defaults to '0' (network controls).
rate_limit = 0
# IP address to secure bind, multiple allowed, defaults to empty (disabled).
#safe =
# The server name (http header), defaults to 'libbitcoin/4'.
server = libbitcoin/4
# Enable websocket interface, defaults to 'true'.
websocket = true
```

## 15. `[bitcoind]`

The bitcoind JSON-RPC and REST interface.

```ini
[bitcoind]
# Allow requests from opaque origin (see CORS), defaults to 'false'.
allow_opaque_origin = false
# IP address to bind, multiple allowed, defaults to empty (disabled).
#bind =
# The trusted client certificate directory (*.PEM), enables client authentication.
cert_auth =
# The path to the server certificate file (.PEM), defaults to empty.
cert_path =
# The time limit for connection establishment, defaults to '0' (network controls).
connect_timeout_seconds = 0
# The required maximum number of connections, defaults to '0'.
connections = 0
# The 'username:password[:method,...]' authorization (not secure), multiple allowed.
#credential =
# The maximum connection duration, defaults to '60'.
expiration_minutes = 60
# The host name (http verification), multiple allowed, defaults to empty (disabled).
#host =
# The idle timeout (http keep-alive), defaults to '10'.
inactivity_minutes = 10
# The password to decrypt the server private key file (.PEM), optional.
key_pass =
# The path to the server private key file (.PEM), defaults to empty.
key_path =
# The maximum write backlog of a channel, defaults to '1048576'.
maximum_backlog = 1048576
# The maximum json response buffer size, defaults to '65536'.
maximum_buffer = 65536
# The maximum allowed request size, defaults to '8004096'.
maximum_request = 8004096
# The minimum retained read buffer size, defaults to '4096'.
minimum_buffer = 4096
# The allowed origin (see CORS), multiple allowed, defaults to empty (disabled).
#origin =
# The send rate limit in bytes per second, defaults to '0' (network controls).
rate_limit = 0
# IP address to secure bind, multiple allowed, defaults to empty (disabled).
#safe =
# The server name (http header), defaults to 'libbitcoin/4'.
server = libbitcoin/4
# The subversion identity (getnetworkinfo), defaults to '/libbitcoin:server/'.
subversion = /libbitcoin:server/
# The version identity (getnetworkinfo), defaults to '0.0'.
version = 0.0
```

## 16. `[bitcoind_zmq]`

The bitcoind ZMQ notification interface.

```ini
[bitcoind_zmq]
# IP address to bind, multiple allowed, defaults to empty (disabled).
#bind =
# The Z85 encoded public key of an authorized client, multiple allowed, defaults to empty (all).
#cert =
# The time limit for connection establishment, defaults to '0' (network controls).
connect_timeout_seconds = 0
# The required maximum number of connections, defaults to '0'.
connections = 0
# The Z85 encoded CurveZMQ server secret key, defaults to none (unencrypted).
key =
# The maximum write backlog of a channel, defaults to '33554432'.
maximum_backlog = 33554432
# The maximum allowed request size, defaults to '4000000'.
maximum_request = 4000000
# The maximum topic subscriptions per connection, defaults to '100'.
maximum_subscriptions = 100
# The minimum retained read buffer size, defaults to '4096'.
minimum_buffer = 4096
# The send rate limit in bytes per second, defaults to '0' (network controls).
rate_limit = 0
# IP address to secure (CurveZMQ) bind, multiple allowed, defaults to empty (disabled).
#safe =
```

## 17. `[btcd]`

The btcd JSON-RPC and websocket interface.

```ini
[btcd]
# Allow requests from opaque origin (see CORS), defaults to 'false'.
allow_opaque_origin = false
# IP address to bind, multiple allowed, defaults to empty (disabled).
#bind =
# The trusted client certificate directory (*.PEM), enables client authentication.
cert_auth =
# The path to the server certificate file (.PEM), defaults to empty.
cert_path =
# The time limit for connection establishment, defaults to '0' (network controls).
connect_timeout_seconds = 0
# The required maximum number of connections, defaults to '0'.
connections = 0
# The 'username:password[:method,...]' authorization (not secure), multiple allowed.
#credential =
# The maximum connection duration, defaults to '60'.
expiration_minutes = 60
# The host name (http verification), multiple allowed, defaults to empty (disabled).
#host =
# The idle timeout (http/ws keep-alive), defaults to '10'.
inactivity_minutes = 10
# The password to decrypt the server private key file (.PEM), optional.
key_pass =
# The path to the server private key file (.PEM), defaults to empty.
key_path =
# The maximum write backlog of a channel, defaults to '20971520'.
maximum_backlog = 20971520
# The maximum json response buffer size, defaults to '65536'.
maximum_buffer = 65536
# The maximum number of loadtxfilter watches, defaults to '1000000'.
maximum_filters = 1000000
# The maximum number of address history entries, defaults to '1000000'.
maximum_history = 1000000
# The maximum allowed request size, defaults to '8004096'.
maximum_request = 8004096
# The minimum retained read buffer size, defaults to '4096'.
minimum_buffer = 4096
# The allowed origin (see CORS), multiple allowed, defaults to empty (disabled).
#origin =
# The send rate limit in bytes per second, defaults to '0' (network controls).
rate_limit = 0
# IP address to secure bind, multiple allowed, defaults to empty (disabled).
#safe =
# The server name (http header), defaults to 'libbitcoin/4'.
server = libbitcoin/4
```

## 18. `[electrum]`

The Electrum protocol server.

```ini
[electrum]
# String returned by server.banner, defaults to empty.
banner_message =
# IP address to bind, multiple allowed, defaults to empty (disabled).
#bind =
# The path to the server certificate file (.PEM), defaults to empty.
cert_path =
# The time limit for connection establishment, defaults to '0' (network controls).
connect_timeout_seconds = 0
# The required maximum number of connections, defaults to '0'.
connections = 0
# String returned by server.donation_address, defaults to empty.
donation_address =
# The maximum connection duration, defaults to '60'.
expiration_minutes = 60
# The idle timeout (http keep-alive), defaults to '10'.
inactivity_minutes = 10
# The path to the server private key file (.PEM), defaults to empty.
key_path =
# The maximum write backlog of a channel, defaults to '1048576'.
maximum_backlog = 1048576
# The maximum json response buffer size, defaults to '65536'.
maximum_buffer = 65536
# The maximum allowed headers returned per request, defaults to '20160'.
maximum_headers = 20160
# The maximum number of address history entries upon one subscription, defaults to '1000000'.
maximum_history = 1000000
# The maximum allowed request size, defaults to '8004096'.
maximum_request = 8004096
# The maximum allowed address subscriptions per channel, defaults to '1000000'.
maximum_subscriptions = 1000000
# The minimum retained read buffer size, defaults to '4096'.
minimum_buffer = 4096
# Advertised host:port at which another server can be reached (defaults to empty).
#more_bind =
# Advertised secure host:port at which another server can be reached (defaults to empty).
#more_safe =
# The seconds between unrequested pings, defaults to '0' (disabled).
ping_interval_seconds = 0
# The hex characters of unrequested ping data, defaults to '0'.
ping_size = 0
# Maximum protocol version, defaults to '1.7'.
protocol_maximum = 1.7
# Minimum protocol version, defaults to '1.0'.
protocol_minimum = 1.0
# The send rate limit in bytes per second, defaults to '0' (network controls).
rate_limit = 0
# IP address to secure bind, multiple allowed, defaults to empty (disabled).
#safe =
# Advertised host:port at which this server can be reached (defaults to empty).
#self_bind =
# Advertised secure host:port at which this server can be reached (defaults to empty).
#self_safe =
# String returned by server.version, defaults to '/libbitcoin:4.0.10255/'.
server_name = /libbitcoin:4.0.10255/
```

## 19. `[sparrow]`

The Electrum protocol server with silent payment extensions, for Sparrow.

```ini
[sparrow]
# String returned by server.banner, defaults to empty.
banner_message =
# IP address to bind, multiple allowed, defaults to empty (disabled).
#bind =
# The path to the server certificate file (.PEM), defaults to empty.
cert_path =
# The time limit for connection establishment, defaults to '0' (network controls).
connect_timeout_seconds = 0
# The required maximum number of connections, defaults to '0'.
connections = 0
# String returned by server.donation_address, defaults to empty.
donation_address =
# The maximum connection duration, defaults to '60'.
expiration_minutes = 60
# The idle timeout (http keep-alive), defaults to '10'.
inactivity_minutes = 10
# The path to the server private key file (.PEM), defaults to empty.
key_path =
# The maximum write backlog of a channel, defaults to '1048576'.
maximum_backlog = 1048576
# The maximum json response buffer size, defaults to '65536'.
maximum_buffer = 65536
# The maximum allowed headers returned per request, defaults to '20160'.
maximum_headers = 20160
# The maximum number of address history entries upon one subscription, defaults to '1000000'.
maximum_history = 1000000
# The maximum allowed request size, defaults to '8004096'.
maximum_request = 8004096
# The maximum allowed address subscriptions per channel, defaults to '1000000'.
maximum_subscriptions = 1000000
# The minimum retained read buffer size, defaults to '4096'.
minimum_buffer = 4096
# Advertised host:port at which another server can be reached (defaults to empty).
#more_bind =
# Advertised secure host:port at which another server can be reached (defaults to empty).
#more_safe =
# The seconds between unrequested pings, defaults to '0' (disabled).
ping_interval_seconds = 0
# The hex characters of unrequested ping data, defaults to '0'.
ping_size = 0
# Maximum protocol version, defaults to '1.7'.
protocol_maximum = 1.7
# Minimum protocol version, defaults to '1.0'.
protocol_minimum = 1.0
# The send rate limit in bytes per second, defaults to '0' (network controls).
rate_limit = 0
# IP address to secure bind, multiple allowed, defaults to empty (disabled).
#safe =
# Advertised host:port at which this server can be reached (defaults to empty).
#self_bind =
# Advertised secure host:port at which this server can be reached (defaults to empty).
#self_safe =
# String returned by server.version, defaults to '/libbitcoin:4.0.10255/'.
server_name = /libbitcoin:4.0.10255/
```

## 20. `[esplora]`

The Esplora interface.

```ini
[esplora]
# Allow requests from opaque origin (see CORS), defaults to 'false'.
allow_opaque_origin = false
# IP address to bind, multiple allowed, defaults to empty (disabled).
#bind =
# The trusted client certificate directory (*.PEM), enables client authentication.
cert_auth =
# The path to the server certificate file (.PEM), defaults to empty.
cert_path =
# The time limit for connection establishment, defaults to '0' (network controls).
connect_timeout_seconds = 0
# The required maximum number of connections, defaults to '0'.
connections = 0
# The maximum connection duration, defaults to '60'.
expiration_minutes = 60
# The host name (http verification), multiple allowed, defaults to empty (disabled).
#host =
# The idle timeout (http keep-alive), defaults to '10'.
inactivity_minutes = 10
# The password to decrypt the server private key file (.PEM), optional.
key_pass =
# The path to the server private key file (.PEM), defaults to empty.
key_path =
# The maximum write backlog of a channel, defaults to '1048576'.
maximum_backlog = 1048576
# The maximum json response buffer size, defaults to '65536'.
maximum_buffer = 65536
# The maximum number of address history entries, defaults to '1000000'.
maximum_history = 1000000
# The maximum allowed request size, defaults to '8004096'.
maximum_request = 8004096
# The minimum retained read buffer size, defaults to '4096'.
minimum_buffer = 4096
# The allowed origin (see CORS), multiple allowed, defaults to empty (disabled).
#origin =
# The send rate limit in bytes per second, defaults to '0' (network controls).
rate_limit = 0
# IP address to secure bind, multiple allowed, defaults to empty (disabled).
#safe =
# The server name (http header), defaults to 'libbitcoin/4'.
server = libbitcoin/4
```
