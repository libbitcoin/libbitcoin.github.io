# Stratum v1

Stratum v1 is the mining protocol in common use, by which a pool gives
work to miners and receives their shares. `bs` serves it from the
`[stratum_v1]` service as a solo pool: each job is a template of the next
block from the `bs` transaction pool, its coinbase pays the miner's
address (or the configured one), and a share that meets the network
target is submitted as a block.

Its protocols share one port, and their secure forms share another:

| Port | Default | Protocols |
| ---- | ------- | --------- |
| Clear (`bind`) | 8880 | TCP, HTTP, WS |
| Secure (`safe`) | 8843 | TCPS, HTTPS, WSS |

Messages are JSON-RPC 1.0, one per line over TCP, one per frame over WS.
Jobs and difficulty are sent as notifications, so a miner connects over
TCP/S or WS/S. HTTP/S answers requests but sends no jobs.

## 1. Setup

The service is disabled by default. Bind an address, allow connections,
and optionally set the payout address:

```ini
[stratum_v1]
bind = 0.0.0.0:8880
connections = 10
payout_address = bc1q...
```

Point the miner at `stratum+tcp://<host>:8880`. Without
`payout_address`, the worker name is the payout: the miner authorizes as
`<address>` or `<address>.<worker>`. With `payout_address`, every block
pays that address, and worker names are free.

As with the other services, connections are refused until the chain is
current ([Service Settings](../configuration/services#until-current)),
and `safe` serves TLS with `cert_path` and `key_path`
([Secure connections](../configuration/services#2-secure-connections)).

| Setting | Default | Purpose |
| ------- | ------- | ------- |
| `stratum_v1.payout_address` | empty | Address paid by the coinbase; empty, the worker name |
| `stratum_v1.coinbase_tag` | empty | Text carried by the coinbase input script (at most 75 bytes) |
| `stratum_v1.extranonce1_size` | 4 | Coinbase extranonce bytes assigned to each connection (at least 4) |
| `stratum_v1.extranonce2_size` | 4 | Coinbase extranonce bytes rolled by the miner |
| `stratum_v1.minimum_difficulty` | 1 | Share difficulty first assigned, and its floor |
| `stratum_v1.share_interval_seconds` | 10 | Target seconds between shares (0 fixes the difficulty) |
| `stratum_v1.authorize_timeout_seconds` | 15 | Seconds to subscribe and authorize before the connection is closed (0 is unlimited) |
| `pool.template_interval_seconds` | 30 | Seconds between replacements of the template (0 disables) |
| `pool.template_fee_increase` | 0 | Satoshis of fees a replacement template must add |

Startup fails if `extranonce1_size` is below 4 (so that the prefixes of
connections are distinct), `extranonce2_size` is zero, the tag exceeds 75
bytes, the two extranonce sizes together exceed 75 bytes, the coinbase
input script would exceed 100 bytes, or the minimum difficulty is not
positive.

With the service enabled, `pool.coinbase_weight` and
`pool.coinbase_sigops` are derived from this coinbase, so that templates
reserve exactly its space: weight 656 and 4 sigops with the defaults and
no payout address (the largest address output, P2PKH for the sigops),
and 608 and 0 with a P2WPKH payout address. A configured value governs,
as for an external miner using [`getblocktemplate`](bitcoind-rpc#getblocktemplate).

### Start difficulty

A connection starts at `minimum_difficulty`, which is also its floor.
At difficulty 1 a 100 TH/s machine finds tens of thousands of shares a
second. Vardiff raises the difficulty fourfold every 16 shares, so it
converges in seconds, but it opens with a flood of shares. For ASICs, set
`minimum_difficulty` near the miner's rate, its hash rate times
`share_interval_seconds` divided by 2<sup>32</sup>: about 230,000 for a
100 TH/s machine at the default 10 seconds.

```ini
[stratum_v1]
minimum_difficulty = 230000
```

A miner may also request its difficulty with
[`mining.suggest_difficulty`](#miningsuggest_difficulty), which is
floored at `minimum_difficulty`.

### Connection limits

A connection that is not both subscribed and authorized within
`authorize_timeout_seconds` (default 15) is closed.
`expiration_minutes` closes every connection after that time, and the
miner reconnects with new jobs and its difficulty reset.
`inactivity_minutes` closes a connection from which nothing has been read
for that time; jobs sent to the miner do not count. Both default to 0,
no limit, for `[stratum_v1]`. A nonzero `inactivity_minutes` should
exceed the longest expected time between shares
([Service Settings](../configuration/services#5-limits)).

## 2. Methods

| Method | Direction | Purpose |
| ------ | --------- | ------- |
| [`mining.configure`](#miningconfigure) | Miner to `bs` | Negotiates version rolling (BIP310) |
| [`mining.subscribe`](#miningsubscribe) | Miner to `bs` | Subscribes to work |
| [`mining.authorize`](#miningauthorize) | Miner to `bs` | Authorizes a worker, and its payout |
| [`mining.submit`](#miningsubmit) | Miner to `bs` | Submits a share |
| [`mining.suggest_difficulty`](#miningsuggest_difficulty) | Miner to `bs` | Requests a share difficulty |
| [`mining.suggest_target`](#miningsuggest_target) | Miner to `bs` | Requests a share target |
| [`mining.extranonce.subscribe`](#miningextranoncesubscribe) | Miner to `bs` | Accepted; the extranonce does not change |
| [`mining.get_transactions`](#miningget_transactions) | Miner to `bs` | Not implemented (answered `20`) |
| [`mining.multi_version`](#miningmulti_version) | Miner to `bs` | Not implemented (answered `20`) |
| [`mining.set_difficulty`](#miningset_difficulty) | `bs` to miner | Sets the share difficulty |
| [`mining.notify`](#miningnotify) | `bs` to miner | Sends a job |
| [`client.reconnect`](#clientreconnect) | `bs` to miner | Not sent |

Jobs begin once the connection is both subscribed and authorized, in
either order.

### mining.configure

**Parameters:** `extensions` (array of names), `parameters` (object).
`version-rolling` is the only extension accepted; others are answered
`false`. The mask is the requested `version-rolling.mask`, limited to the
general purpose version bits (BIP320, `1fffe000`), or all of those bits
if none is requested.

```json
{
    "id": 1,
    "method": "mining.configure",
    "params": [["version-rolling"], {"version-rolling.mask": "1fffe000"}]
}
{
    "id": 1,
    "result": {"version-rolling": true, "version-rolling.mask": "1fffe000"},
    "error": null
}
```

### mining.subscribe

**Parameters:** `user_agent`, `session_id`, `host`, `port` (each
optional or null, and ignored).
**Result:** the subscriptions, the extranonce prefix of the connection
(`extranonce1`, base16) and the size in bytes of the extranonce the miner
rolls (`extranonce2`).

```json
{"id": 2, "method": "mining.subscribe", "params": ["cgminer/4.12.1"]}
{
    "id": 2,
    "result": [
        [
            ["mining.set_difficulty", "0000000000000007"],
            ["mining.notify", "0000000000000007"]
        ],
        "07000000",
        4
    ],
    "error": null
}
```

The prefix is random, neither a prefix of nor prefixed by that of any
other connection, and fixed for the life of the connection.

### mining.authorize

**Parameters:** `username`, `password` (optional or null, not
checked).
**Result:** `true`.

Without `payout_address`, the username up to its first `.` must be an
address of the chain, which the coinbase pays. The first worker
authorized sets the payout of the connection; another worker on the same
connection must pay the same address. An invalid address, or a different
one, is answered `24` (Unauthorized worker).

```json
{
    "id": 3,
    "method": "mining.authorize",
    "params": ["bc1qexampleaddress.rig1", "x"]
}
{"id": 3, "result": true, "error": null}
```

### mining.submit

**Parameters:** `worker_name`, `job_id`, `extranonce2`, `ntime`, `nonce`,
`version_bits` (optional, with version rolling). Each is base16:
`extranonce2` of exactly `extranonce2_size` bytes, and the others of
eight characters, most significant first. **Result:** `true`.

```json
{
    "id": 4,
    "method": "mining.submit",
    "params": [
        "bc1qexampleaddress.rig1",
        "00000002",
        "00000000",
        "6a1b2c3d",
        "1a2b3c4d"
    ]
}
{"id": 4, "result": true, "error": null}
```

The header is rebuilt from the job, the coinbase of `coinb1`,
`extranonce1`, `extranonce2` and `coinb2`, and the submitted time, nonce
and version. The version bits must lie within the negotiated mask, and
the header must be valid in the context of the job: `ntime` past the
median time past of the block, and no more than two hours
(`bitcoin.timestamp_limit_seconds`) ahead of the present. Since the
miner sets only header fields, a valid header makes a valid block.

The share is accepted if its hash does not exceed the target of the
job's difficulty: the difficulty one target (bits `1d00ffff`) divided by
the difficulty. A share that also meets the network target is submitted
as a block, and its outcome is logged; the miner's answer does not wait
for it.

| Error | Code | When |
| ----- | ---- | ---- |
| Other/Unknown | 20 | A parameter is malformed, version bits fall outside the mask, or the header is invalid; the connection is then closed |
| Job not found | 21 | The job is unknown, or was dropped |
| Duplicate share | 22 | The same header was submitted for the job |
| Low difficulty share | 23 | The hash exceeds the share target |
| Unauthorized worker | 24 | The worker is not authorized on the connection |
| Not subscribed | 25 | The connection is not subscribed |

Errors are positional, `[code, message, null]`:

```json
{"id": 4, "result": null, "error": [23, "Low difficulty share", null]}
```

### mining.suggest_difficulty

**Parameters:** `difficulty` (number). **Result:** `true`. The
connection's difficulty becomes the suggestion, floored at
`minimum_difficulty`, and the current job is sent again at it.

### mining.suggest_target

**Parameters:** `target` (64 base16 characters). **Result:** `true`. As
`mining.suggest_difficulty`, with the difficulty of the target. A
malformed target is answered `20`.

### mining.extranonce.subscribe

**Parameters:** none. **Result:** `true`. The extranonce prefix of a
connection never changes, so no `mining.set_extranonce` follows.

### mining.get_transactions

**Parameters:** `job_id`. Not implemented: answered
`[20, "not_implemented", null]`.

### mining.multi_version

**Parameters:** `version` (number). Not implemented: answered
`[20, "not_implemented", null]`.

### mining.set_difficulty

**Parameters:** `difficulty`. Sent before a job whose difficulty differs
from the last sent, and so applies to that job and those that follow.

```json
{"id": null, "method": "mining.set_difficulty", "params": [1.0]}
```

### mining.notify

**Parameters:** `job_id`, `prevhash`, `coinb1`, `coinb2`,
`merkle_branch`, `version`, `nbits`, `ntime`, `clean_jobs`.

| Parameter | Value |
| --------- | ----- |
| `job_id` | Eight base16 characters, unique on the connection |
| `prevhash` | Previous block hash, in header order, each four byte word reversed |
| `coinb1` | Coinbase through the extranonce push opcode, without witness |
| `coinb2` | Coinbase following the extranonce, without witness |
| `merkle_branch` | Hashes from the coinbase to the merkle root, in header order |
| `version` | Block version, eight base16 characters |
| `nbits` | Network target, compact, eight base16 characters |
| `ntime` | Current time, at least one second past the median time past |
| `clean_jobs` | `true` if the previous block changed, and earlier jobs are void |

```json
{
    "id": null,
    "method": "mining.notify",
    "params": [
        "00000002",
        "...",
        "02000000010000...",
        "feffffff02...",
        ["..."],
        "20000000",
        "1703a30c",
        "6a1b2c3d",
        true
    ]
}
```

A job is sent for each new template of the block above the confirmed
top: on each new block, which voids earlier jobs, and while the block is
pending, as the pool replaces the template
(`pool.template_interval_seconds`), which does not. The last 16
jobs of a connection are retained for shares.

### client.reconnect

Not sent: `bs` does not move a miner to another server.

## 3. Coinbase and difficulty

The coinbase is version 2, with one input and two outputs. Its input
script pushes the block height (BIP34), the `coinbase_tag` if any, and
the extranonce of `extranonce1` and `extranonce2`. Its input sequence is
not final (`fffffffe`) and its locktime is the previous height (BIP54). Its first output pays
the subsidy and the template's fees to the payout address; the second
commits to the block's witnesses (BIP141), with a null reserved value.

The difficulty of a connection starts at `minimum_difficulty`. With a
nonzero `share_interval_seconds`, it is retargeted after 16 accepted
shares, or at the first share after 16 intervals: by the ratio of the
target interval to the observed one, limited to between a quarter and
four times, unchanged while that ratio is between 0.8 and 1.25, and never
below `minimum_difficulty`.

A connection that sends no shares cannot retarget, so its difficulty
also decays: every four share intervals, if no share was accepted since
the difficulty was last evaluated, the difficulty falls to a quarter, never
below `minimum_difficulty`. With the defaults, an idle connection's
difficulty is quartered every 40 seconds.

A retarget or decay sends the current job again, with `clean_jobs`
`false`, after `mining.set_difficulty`.
