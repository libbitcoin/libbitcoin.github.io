# Service Settings

The client services (`[admin]`, `[native]`, `[bitcoind]`, `[electrum]`,
`[btcd]`, `[sparrow]` and `[esplora]`) share these settings.
`[zmq]` shares the listening settings, and secures its
connections using CurveZMQ rather than TLS ([Secure connections](#2-secure-connections)).

## 1. Listening

A service runs only when it has somewhere to listen and is allowed
connections:

| Setting | Purpose |
| ------- | ------- |
| `bind` | Address and port for clear connections. Multiple allowed. |
| `safe` | Address and port for secure connections. Multiple allowed. |
| `connections` | Maximum concurrent connections. `0` disables the service. |

An address of `0.0.0.0` (or `[::]` for IPv6) listens on all interfaces,
and `127.0.0.1` (or `[::1]` for IPv6) on the local machine only.

### Until current

By default, while the node syncs it accepts no inbound connections other
than to `[admin]` and `[native]`, the admin site and block explorer. P2P
peers (`[inbound]`) and the other client services are refused until the
chain is current: until the confirmed top block is within
`node.currency_window_minutes` (one day) of the present, or reaches
`node.maximum_height`. A service that is configured but not yet accepting
connections is therefore expected during sync.

To accept every inbound connection from the start, while the chain is
still syncing:

```ini
[node]
delay_inbound = false
```

A client connected before the chain is current sees the chain as of the
sync, not the network's top.

## 2. Secure connections

A `safe` address serves TLS, and requires a server certificate and its
private key. Without both, the service does not listen on its `safe`
addresses.

| Setting | Purpose |
| ------- | ------- |
| `cert_path` | Server certificate file (PEM). |
| `key_path` | Server private key file (PEM). |
| `key_pass` | Password of an encrypted private key, if any. |

The same certificate and key may be used by every service. For example,
`[admin]` over TLS only:

```ini
[admin]
safe = 127.0.0.1:8043
safe = [::1]:8043
connections = 10
cert_path = server.pem
key_path = server.key
```

ZMQ uses CurveZMQ instead of TLS. Its `safe` addresses require the
server's secret key (`zmq.key`, Z85 encoded), made by
`bx curve-new` ([Running a community server](public#2-running-a-community-server), step 3).

### Self-signed certificates

> **Note.** `bx` is not quite ready yet. The commands used here are not
> yet available in a `bx` release.

A service that is not public, such as `[admin]`, needs no certificate
authority. `bx tls-new` makes a P-256 private key from 256 bits of
entropy, from coin flips or dice ([Running a community server](public#2-running-a-community-server), step 3), and `bx tls-cert` makes
a self-signed certificate for it, naming the server by each host name
and address its clients use:

```
$ bx tls-new <entropy> > server.key
$ bx tls-cert --host localhost --ip 127.0.0.1 --ip ::1 < server.key > server.pem
```

The certificate is valid from now for 365 days, or `--days` days, and
`--name` sets its common name. Set the two files as `cert_path` and
`key_path`. A client trusts the server by holding `server.pem`, which
contains no secret, as a trusted certificate (for example, `curl
--cacert server.pem`). A browser shows a warning for a certificate it
does not trust until it is imported or accepted.

## 3. Authentication

Every client service except `[zmq]` has:

| Setting | Purpose |
| ------- | ------- |
| `credential` | A `user:password` for HTTP Basic authentication ([RFC 7617](https://www.rfc-editor.org/rfc/rfc7617.txt), [RFC 9110 §11](https://www.rfc-editor.org/rfc/rfc9110.txt)). Multiple allowed. When any is set, every request must present one of them. Basic authentication is not encrypted, so it is exposed unless the connection is secure. |

`[bitcoind]`, `[btcd]`, `[electrum]` and `[sparrow]` accept raw TCP,
HTTP and websocket clients on the same port. Raw TCP carries no HTTP
headers, so when a credential is set, a raw TCP connection is closed at
its first request, except by `[btcd]`, whose clients authenticate in-band
([BTCD RPC](setups#9-btcd-rpc)). To restrict raw TCP clients, require client
certificates (`cert_auth`) instead.

A credential may end with a list of the methods it permits,
`user:password:method,...`. A request for any other method is refused,
with HTTP 403 or by closing a websocket. JSON-RPC interfaces use their
RPC method names, such as `getblock` or `blockchain.headers.subscribe`.
REST interfaces use these names, one for each kind of request path:

| Section | REST method names |
| ------- | ----------------- |
| `[bitcoind]` | chain_information, block, block_txs, block_hash, block_headers, block_filter, block_filter_headers, block_part, block_spent_tx_outputs, deployment_info, get_utxos, mempool, mempool_information, tx |
| `[native]` | configuration, top, top_subscribe, block, block_header, block_header_context, block_details, block_tx, block_txs, block_filter, block_filter_hash, block_filter_header, block_subscribe, tx, tx_header, tx_details, tx_subscribe, inputs, input, input_script, input_witness, outputs, output, output_script, output_spender, output_spenders, output_subscribe, address, address_confirmed, address_unconfirmed, address_balance, address_subscribe |
| `[esplora]` | blocks, block, block_header, block_height, block_status, block_txid, block_txids, block_txs, tip_hash, tip_height, tx, tx_status, tx_merkle_proof, tx_merkleblock_proof, tx_outspend, tx_outspends, address, address_txs, address_txs_chain, address_txs_mempool, address_utxo, mempool, mempool_txids, mempool_recent, fee_estimates, broadcast, broadcast_package |
| `[admin]` | log_subscribe, event_subscribe |

### Client certificates

`cert_auth` names a directory of trusted certificate files (PEM). When it
is set, a TLS client must present a certificate trusted by one of them,
such as the client's own certificate. The client makes its own key and
self-signed certificate ([Secure connections](#2-secure-connections)), and gives only the certificate to the
server operator, who places it in the `cert_auth` directory:

```
$ bx tls-new <entropy> > client.key
$ bx tls-cert --name alice < client.key > client.pem
```

```ini
[admin]
safe = 127.0.0.1:8043
safe = [::1]:8043
cert_path = server.pem
key_path = server.key
cert_auth = clients
```

The client then presents both files, for example `curl --cert client.pem
--key client.key --cacert server.pem https://localhost:8043/`. A browser
imports a client certificate as PKCS#12, which `openssl pkcs12 -export`
makes from the two files. Removing a certificate from `cert_auth` revokes
that client when `bs` next starts.

### CurveZMQ client keys

Each `zmq.cert` line authorizes one client public key on the ZMQ
`safe` addresses. With no `cert` lines, any client may connect. The
client makes its own key pair with `bx curve-new` and `bx curve-public`
([Running a community server](public#2-running-a-community-server), step 3), and gives only the public key to the server operator:

```ini
[zmq]
safe = 127.0.0.1:8343
safe = [::1]:8343
key = <server secret key>
cert = <client public key>
```

## 4. HTTP services

`[admin]`, `[native]`, `[bitcoind]`, `[btcd]` and `[esplora]` are HTTP
services, and also have:

| Setting | Purpose |
| ------- | ------- |
| `host` | Allowed `Host` header values ([RFC 9110 §7.2](https://www.rfc-editor.org/rfc/rfc9110.txt)). Multiple allowed. |
| `origin` | An origin allowed to make cross-origin requests ([RFC 6454](https://www.rfc-editor.org/rfc/rfc6454.txt)), as a host and port without a scheme, matched against the request's `Origin` header. Multiple allowed. When any are set, the service's own host and port must be listed for the pages it serves to load. |
| `allow_opaque_origin` | Allow requests with an opaque origin ([RFC 6454 §7.3](https://www.rfc-editor.org/rfc/rfc6454.txt)), such as from a page opened as a local file. |

## 5. Limits

Each service has the limits that apply to its protocol. They apply to
each connection separately.

### Time

| Setting | Purpose |
| ------- | ------- |
| `inactivity_minutes` | A connection that has received nothing for this long is closed. This is also the HTTP keep-alive period. Sending does not count as activity. `0` disables it. |
| `expiration_minutes` | A connection is closed this long after it opened, whether or not it is active. `0` disables it. |
| `connect_timeout_seconds` | Time allowed for a new connection to complete its transport layer handshake (TLS, or ZMTP for ZMQ) before it is dropped. Application layer handshakes, such as Electrum version negotiation, are not covered. Each connection's limit is chosen at random between half and all of this value, so that many clients do not time out together. `0` uses `network.connect_timeout_seconds`, which defaults to 5 seconds. |

### Throughput

| Setting | Purpose |
| ------- | ------- |
| `rate_limit` | Maximum send rate of a connection, in bytes per second. The limit is continuous, not a cliff: each send is paced by its size, so a connection is slowed to the rate rather than cut off at a quota. Sends are delayed, not dropped, and throttling never disconnects a client. A client that requests faster than its responses drain is bounded by `maximum_backlog`. This protects against denial of service by bounding the rate at which one client can draw data from the server. `network.rate_limit` applies the same limit to every connection. When both are set the lower applies, and `0` leaves the other in effect (both `0` is unlimited). |
| `maximum_backlog` | Maximum bytes of responses waiting to be sent to a connection, such as to a client that reads slower than it asks. A connection that exceeds it is closed. ZMQ instead drops the notifications that do not fit. This protects against denial of service by bounding the memory a client that does not read can hold on the server. |

### Memory

| Setting | Purpose |
| ------- | ------- |
| `maximum_request` | Largest request accepted, in bytes, by every service: an HTTP body, a websocket message, an Electrum JSON-RPC message, a ZMQ frame, or a P2P message (`[inbound]`, `[outbound]` and `[manual]`). A larger request closes the connection. This protects against denial of service by bounding the memory a client can make the server allocate. |
| `minimum_buffer` | Buffer memory a connection keeps for reading requests, and for writing JSON responses. A buffer expanded beyond this by a large request or response is trimmed back to this size once it is idle. |
| `maximum_buffer` | Size of the buffer a JSON response is written through. A larger response is sent in pieces of this size, so it limits the memory per connection, not the response size. |
