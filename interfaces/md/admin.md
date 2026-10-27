# Admin Console

The admin interface streams the node's log and events over websocket,
served on the `[admin]` binding. The embedded console is a page of this
interface, and can be replaced with a custom site (see [Configuration
§5.5](../configuration/index#55-admin-site)).

Its protocols share one port, and their secure forms share another:

| Port | Default | Protocols |
| ---- | ------- | --------- |
| Clear (`bind`) | 8080 | HTTP, WS |
| Secure (`safe`) | 8043 | HTTPS, WSS |

## 1. Paths

| Path | Method |
| ---- | ------ |
| `/v1/log/subscribe?filter={levels}` | [`log_subscribe`](#log_subscribe) |
| `/v1/event/subscribe?filter={events}` | [`event_subscribe`](#event_subscribe) |

Any other path is a page of the console, such as `/`.

## 2. Calling pattern

### 2.1 Enabling

The service starts only with both an address and a connection limit:

```ini
[admin]
bind = 127.0.0.1:8080
bind = [::1]:8080
connections = 10
```

Unlike the other services, it starts before the node is current.

### 2.2 Subscribing

A subscription is made over a websocket, which connects on the same port.

- Each text frame is one request path, such as
  `/v1/log/subscribe?filter=127`.
- Each request is answered by one frame, `{"previous": N}`, the filter it
  replaced.
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

The interface responds in JSON. A request must ask for it, with
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
| 406 | JSON was not requested |

Over a websocket, an invalid filter or format, or a method the credential
does not permit, closes the connection. An unknown path is ignored.

### 2.6 Credentials

A credential's method list names `log_subscribe` and `event_subscribe`
(see [Configuration §7.3](../configuration/index#73-authentication)).

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
| 10 | `tx_archived` | Count |
| 11 | `tx_validated` | Count |
| 12 | `tx_invalidated` | Count |
| 13 | `block_organized` | Height |
| 14 | `block_reorganized` | Height |
| 15 | `template_issued` | Count |
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

```json
{"event": 3, "value": 920001, "time": 1792987200123}
```

`time` is in milliseconds since the epoch.
