# Native REST

The native interface is libbitcoin's own REST API, served over HTTP and
websocket. It navigates blocks, headers, transactions, inputs, outputs,
spenders and addresses, and serves each object as JSON, as raw bytes, or
as hex text.
It also serves the embedded block explorer (see
[Configuration](../configuration/index#56-block-explorer)).

Its protocols share one port, and their secure forms share another:

| Port | Default | Protocols |
| ---- | ------- | --------- |
| Clear (`bind`) | 8180 | HTTP, WS |
| Secure (`safe`) | 8143 | HTTPS, WSS |

[REST](https://en.wikipedia.org/wiki/REST) (representational state
transfer) is the architectural style of the web, defined by Roy
Fielding in 2000. Its central principle is that a URL identifies a resource, so the
same request URL returns the same object. That is what makes responses
cacheable, by the client or by any proxy between it and the server. It
also requires that requests be stateless, each carrying everything needed
to answer it. And the interface is navigable: from a starting point, every
resource can be reached by following the resources related to it.

In the native interface, a path by hash names an object that never
changes, such as `/v1/block/hash/{block hash}` or `/v1/tx/{tx hash}`, so its
response never changes. A path by height, `top`, or address names the
current state of a chain that grows, so its response can change.

Starting from `top`, every object can be reached, each result carrying the
hashes and indexes that form the next request's URL:

- A height gives a block.
- A block gives its header, whose previous hash gives the block before
  it, back to genesis.
- A block gives its transactions.
- A transaction gives its inputs and outputs.
- An input gives the output it spends.
- An output gives the inputs that spend it.

## 1. Paths

Every path, and the method it calls. `{block}` is `hash/{block hash}` or
`height/{height}`.

| Path | Method |
| ---- | ------ |
| `/v1/configuration` | [`configuration`](#configuration) |
| `/v1/top` | [`top`](#top) |
| `/v1/top/subscribe` | [`top_subscribe`](#top_subscribe) |
| `/v1/block/{block}` | [`block`](#block) |
| `/v1/block/{block}/header` | [`block_header`](#block_header) |
| `/v1/block/{block}/header/context` | [`block_header_context`](#block_header_context) |
| `/v1/block/{block}/details` | [`block_details`](#block_details) |
| `/v1/block/{block}/txs` | [`block_txs`](#block_txs) |
| `/v1/block/{block}/tx/{position}` | [`block_tx`](#block_tx) |
| `/v1/block/{block}/filter/{type}` | [`block_filter`](#block_filter) |
| `/v1/block/{block}/filter/{type}/hash` | [`block_filter_hash`](#block_filter_hash) |
| `/v1/block/{block}/filter/{type}/header` | [`block_filter_header`](#block_filter_header) |
| `/v1/block/subscribe` | [`block_subscribe`](#block_subscribe) |
| `/v1/tx/{tx hash}` | [`tx`](#tx) |
| `/v1/tx/{tx hash}/header` | [`tx_header`](#tx_header) |
| `/v1/tx/{tx hash}/details` | [`tx_details`](#tx_details) |
| `/v1/tx/subscribe` | [`tx_subscribe`](#tx_subscribe) |
| `/v1/input/{tx hash}` | [`inputs`](#inputs) |
| `/v1/input/{tx hash}/{index}` | [`input`](#input) |
| `/v1/input/{tx hash}/{index}/script` | [`input_script`](#input_script) |
| `/v1/input/{tx hash}/{index}/witness` | [`input_witness`](#input_witness) |
| `/v1/output/{tx hash}` | [`outputs`](#outputs) |
| `/v1/output/{tx hash}/{index}` | [`output`](#output) |
| `/v1/output/{tx hash}/{index}/script` | [`output_script`](#output_script) |
| `/v1/output/{tx hash}/{index}/spender` | [`output_spender`](#output_spender) |
| `/v1/output/{tx hash}/{index}/spenders` | [`output_spenders`](#output_spenders) |
| `/v1/output/{tx hash}/{index}/subscribe` | [`output_subscribe`](#output_subscribe) |
| `/v1/address/{script hash}` | [`address`](#address) |
| `/v1/address/{script hash}/confirmed` | [`address_confirmed`](#address_confirmed) |
| `/v1/address/{script hash}/unconfirmed` | [`address_unconfirmed`](#address_unconfirmed) |
| `/v1/address/{script hash}/balance` | [`address_balance`](#address_balance) |
| `/v1/address/{script hash}/subscribe` | [`address_subscribe`](#address_subscribe) |

## 2. Calling pattern

Every request is a `GET` of a path under `/v1`, on the `[native]`
binding (default port 8180):

```
http://localhost:8180/v1/{object}/{identifier}/{component}?format={format}
```

```
$ curl "http://localhost:8180/v1/top?format=json"
9
```

### 2.1 Identifiers

| Identifier | Form |
| ---------- | ---- |
| Block, transaction hash | 64 hex characters, in the usual reversed (display) order |
| Height, position, index | Decimal, no leading zeros |
| Script hash | SHA-256 of an output script, reversed (display) hex, as in Electrum |
| Filter type | `0` (BIP158 basic filter) |

### 2.2 Formats

| `format` | Media type | Response |
| -------- | ---------- | -------- |
| `json` | `application/json` | The object as JSON |
| `data` | `application/octet-stream` | The object's raw bytes, usually its wire serialization |
| `text` | `text/plain` | The `data` bytes as hex |
| `html` | `text/html` | The block explorer page |

`format` takes precedence over the `Accept` header. Without `format`, the
`Accept` header must name one of these media types exactly. Since `*/*`
(curl's default) names none of them, a request with neither is refused
with 406, so give `format` in requests from scripts and tools.

Hashes inside JSON are in display order, and hashes inside `data` and
`text` are in internal (wire) order. A number (such as a height or
balance) is returned as `data` in its minimal little-endian bytes, and as
`text` in their hex. Zero is the single byte `0x00`, so `00` in text,
and `0` in JSON. An empty set or empty data (such as an empty script) is
an empty `data` or `text` body.

Not every method supports every format. Each method below lists its
formats, and an unsupported one is refused with 406.

### 2.3 Options

| Option | Default | Applies to | Purpose |
| ------ | ------- | ---------- | ------- |
| `witness` | `true` | block, transaction and input methods | `false` omits witness data |
| `turbo` | `true` | address methods | `false` runs the query on one thread, as when `database.turbo` is off |
| `stop` | `false` | subscribe methods | `true` ends the subscription |

Each option takes only `true` or `false`. An option the method does not
take, or any other value, is refused with 400.

### 2.4 HTTP status codes

Over HTTP, each response carries one of these statuses
([RFC 9110 §15](https://www.rfc-editor.org/rfc/rfc9110.txt)). Over a websocket
there is no status (§2.5).

| Status | Meaning |
| ------ | ------- |
| 200 | Success |
| 400 | Invalid option, option value or target |
| 401 | Credentials are configured and none were given |
| 403 | The credential does not permit the method, or the origin is not allowed |
| 404 | The object was not found |
| 406 | The format is not supported by the method |
| 500 | Store integrity fault |
| 501 | A required index or feature is disabled (address index, client filters) |

### 2.5 Websocket

Upgrade any request on the native port to a websocket.

- Each frame sent is one request path and query.
- Each reply frame carries only the response body.
- JSON is the default format.
- `data` replies are binary frames.
- A request that finds nothing returns an empty frame.
- An invalid request closes the websocket.
- Subscriptions are per connection.
- Subscriptions can be made over HTTP.
- Notifications are sent only over a websocket.

To subscribe with the `websockets` package (`pip install websockets`):

```python
import asyncio
import websockets

async def main():
    async with websockets.connect("ws://localhost:8180/") as socket:
        await socket.send("/v1/top/subscribe")
        while True:
            print(await socket.recv())

asyncio.run(main())
```

The first reply is the current top height, followed by the height of each
new block:

```
9
10
11
```

## 3. Server

### configuration

The interface's indexes and relevant settings.

```
/v1/configuration
```

Formats: `json`.

```
$ curl "http://localhost:8180/v1/configuration?format=json"
```

```json
{
    "address": true,
    "filter": true,
    "turbo": false,
    "witness": true,
    "retarget": true,
    "difficult": true,
    "pruned": 0
}
```

| Field | Meaning |
| ----- | ------- |
| `address` | The address index is enabled |
| `filter` | Client filters are enabled |
| `turbo` | `database.turbo` |
| `witness` | `node.require_witness` |
| `retarget` | `forks.retarget` |
| `difficult` | `forks.difficult` |
| `pruned` | The height below which blocks are pruned, or `0` |

### top

The height of the top confirmed block.

```
/v1/top
```

Formats: `json`, `data`, `text`.

| Request | Response |
| ------- | -------- |
| `/v1/top?format=json` | `9` |
| `/v1/top?format=text` | `09` |

### top_subscribe

The top height, followed by a notification for each new top.

```
/v1/top/subscribe
```

Formats: `json`, `data`, `text`. Options: `stop`.

The reply is the current top height, as for `top`. Over a websocket, each
new block then sends its height, and a reorganization sends the height of
the fork point:

```
→ /v1/top/subscribe?format=text
← 09
← 0a
→ /v1/top/subscribe?stop=true
←
```

## 4. Blocks

In the block paths below, `{block}` is `hash/{block hash}` or
`height/{height}`. A hash finds any stored block, and a height finds the
block at that height on the confirmed chain.

### block

A block.

```
/v1/block/{block}
```

Formats: `json`, `data`, `text`. Options: `witness`.

```
$ curl "http://localhost:8180/v1/block/height/0?format=json"
```

```json
{
    "header": {
        "hash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
        "version": 1,
        "previous": "0000000000000000000000000000000000000000000000000000000000000000",
        "merkle_root": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
        "timestamp": 1231006505,
        "bits": 486604799,
        "nonce": 2083236893,
        "height": 0
    },
    "transactions": [
        {
            "hash": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
            "version": 1,
            "inputs": [
                {
                    "point": {
                        "hash": "0000000000000000000000000000000000000000000000000000000000000000",
                        "index": 4294967295
                    },
                    "script": "[ffff001d] [04] [5468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73]",
                    "witness": "",
                    "sequence": 4294967295
                }
            ],
            "outputs": [
                {
                    "value": 5000000000,
                    "script": "[04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f] checksig"
                }
            ],
            "locktime": 0
        }
    ]
}
```

Scripts are written as tokens: pushes as `[hex]` and opcodes by name.
`data` is the block in wire format, with witness data (BIP144) unless
`witness=false`, which also omits `witness` from the JSON.

### block_header

A block header.

```
/v1/block/{block}/header
```

Formats: `json`, `data`, `text`.

```
$ curl "http://localhost:8180/v1/block/height/0/header?format=json"
```

```json
{
    "hash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
    "version": 1,
    "previous": "0000000000000000000000000000000000000000000000000000000000000000",
    "merkle_root": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
    "timestamp": 1231006505,
    "bits": 486604799,
    "nonce": 2083236893,
    "height": 0
}
```

`text` is the 80 byte header in hex:

```
0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c
```

### block_header_context

The validation context of a block: its median time past, its state and
the soft forks active at its height.

```
/v1/block/{block}/header/context
```

Formats: `json`.

```
$ curl "http://localhost:8180/v1/block/height/1/header/context?format=json"
```

```json
{
    "hash": "00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048",
    "height": 1,
    "mtp": 1231006505,
    "state": {
        "size": 215,
        "weight": 860,
        "count": 1,
        "validated": true,
        "confirmed": true,
        "confirmable": true,
        "unconfirmable": false
    },
    "forks": {
        "bip30": false,
        "bip34": false,
        "bip66": false,
        "bip65": false,
        "bip90": false,
        "bip68": false,
        "bip112": false,
        "bip113": false,
        "bip141": false,
        "bip143": false,
        "bip147": false,
        "bip42": false,
        "bip341": false,
        "bip342": false
    }
}
```

`state` is present once the block's transactions are stored. `forks` shows
each soft fork as active or not at the block's height. This example is from
a test store, where none are active.

### block_details

Sizes, value and reward of a block.

```
/v1/block/{block}/details
```

Formats: `json`.

```
$ curl "http://localhost:8180/v1/block/height/1/details?format=json"
```

```json
{
    "hash": "00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048",
    "height": 1,
    "count": 1,
    "segregated": false,
    "nominal": 215,
    "maximal": 215,
    "weight": 860,
    "virtual": 215,
    "value": 0,
    "fees": 0,
    "subsidy": 5000000000,
    "reward": 5000000000,
    "claim": 5000000000
}
```

| Field | Meaning |
| ----- | ------- |
| `count` | Transactions in the block |
| `segregated` | The block has witness data |
| `nominal`, `maximal` | Size without and with witness data |
| `weight`, `virtual` | Weight and virtual size |
| `value` | Total value of the block's inputs |
| `fees` | Total fees |
| `subsidy` | Block subsidy |
| `reward` | Fees plus subsidy |
| `claim` | Total value of the coinbase outputs |

### block_txs

The transaction hashes of a block, in order.

```
/v1/block/{block}/txs
```

Formats: `json`, `data`, `text`.

```
$ curl "http://localhost:8180/v1/block/height/0/txs?format=json"
```

```json
[
    "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
]
```

`data` is the 32 byte hashes concatenated, in internal order.

### block_tx

The transaction at a position in a block.

```
/v1/block/{block}/tx/{position}
```

Formats: `json`, `data`, `text`. Options: `witness`.

```
$ curl "http://localhost:8180/v1/block/height/0/tx/0?format=json"
```

The response is the transaction, as for [`tx`](#tx).

### block_filter

The BIP158 client filter of a block. Requires client filters
(`node.provide_filters`).

```
/v1/block/{block}/filter/{type}
```

Formats: `json`, `data`, `text`.

```
$ curl "http://localhost:8180/v1/block/height/0/filter/0?format=json"
```

```json
"019dfca8"
```

### block_filter_hash

The hash of a block's client filter.

```
/v1/block/{block}/filter/{type}/hash
```

Formats: `json`, `data`, `text`.

```
$ curl "http://localhost:8180/v1/block/height/0/filter/0/hash?format=json"
```

```json
"c03705b2d6fb76a59664f1d63fe8fdbb2dc076d18175fdc51d11c43afaf78a4c"
```

### block_filter_header

The client filter header of a block, which commits to its filter and
all those before it.

```
/v1/block/{block}/filter/{type}/header
```

Formats: `json`, `data`, `text`.

```
$ curl "http://localhost:8180/v1/block/height/0/filter/0/header?format=json"
```

```json
"21584579b7eb08997773e5aeff3a7f932700042d0ed2a6129012b7d7ae81b750"
```

### block_subscribe

The top block hash, followed by a notification for each newly confirmed
block.

```
/v1/block/subscribe
```

Formats: `json`, `data`, `text`. Options: `stop`.

```
→ /v1/block/subscribe
← "000000008d9dc510f23c2657fc4f67bea30078cc05a90eb89e84cc475c080805"
← "<hash of the next confirmed block>"
```

## 5. Transactions

### tx

A transaction, confirmed or unconfirmed.

```
/v1/tx/{tx hash}
```

Formats: `json`, `data`, `text`. Options: `witness`.

```
$ curl "http://localhost:8180/v1/tx/4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b?format=json"
```

```json
{
    "hash": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
    "version": 1,
    "inputs": [
        {
            "point": {
                "hash": "0000000000000000000000000000000000000000000000000000000000000000",
                "index": 4294967295
            },
            "script": "[ffff001d] [04] [5468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73]",
            "witness": "",
            "sequence": 4294967295
        }
    ],
    "outputs": [
        {
            "value": 5000000000,
            "script": "[04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f] checksig"
        }
    ],
    "locktime": 0
}
```

`data` is the transaction in wire format, with witness data (BIP144)
unless `witness=false`.

### tx_header

The header of the block that confirms a transaction.

```
/v1/tx/{tx hash}/header
```

Formats: `json`, `data`, `text`.

The response is the header, as for [`block_header`](#block_header). An
unconfirmed transaction returns 404.

### tx_details

Sizes, value and fee of a transaction, and where it is confirmed.

```
/v1/tx/{tx hash}/details
```

Formats: `json`.

```
$ curl "http://localhost:8180/v1/tx/0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098/details?format=json"
```

```json
{
    "segregated": false,
    "coinbase": true,
    "nominal": 134,
    "maximal": 134,
    "weight": 536,
    "virtual": 134,
    "value": 0,
    "spend": 5000000000,
    "fee": 0,
    "confirmed": {
        "height": 1,
        "position": 0
    }
}
```

`value` is the total of the inputs, `spend` the total of the outputs, and
`fee` their difference. `confirmed` is omitted for an unconfirmed
transaction.

### tx_subscribe

A notification for each new transaction. Websocket only.

```
/v1/tx/subscribe
```

Formats: `json`, `data`, `text`. Options: `stop`.

```
→ /v1/tx/subscribe
←
← "0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098"
```

The reply is empty, and each new transaction then sends its hash.

## 6. Inputs

### inputs

All inputs of a transaction.

```
/v1/input/{tx hash}
```

Formats: `json`, `data`, `text`. Options: `witness`.

```
$ curl "http://localhost:8180/v1/input/4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b?format=json"
```

```json
[
    {
        "point": {
            "hash": "0000000000000000000000000000000000000000000000000000000000000000",
            "index": 4294967295
        },
        "script": "[ffff001d] [04] [5468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73]",
        "witness": "",
        "sequence": 4294967295
    }
]
```

`data` is the inputs in wire format, concatenated without a count, and
without witness data.

### input

One input of a transaction.

```
/v1/input/{tx hash}/{index}
```

Formats: `json`, `data`, `text`. Options: `witness`.

The response is the input, as one element of [`inputs`](#inputs).

### input_script

The script of an input.

```
/v1/input/{tx hash}/{index}/script
```

Formats: `json`, `data`, `text`.

```
$ curl "http://localhost:8180/v1/input/4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b/0/script?format=json"
```

```json
"[ffff001d] [04] [5468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73]"
```

`data` is the script bytes, without a length prefix.

### input_witness

The witness of an input.

```
/v1/input/{tx hash}/{index}/witness
```

Formats: `json`, `data`, `text`.

JSON is the witness elements as tokens, for example `"[313131]"`. `data`
is the elements concatenated, each with its length prefix.

## 7. Outputs

### outputs

All outputs of a transaction.

```
/v1/output/{tx hash}
```

Formats: `json`, `data`, `text`.

```
$ curl "http://localhost:8180/v1/output/4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b?format=json"
```

```json
[
    {
        "value": 5000000000,
        "script": "[04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f] checksig"
    }
]
```

`data` is the outputs in wire format, concatenated without a count.

### output

One output of a transaction.

```
/v1/output/{tx hash}/{index}
```

Formats: `json`, `data`, `text`.

The response is the output, as one element of [`outputs`](#outputs).

### output_script

The script of an output.

```
/v1/output/{tx hash}/{index}/script
```

Formats: `json`, `data`, `text`.

```
$ curl "http://localhost:8180/v1/output/4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b/0/script?format=json"
```

```json
"[04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f] checksig"
```

### output_spender

The confirmed input that spends an output.

```
/v1/output/{tx hash}/{index}/spender
```

Formats: `json`, `data`, `text`.

```json
{
    "hash": "<spending transaction hash>",
    "index": 0
}
```

The response is the spending input's point: its transaction hash and
input index. An unspent output, or one spent only by an unconfirmed
transaction, returns 404.

### output_spenders

Every input that spends an output, confirmed or unconfirmed.

```
/v1/output/{tx hash}/{index}/spenders
```

Formats: `json`, `data`, `text`.

The response is an array of points, as for
[`output_spender`](#output_spender). An output with no spender returns
404.

### output_subscribe

The output, as for [`output`](#output).

```
/v1/output/{tx hash}/{index}/subscribe
```

Formats: `json`, `data`, `text`. Options: `stop`.

## 8. Addresses

Address methods identify an address by its script hash (§2.1). They
require the address index, which is enabled unless disabled
([Configuration §5.13](../configuration/index#513-disable-the-address-index)),
and return 501 without it.

### address

Every output ever paid to the address, spent or unspent, confirmed or
unconfirmed.

```
/v1/address/{script hash}
```

Formats: `json`, `data`, `text`. Options: `turbo`.

```
$ curl "http://localhost:8180/v1/address/cc0d7111befe9f24f1824c797e837c5cff2f8773901ccb9aca0372a2a6c48d34?format=json"
```

```json
[
    {
        "point": {
            "hash": "0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098",
            "index": 0
        },
        "value": 5000000000
    }
]
```

`data` is each output's point (36 bytes) and value (8 bytes),
concatenated. An address with no outputs returns 404.

### address_confirmed

The address's confirmed unspent outputs.

```
/v1/address/{script hash}/confirmed
```

Formats: `json`, `data`, `text`. Options: `turbo`.

The response has the same form as [`address`](#address).

### address_unconfirmed

The address's unconfirmed unspent outputs.

```
/v1/address/{script hash}/unconfirmed
```

Formats: `json`, `data`, `text`. Options: `turbo`.

The response has the same form as [`address`](#address).

### address_balance

The total value of the address's confirmed unspent outputs.

```
/v1/address/{script hash}/balance
```

Formats: `json`, `data`, `text`. Options: `turbo`.

| Request | Response |
| ------- | -------- |
| `?format=json` | `5000000000` |
| `?format=text` | `00f2052a01` |

An address with no funds returns `0`.

### address_subscribe

The address's outputs, as for [`address`](#address).

```
/v1/address/{script hash}/subscribe
```

Formats: `json`, `data`, `text`. Options: `turbo`, `stop`.
