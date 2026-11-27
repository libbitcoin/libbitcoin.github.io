# Stratum v2

Stratum v2 is the successor to [Stratum v1](stratum-v1): a binary
mining protocol, with channels, compact jobs and an encrypted,
authenticated transport (Noise). `bs` serves its Mining protocol from
the `[stratum_v2]` service as a solo pool: each job is a template of the
next block from the `bs` transaction pool, its coinbase pays the address
in the channel's user identity (or the configured one), and a share that
meets the network target is submitted as a block. The Template
Distribution and Job Declaration protocols are not served.

Each connection is detected from its first bytes, so its protocols share
one port, and their secure forms share another:

| Port | Default | Protocols |
| ---- | ------- | --------- |
| Clear (`bind`) | 8980 | TCP, WS |
| Secure (`safe`) | 8943 | Noise TCP, WSS, Noise WS |

Over TCP, frames are streamed; over WS, each binary message carries one
frame. On `safe`, a TLS ClientHello is served as WSS and anything else
as Noise, after which the connection is TCP or WS as on `bind`. Miners
and proxies that implement the specification, such as the Stratum V2
reference translator, connect with Noise over TCP on `safe`.

## 1. Setup

The service is disabled by default. Bind an address, allow connections,
and optionally set the payout address. Noise requires a static secret
key and a certificate for it, both made with [`bx`](#noise-keys):

```ini
[stratum_v2]
bind = 0.0.0.0:8980
safe = 0.0.0.0:8943
connections = 10
payout_address = bc1q...
noise_secret = <server secret>
noise_certificate = <certificate>
```

Give miners the host, port 8943, and the authority public key, which
they pin to authenticate the server. Without `payout_address`, the user
identity of each channel is the payout: the miner opens the channel as
`<address>` or `<address>.<worker>`. With `payout_address`, every block
pays that address, and user identities are free.

As with the other services, connections are refused until the chain is
current ([Service Settings](../configuration/services#until-current)).
`safe` serves TLS with `cert_path` and `key_path`
([Secure connections](../configuration/services#2-secure-connections)),
Noise with `noise_secret`, or both on the same port.

| Setting | Default | Purpose |
| ------- | ------- | ------- |
| `stratum_v2.payout_address` | empty | Address paid by the coinbase; empty, the user identity |
| `stratum_v2.coinbase_tag` | empty | Text carried by the coinbase input script (at most 75 bytes) |
| `stratum_v2.extranonce_prefix_size` | 4 | Coinbase extranonce bytes assigned to each extended channel (at least 4) |
| `stratum_v2.extranonce_size` | 8 | Coinbase extranonce bytes rolled by an extended channel miner |
| `stratum_v2.maximum_channels` | 1024 | Mining channels open on a connection |
| `stratum_v2.minimum_difficulty` | 1 | Share difficulty floor of a channel |
| `stratum_v2.start_difficulty` | 0 | Share difficulty of a new channel; 0, from the channel's nominal hash rate |
| `stratum_v2.share_interval_seconds` | 10 | Target seconds between shares (0 fixes the difficulty) |
| `stratum_v2.authorize_timeout_seconds` | 15 | Seconds to set up the connection and open a channel before it is closed (0 is unlimited) |
| `stratum_v2.noise_secret` | empty | Server static secret key; empty, no Noise |
| `stratum_v2.noise_certificate` | empty | Certificate of the static key, issued by the authority |
| `stratum_v2.noise_authority` | empty | Authority secret key, with which the server issues its own certificate |
| `stratum_v2.noise_authority_key` | empty | Authority public key, against which the certificate is checked at startup |
| `stratum_v2.noise_validity_days` | 1 | Days either side of each handshake that a self-issued certificate is valid |
| `pool.template_interval_seconds` | 30 | Seconds between replacements of the template (0 disables) |
| `pool.template_fee_increase` | 0 | Satoshis of fees a replacement template must add |

A standard channel is assigned the whole extranonce, prefix and rolled
bytes together, so the two sizes together may not exceed 32 bytes.
Startup fails if `extranonce_prefix_size` is below 4, `extranonce_size`
or `maximum_channels` is zero, the extranonce exceeds 32 bytes, the tag
exceeds 75 bytes, the coinbase input script would exceed 100 bytes, or
the minimum difficulty is not positive. It also fails on any Noise
setting that is malformed, on both or neither of `noise_authority` and
`noise_certificate` with `noise_secret`, on a certificate that does not
verify against `noise_authority_key`, and on `safe` binds with neither
TLS nor Noise configured.

With the service enabled, `pool.coinbase_weight` and
`pool.coinbase_sigops` are derived from this coinbase, as for
[Stratum v1](stratum-v1#1-setup), the larger of the two when both
services are enabled.

### Noise keys

The transport is Noise_NX over secp256k1 with ElligatorSwift,
ChaCha20-Poly1305 and SHA-256, as the specification defines. The server
is known by its static key, and proves it with a certificate signed
(BIP340) by an authority, whose public key the miner pins. Every key and
certificate is Base58Check, in the same text forms as the Stratum V2
reference implementation, so values move between the two unchanged.

The secret keys are made from entropy, and the certificate on the
authority's machine, so that the authority's secret need never be on the
server ([BX Commands](../client/commands#10-math)):

```
$ bx noise-new <entropy> > authority.secret
$ bx noise-new <other entropy> > server.secret
$ bx noise-public < server.secret
<server public key>
$ bx noise-cert --days 30 <server public key> < authority.secret
<certificate>
$ bx noise-public < authority.secret
<authority public key>
```

Configure `noise_secret` with the server secret and `noise_certificate`
with the certificate, and give miners the authority public key, the
string beginning `9` that the reference implementation also prints. A
certificate is valid from `--valid_from` (default now) for `--days`
(default 365), and must be reissued before it expires.

Alternatively, `noise_authority` configures the authority's secret on the
server, which then issues its own certificate at each handshake, valid
`noise_validity_days` either side of it. This is simpler for testing, but
places the authority's secret on the server. `noise_authority_key`, if
set, is checked against the certificate at startup.

### Start difficulty

A channel starts at `start_difficulty` if set, otherwise at the rate of
its nominal hash rate: the hash rate times `share_interval_seconds`
divided by 2<sup>32</sup>. Its floor is the higher of
`minimum_difficulty` and the difficulty of the channel's maximum target.
Vardiff then adjusts it, as for [Stratum v1](stratum-v1#start-difficulty),
and [`update_channel`](#update_channel) restarts it from a new hash rate
when `start_difficulty` is 0.

### Connection limits

A connection that has not completed setup and opened a channel within
`authorize_timeout_seconds` (default 15) is closed.
`expiration_minutes` and `inactivity_minutes` default to 0, no limit, as
for [Stratum v1](stratum-v1#connection-limits).

With `credential` set, only a WS upgrade can carry a credential (HTTP
basic authentication), and TCP connections are refused. Miners using TCP
are therefore limited by Noise, `bind` address or firewall
([Authentication](../configuration/services#3-authentication)).

## 2. Messages

| Message | Direction | Status |
| ------- | --------- | ------ |
| [`setup_connection`](#setup_connection) | Miner to `bs` | Mining protocol only |
| [`setup_connection_success`](#setup_connection_success) | `bs` to miner | Sent |
| [`setup_connection_error`](#setup_connection_error) | `bs` to miner | Sent |
| [`open_standard_mining_channel`](#open_standard_mining_channel) | Miner to `bs` | Handled |
| [`open_standard_mining_channel_success`](#open_standard_mining_channel_success) | `bs` to miner | Sent |
| [`open_extended_mining_channel`](#open_extended_mining_channel) | Miner to `bs` | Handled |
| [`open_extended_mining_channel_success`](#open_extended_mining_channel_success) | `bs` to miner | Sent |
| [`open_mining_channel_error`](#open_mining_channel_error) | `bs` to miner | Sent |
| [`update_channel`](#update_channel) | Miner to `bs` | Handled |
| [`update_channel_error`](#update_channel_error) | `bs` to miner | Sent |
| [`close_channel`](#close_channel) | Miner to `bs` | Handled |
| [`set_target`](#set_target) | `bs` to miner | Sent |
| [`new_mining_job`](#new_mining_job) | `bs` to miner | Sent |
| [`new_extended_mining_job`](#new_extended_mining_job) | `bs` to miner | Sent |
| [`set_new_prev_hash`](#set_new_prev_hash) | `bs` to miner | Sent |
| [`submit_shares_standard`](#submit_shares_standard) | Miner to `bs` | Handled |
| [`submit_shares_extended`](#submit_shares_extended) | Miner to `bs` | Handled |
| [`submit_shares_success`](#submit_shares_success) | `bs` to miner | Sent |
| [`submit_shares_error`](#submit_shares_error) | `bs` to miner | Sent |
| [`set_custom_mining_job`](#set_custom_mining_job) | Miner to `bs` | Not implemented (work selection refused) |
| [`set_extranonce_prefix`](#set_extranonce_prefix) | `bs` to miner | Not sent |
| [`set_group_channel`](#set_group_channel) | `bs` to miner | Not sent |
| [`reconnect`](#reconnect) | `bs` to miner | Not sent |

Jobs begin once a channel is open. Error reasons are the codes of the
specification.

## 3. Connection

### setup_connection

Opens the connection, with the subprotocol, the range of versions and
the flags of the features the miner requires. `bs` serves the Mining
protocol at version 2, and accepts the flags `REQUIRES_STANDARD_JOBS` and
`REQUIRES_VERSION_ROLLING`.

### setup_connection_success

Accepts the connection, at version 2, with no flags.

### setup_connection_error

Refuses the connection, then closes it: `unsupported-protocol` for any
subprotocol other than Mining, `protocol-version-mismatch` if version 2
is outside the miner's range, and `unsupported-feature-flags`, with the
flags, for any other flag, including `REQUIRES_WORK_SELECTION`.

## 4. Channels

### open_standard_mining_channel

Opens a channel in which the miner varies only the header, with its user
identity, nominal hash rate and maximum target.

### open_standard_mining_channel_success

Accepts the standard channel, with its identifier, target and
extranonce prefix, which is the channel's whole extranonce.

### open_extended_mining_channel

Opens a channel in which the miner also rolls part of the coinbase, with
its user identity, nominal hash rate, maximum target and the least
extranonce size it needs.

### open_extended_mining_channel_success

Accepts the extended channel, with its identifier, target, extranonce
size (`extranonce_size`) and extranonce prefix.

### open_mining_channel_error

Refuses either kind of channel: `unknown-user` if the user identity is
not an address and no `payout_address` is configured,
`max-target-out-of-range` for a zero maximum target,
`too-many-channels` beyond `maximum_channels`, and
`min-extranonce-size-too-large` if an extended channel needs more than
`extranonce_size`.

### update_channel

Updates a channel's nominal hash rate and maximum target. The maximum
target sets the channel's floor, and with `start_difficulty` 0 the hash
rate sets its difficulty, sent by [`set_target`](#set_target).

### update_channel_error

Refuses the update: `invalid-channel-id` or `max-target-out-of-range`.

### close_channel

Closes a channel.

## 5. Work

### set_target

Sets the target of the shares a channel submits, as vardiff adjusts it.

### new_mining_job

Sends a job to a standard channel: its merkle root and version.

### new_extended_mining_job

Sends a job to an extended channel: the coinbase around the extranonce,
the merkle path and the version.

### set_new_prev_hash

Starts mining on a new previous block, with its hash, time and target,
for a job already sent.

### submit_shares_standard

Submits a share on a standard channel: the channel, sequence number, job,
nonce, time and version. Version bits may be rolled only within the
general purpose bits (BIP320).

### submit_shares_extended

Submits a share on an extended channel, as for a standard channel, with
the rolled extranonce, which must be exactly `extranonce_size` bytes.

### submit_shares_success

Acknowledges each accepted share, with its sequence number and the sum
of its difficulty. A share is valid work whatever the outcome of a block
it mines.

### submit_shares_error

Rejects a share: `invalid-channel-id`, `invalid-job-id`,
`stale-share` for a job that has been replaced, `difficulty-too-low` or
`duplicate-share`. A share that cannot be valid, with the wrong
extranonce size (`invalid-extranonce-size`), version bits outside the
general purpose bits (`invalid-version`) or an invalid header
(`invalid-share`), is rejected and the connection closed.

## 6. Not served

### set_custom_mining_job

Proposes a job whose transactions the miner chose (work selection, with
its success and error replies). A miner that requires work selection is
refused at setup.

### set_extranonce_prefix

Changes a channel's extranonce prefix. Not sent; the prefix does not
change.

### set_group_channel

Groups standard channels. Not sent; there are no group channels.

### reconnect

Moves the miner to another server. Not sent.
