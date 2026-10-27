# Electrum

The Electrum interface is the protocol of the Electrum wallet, served on
the `[electrum]` binding. It is versioned, and `bs` serves every Bitcoin
version, 1.0 through 1.7, choosing the version with each client by
negotiation (§2.3).

Its protocols share one port, and their secure forms share another:

| Port | Default | Protocols |
| ---- | ------- | --------- |
| Clear (`bind`) | 8580 | TCP, HTTP, WS |
| Secure (`safe`) | 8543 | TCPS, HTTPS, WSS |

This page documents the protocol version by version. Its source is the
[protocol specification](https://github.com/spesmilo/electrum-protocol),
checked against the Electrum client and the main servers. Methods added
by altcoin forks, which appear in some Electrum server documentation, are
not part of the Bitcoin protocol and are not covered. Sparrow's
extensions are served on their own binding, `[sparrow]`, along with this
same Electrum interface.

## 1. Versions

| Version | Date | Changes |
| ------- | ---- | ------- |
| 1.0 | 2017-01 | The protocol as first written down |
| 1.1 | 2017-09 | Version negotiation, script hash methods, `server.features`, `server.add_peer`; address methods deprecated |
| 1.2 | 2018-03 | `blockchain.block.headers`, `server.ping`, `mempool.get_fee_histogram`, verbose transactions |
| 1.3 | 2018-07 | `blockchain.block.header`; address methods removed |
| 1.4 | 2018-07 | Checkpoint proofs (`cp_height`), `blockchain.transaction.id_from_pos`; chunk and header getters removed; raw headers only |
| 1.4.1 | 2019-01 | No change for Bitcoin |
| 1.4.2 | 2019-04 | `blockchain.scripthash.unsubscribe` |
| 1.6 | 2025-11 | Package broadcast, `mempool.get_info`, fee estimate modes, headers as a list, mempool order defined; `blockchain.relayfee` removed |
| 1.7 | 2026-07 | Script methods replace script hash methods, outpoint methods, `mempool.recent`, `blockchain.transaction.testmempoolaccept`, `server.ping` redesigned |

There is no Bitcoin 1.5: it was skipped, and 1.4.3 is a Namecoin version.
Version 1.7 was merged into the specification in July 2026, but parts
remain under discussion, and this page follows its current text. The
Electrum client negotiates up to 1.6.

## 2. Protocol

### 2.1 Method versions

Each method's section begins with the versions that define it, and with
each version that changed it.

| Method | 1.0 | 1.1 | 1.2 | 1.3 | 1.4 | 1.4.2 | 1.6 | 1.7 |
| ------ | :-: | :-: | :-: | :-: | :-: | :---: | :-: | :-: |
| [`server.version`](#serverversion) | • | Δ | • | • | Δ | • | Δ | • |
| [`server.banner`](#serverbanner) | • | • | • | • | • | • | • | • |
| [`server.donation_address`](#serverdonation_address) | • | • | • | • | • | • | • | • |
| [`server.features`](#serverfeatures) | | + | • | • | • | • | • | Δ |
| [`server.peers.subscribe`](#serverpeerssubscribe) | • | • | • | • | • | • | • | • |
| [`server.add_peer`](#serveradd_peer) | | + | • | • | • | • | • | • |
| [`server.ping`](#serverping) | | | + | • | • | • | • | Δ |
| [`blockchain.headers.subscribe`](#blockchainheaderssubscribe) | • | • | Δ | Δ | Δ | • | • | • |
| [`blockchain.block.header`](#blockchainblockheader) | | | | + | Δ | • | • | • |
| [`blockchain.block.headers`](#blockchainblockheaders) | | | + | • | Δ | • | Δ | • |
| [`blockchain.block.get_header`](#blockchainblockget_header) | • | • | • | • | | | | |
| [`blockchain.block.get_chunk`](#blockchainblockget_chunk) | • | • | • | • | | | | |
| [`blockchain.numblocks.subscribe`](#blockchainnumblockssubscribe) | • | | | | | | | |
| [`blockchain.estimatefee`](#blockchainestimatefee) | • | • | • | • | • | • | Δ | • |
| [`blockchain.relayfee`](#blockchainrelayfee) | • | • | • | • | • | • | | |
| [`mempool.get_fee_histogram`](#mempoolget_fee_histogram) | | | + | • | • | • | • | • |
| [`mempool.get_info`](#mempoolget_info) | | | | | | | + | • |
| [`mempool.recent`](#mempoolrecent) | | | | | | | | + |
| [`blockchain.transaction.broadcast`](#blockchaintransactionbroadcast) | • | Δ | • | • | • | • | • | • |
| [`blockchain.transaction.broadcast_package`](#blockchaintransactionbroadcast_package) | | | | | | | + | • |
| [`blockchain.transaction.testmempoolaccept`](#blockchaintransactiontestmempoolaccept) | | | | | | | | + |
| [`blockchain.transaction.get`](#blockchaintransactionget) | • | Δ | Δ | • | • | • | • | • |
| [`blockchain.transaction.get_merkle`](#blockchaintransactionget_merkle) | • | • | • | • | • | • | • | • |
| [`blockchain.transaction.id_from_pos`](#blockchaintransactionid_from_pos) | | | | | + | • | • | • |
| [`blockchain.utxo.get_address`](#blockchainutxoget_address) | • | | | | | | | |
| [`blockchain.outpoint.*`](#7-outpoints) | | | | | | | | + |
| [`blockchain.scriptpubkey.*`](#8-scripts) | | | | | | | | + |
| [`blockchain.scripthash.*`](#9-script-hashes) | | + | • | • | • | • | Δ | |
| [`blockchain.address.*`](#10-addresses) | • | • | • | | | | | |

`+` added, `•` defined, `Δ` changed, blank not defined. Version 1.4.1 is
the same as 1.4 for Bitcoin. `blockchain.scripthash.unsubscribe` is added
in 1.4.2.

### 2.2 Messages

Messages are JSON-RPC requests, responses and notifications. Version 2.0
is recommended, and 1.0 is accepted. A 1.0 request must have `params` as
an array and an `id`. A 2.0 request may name its parameters, using the
names given in each method's section.

```json
{"jsonrpc": "2.0", "id": 1, "method": "blockchain.block.header", "params": [1]}
```

```json
{"jsonrpc": "2.0", "id": 1, "result": "010000006fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000982051fd1e4ba744bbbe680e1fee14677ba1a3c3540bf7b1cdb606e857233e0e61bc6649ffff001d01e36299"}
```

A request may be a batch, an array of requests answered by an array of
responses in the same order. A subscription is answered once, then
followed by notifications, which are requests without an `id`.

### 2.3 Version negotiation

A client begins with [`server.version`](#serverversion), giving the
versions it supports, as one version or as `[minimum, maximum]`. The
server answers with the highest version both support, and the connection
uses that version from then on.

| Client | Server range | Negotiated |
| ------ | ------------ | ---------- |
| `"1.4"` | 1.0–1.7 | 1.4 |
| `["1.4", "2.0"]` | 1.0–1.7 | 1.7 |
| `["1.4", "1.5"]` | 1.0–1.7 | 1.4.2 |
| `"1.8"` | 1.0–1.7 | Error, and the connection closes |
| Omitted | 1.0–1.7 | 1.0 |

`electrum.protocol_minimum` and `electrum.protocol_maximum` set the
server's range (default 1.0 and 1.7).

From 1.6, `server.version` must be the first message. Before 1.6, `bs`
also accepts other messages first, and serves them at the minimum
version. Such a connection may then negotiate up to 1.4.2. From 1.4,
`server.version` may be sent only once.

### 2.4 Transports

`bs` serves every transport on each port, choosing by the first bytes of
the connection:

| Transport | Requests | Notifications |
| --------- | -------- | ------------- |
| TCP/S | One JSON message or batch per line | Yes |
| WS/S | One JSON message per frame, no batches | Yes |
| HTTP/S | `POST /`, one message or batch per request | No |

TCP/S is the Electrum transport, used by Electrum clients. The
specification also defines messages over WS/S, as one frame each without
the line ending, which ElectrumX and Fulcrum serve. HTTP/S is a `bs`
extension, on the model of bitcoind's JSON-RPC: each request is posted to
`/` and answered in its response. HTTP/S carries no notifications, so a
subscription made over HTTP/S is dormant until the connection is upgraded
to WS/S.

Each curl command is a new connection, so a batch that begins with
`server.version` sets its version:

```
$ curl -d '[{"jsonrpc":"2.0","id":0,"method":"server.version","params":["curl","1.7"]},{"jsonrpc":"2.0","id":1,"method":"blockchain.block.header","params":[1]}]' "http://localhost:8580/"
```

```json
[
    {"jsonrpc": "2.0", "id": 0, "result": ["/libbitcoin:4.0.x/", "1.7"]},
    {"jsonrpc": "2.0", "id": 1, "result": "010000006fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000982051fd1e4ba744bbbe680e1fee14677ba1a3c3540bf7b1cdb606e857233e0e61bc6649ffff001d01e36299"}
]
```

### 2.5 Encodings

| Value | Encoding |
| ----- | -------- |
| Transaction, block hash | Hex, in the usual reversed (display) order |
| Script hash | SHA-256 of the output script, as hex in reversed order |
| Script | Hex of the output script, without its length |
| Header | Hex of the 80 byte header, as serialized |
| Transaction | Hex of the transaction, as serialized with witness data |
| Amount, fee | Integer satoshis |
| Fee rate | BTC per 1000 virtual bytes, except the fee histogram in satoshis per virtual byte |
| Height | Integer; for an unconfirmed transaction, `0` if all its inputs are confirmed, otherwise `-1` |

### 2.6 History and status

The history of a script (or script hash, or address) lists its
confirmed transactions, ordered by height and then by position in the
block, followed by its unconfirmed transactions:

```json
[
    {"tx_hash": "<txid>", "height": 10},
    {"tx_hash": "<txid>", "height": 0, "fee": 1000},
    {"tx_hash": "<txid>", "height": -1, "fee": 2000}
]
```

Its status is a hash of the history, which changes whenever the history
does. It is the SHA-256 of the concatenation of `tx_hash:height:` for each
entry, as hex, and `null` for an empty history.

| Versions | Order of unconfirmed transactions |
| -------- | --------------------------------- |
| 1.0–1.4.2 | Not defined |
| 1.6+ | Height `0` before `-1`, then by `tx_hash` as hex |

`bs` uses the 1.6 order at every version.

### 2.7 Errors

An error response carries a code and a message:

```json
{"jsonrpc": "2.0", "id": 1, "error": {"code": 1, "message": "bad_request"}}
```

| Code | Meaning |
| ---- | ------- |
| 1 | Bad request: an invalid argument, an object not found, or a method not defined at the negotiated version |
| 2 | Daemon error: the node could not complete the request |
| 10001 | History too large (`electrum.maximum_history`) |
| -101 | Too many subscriptions (`electrum.maximum_subscriptions`) |
| -32601 | Method not found |

A malformed message, or a request with missing, extra or mistyped
parameters, closes the connection without a response.

### 2.8 Configuration

```ini
[electrum]
bind = 0.0.0.0:8580
safe = 0.0.0.0:8543
connections = 100
```

The service starts only with an address and a connection limit. The
script, script hash and address methods require the address index, and
return -32601 without it. To serve clients that expect the usual ports,
bind 50001 and 50002 instead. See
[Configuration §5.7](../configuration/index#57-electrum-server) for TLS,
credentials and limits.

## 3. Server

### server.version

Negotiates the protocol version (§2.3).

| Versions | Parameters | Result |
| -------- | ---------- | ------ |
| 1.0 | `client_name`, `protocol_version` (ignored) | Server name |
| 1.1+ | `client_name`, `protocol_version` | `[server_name, version]` |

`protocol_version` is a version, or `[minimum, maximum]`, and defaults to
the server's minimum. From 1.6, the server ignores further parameters.

```json
{"jsonrpc": "2.0", "id": 0, "method": "server.version", "params": ["Electrum 4.7.0", ["1.4", "1.6"]]}
```

```json
{"jsonrpc": "2.0", "id": 0, "result": ["/libbitcoin:4.0.x/", "1.6"]}
```

The server name is `electrum.server_name`.

### server.banner

The server's banner, `electrum.banner_message`.

**Versions:** 1.0+. **Parameters:** none. **Result:** a string.

### server.donation_address

The server's donation address, `electrum.donation_address`.

**Versions:** 1.0+. **Parameters:** none. **Result:** a string.

### server.features

The server's features.

**Versions:** 1.1+, changed in 1.7. **Parameters:** none.

```json
{
    "genesis_hash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
    "hosts": {"electrum.example.com": {"tcp_port": 50001, "ssl_port": 50002}},
    "server_version": "/libbitcoin:4.0.x/",
    "protocol_min": "1.0",
    "protocol_max": "1.7",
    "pruning": null,
    "method_flavours": {
        "blockchain.transaction.broadcast_package": {"supports_verbose_true": false}
    }
}
```

Before 1.7 the result also carries `"hash_function": "sha256"`. `hosts`
is set by `electrum.self_bind` and `electrum.self_safe`. `bs` also serves
this method at 1.0.

### server.peers.subscribe

Other servers, for the client to connect to.

**Versions:** 1.0+. **Parameters:** none. **Result:** an array of
`[ip, host, features]`, where features include `"t<port>"` and
`"s<port>"`.

`bs` returns the servers set by `electrum.more_bind` and
`electrum.more_safe`, and sends no notifications.

### server.add_peer

Asks the server to add a peer server.

**Versions:** 1.1+. `bs` does not add servers, and returns -32601.

### server.ping

Keeps the connection open.

| Versions | Parameters | Result |
| -------- | ---------- | ------ |
| 1.2–1.6 | none | `null` |
| 1.7 | `pong_len` (0), `data` (`""`) | `{"data": hex}`, of length `pong_len` |

From 1.7, both sides may also send `server.ping` as a notification. `bs`
sends one every `electrum.ping_interval_seconds` over TCP and websocket,
with `electrum.ping_size` characters of data.

## 4. Headers

### blockchain.headers.subscribe

The top header, and a notification for each new top.

| Versions | Parameters | Result |
| -------- | ---------- | ------ |
| 1.0–1.1 | none | Header as an object |
| 1.2 | `raw` (`false`) | Header as an object, or with `raw` `{"height", "hex"}` |
| 1.3 | `raw` (`true`) | `{"height", "hex"}`, or without `raw` an object |
| 1.4+ | none | `{"height", "hex"}` |

```json
{"height": 1, "hex": "010000006fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000982051fd1e4ba744bbbe680e1fee14677ba1a3c3540bf7b1cdb606e857233e0e61bc6649ffff001d01e36299"}
```

The header object is:

```json
{
    "block_height": 1,
    "version": 1,
    "prev_block_hash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
    "merkle_root": "0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098",
    "timestamp": 1231469665,
    "bits": 486604799,
    "nonce": 2573394689
}
```

The notification's parameters are `[header]`. A notification may skip
intermediate tops, and follows a reorganization.

### blockchain.block.header

The header at a height, with an optional proof of it.

| Versions | Parameters |
| -------- | ---------- |
| 1.3 | `height` |
| 1.4+ | `height`, `cp_height` (0) |

Without `cp_height`, the result is the header as hex. With it, the result
proves the header against a checkpoint:

```json
{
    "header": "<header hex>",
    "branch": ["<hash>", "..."],
    "root": "<hash>"
}
```

`root` is the merkle root of the hashes of blocks 0 to `cp_height`, and
`branch` the hashes that prove the block's hash in that tree, deepest
first. `height` must not exceed `cp_height`, nor `cp_height` the top. `bs`
also accepts `cp_height` at 1.3.

### blockchain.block.headers

Consecutive headers, with an optional proof of the last.

| Versions | Parameters | Result |
| -------- | ---------- | ------ |
| 1.2–1.3 | `start_height`, `count` | `{"count", "hex", "max"}` |
| 1.4–1.4.2 | `start_height`, `count`, `cp_height` (0) | `{"count", "hex", "max"}` |
| 1.6+ | `start_height`, `count`, `cp_height` (0) | `{"count", "headers", "max"}` |

`hex` is the headers concatenated, and `headers` an array of them. `max`
is the most headers returned, `electrum.maximum_headers` (default 20160).
With `cp_height`, `branch` and `root` prove the last header returned, as
in [`blockchain.block.header`](#blockchainblockheader).

```json
{"count": 2, "headers": ["<header 0 hex>", "<header 1 hex>"], "max": 20160}
```

### blockchain.block.get_header

The header at a height, as an object (see
[`blockchain.headers.subscribe`](#blockchainheaderssubscribe)).

**Versions:** 1.0–1.3, deprecated in 1.3. **Parameters:** `height`.

### blockchain.block.get_chunk

The 2016 headers from height `index × 2016`, concatenated as hex.

**Versions:** 1.0–1.3, deprecated in 1.2. **Parameters:** `index`.

### blockchain.numblocks.subscribe

The top height, and a notification for each new top.

**Versions:** 1.0, deprecated. **Parameters:** none. **Result:** an
integer. The notification's parameter is the height.

## 5. Fees and memory pool

### blockchain.estimatefee

The fee rate for a transaction to confirm within a number of blocks.

| Versions | Parameters |
| -------- | ---------- |
| 1.0–1.4.2 | `number` |
| 1.6+ | `number`, `mode` |

**Result:** BTC per 1000 virtual bytes, or `-1` without an estimate.

`mode` is `economical` or `conservative`, and `bs` adds `basic` (the
default) and `geometric`. Estimates require `node.fee_estimate_horizon`.

### blockchain.relayfee

The minimum fee rate for relay, in BTC per 1000 virtual bytes.

**Versions:** 1.0–1.4.2, replaced in 1.6 by
[`mempool.get_info`](#mempoolget_info). **Parameters:** none. `bs` returns
`node.minimum_fee_rate`.

### mempool.get_fee_histogram

The fee rates of the memory pool.

**Versions:** 1.2+. **Parameters:** none. **Result:** `[[fee_rate,
vsize], ...]`, by descending fee rate in satoshis per virtual byte, where
`vsize` is the virtual size of the transactions at that rate.

### mempool.get_info

The fee policy of the memory pool, in BTC per 1000 virtual bytes.

**Versions:** 1.6+. **Parameters:** none.

```json
{"mempoolminfee": 0.000001, "minrelaytxfee": 0.000001, "incrementalrelayfee": 0.000001}
```

`bs` returns the configured rates, `node.minimum_fee_rate` and
`node.minimum_bump_rate`.

### mempool.recent

The 10 transactions most recently added to the memory pool.

**Versions:** 1.7. **Parameters:** none.

```json
[{"txid": "<txid>", "fee": 1000, "vsize": 110}]
```

## 6. Transactions

### blockchain.transaction.broadcast

Submits a transaction to the memory pool.

**Versions:** 1.0+, changed in 1.1. **Parameters:** `raw_tx`.
**Result:** the transaction hash.

In 1.0, a rejected transaction returns the reason as the result. From
1.1, it returns error 2.

### blockchain.transaction.broadcast_package

Submits a package of transactions to the memory pool.

**Versions:** 1.6+. **Parameters:** `raw_txs`, `verbose` (`false`).

```json
{"success": false, "errors": [{"txid": "<txid>", "error": "<reason>"}]}
```

`bs` does not support `verbose`.

### blockchain.transaction.testmempoolaccept

Tests whether transactions would be accepted to the memory pool, without
submitting them.

**Versions:** 1.7. **Parameters:** `raw_txs`, up to 25.

```json
[{"txid": "<txid>", "wtxid": "<wtxid>", "allowed": false, "reason": "<reason>"}]
```

### blockchain.transaction.get

A transaction, confirmed or unconfirmed.

| Versions | Parameters |
| -------- | ---------- |
| 1.0 | `tx_hash`, `height` (ignored) |
| 1.1 | `tx_hash` |
| 1.2+ | `tx_hash`, `verbose` (`false`) |

**Result:** the transaction as hex, or with `verbose` as bitcoind's
`getrawtransaction` object.

### blockchain.transaction.get_merkle

The merkle proof of a confirmed transaction.

**Versions:** 1.0+. **Parameters:** `tx_hash`, `height`.

```json
{"block_height": 1, "merkle": [], "pos": 0}
```

`merkle` is the branch, deepest first, and `pos` the transaction's
position in the block. `bs` serves this method from 1.4.

### blockchain.transaction.id_from_pos

The hash of the transaction at a position in a block.

**Versions:** 1.4+. **Parameters:** `height`, `tx_pos`, `merkle`
(`false`). **Result:** the transaction hash, or with `merkle`
`{"tx_hash", "merkle"}`.

## 7. Outpoints

### blockchain.utxo.get_address

The address of an output.

**Versions:** 1.0, deprecated. **Parameters:** `tx_hash`, `index`.
**Result:** the address, or `null`.

### blockchain.outpoint.get_status

The funding and spending of an output.

**Versions:** 1.7. **Parameters:** `tx_hash`, `txout_idx`, `spk_hint`.

```json
{"funder_height": 1, "spender_txhash": "<txid>", "spender_height": 170}
```

An unspent output has only `funder_height`, and an unknown one returns
`{}`. `spk_hint` is the output's script. `bs` does not require it.

### blockchain.outpoint.subscribe

As [`blockchain.outpoint.get_status`](#blockchainoutpointget_status), with
a notification of `[tx_hash, txout_idx, status]` for each change.

**Versions:** 1.7.

### blockchain.outpoint.unsubscribe

Ends an outpoint subscription.

**Versions:** 1.7. **Parameters:** `tx_hash`, `txout_idx`. **Result:**
`true` if it was subscribed.

## 8. Scripts

These identify an output script by its hex, and replace the script hash
methods in 1.7. Each takes `scriptpubkey`. Notifications carry the
script's hash and status, `[scripthash, status]`, including for a
reorganization that changes the block of a transaction without changing
its height.

### blockchain.scriptpubkey.get_balance

**Versions:** 1.7. **Result:** `{"confirmed", "unconfirmed"}`, in
satoshis. `bs` returns `0` for `unconfirmed`.

### blockchain.scriptpubkey.get_history

**Versions:** 1.7. **Result:** `{"history": [...]}`, the history (§2.6).

### blockchain.scriptpubkey.get_mempool

**Versions:** 1.7. **Result:** `{"history": [...]}`, the unconfirmed
part of the history.

### blockchain.scriptpubkey.listunspent

**Versions:** 1.7. **Result:** `{"utxos": [...]}`, each
`{"tx_hash", "tx_pos", "height", "value"}`, where an unconfirmed output
has height `0`.

### blockchain.scriptpubkey.subscribe

**Versions:** 1.7. **Result:** the status (§2.6), and a notification for
each change.

### blockchain.scriptpubkey.unsubscribe

**Versions:** 1.7. **Result:** `true` if it was subscribed.

## 9. Script hashes

These identify an output script by its hash (§2.5). Each takes
`scripthash`. Results are as for the script methods, without the
`history` and `utxos` objects. Notifications are
`[scripthash, status]`.

### blockchain.scripthash.get_balance

**Versions:** 1.1–1.6.

### blockchain.scripthash.get_history

**Versions:** 1.1–1.6.

### blockchain.scripthash.get_mempool

**Versions:** 1.1–1.6, order defined in 1.6 (§2.6).

### blockchain.scripthash.listunspent

**Versions:** 1.1–1.6.

### blockchain.scripthash.subscribe

**Versions:** 1.1–1.6, status order defined in 1.6 (§2.6).

### blockchain.scripthash.unsubscribe

**Versions:** 1.4.2–1.6.

## 10. Addresses

These identify an output by its address, and are replaced by the script
hash methods. Each takes `address`. Results are as for the script hash
methods. `bs` accepts base58 (P2PKH and P2SH) addresses.

### blockchain.address.get_balance

**Versions:** 1.0–1.2, deprecated in 1.1.

### blockchain.address.get_history

**Versions:** 1.0–1.2, deprecated in 1.1.

### blockchain.address.get_mempool

**Versions:** 1.0–1.2, deprecated in 1.1.

### blockchain.address.listunspent

**Versions:** 1.0–1.2, deprecated in 1.1.

### blockchain.address.subscribe

**Versions:** 1.0–1.2, deprecated in 1.1.
