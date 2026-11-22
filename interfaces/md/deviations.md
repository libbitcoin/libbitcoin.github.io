# Standards Deviations

The client-server interfaces of `bs` are built on public standards:
HTTP/1.1, TLS 1.3, newline-delimited TCP, WebSocket, ZMTP 3.1 with
CurveZMQ, JSON and JSON-RPC.
This page lists where `bs` does not comply with them, and where the
implementations whose interfaces `bs` serves do not, with what `bs` does
about each.

## 1. bs

Where `bs` itself departs from a standard, whatever the client.

| Standard | Requirement | Departure |
| -------- | ----------- | --------- |
| JSON-RPC 2.0 (§6) | A batch, an array of requests, is answered with an array of responses. | `bs` refuses a batch over WS/S. Messages may be pipelined instead. |
| JSON-RPC 2.0 (§4) | An `id` may be any number, though one SHOULD NOT have a fraction. | `bs` refuses a fractional numeric `id`. |

HTTP/1.1, TLS 1.3, TCP/S framing, WebSocket, ZMTP, CurveZMQ and JSON
parsing and serialization have no known departures.

## 2. Implementations

Where an implementation whose interface `bs` serves departs from a
standard. Clients are written against the implementation, and depend on
its departures, so `bs` departs in the same way.

### 2.1 bitcoind

| Standard | Requirement | Departure |
| -------- | ----------- | --------- |
| HTTP/1.1 ([RFC 9110 §15.5.5](https://www.rfc-editor.org/rfc/rfc9110.txt)) | The status is of the HTTP request. 404 means the target resource is not found. | bitcoind sends a JSON-RPC version 1.0 error with an HTTP error status, though the HTTP request succeeded: 404 for an unknown method, though its target exists, 400 for an invalid request, and 500 for any other error. |
| JSON-RPC 1.0 (§1.3) | A notification, a request with a null `id`, has no response. | bitcoind sends a response, with the `result` or `error` of the method and a null `id`. |
| JSON-RPC 1.0 (§1.1) | A request has `method`, `params` and `id`. | bitcoind accepts a request without `id`, read as null, or without `params`, read as empty. |
| JSON-RPC 1.0 (§1.1) | `params` is an array. | bitcoind accepts named parameters, an object. |
| JSON-RPC 1.0 | A message is one request. Batches are defined only by version 2.0. | bitcoind accepts version 1.0 requests in a batch. |

### 2.2 btcd

| Standard | Requirement | Departure |
| -------- | ----------- | --------- |
| JSON-RPC 2.0 (§5.1) | -32603 means an internal error, and -32602 invalid parameters. | btcd answers a method its credential is restricted from with -32603 over HTTP, and with -32602 over WS/S and TCP/S. |

### 2.3 Electrum

The Sparrow interface extends Electrum, with the same departures.

| Standard | Requirement | Departure |
| -------- | ----------- | --------- |
| JSON-RPC 2.0 (§4.2) | `params` is an array or an object. | ElectrumX accepts a single value, read as an array of that value. |
| JSON-RPC 2.0 (§4.2) | `params` is an array or an object. | ElectrumX sends `blockchain.numblocks.subscribe` notifications with a single value. |

### 2.4 libzmq

libzmq is the reference implementation of ZeroMQ, and it departs from
the ZeroMQ specifications. bitcoind serves its ZeroMQ interface through
libzmq, without CurveZMQ. ZeroMQ clients also use libzmq, including for
CurveZMQ on the `bs` secure port, and could not read `bs` if it did not
depart in the same way.

| Standard | Requirement | Departure |
| -------- | ----------- | --------- |
| CurveZMQ ([26/CURVEZMQ](https://rfc.zeromq.org/spec/26/)) | `MESSAGE` is a command, framed with the command flag. | libzmq frames it as a message, without the command flag. |

### 2.5 Others

Esplora, the bitcoind REST interface and the native interface have no
known departures.

## 3. Clients

Where a client departs from a standard.

| Client | Standard | Requirement | Departure | bs |
| ------ | -------- | ----------- | --------- | -- |
| Fulcrum | HTTP/1.1 ([RFC 9112 §6.1](https://www.rfc-editor.org/rfc/rfc9112.txt)) | A client reads a chunked response body. | Fulcrum does not. bitcoind never sends one. | Rejected: every HTTP/1.1 response is chunked ([Client Compatibility](clients#fulcrum)) |
| bitcoind clients | JSON ([RFC 8259 §6](https://www.rfc-editor.org/rfc/rfc8259.txt)) | A number may be written with a fraction or exponent. | Some refuse an integer so written. bitcoind writes neither. | Accommodated: integers are written without either |
| bitcoind clients | JSON ([RFC 8259 §6](https://www.rfc-editor.org/rfc/rfc8259.txt)) | A number may be written with any number of fraction digits. | Some refuse an amount that is not an eight place decimal. bitcoind writes exactly eight places. | Accommodated: amounts are written in bitcoin with exactly eight places, such as `0.00010000` |
| bitcoind clients | JSON ([RFC 8259 §6](https://www.rfc-editor.org/rfc/rfc8259.txt)) | A number may be written with an exponent. | Some refuse a floating point value so written. bitcoind writes fixed notation. | Accommodated: other floating point values are written in fixed notation |

JSON has one number type. `1`, `1.0` and `1.00000000` are the same
number, and RFC 8259 leaves their form to the writer. bitcoind also
accepts an amount as a number or as a string, such as `"0.1"` or
`"1e-8"`: valid JSON, but two distinct JSON types applied to the same
parameter. `bs` accepts both, and requires either to be a whole number of
satoshis.
