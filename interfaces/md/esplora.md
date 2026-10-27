# Esplora

The Esplora interface is a drop-in for the Esplora explorer API,
served on the `[esplora]` binding. Transactions are served as decoded JSON
with resolved previous outputs and computed fees, and addresses by encoded
address or by output script hash.

Its protocols share one port, and their secure forms share another:

| Port | Default | Protocols |
| ---- | ------- | --------- |
| Clear (`bind`) | 8780 | HTTP, WS |
| Secure (`safe`) | 8743 | HTTPS, WSS |

## 1. Paths

Every path, and the method it calls. A `{key}` is `address/{address}` or
`scripthash/{scripthash}` (§2.1).

| Path | Method |
| ---- | ------ |
| `/tx/{txid}` | [`tx`](#tx) |
| `/tx/{txid}/hex` | [`tx`](#tx) |
| `/tx/{txid}/raw` | [`tx`](#tx) |
| `/tx/{txid}/status` | [`tx_status`](#tx_status) |
| `/tx/{txid}/merkleblock-proof` | [`tx_merkleblock_proof`](#tx_merkleblock_proof) |
| `/tx/{txid}/merkle-proof` | [`tx_merkle_proof`](#tx_merkle_proof) |
| `/tx/{txid}/outspend/{vout}` | [`tx_outspend`](#tx_outspend) |
| `/tx/{txid}/outspends` | [`tx_outspends`](#tx_outspends) |
| `POST /tx` | [`broadcast`](#broadcast) |
| `POST /txs/package` | [`broadcast_package`](#broadcast_package) |
| `/{key}` | [`address`](#address) |
| `/{key}/txs` | [`address_txs`](#address_txs) |
| `/{key}/txs/chain` | [`address_txs_chain`](#address_txs_chain) |
| `/{key}/txs/chain/{txid}` | [`address_txs_chain`](#address_txs_chain) |
| `/{key}/txs/mempool` | [`address_txs_mempool`](#address_txs_mempool) |
| `/{key}/utxo` | [`address_utxo`](#address_utxo) |
| `/block/{hash}` | [`block`](#block) |
| `/block/{hash}/raw` | [`block`](#block) |
| `/block/{hash}/header` | [`block_header`](#block_header) |
| `/block/{hash}/status` | [`block_status`](#block_status) |
| `/block/{hash}/txs` | [`block_txs`](#block_txs) |
| `/block/{hash}/txs/{start}` | [`block_txs`](#block_txs) |
| `/block/{hash}/txids` | [`block_txids`](#block_txids) |
| `/block/{hash}/txid/{index}` | [`block_txid`](#block_txid) |
| `/block-height/{height}` | [`block_height`](#block_height) |
| `/blocks` | [`blocks`](#blocks) |
| `/blocks/{height}` | [`blocks`](#blocks) |
| `/blocks/tip/height` | [`tip_height`](#tip_height) |
| `/blocks/tip/hash` | [`tip_hash`](#tip_hash) |
| `/mempool` | [`mempool`](#mempool) |
| `/mempool/txids` | [`mempool_txids`](#mempool_txids) |
| `/mempool/recent` | [`mempool_recent`](#mempool_recent) |
| `/fee-estimates` | [`fee_estimates`](#fee_estimates) |

## 2. Calling pattern

Every request is a `GET` of a path on the `[esplora]` binding, except the
two broadcasts, which are a `POST` with a body:

```
http://localhost:8780/{resource}/{identifier}
```

```
$ curl "http://localhost:8780/block-height/0"
000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f
```

Paths are rooted at `/`. A client configured with a base URL that ends in
a prefix, such as `/api`, needs that prefix removed.

### 2.1 Identifiers

| Identifier | Form |
| ---------- | ---- |
| Block, transaction hash | 64 hex characters, in the usual reversed (display) order |
| Height, index, start, output index | Decimal, no leading zeros |
| Address | An address, encoded with the [`[wallet]`](../configuration/reference#6-wallet) prefixes |
| Script hash | 64 hex characters, the SHA-256 of an output script, not reversed |

### 2.2 Formats

The format is fixed by the path. There is no format query and the
`Accept` header is not consulted.

| Response | Media type |
| -------- | ---------- |
| Objects and arrays | `application/json` |
| Hex, hashes and numbers | `text/plain` |
| `/raw` paths | `application/octet-stream` |

> JSON numbers may be written differently than in Esplora, for example
> `1E0` for `1`. These are equivalent JSON encodings.

### 2.3 HTTP status codes

Each response carries one of these statuses
([RFC 9110 §15](https://www.rfc-editor.org/rfc/rfc9110.txt)).

| Status | Meaning |
| ------ | ------- |
| 200 | Success |
| 400 | Invalid address, query value or broadcast |
| 401 | Credentials are configured and none were given |
| 403 | The credential does not permit the method, or the origin is not allowed |
| 404 | The object was not found, or the path is not supported |
| 405 | `GET` of a broadcast, or `POST` of any other path |
| 500 | Store integrity fault |
| 501 | Address paths, without the address index |

### 2.4 Credentials

A credential's method list names Esplora endpoints by the method names in
§1 (see [Configuration §7.3](../configuration/index#73-authentication)).
The `/hex` and `/raw` paths share the method of their object.

### 2.5 Websocket

Esplora is an HTTP/S interface. WS/S is a `bs` extension, which carries
the same request paths as frames on the same port.

- Each text frame is one request path, such as `/blocks/tip/height`.
- A broadcast follows the path with a newline and the body.
- Each response is one frame, the body alone.
- Responses are sent in request order.
- An invalid path, or a method the credential does not permit, closes the
  connection.

```python
import asyncio, websockets

async def main():
    async with websockets.connect("ws://localhost:8780/") as ws:
        await ws.send("/blocks/tip/height")
        print(await ws.recv())

asyncio.run(main())
```

```
9
```

## 3. Transactions

### tx

A transaction, confirmed or unconfirmed.

```
/tx/{txid}
/tx/{txid}/hex
/tx/{txid}/raw
```

```
$ curl "http://localhost:8780/tx/0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098"
```

```json
{
    "txid": "0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098",
    "version": 1,
    "locktime": 0,
    "vin": [
        {
            "txid": "0000000000000000000000000000000000000000000000000000000000000000",
            "vout": 4294967295,
            "is_coinbase": true,
            "scriptsig": "04ffff001d0104",
            "scriptsig_asm": "486604799 4",
            "witness": [],
            "sequence": 4294967295
        }
    ],
    "vout": [
        {
            "scriptpubkey": "410496b538e853519c726a2c91e61ec11600ae1390813a627c66fb8be7947be63c52da7589379515d4e0a604f8141781e62294721166bf621e73a82cbf2342c858eeac",
            "scriptpubkey_asm": "0496b538e853519c726a2c91e61ec11600ae1390813a627c66fb8be7947be63c52da7589379515d4e0a604f8141781e62294721166bf621e73a82cbf2342c858ee OP_CHECKSIG",
            "scriptpubkey_type": "p2pk",
            "value": 5000000000
        }
    ],
    "size": 134,
    "weight": 536,
    "fee": 0,
    "status": {
        "confirmed": true,
        "block_height": 1,
        "block_hash": "00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048",
        "block_time": 1231469665
    }
}
```

Each input that spends a known output also carries that output as
`prevout`, and each output with an address carries it as
`scriptpubkey_address`, encoded with the [`[wallet]`](../configuration/reference#6-wallet) prefixes. An unconfirmed transaction's status is
`{"confirmed": false}`. `/hex` is the transaction in wire format, with
witness data, as hex, and `/raw` the same bytes.

### tx_status

The confirmation status of a transaction, the `status` object of
[`tx`](#tx).

```
/tx/{txid}/status
```

```json
{
    "confirmed": true,
    "block_height": 1,
    "block_hash": "00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048",
    "block_time": 1231469665
}
```

### tx_merkleblock_proof

A confirmed transaction's merkle block (BIP37), as hex.

```
/tx/{txid}/merkleblock-proof
```

The hex begins with the block header. An unconfirmed transaction returns
404.

### tx_merkle_proof

A confirmed transaction's merkle branch.

```
/tx/{txid}/merkle-proof
```

```
$ curl "http://localhost:8780/tx/0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098/merkle-proof"
```

```json
{
    "block_height": 1,
    "merkle": [],
    "pos": 0
}
```

`merkle` is the branch hashes, and `pos` the transaction's position in
the block. An unconfirmed transaction returns 404.

### tx_outspend

The spender of an output.

```
/tx/{txid}/outspend/{vout}
```

```json
{
    "spent": true,
    "txid": "<spending transaction hash>",
    "vin": 0,
    "status": { "confirmed": true, "block_height": 170, ... }
}
```

An unspent output is `{"spent": false}`. A confirmed spender is returned
before an unconfirmed one.

### tx_outspends

The spender of each output of a transaction, an array of
[`tx_outspend`](#tx_outspend) objects in output order.

```
/tx/{txid}/outspends
```

### broadcast

Submits a transaction to the memory pool.

```
POST /tx
```

```
$ curl -X POST --data "<transaction hex>" "http://localhost:8780/tx"
```

The body is the transaction as hex, with nothing following it, and the
response is its hash as text. A transaction already in the pool also
returns its hash. A rejected transaction returns 400, with the reason as
text, and the pool accepts transactions only when the node is current.

### broadcast_package

Submits a package of up to 25 transactions to the memory pool.

```
POST /txs/package
```

The body is a JSON array of transactions as hex. The response is that of
bitcoind's `submitpackage`:

```json
{
    "package_msg": "success",
    "tx-results": {
        "<wtxid>": {
            "txid": "<txid>",
            "vsize_adjusted": 110,
            "vsize": 110,
            "vsize_bip141": 110,
            "fees": {
                "base": 1E-5,
                "effective-feerate": 9.090909090909092E-5,
                "effective-includes": ["<wtxid>"]
            }
        }
    },
    "replaced-transactions": []
}
```

An empty package, or one of more than 25 transactions, returns 400.

## 4. Addresses

These require the address index (`database.address.buckets`), and return
501 without it. Each path takes either form of `{key}`, and the examples
use the output script of the block 1 coinbase,
`scripthash/348dc4a6a27203ca9acb1c9073872fff5c7c837e794c82f1249ffebe11710dcc`.
`esplora.maximum_history` limits the history read for one key.

### address

The funding and spending totals of an address.

```
/address/{address}
/scripthash/{scripthash}
```

```
$ curl "http://localhost:8780/scripthash/348dc4a6a27203ca9acb1c9073872fff5c7c837e794c82f1249ffebe11710dcc"
```

```json
{
    "scripthash": "348dc4a6a27203ca9acb1c9073872fff5c7c837e794c82f1249ffebe11710dcc",
    "chain_stats": {
        "funded_txo_count": 1,
        "funded_txo_sum": 5000000000,
        "spent_txo_count": 0,
        "spent_txo_sum": 0,
        "tx_count": 1
    },
    "mempool_stats": {
        "funded_txo_count": 0,
        "funded_txo_sum": 0,
        "spent_txo_count": 0,
        "spent_txo_sum": 0,
        "tx_count": 0
    }
}
```

The first field is `address` or `scripthash`, echoing the request.

### address_txs

The transactions of an address, as [`tx`](#tx) objects: up to 50
unconfirmed, then up to 25 confirmed, each newest first.

```
/{key}/txs
```

### address_txs_chain

The confirmed transactions of an address, 25 at a time, newest first.

```
/{key}/txs/chain
/{key}/txs/chain/{txid}
```

With a `txid`, the page starts after that transaction. An unknown `txid`
returns 404, and the last returns `[]`.

### address_txs_mempool

The unconfirmed transactions of an address, up to 50, newest first.

```
/{key}/txs/mempool
```

### address_utxo

The unspent outputs of an address.

```
/{key}/utxo
```

```json
[
    {
        "txid": "0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098",
        "vout": 0,
        "value": 5000000000,
        "status": {
            "confirmed": true,
            "block_height": 1,
            "block_hash": "00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048",
            "block_time": 1231469665
        }
    }
]
```

## 5. Blocks

### block

A block.

```
/block/{hash}
/block/{hash}/raw
```

```
$ curl "http://localhost:8780/block/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
```

```json
{
    "id": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
    "height": 0,
    "version": 1,
    "timestamp": 1231006505,
    "bits": 486604799,
    "nonce": 2083236893,
    "difficulty": 1E0,
    "merkle_root": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
    "tx_count": 1,
    "size": 285,
    "weight": 1140,
    "mediantime": 1231006505
}
```

Every block but genesis also carries `previousblockhash`. `/raw` is the
block in wire format, with witness data.

### block_header

A block header, as hex.

```
/block/{hash}/header
```

```
$ curl "http://localhost:8780/block/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f/header"
0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c
```

A header is returned even before its block is stored.

### block_status

Whether a block is on the confirmed chain.

```
/block/{hash}/status
```

```json
{
    "in_best_chain": true,
    "next_best": "000000006a625f06636b8bb6ac7b960a8d03705d1ace08b1a19da3fdcc99ddbd"
}
```

`next_best` is the following confirmed block, and is omitted for the top.

### block_txs

The transactions of a block, as [`tx`](#tx) objects, 25 at a time.

```
/block/{hash}/txs
/block/{hash}/txs/{start}
```

`start` is a multiple of 25, and returns 400 otherwise. A `start` past the
last transaction returns 404.

### block_txids

The transaction hashes of a block, as a JSON array.

```
/block/{hash}/txids
```

```json
[
    "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
]
```

### block_txid

The hash of the transaction at an index in a block, as text.

```
/block/{hash}/txid/{index}
```

### block_height

The hash of the block at a height on the confirmed chain, as text.

```
/block-height/{height}
```

```
$ curl "http://localhost:8780/block-height/0"
000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f
```

### blocks

Up to 10 blocks, as [`block`](#block) objects, descending from a height
on the confirmed chain.

```
/blocks
/blocks/{height}
```

Without a height, the top is used. A height above the top returns 404.

### tip_height

The height of the top confirmed block, as text.

```
/blocks/tip/height
```

```
$ curl "http://localhost:8780/blocks/tip/height"
9
```

### tip_hash

The hash of the top confirmed block, as text.

```
/blocks/tip/hash
```

```
$ curl "http://localhost:8780/blocks/tip/hash"
000000008d9dc510f23c2657fc4f67bea30078cc05a90eb89e84cc475c080805
```

## 6. Memory pool

### mempool

The size and fee histogram of the memory pool.

```
/mempool
```

```json
{
    "count": 1,
    "vsize": 110,
    "total_fee": 1000,
    "fee_histogram": [[9.090909090909092E0, 110]]
}
```

Each histogram entry is a fee rate, in satoshis per virtual byte, and the
virtual size of the transactions at or above it, in bins of 50,000
virtual bytes.

### mempool_txids

The hashes of all transactions in the memory pool, as a JSON array.

```
/mempool/txids
```

### mempool_recent

The 10 transactions most recently added to the memory pool.

```
/mempool/recent
```

```json
[
    {
        "txid": "<txid>",
        "fee": 1000,
        "vsize": 110,
        "value": 4999999000
    }
]
```

`value` is the total of the transaction's outputs.

### fee_estimates

Fee rate estimates, in satoshis per virtual byte, keyed by confirmation
target in blocks.

```
/fee-estimates
```

```json
{
    "1": 21,
    "2": 21,
    "3": 18,
    ...
    "144": 4,
    "504": 2,
    "1008": 1
}
```

The targets are 1 to 25, 144, 504 and 1008. A target without an estimate
is omitted, so a node without fee history returns `{}`.
