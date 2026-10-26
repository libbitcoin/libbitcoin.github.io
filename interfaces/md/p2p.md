# Bitcoin P2P

The Bitcoin P2P interface is Bitcoin's wire protocol, on which `bs` both
syncs the chain and serves it. It is configured by the `[network]`,
`[peer]`, `[inbound]`, `[outbound]` and `[manual]` sections, and listens
on port 8333 (see [Configuration §5.18](../configuration/index#518-peer-services-and-policy)).

`bs` supports every feature of the Bitcoin P2P protocol that is deployed
and not deprecated:

| BIP | Feature |
| --- | ------- |
| [BIP14](https://github.com/bitcoin/bips/blob/master/bip-0014.mediawiki) | User agent |
| [BIP31](https://github.com/bitcoin/bips/blob/master/bip-0031.mediawiki) | `pong` |
| [BIP35](https://github.com/bitcoin/bips/blob/master/bip-0035.mediawiki) | `mempool` |
| [BIP111](https://github.com/bitcoin/bips/blob/master/bip-0111.mediawiki) | `node_bloom` (not advertised) |
| [BIP130](https://github.com/bitcoin/bips/blob/master/bip-0130.mediawiki) | `sendheaders` |
| [BIP133](https://github.com/bitcoin/bips/blob/master/bip-0133.mediawiki) | `feefilter` |
| [BIP144](https://github.com/bitcoin/bips/blob/master/bip-0144.mediawiki) | Witness serialization and inventory |
| [BIP152](https://github.com/bitcoin/bips/blob/master/bip-0152.mediawiki) | Compact blocks |
| [BIP155](https://github.com/bitcoin/bips/blob/master/bip-0155.mediawiki) | `addrv2` |
| [BIP157](https://github.com/bitcoin/bips/blob/master/bip-0157.mediawiki) | Client filter messages |
| [BIP158](https://github.com/bitcoin/bips/blob/master/bip-0158.mediawiki) | Client filters |
| [BIP159](https://github.com/bitcoin/bips/blob/master/bip-0159.mediawiki) | `node_network_limited` |
| [BIP324](https://github.com/bitcoin/bips/blob/master/bip-0324.mediawiki) | Encrypted transport |
| [BIP339](https://github.com/bitcoin/bips/blob/master/bip-0339.mediawiki) | `wtxidrelay` |

Of the deprecated, BIP61 (`reject`) is supported, and BIP37 (bloom
filters) is not.

## 1. Messages

The protocol version is the minimum negotiated version at which `bs` uses
the message, and the setting is the one that enables it.

| Message | Version | Setting |
| ------- | ------- | ------- |
| [`version`](#version), [`verack`](#verack), [`ping`](#ping) | 106 | |
| [`getblocks`](#getblocks), [`inv`](#inv), [`getdata`](#getdata), [`block`](#block) | 106 | `node.provide_blocks` |
| [`tx`](#tx) | 106 | `peer.enable_relay` |
| [`getaddr`](#getaddr) | 209 | `peer.enable_address` |
| [`alert`](#alert) | 311 | `peer.enable_alert` |
| [`addr`](#addr) | 31402 | `peer.enable_address` |
| [`getheaders`](#getheaders), [`headers`](#headers) | 31800 | |
| [`pong`](#pong) | 60001 | |
| [`mempool`](#mempool) | 60002 | `peer.enable_memory_pool` |
| [`notfound`](#notfound) | 70001 | `peer.enable_not_found` |
| [`reject`](#reject) | 70002 | `peer.enable_reject` |
| [`sendheaders`](#sendheaders) | 70012 | |
| [`feefilter`](#feefilter) | 70013 | `peer.enable_relay` |
| [`sendcmpct`](#sendcmpct), [`cmpctblock`](#cmpctblock), [`getblocktxn`](#getblocktxn), [`blocktxn`](#blocktxn) | 70014 | `peer.enable_compact` |
| [`getcfilters`](#getcfilters), [`getcfheaders`](#getcfheaders), [`getcfcheckpt`](#getcfcheckpt) | 70015 | `node.provide_filters` |
| [`addrv2`](#addrv2), [`sendaddrv2`](#sendaddrv2) | 70016 | `peer.enable_address_v2` |
| [`wtxidrelay`](#wtxidrelay) | 70016 | `peer.enable_witness_tx` |

`filterload`, `filteradd`, `filterclear` and `merkleblock` (BIP37) are not
supported (§9).

## 2. Connections

### 2.1 Sessions

| Session | Section | Purpose |
| ------- | ------- | ------- |
| Inbound | `[inbound]` | Peers that connect to `bs` |
| Outbound | `[outbound]` | Peers that `bs` connects to from its address pool |
| Manual | `[manual]` | Peers that `bs` always connects to |
| Seed | `[outbound]` | Seed peers, to fill the address pool |

Outbound and manual peers must advertise full blocks and witness data
(`node_network` and `node_witness`), as `node.require_blocks` and
`node.require_witness` are set by default. Once the node is current,
outbound connections are reduced to `outbound.current_connections`
(default 10). Inbound connections are refused until the node is current
while `node.delay_inbound` is set (the default).

### 2.2 Service bits

The services `bs` advertises in its version message and its address:

| Bit | Service | Setting |
| --- | ------- | ------- |
| 0 | `node_network` | `node.provide_blocks` |
| 3 | `node_witness` | `node.provide_witness` |
| 6 | `node_client_filters` | `node.provide_filters` |
| 10 | `node_network_limited` | `node.limited_blocks`, in place of `node_network` |
| 11 | `node_encrypted_transport` | `node.provide_privacy` |

`node_utxo` (bit 1) and `node_bloom` (bit 2) are never advertised. A peer
advertising any of `peer.invalid_services` is refused.

### 2.3 Encrypted transport

With `node.provide_privacy`, connections are encrypted (BIP324) where
both sides support it, on the same port:

- An inbound peer is served encrypted or clear, as it begins.
- An outbound connection is encrypted when the peer's address advertises
  `node_encrypted_transport`.
- Seed and manual connections are clear.

### 2.4 Proxies and anonymity networks

Outbound, seed and manual connections can be made through a SOCKS5 proxy,
such as Tor, set by `outbound.socks` and `manual.socks`, with optional
`username` and `password`. Onion and I2P addresses are connected only
through a proxy, and are gossiped when `network.gossip_tor` and
`network.gossip_i2p` are set.

Inbound I2P connections are accepted through a SAM bridge
(`inbound.sam`), with the destination key at `inbound.key_path`. An onion
service is set up in Tor, and advertised with `inbound.self`.

### 2.5 Timers

| Setting | Default | Effect |
| ------- | ------- | ------ |
| `peer.handshake_timeout_seconds` | 15 | Time allowed for the version handshake |
| `peer.channel_heartbeat_minutes` | 10 | Interval between pings |
| `peer.maximum_skew_minutes` | 120 | Clock difference allowed in the version message |
| `inactivity_minutes` | 10 | A connection that sends nothing for this long is dropped |
| `expiration_minutes` | 60 | A connection is dropped at this age, and replaced |

The last two are set in each of `[inbound]`, `[outbound]` and `[manual]`,
and 0 disables them.

### 2.6 Misbehavior

A peer that violates the protocol is disconnected. This includes an
unknown or malformed message, a message below the negotiated version, and
an unrequested or invalid header, block, or transaction. There is no
banning. `network.blacklist` and `network.whitelist` set which addresses
connect at all.

Limits that protect against denial of service apply to every service,
including P2P (see [Configuration §7.5](../configuration/index#75-limits)).

## 3. Handshake

### version

Sent on connection, with:

- the protocol version, `peer.protocol_maximum` (default 70016);
- the advertised services (§2.2);
- the user agent, `peer.user_agent`;
- the height of the top confirmed block;
- the relay flag, set if `peer.enable_relay` is set and the node is
  current.

A peer is refused if its version is below `peer.protocol_minimum`
(default 31800), if it lacks the required services, or if its clock
differs by more than `peer.maximum_skew_minutes`. The negotiated version
is the lower of the two.

### verack

Sent on receipt of the peer's `version`, completing the handshake.

### sendaddrv2

Sent after `version` and before `verack` when `peer.enable_address_v2`
is set and Tor or I2P addresses are gossiped. A peer that sends it
receives addresses as `addrv2`.

### wtxidrelay

Sent after `version` and before `verack` when `peer.enable_witness_tx`
is set. When both peers send it, transactions are announced and requested
by witness hash.

## 4. Liveness

### ping

Sent once the handshake completes, and then every
`peer.channel_heartbeat_minutes`. A peer that has not answered by the next
ping is disconnected.

### pong

Answers a `ping`, with its nonce. A `pong` with the wrong nonce
disconnects the peer.

## 5. Addresses

### getaddr

Sent once to each outbound and manual peer. Answered once per
connection, with a random sample of the address pool, up to 1000.

### addr

Addresses, up to 1000. Those received from outbound and manual peers are
added to the address pool, up to `network.host_pool_capacity`. Those from
inbound peers are ignored. On connection, `bs` sends its own addresses,
`inbound.self`.

### addrv2

As `addr`, for every network type (BIP155). Sent to peers that sent
`sendaddrv2`.

## 6. Headers and blocks

### getheaders

Requests up to 2000 headers following a locator. `bs` syncs headers
first from each outbound peer, and answers with the headers of its
confirmed chain. While not current, it answers with no headers.

### headers

Up to 2000 headers. A peer that sends invalid or unconnected headers is
disconnected.

### sendheaders

Asks for new blocks to be announced by `headers` in place of `inv`
(BIP130). `bs` sends it once its first header sync completes.

### getblocks

Requests the hashes of up to 500 blocks following a locator, answered by
`inv`. While not current, the `inv` is empty.

### inv

Announces blocks and transactions by hash, up to 50,000. `bs` announces
each block once it is confirmed, while current, and each transaction
accepted to its memory pool.

### getdata

Requests blocks or transactions by hash, up to 50,000. `bs` downloads
blocks in parallel across peers, and drops peers that are much slower than
the rest. It serves blocks and transactions from its store, confirmed or
not.

### block

A block. A block that fails validation disconnects the peer that sent it.

### notfound

Answers a `getdata` for an object `bs` does not have. Without
`peer.enable_not_found`, the peer is disconnected instead.

### sendcmpct

Enables compact blocks (BIP152), version 2. `bs` sends it in low
bandwidth mode after the handshake, and in high bandwidth mode once
current.

### cmpctblock

A compact block. `bs` rebuilds received compact blocks from its memory
pool, and downloads the full block when more than
`node.compact_missing_percent` (default 50) of it is missing. It sends a
compact block for each confirmed block to peers in high bandwidth mode.

### getblocktxn

Requests the transactions missing from a compact block.

### blocktxn

The transactions requested by `getblocktxn`.

## 7. Transactions

### tx

A transaction. `bs` requests announced transactions while current, and
adds them to its memory pool. A peer that sends a transaction that was not
requested is disconnected.

### feefilter

The minimum fee rate of transactions to announce (BIP133). `bs` sends
`node.minimum_fee_rate` while current, and the maximum otherwise. It does
not announce transactions below a peer's rate.

### mempool

Requests the hashes of the memory pool (BIP35), answered by `inv`.
Ignored unless `peer.enable_memory_pool` is set.

## 8. Client filters

These require `node.provide_filters` (BIP157), and are ignored without it.
Only basic filters are served.

### getcfilters

Requests the filters of up to 1000 blocks, answered by a `cfilter` for
each.

### getcfheaders

Requests the filter headers of up to 2000 blocks, answered by
`cfheaders`.

### getcfcheckpt

Requests the filter header of every 1000th block up to a stop block,
answered by `cfcheckpt`.

### cfilter

A block's filter, answering `getcfilters`.

### cfheaders

Filter headers, answering `getcfheaders`.

### cfcheckpt

Filter header checkpoints, answering `getcfcheckpt`.

## 9. Other messages

### reject

Sent when a peer is refused during the handshake (BIP61), and logged when
received. Off by default.

### alert

Logged when received. Off by default.

### filterload

Not supported (BIP37). `bs` ignores bloom filter messages, does not send
filtered blocks, and does not advertise `node_bloom`.

### filteradd

Not supported, as `filterload`.

### filterclear

Not supported, as `filterload`.

### merkleblock

Not supported, as `filterload`.
