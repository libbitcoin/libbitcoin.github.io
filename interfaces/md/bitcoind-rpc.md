# Bitcoind JSON-RPC

The bitcoind JSON-RPC interface is a drop-in for the node methods of
bitcoind's JSON-RPC interface, served on the `[bitcoind]` binding with
the [bitcoind REST](bitcoind-rest) interface. It serves no wallet or
signing methods; keys never reach the server.

Its protocols share one port, and their secure forms share another:

| Port | Default | Protocols |
| ---- | ------- | --------- |
| Clear (`bind`) | 8280 | HTTP, TCP, WS |
| Secure (`safe`) | 8243 | HTTPS, TCPS, WSS |

bitcoind serves JSON-RPC over HTTP only. btcd also serves it over WS/S,
but the protocol is not versioned and its methods are out of date or
inconsistent, so `bs` follows bitcoind's methods on both its bitcoind
and BTCD interfaces. TCP/S is a `bs` extension. All carry the same
messages (§2.4).

## 1. Methods

| Category | Methods |
| -------- | ------- |
| [Blockchain](#3-blockchain) | Blocks, headers, outputs and chain state |
| [Memory pool](#4-memory-pool) | Pool contents and persistence |
| [Transactions](#5-transactions) | Raw transactions, PSBTs and broadcast |
| [Mining](#6-mining) | Hash rate, headers and mining state |
| [Network](#7-network) | Peers and connections |
| [Utility](#8-utility) | Addresses, descriptors, messages and fees |
| [Control](#9-control) | Help, discovery and server state |
| [Notifications](#10-notifications) | ZMQ endpoints |

Methods that `bs` does not serve are listed in §11.

## 2. Calling pattern

### 2.1 Requests

Each request is a JSON-RPC message posted to `/`:

```
$ curl --user user:pass -d '{"jsonrpc":"2.0","id":1,"method":"getblockcount","params":[]}' "http://localhost:8280/"
```

```json
{"jsonrpc": "2.0", "id": 1, "result": 9}
```

- Parameters are positional (an array) or named (an object), with the
  names given in each method's section.
- A request may be a batch, an array of requests answered in order.
- A version 2.0 request without an `id` is a notification: it is run, and
  answered with HTTP 204 and no body.
- A version 1.0 request (no `jsonrpc`) must have `params` as an array and
  an `id`, and is answered with both `result` and `error`.

> JSON numbers may be written differently than by bitcoind, for example
> `1E0` for `1`, or `5E1` for `50.00000000`. These are equivalent JSON
> encodings.

### 2.2 Errors

An error carries bitcoind's code, and its name as the message:

```json
{"jsonrpc": "2.0", "id": 1, "error": {"code": -8, "message": "invalid_parameter"}}
```

| Code | Name |
| ---- | ---- |
| -1 | `misc_error` |
| -3 | `type_error` |
| -5 | `invalid_address_or_key` |
| -8 | `invalid_parameter` |
| -20 | `database_error` |
| -22 | `deserialization_error` |
| -24 | `node_not_added` |
| -25 | `verify_error` |
| -26 | `verify_rejected` |
| -27 | `already_in_utxo_set` |
| -29 | `node_not_connected` |
| -33 | `client_mempool_disabled` |
| -32601 | `method_not_found` |
| -32602 | `invalid_params` |
| -32603 | `internal_error` |

Errors are sent with HTTP 200. A message that cannot be read, or a
request with a missing, extra or mistyped parameter, closes the
connection without a response. bitcoind instead answers these with an
error, and accepts some types that `bs` does not, such as a boolean for
`getrawtransaction` verbosity or a quoted amount.

### 2.3 Credentials

```ini
[bitcoind]
bind = 127.0.0.1:8280
connections = 10
credential = user:pass
credential = monitor:secret:getblockcount,getblockchaininfo
```

Each `credential` is `username:password`, optionally followed by the
methods it may call (see
[Configuration §7.3](../configuration/index#73-authentication)). With no
credential, no authentication is required. The credential is stored as
written, and its password may not contain `:`.

Clients of `bs` and of bitcoind can authenticate with HTTP basic
authentication. bitcoind can also generate a random password in a cookie file, or be configured
with a salted hash of the password in place of the password. Basic
authentication is insecure by design, and client certificates are the
modern technique.

| Status | Meaning |
| ------ | ------- |
| 401 | Credentials are configured, and none or wrong ones were given |
| 403 | The credential does not permit the method, or the origin is not allowed |

TCP/S carries no credentials, so with any credential configured, a TCP/S
connection is closed.

Client certificates are a `bs` extension, though this does not support
method binding. With `bitcoind.cert_auth` set, each secure
connection must present a client certificate trusted by one of the files
in that directory (see
[Configuration §7.2](../configuration/index#72-secure-connections)).
This also restricts TCPS clients, which carry no credentials.

### 2.4 Transports

| Transport | Requests | Responses |
| --------- | -------- | --------- |
| HTTP/S | `POST /`, one message or batch | The response body |
| TCP/S | One JSON message or batch, ending at its closing bracket | One per line |
| WS/S | One JSON message per frame, no batches | One per frame |

The first bytes of a connection select its transport, so all three share
a port. A WS/S connection is authorized by its upgrade request.

### 2.5 Addresses

Addresses, keys and descriptors in requests and responses are encoded
with the [`[wallet]`](../configuration/reference#6-wallet) prefixes, so a
test chain uses its own. An address of another chain is rejected.

## 3. Blockchain

### getbestblockhash

The hash of the top confirmed block. **Parameters:** none.

### getblockcount

The height of the top confirmed block. **Parameters:** none.

```json
9
```

### getblockhash

The hash of the block at a height on the confirmed chain.
**Parameters:** `height`.

```
$ curl -d '{"jsonrpc":"2.0","id":1,"method":"getblockhash","params":[0]}' "http://localhost:8280/"
```

```json
{"jsonrpc": "2.0", "id": 1, "result": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"}
```

### getblock

A block. **Parameters:** `blockhash`, `verbosity` (1).

| Verbosity | Result |
| --------- | ------ |
| 0 | The block as hex |
| 1 | The block, with transaction hashes |
| 2 | The block, with transaction objects and fees |
| 3 | As 2, with each input's `prevout` |

Verbosity is a number. Values below 0 are read as 0, and above 3 as 3.
The `coinbase_tx` field is not included. A block that is not confirmed has
`confirmations` of -1.

### getblockheader

A block header. **Parameters:** `blockhash`, `verbose` (`true`).
**Result:** the header as hex, or with `verbose` an object with its
height, confirmations, median time, chain work and adjacent hashes.

### getblockchaininfo

The state of the chain. **Parameters:** none.

```json
{
    "chain": "main",
    "blocks": 9,
    "headers": 9,
    "bestblockhash": "000000008d9dc510f23c2657fc4f67bea30078cc05a90eb89e84cc475c080805",
    "bits": "1d00ffff",
    "target": "00000000ffff0000000000000000000000000000000000000000000000000000",
    "difficulty": 1E0,
    "time": 1231473279,
    "mediantime": 1231471428,
    "verificationprogress": 1E0,
    "initialblockdownload": true,
    "chainwork": "0000000000000000000000000000000000000000000000000000000a000a000a",
    "size_on_disk": <bytes>,
    "pruned": false,
    "warnings": [],
    "bip9_softforks": {}
}
```

`headers` is the top candidate height, and `verificationprogress` the
ratio of `blocks` to `headers`. `size_on_disk` is the size of the store.
`bip9_softforks`, read by btcd clients such as lnd, lists taproot once it
is active. The pruning and signet fields are not included.

### getblockfilter

A block's client filter. **Parameters:** `blockhash`, `filtertype`
(`basic`). **Result:** `{"filter", "header"}`. Requires client filters,
and returns -1 without them.

### getblockstats

Statistics of a confirmed block, in satoshis. **Parameters:**
`hash_or_height`, `stats` (all). `utxo_size_inc` and
`utxo_size_inc_actual` are not provided.

### getchainstates

The chains being validated. **Parameters:** none. **Result:**
`{"headers", "chainstates"}`, with the confirmed chain, and the candidate
chain while it differs. The cache sizes are 0, and there is no snapshot.

### getchaintips

The tips of the confirmed and candidate chains. **Parameters:** none.
**Result:** the confirmed top as `active`, and the candidate top, if
higher, as `valid-headers` or `headers-only`.

### getchaintxstats

Transaction counts and rate over a window of blocks. **Parameters:**
`nblocks` (one month), `blockhash` (the top). A negative `nblocks` is read
as the default.

### getdeploymentinfo

The deployments at a block. **Parameters:** `blockhash` (the top).
**Result:** `{"hash", "height", "deployments"}`, with the buried
deployments bip34, bip66, bip65, csv and segwit, as configured.

### getdescriptoractivity

The receives and spends of descriptors, in blocks and in the memory
pool. **Parameters:** `blockhashes` (`[]`), `scanobjects` (`[]`),
`include_mempool` (`true`). `include_mempool` requires the address index,
and returns -1 without it. Blocks are reported in the order given.

### getdifficulty

The difficulty of the top block. **Parameters:** none.

### gettxout

An unspent output. **Parameters:** `txid`, `n`, `include_mempool`
(`true`). **Result:** `{"bestblock", "confirmations", "value",
"scriptPubKey", "coinbase"}`, or `null` if spent or unknown. `bs` has no
separate output set: an output is unspent if nothing spends it.

### gettxoutproof

The merkle proof of transactions in a block. **Parameters:** `txids`,
`blockhash` (found from the transactions). No transaction index setting
is required.

### verifytxoutproof

The transactions proven by a proof. **Parameters:** `proof`. **Result:**
an array of transaction hashes, empty if the proof is invalid.

### gettxoutsetinfo

Statistics of the unspent outputs. **Parameters:** `hash_type`
(`hash_serialized_3`), `hash_or_height` (the top), `use_index`
(`true`).

This scans the store, and may take a long time. It returns the fields of
both of bitcoind's forms, with and without the index, at any height and
with any hash type. `muhash` and `none` are also accepted.

### scantxoutset

The unspent outputs of descriptors. **Parameters:** `action`,
`scanobjects` (`[]`).

| Action | Result |
| ------ | ------ |
| `start` | The outputs found |
| `status` | `null` |
| `abort` | `false` |

With the address index, each script is found directly. Without it, the
store is scanned. `desc` in the result is inferred from the script.

### scanblocks

The blocks whose client filters match descriptors. **Parameters:**
`action`, `scanobjects`, `start_height` (0), `stop_height` (the top),
`filtertype` (`basic`), `options` (ignored). Only `start` is supported.
Requires client filters. As filters are probabilistic, some blocks may
not contain a match.

### verifychain

Verifies the chain. **Parameters:** `checklevel` (3), `nblocks` (6).
**Result:** `true`. The store does not need verification, so this does
nothing.

### preciousblock

Prefers a block over another of equal work. **Parameters:** `blockhash`.
**Result:** `null`, once the chain is reorganized. A block already
confirmed returns -5.

### waitforblock

Waits for a block to be confirmed. **Parameters:** `blockhash`, `timeout`
(0, no limit). **Result:** `{"hash", "height"}` of the top. Returns when
the block is confirmed at any depth.

### waitforblockheight

Waits for the top to reach a height. **Parameters:** `height`, `timeout`
(0). **Result:** `{"hash", "height"}` of the top.

### waitfornewblock

Waits for a new top. **Parameters:** `timeout` (0), `current_tip`.
**Result:** `{"hash", "height"}` of the top.

The timeouts are in milliseconds. A connection waits for one of these at
a time.

## 4. Memory pool

The memory pool is the set of unconfirmed transactions that can be
confirmed.

### getmempoolinfo

The size and fee policy of the pool. **Parameters:** none.

| Field | Value |
| ----- | ----- |
| `loaded` | `true` |
| `size`, `bytes`, `total_fee` | The count, virtual size and fees of the pool |
| `usage` | The size of the pool's tables in the store |
| `maxmempool` | The free space of the store's volume |
| `mempoolminfee` | `node.minimum_fee_rate`, or the maximum while the node is not current |
| `minrelaytxfee` | `node.minimum_fee_rate` |
| `incrementalrelayfee` | `node.minimum_bump_rate` |
| `unbroadcastcount` | `0` |
| `fullrbf` | `false` |

### getrawmempool

The transactions in the pool. **Parameters:** `verbose` (`false`),
`mempool_sequence` (`false`). `mempool_sequence` is always 1.

### getmempoolentry

A transaction in the pool. **Parameters:** `txid`. **Result:** its size,
time, height, fees, and ancestor and descendant totals.

### getmempoolancestors

The pooled ancestors of a pooled transaction. **Parameters:** `txid`,
`verbose` (`false`).

### getmempooldescendants

The pooled descendants of a pooled transaction. **Parameters:** `txid`,
`verbose` (`false`).

### gettxspendingprevout

The spenders of outputs. **Parameters:** `outputs`, `options`.
**Result:** each output, with its `spendingtxid` if spent. A pooled
spender is returned before a confirmed one. No index setting is
required.

### savemempool

Writes the pool to `mempool.dat` in the store directory. **Parameters:**
none. **Result:** `{"filename"}`. The file is version 1.

### importmempool

Submits the transactions of a `mempool.dat` file on the server.
**Parameters:** `filepath`, `options` (ignored). **Result:** `{}`.
Transactions that are rejected are skipped.

## 5. Transactions

### getrawtransaction

A transaction, confirmed or unconfirmed. **Parameters:** `txid`,
`verbosity` (0), `blockhash` (ignored).

| Verbosity | Result |
| --------- | ------ |
| 0 | The transaction as hex |
| 1 | The transaction, with its block and confirmations |
| 2 | As 1, with each input's `prevout` and the fee |

No transaction index setting is required. Verbosity is a number, not a
boolean.

### sendrawtransaction

Submits a transaction to the memory pool. **Parameters:** `hexstring`,
`maxfeerate`, `maxburnamount` (both ignored). **Result:** the
transaction hash. The pool accepts transactions only when the node is
current.

### testmempoolaccept

Tests whether transactions would be accepted to the memory pool.
**Parameters:** `rawtxs`, `maxfeerate` (ignored). **Result:** for each,
`{"txid", "wtxid", "allowed", "reject-reason"}`. The transactions are
tested as one package.

### submitpackage

Submits a package of up to 25 transactions to the memory pool.
**Parameters:** `package`, `maxfeerate`, `maxburnamount` (both ignored).

### createrawtransaction

Creates an unsigned transaction. **Parameters:** `inputs`, `outputs`,
`locktime` (0), `replaceable` (`true`), `version` (2). Amounts are
numbers, not strings.

### decoderawtransaction

Decodes a transaction. **Parameters:** `hexstring`, `iswitness`.
**Result:** the transaction, including its `hex`.

### decodescript

Decodes a script. **Parameters:** `hexstring`.

### combinerawtransaction

Combines the signatures of partially signed copies of a transaction.
**Parameters:** `txs`.

### createpsbt

Creates a PSBT. **Parameters:** `inputs`, `outputs`, `locktime` (0),
`replaceable` (`true`), `version` (2), `psbt_version` (2).

### converttopsbt

Converts a transaction to a PSBT. **Parameters:** `hexstring`,
`permitsigdata` (`false`), `iswitness`, `psbt_version` (2).

### decodepsbt

Decodes a PSBT, version 0 or 2. **Parameters:** `psbt`.

### analyzepsbt

The state of a PSBT, and its next role. **Parameters:** `psbt`.

### combinepsbt

Combines PSBTs of the same transaction. **Parameters:** `txs`.

### finalizepsbt

Finalizes a PSBT, and optionally extracts its transaction.
**Parameters:** `psbt`, `extract` (`true`).

### joinpsbts

Joins the inputs and outputs of PSBTs. **Parameters:** `txs`.

### utxoupdatepsbt

Adds the previous outputs, and the scripts and derivations of matching
descriptors, to a PSBT. **Parameters:** `psbt`, `descriptors` (`[]`).

## 6. Mining

### getmininginfo

The mining state. **Parameters:** none. `networkhashps` is computed from
the difficulty. `pooledtx` is 0, and `blockmintxfee` is the maximum.

### getnetworkhashps

The hash rate over a window of blocks. **Parameters:** `nblocks` (120),
`height` (the top).

### submitheader

Submits a block header. **Parameters:** `hexdata`. **Result:** `null`.

## 7. Network

### getnetworkinfo

The state of the network. **Parameters:** none. `version` and
`subversion` are `bitcoind.version` and `bitcoind.subversion`.

### getconnectioncount

The number of peer connections. **Parameters:** none.

### getpeerinfo

The connected peers. **Parameters:** none.

### getnettotals

The bytes sent and received. **Parameters:** none.

### getnodeaddresses

Addresses from the address pool. **Parameters:** `count` (1, 0 for all),
`network`.

### getaddrmaninfo

The address pool, by network. **Parameters:** none.

### addnode

Connects to a peer. **Parameters:** `node`, `command`, `v2transport`
(`false`). `add` connects now and keeps reconnecting, `onetry` connects
once, and `remove` disconnects.

### getaddednodeinfo

The connected manual peers. **Parameters:** `node`.

### disconnectnode

Disconnects a peer. **Parameters:** `address` or `nodeid`. A manual peer
reconnects.

### setnetworkactive

Suspends or resumes the network. **Parameters:** `state`. **Result:** the
resulting state.

### ping

**Parameters:** none. **Result:** `null`. `bs` pings each peer on its own
schedule.

## 8. Utility

### validateaddress

Validates an address. **Parameters:** `address`. An invalid address
returns only `{"isvalid": false}`.

### createmultisig

Creates a multisig script. **Parameters:** `nrequired`, `keys`,
`address_type` (`legacy`). Up to 16 keys.

### deriveaddresses

Derives addresses from a descriptor. **Parameters:** `descriptor`,
`range`. Up to 10,000 addresses. The checksum is optional.

### getdescriptorinfo

Analyzes a descriptor. **Parameters:** `descriptor`.

### verifymessage

Verifies a signed message. **Parameters:** `address`, `signature`,
`message`.

### estimatesmartfee

The fee rate for a transaction to confirm within a number of blocks.
**Parameters:** `conf_target` (1 to 1008), `estimate_mode`
(`economical`). Requires `node.fee_estimate_horizon`.

### getindexinfo

The indexes. **Parameters:** `index_name`. **Result:** `txindex`, and the
basic block filter index when client filters are stored.

## 9. Control

### help

The served methods, as one line, or the usage of a method.
**Parameters:** `command`.

### rpc.discover

The OpenRPC description of the methods. **Parameters:** `show_hidden`.

### getopenrpcinfo

As [`rpc.discover`](#rpcdiscover).

### getrpcinfo

The active commands and the log path. **Parameters:** none.

### getmemoryinfo

**Parameters:** `mode` (`stats`). **Result:** zeros, as `bs` locks no
memory.

### uptime

Seconds since the server started. **Parameters:** none.

### logging

The log levels of `bs` (see [Admin Console](admin#log_subscribe)), which
can be read but not changed. **Parameters:** `include`, `exclude`.

## 10. Notifications

### getzmqnotifications

The [Bitcoind ZMQ](zeromq) topics and their addresses. **Parameters:**
none. Every topic is published on every `[bitcoind_zmq]` address.

## 11. Methods not served

| Methods | Reason | Error |
| ------- | ------ | ----- |
| Wallet methods, `signrawtransactionwithkey`, `descriptorprocesspsbt`, `signmessagewithprivkey` | Signing belongs in the wallet, so private keys never reach the server | -32601 |
| `getblocktemplate`, `submitblock`, `prioritisetransaction`, `getprioritisedtransactions`, `getmempoolcluster` | Mining and prioritisation order pool transactions by their dependencies, which requires the transaction graph of the version 5 pool | -33 |
| `invalidateblock`, `reconsiderblock` | The store does not record a valid block as invalid by command | -32601 |
| `pruneblockchain` | Dynamic pruning is not supported | -1 |
| `dumptxoutset`, `loadtxoutset` | These serve assumeutxo, which starts a node from an output set it has not validated | -32601 |
| `getblockfrompeer` | Refills dynamically pruned blocks, and dynamic pruning is not supported | -32601 |
| `setban`, `listbanned`, `clearbanned` | A peer that violates the protocol is disconnected, and none is banned (see [P2P](p2p#26-misbehavior)) | -20 |
| `exportasmap` | Not yet implemented | -1 |
| `abortprivatebroadcast`, `getprivatebroadcastinfo` | Private broadcast is experimental in bitcoind, and not supported | -32601 |
| `stop` | The server is stopped at its console or by signal, not by a client | -32601 |
| Test methods | These control bitcoind's own test suite | -32601 |