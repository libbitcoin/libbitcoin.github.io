# Admin Console

The admin interface streams the node's log and events, and the mining
channels of the stratum services, over websocket, served on the
`[admin]` binding. It also serves the full
[native interface](native), so the console needs only this one address.
The embedded console is a page of this interface, and can be replaced
with a custom site (see [Configuration
§5.5](../configuration/setups#5-admin-site)).

The admin service is enabled by default, on the local machine only
(`127.0.0.1`, clear port). Its protocols share one port, and their secure
forms share another:

| Port | Default | Protocols |
| ---- | ------- | --------- |
| Clear (`bind`) | 8080 | HTTP, WS |
| Secure (`safe`) | 8043 | HTTPS, WSS |

## 1. Paths

| Path | Method |
| ---- | ------ |
| `/v1/log/subscribe?filter={levels}` | [`log_subscribe`](#log_subscribe) |
| `/v1/event/subscribe?filter={events}` | [`event_subscribe`](#event_subscribe) |
| `/v1/mining` | [`mining`](#mining) |
| `/v1/mining/subscribe` | [`mining_subscribe`](#mining_subscribe) |

Every path of the [native interface](native#1-paths) is also served,
with the same responses and websocket subscriptions. Any other path is a
page of the console, such as `/`.

Native requests made here are governed by the `[admin]` settings
(addresses, hosts, origins, TLS and credentials), not by `[native]`, and
are served whether or not `[native]` is enabled.

## 2. Calling pattern

### 2.1 Enabling

The service is enabled by default, on `127.0.0.1` with `connections = 10`.
Setting `bind` replaces the default address. To also listen on the IPv6
loopback:

```ini
[admin]
bind = 127.0.0.1
bind = [::1]
```

`connections = 0` disables it.

Unlike the other services, it starts before the node is current.

### 2.2 Subscribing

A subscription is made over a websocket, which connects on the same port.

- Each text frame is one request path, such as
  `/v1/log/subscribe?filter=127`.
- Each log or event request is answered by one frame,
  `{"previous": N}`, the filter it replaced.
- Matching log messages and events then follow, one per frame.
- A filter of 0, or no filter, ends the subscription.
- The log and event subscriptions of a connection are independent.

```python
import asyncio, websockets

async def main():
    async with websockets.connect("ws://localhost:8080/") as ws:
        await ws.send("/v1/event/subscribe?filter=8192")
        while True:
            print(await ws.recv())

asyncio.run(main())
```

```
{"previous":0}
{"event":13,"value":920001,"time":1792987200123}
{"event":13,"value":920002,"time":1792987201456}
```

The same request over HTTP/S returns the `previous` object, and the
subscription is dormant until the connection is upgraded to WS/S.

### 2.3 Filters

A filter is a decimal bit mask, where bit n selects log level n or event
n (§3). To select levels 0 to 6, add their masks:

| Bit | Level | Mask |
| --- | ----- | ---- |
| 0 | application | 1 |
| 1 | news | 2 |
| 2 | session | 4 |
| 3 | protocol | 8 |
| 4 | proxy | 16 |
| 5 | remote | 32 |
| 6 | fault | 64 |
| | Filter | `127` |

### 2.4 Formats

The admin methods respond in JSON. A request must ask for it, with
`format=json` or an `Accept: application/json` header, or it returns 406.
A websocket request is JSON by default.

```
$ curl "http://localhost:8080/v1/log/subscribe?filter=0&format=json"
{"previous":0}
```

A browser request (`text/html`) for any path returns the console.

### 2.5 HTTP status codes

Each response carries one of these statuses
([RFC 9110 §15](https://www.rfc-editor.org/rfc/rfc9110.txt)).

| Status | Meaning |
| ------ | ------- |
| 200 | Success |
| 400 | Invalid filter or format |
| 401 | Credentials are configured and none were given |
| 403 | The credential does not permit the method, or the origin is not allowed |
| 404 | A console file was not found |
| 405 | Any method other than `GET` |
| 406 | JSON was not requested, or `mining_subscribe` was not over a websocket |

Over a websocket, an invalid path is answered with 400 and the connection
is kept. An invalid filter or format, or a method the credential does not
permit, is answered with an error and closes the connection.

### 2.6 Credentials

A credential's method list names `log_subscribe`, `event_subscribe`,
`mining`, `mining_subscribe` and the native method names (see
[Configuration §7.3](../configuration/services#3-authentication)). A
credential with no method list permits every method. One with a list
permits only those named, so for the console it names `log_subscribe`,
`event_subscribe`, `mining_subscribe`, `configuration`, `top`,
`top_subscribe`, `block_header` and `fees`.

## 3. Methods

### log_subscribe

Streams the node's log messages, of the levels selected by the filter.

```
/v1/log/subscribe?filter={levels}
```

| Bit | Level | Mask |
| --- | ----- | ---- |
| 0 | application | 1 |
| 1 | news | 2 |
| 2 | session | 4 |
| 3 | protocol | 8 |
| 4 | proxy | 16 |
| 5 | remote | 32 |
| 6 | fault | 64 |
| 7 | quitting | 128 |
| 8 | objects | 256 |
| 9 | verbose | 512 |

```json
{"level": 1, "time": 1792987200000, "message": "Node is current.\n"}
```

`time` is in milliseconds since the epoch, to the second. A level produces
messages only if it was built in. The `[log]` settings do not apply here.

### event_subscribe

Streams the node's events, of the types selected by the filter.

```
/v1/event/subscribe?filter={events}
```

| Bit | Event | Value |
| --- | ----- | ----- |
| 0 | `header_archived` | Height |
| 1 | `header_organized` | Height |
| 2 | `header_reorganized` | Height |
| 3 | `block_archived` | Height |
| 4 | `block_buffered` | Height |
| 5 | `block_validated` | Height |
| 6 | `block_confirmed` | Height |
| 7 | `block_unconfirmable` | Height |
| 8 | `validate_bypassed` | Height |
| 9 | `confirm_bypassed` | Height |
| 10 | `tx_archived` | Fee rate, satoshis per virtual kilobyte |
| 11 | `tx_validated` | Count |
| 12 | `tx_invalidated` | Count |
| 13 | `block_organized` | Height |
| 14 | `block_reorganized` | Height |
| 15 | `template_issued` | Transaction count |
| 16 | `snapshot_secs` | Seconds |
| 17 | `prune_msecs` | Milliseconds |
| 18 | `reload_msecs` | Milliseconds |
| 19 | `block_usecs` | Microseconds |
| 20 | `ancestry_msecs` | Milliseconds |
| 21 | `filter_msecs` | Milliseconds |
| 22 | `filterhashes_msecs` | Milliseconds |
| 23 | `filterchecks_msecs` | Milliseconds |
| 24 | `ecdsa_secs` | Seconds |
| 25 | `schnorr_secs` | Seconds |
| 26 | `silent_secs` | Seconds |
| 27 | `validate_usecs` | Microseconds |
| 28 | `top_usecs` | Microseconds |
| 29 | `pool_rows` | Row count |
| 30 | `pool_submit_usecs` | Microseconds |
| 31 | `pool_coverage_usecs` | Microseconds |
| 32 | `pool_connect_usecs` | Microseconds |
| 33 | `pool_admit_usecs` | Microseconds |
| 34 | `pool_compact_usecs` | Microseconds |
| 35 | `pool_block_in_usecs` | Microseconds |
| 36 | `pool_block_out_usecs` | Microseconds |
| 37 | `pool_context_usecs` | Microseconds |
| 38 | `pool_template_usecs` | Microseconds |
| 39 | `pool_project_usecs` | Microseconds |
| 40 | `pool_confirmable_usecs` | Microseconds |
| 41 | `tx_dropped` | Transaction count |
| 42 | `tx_refused` | Transaction count |
| 43 | `tx_unserved` | Transaction count |

`validate_usecs` is fired only for a block validated alone, and
`top_usecs`, from a candidate header to its block organized as the
confirmed top, only for a single block above a current top. `pool_rows`,
`pool_block_in_usecs` and `pool_block_out_usecs` are fired at each
organized or reorganized block only while the pool is indexing (relay
enabled). `pool_rows` counts every row of the pool table, including
transactions that cannot confirm, so it exceeds the `size` of
[`getmempoolinfo`](bitcoind-rpc#getmempoolinfo). `tx_dropped` is the size
of a transaction set for which a peer was dropped, `tx_refused` the size of
a set not admitted in full for which the peer was kept, and `tx_unserved`
the count of requested transactions that a peer did not send.

```json
{"event": 3, "value": 920001, "time": 1792987200123}
```

`time` is in milliseconds since the epoch.

### mining

The mining channels of the stratum services, and the blocks they found.

```
/v1/mining
```

```json
{
    "channels": [
        {
            "id": "00000000000000a3:0",
            "service": "stratum_v1",
            "transport": "tcp",
            "address": "192.168.1.20:51234",
            "client": "cgminer/4.11.1",
            "workers": ["bc1q....bitaxe"],
            "connected": 1792987200123,
            "difficulty": 4096,
            "hashrate": 1210000000000,
            "accepted": 1712,
            "rejected": 3,
            "rejections": {"low_difficulty": 1, "job_not_found": 2},
            "last_share": 1792990801456,
            "shares": [
                {"time": 1792990801456, "height": 920001, "difficulty": 4096, "result": "accepted"}
            ],
            "history": [[1792990740000, 1190000000000], [1792990800000, 1230000000000]]
        }
    ],
    "blocks": [
        {"hash": "00000000000000000001...", "height": 919990, "time": 1792987900000, "channel": "00000000000000a3:0"}
    ]
}
```

`channels` has one entry per Stratum v1 connection and per Stratum v2
channel. `blocks` has the last 10 blocks found through stratum and
accepted by the node, newest first, each with the `id` of its channel.

| Field | Meaning |
| ----- | ------- |
| `id` | The connection, as 16 hex characters, and the channel (0 for Stratum v1) |
| `service` | `stratum_v1` or `stratum_v2` |
| `transport` | `tcp`, `tls`, `ws`, `wss` or `noise` |
| `address` | The miner's address and port |
| `client` | The user agent of `mining.subscribe` (v1), or the vendor and firmware of `SetupConnection` (v2) |
| `workers` | The authorized worker names (v1), or the channel's user identity (v2) |
| `connected` | When the channel opened |
| `difficulty` | The current share difficulty |
| `hashrate` | Hashes per second, the mean of `history` |
| `accepted`, `rejected` | Shares accepted and rejected |
| `rejections` | Rejected shares, by result |
| `last_share` | When the last share was received, or `null` |
| `shares` | The last 20 shares, newest first |
| `history` | The rate of each completed minute, to 30, as `[minute, hashes per second]` |

A share's `result` is `accepted`, `submitted` (accepted, and it mined a
block), `duplicate`, `low_difficulty`, `invalid`, `stale` (a job
no longer current, v2 only) or `job_not_found`. A minute's rate is the
work of its accepted shares, difficulty times 2<sup>32</sup> hashes,
over 60 seconds, so a channel shows 0 for its first minute.

Times are in milliseconds since the epoch. The registry is held in
memory: a channel is removed when it or its connection closes, and the
channels and blocks start empty when the node starts.

### mining_subscribe

Responds with [`mining`](#mining), and pushes it again every 5 seconds,
or within a second of a mining channel opening or closing.

```
/v1/mining/subscribe
```

It is served over a websocket only. Over HTTP/S it returns 406.
