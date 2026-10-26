# Bitcoind REST

The bitcoind REST interface is a drop-in for the REST interface of
bitcoind, served on the `[bitcoind]` binding alongside the bitcoind
JSON-RPC interface. Unlike bitcoind, it is always enabled, and it is
protected by the binding's credentials and certificates.

It is reached on the same ports as the bitcoind JSON-RPC interface:

| Port | Default | Protocols |
| ---- | ------- | --------- |
| Clear (`bind`) | 8280 | HTTP |
| Secure (`safe`) | 8243 | HTTPS |

## 1. Paths

Every path, and the method it calls. The extension selects the format
(§2.2).

| Path | Method |
| ---- | ------ |
| `/rest/chaininfo.json` | [`chaininfo`](#chaininfo) |
| `/rest/block/{hash}.{ext}` | [`block`](#block) |
| `/rest/block/notxdetails/{hash}.{ext}` | [`block/notxdetails`](#blocknotxdetails) |
| `/rest/blockhashbyheight/{height}.{ext}` | [`blockhashbyheight`](#blockhashbyheight) |
| `/rest/headers/{hash}.{ext}?count={count}` | [`headers`](#headers) |
| `/rest/blockpart/{hash}.{ext}?offset={offset}&size={size}` | [`blockpart`](#blockpart) |
| `/rest/spenttxouts/{hash}.{ext}` | [`spenttxouts`](#spenttxouts) |
| `/rest/getutxos/{txid}-{n}/....{ext}` | [`getutxos`](#getutxos) |
| `/rest/tx/{txid}.{ext}` | [`tx`](#tx) |
| `/rest/deploymentinfo/{hash}.json` | [`deploymentinfo`](#deploymentinfo) |
| `/rest/blockfilter/basic/{hash}.{ext}` | [`blockfilter`](#blockfilter) |
| `/rest/blockfilterheaders/basic/{hash}.{ext}?count={count}` | [`blockfilterheaders`](#blockfilterheaders) |
| `/rest/mempool/contents.json` | [`mempool`](#mempool) |
| `/rest/mempool/info.json` | [`mempool/info`](#mempoolinfo) |

## 2. Calling pattern

Every request is a `GET` of a path under `/rest`, on the `[bitcoind]`
binding:

```
http://localhost:8280/rest/{resource}/{identifier}.{ext}
```

```
$ curl "http://localhost:8280/rest/blockhashbyheight/0.json"
{"blockhash":"000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"}
```

### 2.1 Identifiers

| Identifier | Form |
| ---------- | ---- |
| Block, transaction hash | 64 hex characters, in the usual reversed (display) order |
| Height, count, offset, size, output index | Decimal, no leading zeros |
| Outpoint | `{txid}-{n}`, a transaction hash and output index |

### 2.2 Formats

The format is selected by the path's extension, not by the `Accept`
header.

| Extension | Media type | Response |
| --------- | ---------- | -------- |
| `.json` | `application/json` | The object as JSON |
| `.bin` | `application/octet-stream` | The object's raw bytes |
| `.hex` | `text/plain` | The raw bytes as hex, followed by a newline |

Not every endpoint supports every extension. Each endpoint below lists its
extensions, and an unsupported one returns 404.

> JSON numbers may be written differently than in bitcoind, for
> example `1E0` for `1`, or `5E1` for `50.00000000`. These are equivalent
> JSON encodings.

### 2.3 HTTP status codes

Each response carries one of these statuses
([RFC 9110 §15](https://www.rfc-editor.org/rfc/rfc9110.txt)).

| Status | Meaning |
| ------ | ------- |
| 200 | Success |
| 400 | Invalid identifier or query value |
| 401 | Credentials are configured and none were given |
| 403 | The credential does not permit the method, or the origin is not allowed |
| 404 | The object was not found, or the path or extension is not supported |
| 500 | Store integrity fault |

### 2.4 Credentials

A credential's method list names REST endpoints by these method names,
which are distinct from the RPC names (see
[Configuration §7.3](../configuration/index#73-authentication)):

| Endpoint | Method name |
| -------- | ----------- |
| `chaininfo` | `chain_information` |
| `block` | `block` |
| `block/notxdetails` | `block_txs` |
| `blockhashbyheight` | `block_hash` |
| `headers` | `block_headers` |
| `blockpart` | `block_part` |
| `spenttxouts` | `block_spent_tx_outputs` |
| `getutxos` | `get_utxos` |
| `tx` | `tx` |
| `deploymentinfo` | `deployment_info` |
| `blockfilter` | `block_filter` |
| `blockfilterheaders` | `block_filter_headers` |
| `mempool` | `mempool` |
| `mempool/info` | `mempool_information` |

## 3. Chain

### chaininfo

The state of the chain.

```
/rest/chaininfo.json
```

Extensions: `.json`.

```
$ curl "http://localhost:8280/rest/chaininfo.json"
```

```json
{
    "chain": "main",
    "blocks": 9,
    "headers": 9,
    "bestblockhash": "000000008d9dc510f23c2657fc4f67bea30078cc05a90eb89e84cc475c080805",
    "bits": "1d00ffff",
    "difficulty": 1E0,
    "time": 1231473279,
    "mediantime": 1231471428,
    "pruned": false
}
```

`blocks` is the top confirmed height, and `headers` the top candidate
height. This is a subset of bitcoind's `chaininfo`.

### deploymentinfo

The soft forks active at a block.

```
/rest/deploymentinfo.json
/rest/deploymentinfo/{hash}.json
```

Extensions: `.json`. Without a hash, the top block is used.

```
$ curl "http://localhost:8280/rest/deploymentinfo/000000009b7262315dbf071787ad3656097b892abffd1f95a1a022f896f533fc.json"
```

```json
{
    "hash": "000000009b7262315dbf071787ad3656097b892abffd1f95a1a022f896f533fc",
    "height": 5,
    "deployments": {
        "bip34": { "type": "buried", "active": false, "height": 227931 },
        "bip66": { "type": "buried", "active": false, "height": 363725 },
        "bip65": { "type": "buried", "active": false, "height": 388381 },
        "csv": { "type": "buried", "active": false, "height": 419328 },
        "segwit": { "type": "buried", "active": false, "height": 481824 }
    }
}
```

The order of the deployments is not fixed. An unknown hash returns 400, as
in bitcoind.

## 4. Blocks

### block

A block, with full transaction details.

```
/rest/block/{hash}.{ext}
```

Extensions: `.json`, `.bin`, `.hex`.

```
$ curl "http://localhost:8280/rest/block/00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048.json"
```

```json
{
    "hash": "00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048",
    "version": 1,
    "versionHex": "00000001",
    "merkleroot": "0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098",
    "time": 1231469665,
    "nonce": 2573394689,
    "bits": "1d00ffff",
    "target": "00000000ffff0000000000000000000000000000000000000000000000000000",
    "difficulty": 1E0,
    "nTx": 1,
    "strippedsize": 215,
    "size": 215,
    "weight": 860,
    "tx": [
        {
            "hex": "01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff0704ffff001d0104ffffffff0100f2052a0100000043410496b538e853519c726a2c91e61ec11600ae1390813a627c66fb8be7947be63c52da7589379515d4e0a604f8141781e62294721166bf621e73a82cbf2342c858eeac00000000",
            "txid": "0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098",
            "hash": "0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098",
            "size": 134,
            "vsize": 134,
            "weight": 536,
            "version": 1,
            "locktime": 0,
            "vin": [
                {
                    "coinbase": "04ffff001d0104",
                    "sequence": 4294967295
                }
            ],
            "vout": [
                {
                    "value": 5E1,
                    "scriptPubKey": {
                        "asm": "0496b538e853519c726a2c91e61ec11600ae1390813a627c66fb8be7947be63c52da7589379515d4e0a604f8141781e62294721166bf621e73a82cbf2342c858ee OP_CHECKSIG",
                        "hex": "410496b538e853519c726a2c91e61ec11600ae1390813a627c66fb8be7947be63c52da7589379515d4e0a604f8141781e62294721166bf621e73a82cbf2342c858eeac",
                        "type": "pubkey"
                    },
                    "n": 0
                }
            ]
        }
    ]
}
```

`.bin` is the block in wire format, with witness data. Unlike bitcoind,
the JSON omits the block's height, confirmations, chain work and adjacent
block hashes.

### block/notxdetails

A block, with transaction hashes in place of transaction details.

```
/rest/block/notxdetails/{hash}.{ext}
```

Extensions: `.json`, `.bin`, `.hex`.

The JSON is as for [`block`](#block), with `tx` an array of transaction
hashes:

```json
"tx": [
    "0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098"
]
```

`.bin` and `.hex` are the full block, as for `block`.

### blockhashbyheight

The hash of the block at a height on the confirmed chain.

```
/rest/blockhashbyheight/{height}.{ext}
```

Extensions: `.json`, `.bin`, `.hex`.

```
$ curl "http://localhost:8280/rest/blockhashbyheight/0.json"
```

```json
{
    "blockhash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
}
```

`.bin` and `.hex` are the hash in internal (wire) order, as in Bitcoin
Core:

```
6fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000
```

### headers

Consecutive block headers, starting at a block on the confirmed chain.

```
/rest/headers/{hash}.{ext}?count={count}
/rest/headers/{count}/{hash}.{ext}
```

Extensions: `.json`, `.bin`, `.hex`. `count` defaults to 5, and is limited
to 2000.

```
$ curl "http://localhost:8280/rest/headers/00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048.json?count=1"
```

```json
[
    {
        "hash": "00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048",
        "version": 1,
        "versionHex": "00000001",
        "merkleroot": "0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098",
        "time": 1231469665,
        "nonce": 2573394689,
        "bits": "1d00ffff",
        "target": "00000000ffff0000000000000000000000000000000000000000000000000000",
        "difficulty": 1E0
    }
]
```

`.bin` is the 80 byte headers concatenated. A `count` of 0 returns 404,
and a `count` above 2000 is reduced to 2000, where bitcoind refuses both
with 400.

### blockpart

A range of bytes from a block.

```
/rest/blockpart/{hash}.{ext}?offset={offset}&size={size}
```

Extensions: `.bin`, `.hex`. `offset` and `size` are required.

```
$ curl "http://localhost:8280/rest/blockpart/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f.hex?offset=0&size=80"
0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c
```

The bytes are taken from the block in wire format, with witness data. A
range past the end of the block returns 400.

### spenttxouts

The outputs spent by each transaction of a confirmed block.

```
/rest/spenttxouts/{hash}.{ext}
```

Extensions: `.json`, `.bin`, `.hex`.

The JSON is an array with one entry per transaction, each an array of the
outputs that transaction spends. The coinbase spends none, so its entry is
empty. For a block with only a coinbase:

```json
[
    []
]
```

Each spent output is `{"value", "scriptPubKey"}`, where `scriptPubKey`
also carries `desc`, and `address` where one exists.

## 5. Transactions

### tx

A transaction, confirmed or unconfirmed.

```
/rest/tx/{txid}.{ext}
```

Extensions: `.json`, `.bin`, `.hex`.

```
$ curl "http://localhost:8280/rest/tx/0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098.json"
```

The JSON is the transaction as in [`block`](#block), with `desc` added to
each `scriptPubKey`, followed by:

```json
"blockhash": "00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048",
"confirmations": 9,
"in_active_chain": true,
"blocktime": 1231469665,
"time": 1231469665
```

An unconfirmed transaction has only `"confirmations": 0`. Unlike Bitcoin
Core, no transaction index setting is required.

### getutxos

The state of up to 15 outputs.

```
/rest/getutxos/{txid}-{n}/{txid}-{n}.{ext}
/rest/getutxos/checkmempool/{txid}-{n}.{ext}
```

Extensions: `.json`, `.bin`, `.hex`. The extension follows the last
outpoint. With `checkmempool`, unconfirmed outputs count as unspent and
outputs spent by unconfirmed transactions count as spent.

```
$ curl "http://localhost:8280/rest/getutxos/0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098-0.json"
```

| Field | Value |
| ----- | ----- |
| `chainHeight` | `9` |
| `chaintipHash` | `000000008d9dc510f23c2657fc4f67bea30078cc05a90eb89e84cc475c080805` |
| `bitmap` | `"1"`, one character per outpoint, `1` if unspent |
| `utxos` | One `{"height", "value", "scriptPubKey"}` per unspent outpoint |

`.bin` is the BIP64 encoding. An unknown outpoint returns 200, with `0` in
its bitmap position.

## 6. Client filters

These require client filters (`node.provide_filters`), and return 404
without them.

### blockfilter

The BIP158 basic filter of a block.

```
/rest/blockfilter/basic/{hash}.{ext}
```

Extensions: `.json`, `.bin`, `.hex`.

The JSON is `{"filter": "<hex>"}`. `.bin` is the filter type (`0x00`), the
block hash in wire order, and the length-prefixed filter.

### blockfilterheaders

Consecutive filter headers, starting at a block on the confirmed chain.

```
/rest/blockfilterheaders/basic/{hash}.{ext}?count={count}
/rest/blockfilterheaders/basic/{count}/{hash}.{ext}
```

Extensions: `.json`, `.bin`, `.hex`. `count` defaults to 5, and is limited
to 2000.

```
$ curl "http://localhost:8280/rest/blockfilterheaders/basic/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f.json?count=1"
```

```json
[
    "21584579b7eb08997773e5aeff3a7f932700042d0ed2a6129012b7d7ae81b750"
]
```

`.bin` is the 32 byte filter headers concatenated.

## 7. Memory pool

### mempool

The transactions in the memory pool.

```
/rest/mempool/contents.json?verbose={verbose}&mempool_sequence={sequence}
```

Extensions: `.json`. `verbose` defaults to `true`, and `mempool_sequence`
to `false`.

| Query | Response |
| ----- | -------- |
| `verbose=true` | An object keyed by transaction hash, with each transaction's size, fees, ancestors and descendants |
| `verbose=false` | An array of transaction hashes |
| `verbose=false&mempool_sequence=true` | `{"txids": [...], "mempool_sequence": 1}` |

An empty pool returns `{}`, or `[]` with `verbose=false`. `verbose=true`
with `mempool_sequence=true` returns 400.

### mempool/info

The size and fee policy of the memory pool.

```
/rest/mempool/info.json
```

Extensions: `.json`.

```json
{
    "loaded": true,
    "size": 0,
    "bytes": 0,
    "usage": 0,
    "total_fee": 0E0,
    "maxmempool": 0,
    "mempoolminfee": 0E0,
    "minrelaytxfee": 0E0,
    "incrementalrelayfee": 0E0,
    "unbroadcastcount": 0,
    "fullrbf": false
}
```

`usage` is the size of the pool's tables in the store, and `maxmempool` the
free space on the store's volume. The fee rates are those of the node's
configuration.
