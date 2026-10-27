# BTCD

The BTCD interface is the [bitcoind JSON-RPC](bitcoind-rpc) interface,
with the methods and websocket notifications of btcd. It is served on the
`[btcd]` binding, which has the settings of `[bitcoind]`, configured
separately. Every bitcoind JSON-RPC method is served as documented on the
[Bitcoind JSON-RPC](bitcoind-rpc) page, following bitcoind where the two
differ. This page documents only the btcd methods.

Its protocols share one port, and their secure forms share another:

| Port | Default | Protocols |
| ---- | ------- | --------- |
| Clear (`bind`) | 8480 | HTTP, TCP, WS |
| Secure (`safe`) | 8443 | HTTPS, TCPS, WSS |

btcd serves JSON-RPC over HTTP/S, and its notifications over WS/S. TCP/S
is a `bs` extension, which also carries notifications.

## 1. Methods

| Category | Methods |
| -------- | ------- |
| [Connection](#3-connection) | `authenticate`, `session`, `version`, `node` |
| [Chain](#4-chain) | `getbestblock`, `getheaders`, `getcfilter`, `getcfilterheader`, `getcurrentnet`, `getinfo`, `estimatefee`, `getblockchaininfo`, `getdifficulty`, `getnettotals` |
| [Search](#5-search) | `searchrawtransactions` |
| [Notifications](#6-notifications) | `notifyblocks`, `notifynewtransactions`, `loadtxfilter`, `notifyreceived`, `notifyspent`, their `stop` methods, `rescanblocks`, `rescan` |

Methods that `bs` does not serve are listed in §7. All methods are served
over every transport. btcd serves the notification methods over WS/S
only.

## 2. Configuration

```ini
[btcd]
bind = 127.0.0.1:8480
connections = 10
credential = user:pass
```

`[btcd]` adds two settings to those of `[bitcoind]`:

| Setting | Default | Purpose |
| ------- | ------- | ------- |
| `btcd.maximum_filters` | 1,000,000 | Addresses and outputs one connection may watch, by all notification methods together |
| `btcd.maximum_history` | 1,000,000 | History read for one address |

Address search and address watches require the address index, and return
-1 without it. Addresses are encoded with the
[`[wallet]`](../configuration/reference#6-wallet) prefixes.

A connection, with its subscriptions and watches, lasts up to
`btcd.expiration_minutes` (default 60). Set it to 0 for a subscriber that
stays connected.

## 3. Connection

### authenticate

Authenticates a WS/S or TCP/S connection in-band, as btcd clients do.
**Parameters:** `username`, `passphrase`. **Result:** `null`.

A WS/S connection may instead be authorized by the credentials of its
upgrade request. Until a connection is authorized, every other method
returns error 117 (`unauthorized`), and the connection stays open. A
wrong credential returns the same error, and closes the connection. With
no credential configured, the connection is authorized from the start,
and `authenticate` returns the error. Over HTTP/S, credentials are sent
with each request.

### session

The connection's identifier. **Parameters:** none. **Result:**
`{"id": n}`. btcd names the field `sessionid`.

### version

The btcd JSON-RPC version. **Parameters:** none.

```json
{"btcdjsonrpcapi": {"versionstring": "1.3.0", "major": 1, "minor": 3, "patch": 0, "prerelease": "", "buildmetadata": ""}}
```

### node

Connects to or disconnects a peer. **Parameters:** `subcmd`, `target`,
`connectsubcmd`.

| `subcmd` | Effect |
| -------- | ------ |
| `connect` | Connects to `target`, once with `temp`, or keeping the connection with `perm` |
| `disconnect` | Disconnects the peer, which may reconnect |
| `remove` | Disconnects the peer, and stops its reconnection |

`target` is a peer address, or a connection number.

## 4. Chain

### getbestblock

The top confirmed block. **Parameters:** none.

```json
{"hash": "000000008d9dc510f23c2657fc4f67bea30078cc05a90eb89e84cc475c080805", "height": 9}
```

### getheaders

Up to 2000 headers following a block locator, as hex. **Parameters:**
`blocklocators`, `hashstop` (`""`, none).

### getcfilter

A block's client filter, as hex. **Parameters:** `hash`, `filtertype`
(0, basic). Requires client filters, and returns -5 without them.

### getcfilterheader

A block's client filter header. **Parameters:** `hash`, `filtertype`
(0). Requires client filters.

### getcurrentnet

The network's magic number. **Parameters:** none.

```json
3652501241
```

### getinfo

A summary of the node. **Parameters:** none. **Result:** `version`,
`protocolversion`, `blocks`, `timeoffset`, `connections`, `proxy`,
`difficulty`, `testnet`, `relayfee` and `errors`. `version` is 260200,
reporting btcd 0.26.2 compatibility. `testnet` is set for every chain
other than mainnet.

### estimatefee

The fee rate for a transaction to confirm within a number of blocks, in
BTC per 1000 virtual bytes. **Parameters:** `numblocks` (1 to 1008).
Returns -1 without an estimate. Requires `node.fee_estimate_horizon`.

### getblockchaininfo

As the [bitcoind method](bitcoind-rpc#getblockchaininfo), including
`bip9_softforks`, which btcd clients such as lnd read.

### getdifficulty

As the [bitcoind method](bitcoind-rpc#getdifficulty).

### getnettotals

The bytes sent and received, as btcd reports them, without bitcoind's
`uploadtarget`. **Parameters:** none.

## 5. Search

### searchrawtransactions

The confirmed transactions of an address. **Parameters:**

| Parameter | Default | Value |
| --------- | ------- | ----- |
| `address` | | An address, or a public key as hex for its P2PK and P2PKH scripts |
| `verbose` | 1 | 0 for hex, 1 for objects |
| `skip` | 0 | Transactions to skip |
| `count` | 100 | Transactions to return |
| `vinextra` | 0 | 1 to add each input's previous output |
| `reverse` | `false` | `true` for newest first |
| `filteraddrs` | `[]` | Addresses to which inputs and outputs are limited |

Unconfirmed transactions are not included. An address with no
transactions, or a `skip` past them, returns -5.

## 6. Notifications

Notifications are sent over WS/S and TCP/S, as JSON-RPC requests with
no `id`. Each subscription belongs to its connection, and ends with it.
Notifications are sent for confirmed blocks only, except
`txaccepted`.

### notifyblocks

Notifies each block added to or removed from the confirmed chain.
**Parameters:** none. **Result:** `null`.

| Notification | Parameters |
| ------------ | ---------- |
| `blockconnected` | `[hash, height, time]` |
| `filteredblockconnected` | `[height, header, transactions]`, the header as hex and the transactions matching `loadtxfilter` |
| `blockdisconnected` | `[hash, height, time]` |
| `filteredblockdisconnected` | `[height, header]` |

### stopnotifyblocks

Ends `notifyblocks`. **Parameters:** none.

### notifynewtransactions

Notifies each transaction accepted to the memory pool. **Parameters:**
`verbose` (`false`).

| Notification | Parameters |
| ------------ | ---------- |
| `txaccepted` | `[txid, amount]`, the total of its outputs in BTC |
| `txacceptedverbose` | `[transaction]`, as an object |

### stopnotifynewtransactions

Ends `notifynewtransactions`. **Parameters:** none.

### loadtxfilter

Sets the addresses and outputs whose transactions
`filteredblockconnected` and `rescanblocks` report. **Parameters:**
`reload`, `addresses`, `outpoints`, where each outpoint is
`{"hash", "index"}`. With `reload`, the filter is replaced; otherwise it
is added to. Only blocks confirmed later match. Outputs do not require
the address index.

### rescanblocks

The transactions matching `loadtxfilter` in blocks. **Parameters:**
`blockhashes`. **Result:** `[{"hash", "transactions"}]`, for each block
with a match, as hex. Requires the address index.

### notifyreceived

Notifies each confirmed transaction that pays an address, and then the
spending of that payment. **Parameters:** `addresses`.

| Notification | Parameters |
| ------------ | ---------- |
| `recvtx` | `[transaction, block]`, the transaction as hex and `{"height", "hash", "index", "time"}` |

btcd deprecates this method in favor of `loadtxfilter`.

### stopnotifyreceived

Ends `notifyreceived` for addresses. **Parameters:** `addresses`.

### notifyspent

Notifies the confirmed spending of each output, once. **Parameters:**
`outpoints`.

| Notification | Parameters |
| ------------ | ---------- |
| `redeemingtx` | `[transaction, block]`, as `recvtx` |

btcd deprecates this method in favor of `loadtxfilter`.

### stopnotifyspent

Ends `notifyspent` for outputs. **Parameters:** `outpoints`.

### rescan

Searches past blocks for the transactions of addresses and outputs.
**Parameters:** `beginblock`, `addresses`, `outpoints`, `endblock`.

In btcd, this searches the blocks from `beginblock` to `endblock`,
notifying each transaction paying an address (`recvtx`) or spending an
output (`redeemingtx`), then `rescanfinished`. `bs` does not implement
the search: with addresses or outputs, it returns -1. With neither,
there is nothing to search, so it returns `null` and notifies
`rescanfinished` with `[hash, height, time]` of the top block.

btcd deprecates this method in favor of `loadtxfilter` with
`rescanblocks`, which `bs` serves.

## 7. Methods not served

| Methods | Reason | Error |
| ------- | ------ | ----- |
| `generate`, `getgenerate`, `setgenerate`, `gethashespersec` | Mining awaits the transaction graph of the version 5 pool | -32601 |
| `debuglevel` | Log levels are set by configuration | -32601 |

## 8. Differences from btcd

| Topic | `bs` | btcd |
| ----- | ---- | ---- |
| Methods shared with bitcoind | As bitcoind | As btcd |
| Notification methods | Every transport | WS/S only |
| Unauthenticated request | Error 117, connection kept | Connection closed |
| `session` result | `{"id"}` | `{"sessionid"}` |
| `notifyreceived`, `notifyspent`, `searchrawtransactions` | Confirmed transactions only | Also memory pool transactions |
| `rescan` | Not implemented, except with no addresses or outputs, which finishes at once | Searches past blocks, notifying each match |
| Watches per connection | `btcd.maximum_filters` | No limit |
| Invalid argument | Error -8 | Error -5 or -22 |
| Mistyped parameter | Connection closed | Error |
