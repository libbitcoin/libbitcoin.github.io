# Native REST

The native interface is libbitcoin's own REST API, served over HTTP and
websocket. It navigates blocks, headers, transactions, inputs, outputs,
spenders and addresses, and serves each object as JSON, as raw bytes, or
as hex text.
It also serves the embedded block explorer (see
[Configuration](../configuration/setups#6-block-explorer)). The
[admin interface](admin) serves it as well, on the admin port. By default
(`node.delay_inbound`) the native port refuses connections until the chain
is current, while the admin port serves it from the start.

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

Every path, and the method it calls. `{chain}` is `confirmed` or
`candidate`, and `{block}` is `hash/{block hash}` or `{chain}/{height}`.

| Path | Method |
| ---- | ------ |
| `/v1/configuration` | [`configuration`](#configuration) |
| `/v1/top` | [`top`](#top) |
| `/v1/top/subscribe` | [`top_subscribe`](#top_subscribe) |
| `/v1/top/{chain}` | [`top_chain`](#top_chain) |
| `/v1/top/{chain}/height` | [`top_height`](#top_height) |
| `/v1/headers/top` | [`headers_top`](#headers_top) |
| `/v1/headers/{chain}/top` | [`top_chain`](#top_chain) |
| `/v1/block/{block}` | [`block`](#block) |
| `/v1/block/{block}/header` | [`block_header`](#block_header) |
| `/v1/block/{block}/header/context` | [`block_header_context`](#block_header_context) |
| `/v1/block/{block}/details` | [`block_details`](#block_details) |
| `/v1/block/{block}/txs` | [`block_txs`](#block_txs) |
| `/v1/block/{block}/txs/details` | [`block_txs_details`](#block_txs_details) |
| `/v1/block/{block}/tx/{position}` | [`block_tx`](#block_tx) |
| `/v1/block/{block}/tx/{position}/input/{index}/script` | [`block_tx_input_script`](#block_tx_input_script) |
| `/v1/block/{block}/tx/{position}/output/{index}/script` | [`block_tx_output_script`](#block_tx_output_script) |
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
| `/v1/fees` | [`fees`](#fees) |
| `/v1/template/{height}` | [`template`](#template) |
| `/v1/template/{height}/txs` | [`template_txs`](#template_txs) |
| `/v1/template/{height}/txs/details` | [`template_txs_details`](#template_txs_details) |
| `/v1/template/subscribe` | [`template_subscribe`](#template_subscribe) |
| `/v1/txs/unconfirmed` | [`txs_unconfirmed`](#txs_unconfirmed) |
| `/v1/txs/unconfirmed/details` | [`txs_unconfirmed_details`](#txs_unconfirmed_details) |

`/v1/headers`, `/v1/headers/{chain}`, `/v1/txs`, `/v1/txs/details`,
`/v1/txs/confirmed` and `/v1/txs/confirmed/details` are reserved and
return 501.

## 2. Calling pattern

Every request is a `GET` of a path under `/v1`, on the `[native]`
binding (default port 8180):

```
http://localhost:8180/v1/{object}/{identifier}/{component}?format={format}
```

```
$ curl "http://localhost:8180/v1/top?format=json"
{"confirmed":{"hash":"000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f","height":0,"header":{"hash":"000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f","version":1,"previous":"0000000000000000000000000000000000000000000000000000000000000000","merkle_root":"4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b","timestamp":1231006505,"bits":486604799,"nonce":2083236893}},"candidate":{"hash":"000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f","height":0,"header":{"hash":"000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f","version":1,"previous":"0000000000000000000000000000000000000000000000000000000000000000","merkle_root":"4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b","timestamp":1231006505,"bits":486604799,"nonce":2083236893}}}
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
| `html` | `text/html` | The block explorer's page for the path |

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
there is no status (§2.6).

| Status | Meaning |
| ------ | ------- |
| 200 | Success |
| 400 | Invalid option, option value or target |
| 401 | Credentials are configured and none were given |
| 403 | The credential does not permit the method, or the origin is not allowed |
| 404 | The object was not found |
| 406 | The format is not supported by the method |
| 500 | Store integrity fault |
| 501 | A required index or feature is disabled (address index, client filters, transaction relay), or the path is reserved |
| 503 | The transaction pool is not yet open |

### 2.5 Pruned blocks

Under pruning (`node.limited_blocks`), a block under the milestone is
stored without the input scripts and witnesses of its transactions, other
than the coinbase ([Querying pruned blocks](../configuration/setups#querying-pruned-blocks)).
Its header, transaction hashes, outputs, spends and details remain. A
method that would return a whole pruned block or transaction, or a
pruned input's script or witness, returns 404: `block`, `block_tx`,
`block_tx_input_script`, `tx`, `input_script` and `input_witness`.
`inputs` and `input` return the `point` and `sequence` of each pruned
input, as JSON only. `configuration` gives the pruned height as
`store.pruned`.

### 2.6 Websocket

Upgrade any request on the native port to a websocket.

- Each frame sent is one request path and query.
- Each reply frame carries only the response body.
- JSON is the default format.
- `data` replies are binary frames.
- A request that finds nothing returns an empty frame.
- An invalid request is answered with its HTTP status. An invalid path
  or format leaves the websocket open. An invalid option, or a method the
  credential does not permit, closes it.
- Subscriptions are per connection.
- HTTP subscriptions are dormant until a websocket upgrade.

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

The first reply is the current tops, followed by the tops again each
time either chain changes ([top_subscribe](#top_subscribe)).

## 3. Server

### configuration

The store's contents, the node's and network's peer settings, the wallet
prefixes and the consensus rules. The node and network settings are also
discoverable by interrogating the node over P2P.

```
/v1/configuration
```

Formats: `json`.

```
$ curl "http://localhost:8180/v1/configuration?format=json"
```

```json
{
    "store": {
        "address": true,
        "filter": true,
        "silent": null,
        "turbo": true,
        "pruned": 0
    },
    "node": {
        "network": "mainnet",
        "limited": false,
        "blocks": true,
        "witness": true,
        "filters": false,
        "privacy": true
    },
    "wallet": {
        "p2kh": 0,
        "p2sh": 5,
        "wif": 128,
        "witness": "bc",
        "silent": "sp",
        "hd_private": 76066276,
        "hd_public": 76067358
    },
    "network": {
        "relay": true,
        "alert": false,
        "reject": false,
        "compact": true,
        "address": true,
        "witness_tx": true,
        "memory_pool": true,
        "not_found": true,
        "protocol_maximum": 70016,
        "protocol_minimum": 31800
    },
    "forks": {
        "bip16": true,
        "bip90": false,
        "bip30": true,
        "bip42": true,
        "bip34": true,
        "bip65": true,
        "bip66": true,
        "bip68": true,
        "bip112": true,
        "bip113": true,
        "bip141": true,
        "bip143": true,
        "bip147": true,
        "bip341": true,
        "bip342": true,
        "bip54_timewarp": true,
        "bip54_timespan": true,
        "bip54_sigops": true,
        "bip54_txsize": true,
        "bip54_coinbase": true,
        "retarget": true,
        "difficult": true,
        "time_warp_patch": false,
        "block_storm_patch": false,
        "signet": false,
        "ltc_time_warp_patch": false,
        "ltc_retarget_overflow_patch": false,
        "ltc_scrypt_proof_of_work": false
    }
}
```

| Field | Meaning |
| ----- | ------- |
| `store.address` | The address index is enabled |
| `store.filter` | Client filters are enabled |
| `store.silent` | The height from which the silent payment index starts, or `null` if it is disabled |
| `store.turbo` | `database.turbo` |
| `store.pruned` | The height above which blocks are not pruned, or `0` |
| `node.network` | The network whose genesis block is configured (`mainnet`, `testnet3`, `testnet4`, `testnet5`, `regtest` or `signet`), or empty if none |
| `node.limited` | `node.limited_blocks` |
| `node.blocks` | `node.provide_blocks` |
| `node.witness` | `node.provide_witness` |
| `node.filters` | `node.provide_filters` |
| `node.privacy` | `node.provide_privacy` |
| `wallet.p2kh` | `wallet.p2kh_prefix` |
| `wallet.p2sh` | `wallet.p2sh_prefix` |
| `wallet.wif` | `wallet.wif_prefix` |
| `wallet.witness` | `wallet.witness_prefix` |
| `wallet.silent` | `wallet.silent_prefix` |
| `wallet.hd_private` | `wallet.hd_private_prefix` |
| `wallet.hd_public` | `wallet.hd_public_prefix` |
| `network.relay` | `peer.enable_relay` |
| `network.alert` | `peer.enable_alert` |
| `network.reject` | `peer.enable_reject` |
| `network.compact` | `peer.enable_compact` |
| `network.address` | `peer.enable_address` |
| `network.witness_tx` | `peer.enable_witness_tx` |
| `network.memory_pool` | `peer.enable_memory_pool` |
| `network.not_found` | `peer.enable_not_found` |
| `network.protocol_maximum` | `peer.protocol_maximum` |
| `network.protocol_minimum` | `peer.protocol_minimum` |
| `forks.*` | Each `[forks]` setting of the same name |

### top

The strong tops: the top block of the confirmed chain, and of the
candidate chain where it differs.

```
/v1/top
```

Formats: `json`, `data`, `text`.

```json
[
    {
        "hash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
        "height": 0,
        "header": {
            "hash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
            "version": 1,
            "previous": "0000000000000000000000000000000000000000000000000000000000000000",
            "merkle_root": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
            "timestamp": 1231006505,
            "bits": 486604799,
            "nonce": 2083236893
        },
        "chain": "confirmed"
    }
]
```

The array is the confirmed top, then the candidate top. When both are
the same block it is one element, labeled `confirmed`. A caller that
wants only the confirmed top reads the first. Each top is its block
hash, its height, its header and its `chain`. `data` is each top in the
same order, its block hash (32 bytes), its height (4 bytes,
little-endian) and its header (80 bytes), 116 bytes each. For this top,
`text` is:

```
6fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000000000000100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c
```

The candidate chain is the chain of headers the node is working toward,
and it runs ahead of the confirmed chain during sync. The two tops can be
at the same height with different hashes, on competing branches. A
candidate top below the confirmed top is a pending reorganization.

### top_subscribe

The confirmed and candidate tops, followed by a notification each time
either chain changes.

```
/v1/top/subscribe
```

Formats: `json`, `data`, `text`. Options: `stop`.

The reply is the current tops, as for `top`. Over a websocket, the tops
are sent again each time a block is confirmed, the confirmed chain is
reorganized, headers are added to the candidate chain, or the candidate
chain is regressed or disorganized:

```
→ /v1/top/subscribe
← [{"hash":"…","height":9,"header":{…},"chain":"confirmed"},{"hash":"…","height":12,"header":{…},"chain":"candidate"}]
← [{"hash":"…","height":10,"header":{…},"chain":"confirmed"},{"hash":"…","height":12,"header":{…},"chain":"candidate"}]
→ /v1/top/subscribe?stop=true
←
```

### top_chain

The top block of one chain.

```
/v1/top/{chain}
/v1/headers/{chain}/top
```

Formats: `json`, `data`, `text`.

```
$ curl "http://localhost:8180/v1/top/confirmed?format=json"
```

```json
{
    "hash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
    "height": 0,
    "header": {
        "hash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
        "version": 1,
        "previous": "0000000000000000000000000000000000000000000000000000000000000000",
        "merkle_root": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
        "timestamp": 1231006505,
        "bits": 486604799,
        "nonce": 2083236893
    },
    "chain": "confirmed"
}
```

The top is as for `top`, so `data` is 116 bytes.

### top_height

The height of the top block of one chain.

```
/v1/top/{chain}/height
```

Formats: `json`, `data`, `text`.

```
$ curl "http://localhost:8180/v1/top/candidate/height?format=json"
0
```

`data` is the height in 4 bytes, little-endian.

### headers_top

The top of every branch of the header tree.

```
/v1/headers/top
```

Formats: `json`, `data`, `text`.

The strong tops, as for `top`, followed by the top of each weak branch,
a stored branch that is on neither chain. A weak branch top has no
`chain` field. `data` and `text` are each top in the same order, 116
bytes each.

## 4. Blocks

In the block paths below, `{block}` is `hash/{block hash}`,
`confirmed/{height}` or `candidate/{height}`. A hash finds any stored
block, and a height finds the block at that height on the named chain.
Near the candidate top, a block's transactions may not be downloaded or
its filter computed yet, and those are not found.

### block

A block.

```
/v1/block/{block}
```

Formats: `json`, `data`, `text`. Options: `witness`.

```
$ curl "http://localhost:8180/v1/block/confirmed/0?format=json"
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
$ curl "http://localhost:8180/v1/block/confirmed/0/header?format=json"
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
$ curl "http://localhost:8180/v1/block/confirmed/1/header/context?format=json"
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
        "bip30": true,
        "bip34": false,
        "bip66": false,
        "bip65": false,
        "bip68": false,
        "bip112": false,
        "bip113": false,
        "bip141": false,
        "bip143": false,
        "bip147": false,
        "bip42": true,
        "bip341": false,
        "bip342": false,
        "bip54_timewarp": false,
        "bip54_timespan": false,
        "bip54_sigops": false,
        "bip54_txsize": false,
        "bip54_coinbase": false
    }
}
```

`state` is present once the block's transactions are stored. `forks` shows
each soft fork as active or not at the block's height. BIP30, BIP42 and BIP90
are configured forks, active at every height when configured
([Activation](../architecture/system/chain#43-activation)). The mainnet
defaults configure BIP30 and BIP42, not BIP90. BIP54 has no mainnet
activation, and the other forks activate later in the chain.

### block_details

Sizes, value and reward of a block.

```
/v1/block/{block}/details
```

Formats: `json`.

```
$ curl "http://localhost:8180/v1/block/confirmed/1/details?format=json"
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
$ curl "http://localhost:8180/v1/block/confirmed/0/txs?format=json"
```

```json
[
    "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
]
```

`data` is the 32 byte hashes concatenated, in internal order.

### block_txs_details

The sizes, value, fee and cluster of each transaction of a block, in
order, the coinbase first.

```
/v1/block/{block}/txs/details
```

Formats: `json`, `data`, `text`.

```
$ curl "http://localhost:8180/v1/block/confirmed/1/txs/details?format=json"
```

```json
[
    {
        "segregated": false,
        "nominal": 134,
        "maximal": 134,
        "weight": 536,
        "virtual": 134,
        "value": 5000000000,
        "spend": 5000000000,
        "fee": 0,
        "cluster": 0
    }
]
```

| Field | Meaning |
| ----- | ------- |
| `segregated` | The transaction has witness data |
| `nominal`, `maximal` | Size without and with witness data |
| `weight`, `virtual` | Weight and virtual size |
| `value` | Total value of the inputs; for the coinbase, the block reward (subsidy and fees) |
| `spend` | Total value of the outputs; for the coinbase, the reward claimed |
| `fee` | `value` less `spend`; 0 for the coinbase |
| `cluster` | Label of the transaction's cluster, numbered in order of first appearance |

A cluster is a set of the block's transactions joined by spends among
them: a transaction that spends an output of another in the block is in
its cluster.

`data` is a 36 byte record for each transaction, in the same order, its
fields little-endian:

| Bytes | Field |
| ----- | ----- |
| 4 | `nominal` |
| 4 | `maximal` |
| 8 | `value` |
| 8 | `spend` |
| 8 | `fee` |
| 4 | `cluster` |

`text` is the same bytes in hex. The other `json` fields follow from the
sizes: `segregated` is `maximal` other than `nominal`, and `weight` and
`virtual` are computed from both.

### block_tx

The transaction at a position in a block.

```
/v1/block/{block}/tx/{position}
```

Formats: `json`, `data`, `text`. Options: `witness`.

```
$ curl "http://localhost:8180/v1/block/confirmed/0/tx/0?format=json"
```

The response is the transaction, as for [`tx`](#tx).

### block_tx_input_script

The script of an input of the transaction at a position in a block.

```
/v1/block/{block}/tx/{position}/input/{index}/script
```

Formats: `json`, `data`, `text`.

```
$ curl "http://localhost:8180/v1/block/confirmed/0/tx/0/input/0/script?format=json"
```

```json
"[ffff001d] [04] [5468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73]"
```

The response is the script, as for [`input_script`](#input_script).

### block_tx_output_script

The script of an output of the transaction at a position in a block.

```
/v1/block/{block}/tx/{position}/output/{index}/script
```

Formats: `json`, `data`, `text`.

```
$ curl "http://localhost:8180/v1/block/confirmed/0/tx/0/output/0/script?format=json"
```

```json
"[04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f] checksig"
```

The response is the script, as for [`output_script`](#output_script).

### block_filter

The BIP158 client filter of a block. Requires client filters
(`node.provide_filters`).

```
/v1/block/{block}/filter/{type}
```

Formats: `json`, `data`, `text`.

```
$ curl "http://localhost:8180/v1/block/confirmed/0/filter/0?format=json"
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
$ curl "http://localhost:8180/v1/block/confirmed/0/filter/0/hash?format=json"
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
$ curl "http://localhost:8180/v1/block/confirmed/0/filter/0/header?format=json"
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
transaction, which instead has `time`, when it was pooled, in Unix
seconds. The time of a confirmed transaction is that of its block
([`tx_header`](#tx_header)).

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

An input of a pruned transaction ([Pruned blocks](#25-pruned-blocks)) has
only its `point` and `sequence`, as JSON only:

```json
{
    "point": {
        "hash": "...",
        "index": 0
    },
    "sequence": 4294967295
}
```

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
([Configuration §5.13](../configuration/setups#13-disable-the-address-index)),
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

## 9. Pool

These answer from the transaction pool, so they require transaction
relay (`peer.enable_relay`): without it they return 501, and until the
pool opens, 503.

### fees

The fee rates of the confirmable transactions of the pool.

```
/v1/fees
```

Formats: `json`.

```json
{
    "count": 17054,
    "virtual": 9734212,
    "fee": 41208733,
    "histogram": [[12.5, 50211], [4.1, 50004], [1.0, 23119]]
}
```

| Field | Meaning |
| ----- | ------- |
| `count` | Confirmable transactions |
| `virtual` | Their total virtual size |
| `fee` | Their total fee, in satoshis |
| `histogram` | `[rate, virtual]` bins in descending fee rate (satoshis per virtual byte), each closed once it exceeds 50,000 virtual bytes |

### template

A summary of the template of the next block.

```
/v1/template/{height}
```

Formats: `json`.

```json
{
    "height": 950001,
    "count": 3412,
    "virtual": 997921,
    "weight": 3991684,
    "fees": 2310441,
    "clusters": 2987
}
```

| Field | Meaning |
| ----- | ------- |
| `height` | Height of the block |
| `count` | Transactions, without the coinbase |
| `virtual`, `weight` | Virtual size and weight of those transactions |
| `fees` | Their total fee |
| `clusters` | Their clusters ([`block_txs_details`](#block_txs_details)) |

Only the template of the next block, the confirmed top plus one, is
held. Any other height returns 404.

### template_txs

The transaction hashes of the template, in block order.

```
/v1/template/{height}/txs
```

Formats: `json`, `data`, `text`.

Position 0 is the coinbase, which the template does not contain, given
as the null hash (64 zeros), so that each position is that of the mined
block. `data` is the 32 byte hashes concatenated, in internal order.

### template_txs_details

The details of each transaction of the template, in block order, as for
[`block_txs_details`](#block_txs_details).

```
/v1/template/{height}/txs/details
```

Formats: `json`, `data`, `text`.

Position 0 models the coinbase from the space reserved for it
(`pool.coinbase_weight`): `maximal` is the size the reservation allows
with witness, and `nominal` that less the witness and its commitment
output (527 and 444 at the default 2000, so `weight` 1859 and `virtual`
465). `value` and `spend` are the block reward, the subsidy and the
template's fees. Its `cluster` is 0, and the clusters of the
transactions follow from 1.

### template_subscribe

A notification for each new template. Websocket only.

```
/v1/template/subscribe
```

Formats: `json`, `data`, `text`. Options: `stop`.

```
→ /v1/template/subscribe
←
← 950001
```

The reply is empty, and each new template then sends its height: a JSON
number, or four bytes little-endian as `data`, or their hex as `text`.
While subscribed, the node keeps building templates, replacing them on
each new block and as the pool changes (`pool.template_interval_seconds`).

### txs_unconfirmed

The transaction hashes of the confirmable transactions of the pool, in
pool order.

```
/v1/txs/unconfirmed
```

Formats: `json`, `data`, `text`.

`data` is the 32 byte hashes concatenated, in internal order.

### txs_unconfirmed_details

The details of each confirmable transaction of the pool, in the order of
[`txs_unconfirmed`](#txs_unconfirmed), as for
[`block_txs_details`](#block_txs_details), with the time each was pooled.

```
/v1/txs/unconfirmed/details
```

Formats: `json`, `data`, `text`.

There is no coinbase entry. Each object adds `time`, when the
transaction was pooled, in Unix seconds. Its `data` record adds `time`
as 4 more bytes, little-endian, 40 bytes in all.
