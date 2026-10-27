# Sparrow

The Sparrow interface is the [Electrum](electrum) interface, with the
silent payment (BIP352) extensions defined by Frigate and used by the
Sparrow wallet. It is served on the `[sparrow]` binding, which has the
same settings as `[electrum]`, configured separately. Every Electrum
method, version and transport is served as documented on the
[Electrum](electrum) page. This page documents only the extensions.

Its protocols share one port, and their secure forms share another:

| Port | Default | Protocols |
| ---- | ------- | --------- |
| Clear (`bind`) | 8680 | TCP, HTTP, WS |
| Secure (`safe`) | 8643 | TCPS, HTTPS, WSS |

## 1. Methods

| Method | Purpose |
| ------ | ------- |
| [`server.features`](#serverfeatures) | Adds silent payment support |
| [`blockchain.silentpayments.subscribe`](#blockchainsilentpaymentssubscribe) | Scans for a wallet's silent payments, and notifies new ones |
| [`blockchain.silentpayments.unsubscribe`](#blockchainsilentpaymentsunsubscribe) | Ends a silent payment subscription |
| [`blockchain.block.stats`](#blockchainblockstats) | Not yet implemented |

The extensions are not versioned, and are available at every negotiated
Electrum version.

## 2. Configuration

Silent payments are indexed from a height set when the store is created,
`node.silent_start_height`, which requires witness data
(`node.require_witness`). Without the index, subscription returns
-32601. The silent payment address prefix is `wallet.silent_prefix`
(see [`[wallet]`](../configuration/reference#6-wallet)).

```ini
[node]
silent_start_height = 709632

[sparrow]
bind = 127.0.0.1:8680
connections = 10
```

A subscription finds the transactions that pay a wallet. The wallet then
follows each payment with the Electrum script hash methods, which require
the address index.

Notifications require TCP/S or WS/S. Over HTTP/S, a subscription is
dormant until the connection is upgraded to WS/S.

## 3. Methods

### server.features

The [Electrum `server.features`](electrum#serverfeatures) result, with
the supported silent payment versions:

```json
"silent_payments": [0]
```

### blockchain.silentpayments.subscribe

Scans for the silent payments of a wallet, from a start, and notifies
each new one.

**Parameters:** `scan_private_key`, `spend_public_key`, `start` (0),
`labels` (`[]`).

| Parameter | Value |
| --------- | ----- |
| `scan_private_key` | The 32 byte scan private key, as hex |
| `spend_public_key` | The 33 byte compressed spend public key, as hex |
| `start` | A height, a unix time (500,000,000 or more), or a range `"FROM-TO"` of either |
| `labels` | Label numbers to scan for. Label 0, for change, is always included |

A time start begins at the first block whose median time past is at or
after it. A range also limits later notifications to blocks within it.

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "blockchain.silentpayments.subscribe",
    "params": [
        "0f694e068028a717f8af6b9411f9a133dd3565258714cc226594b34db90c1f2c",
        "025cc9856d6f8375350e123978daac200c260cb5b5ae83106cab90484dcd8fcf36"
    ]
}
```

**Result:** the subscription.

```json
{
    "address": "sp1qqgste7k9hx0qftg6qmwlkqtwuy6cycyavzmzj85c6qdfhjdpdjtdgqjuexzk6murw56suy3e0rd2cgqvycxttddwsvgxe2usfpxumr70xc9pkqwv",
    "labels": [0],
    "start_height": 0
}
```

`start_height` is the start as given, a height or a time.

**Notifications:** `[subscription, progress, history]`, where
`subscription` is the result above. The scan's matches are sent in pages
of up to 1000, with `progress` the fraction sent, and the last page with
`1.0`. At least one notification follows each subscription. New matches
are then notified as they are found.

```json
{
    "jsonrpc": "2.0",
    "method": "blockchain.silentpayments.subscribe",
    "params": [
        {"address": "sp1qqgste7k9hx0qftg6qmwlkqtwuy6cycyavzmzj85c6qdfhjdpdjtdgqjuexzk6murw56suy3e0rd2cgqvycxttddwsvgxe2usfpxumr70xc9pkqwv", "labels": [0], "start_height": 0},
        1.0,
        [{"height": 0, "tx_hash": "<txid>", "tweak_key": "024ac253c216532e961988e2a8ce266a447c894c781e52ef6cee902361db960004"}]
    ]
}
```

Each history entry is a transaction paying the wallet: its height (`0`
if unconfirmed), its hash, and the tweak key with which the wallet
derives its outputs. Confirmed entries come first, by height.

Subscribing again with the same keys replaces the subscription, and scans
again from the lower of the two starts. Each connection may hold up to
`sparrow.maximum_subscriptions`, beyond which -101 is returned.

### blockchain.silentpayments.unsubscribe

Ends a subscription.

**Parameters:** `scan_private_key`, `spend_public_key`. **Result:** the
silent payment address, or `null` if it was not subscribed.

### blockchain.block.stats

Statistics of a block. Not yet implemented, and returns -32601.

## 4. Differences from Frigate

| Topic | `bs` | Frigate |
| ----- | ---- | ------- |
| Port | Its own binding, beside `[electrum]` | The Electrum port |
| Electrum versions | 1.0–1.7 | 1.4–1.6 |
| Time start | First block with median time past at or after it, returned as given | Last block with header time at or before it, returned as a height |
| Ranges | Heights or times; also limit later notifications | Heights only |
| Labels | Any number | Up to 10, nonzero |
| Unsubscribe, not subscribed | `null` | The address |
| Errors | 1 for invalid keys, -101 for too many subscriptions | -32602 |
