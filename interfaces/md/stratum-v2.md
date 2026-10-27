# Stratum v2

<div class="banner"><strong>Stratum is planned for version 5.</strong></div>

Stratum v2 is the successor to [Stratum v1](stratum-v1): a binary
protocol, encrypted and authenticated by the Noise protocol, over TCP/S.
These are the messages of its mining protocol.

## 1. Messages

| Message | Direction | Purpose |
| ------- | --------- | ------- |
| [`setup_connection`](#setup_connection) | Miner to pool | Opens the connection, with the protocol and versions |
| [`setup_connection_success`](#setup_connection_success) | Pool to miner | Accepts the connection |
| [`setup_connection_error`](#setup_connection_error) | Pool to miner | Refuses the connection |
| [`open_standard_mining_channel`](#open_standard_mining_channel) | Miner to pool | Opens a channel for header-only mining |
| [`open_standard_mining_channel_success`](#open_standard_mining_channel_success) | Pool to miner | Accepts the channel |
| [`open_standard_mining_channel_error`](#open_standard_mining_channel_error) | Pool to miner | Refuses the channel |
| [`open_extended_mining_channel`](#open_extended_mining_channel) | Miner to pool | Opens a channel in which the miner varies the extranonce |
| [`open_extended_mining_channel_success`](#open_extended_mining_channel_success) | Pool to miner | Accepts the channel |
| [`open_extended_mining_channel_error`](#open_extended_mining_channel_error) | Pool to miner | Refuses the channel |
| [`update_channel`](#update_channel) | Miner to pool | Updates the channel's hash rate and target |
| [`update_channel_error`](#update_channel_error) | Pool to miner | Refuses the update |
| [`close_channel`](#close_channel) | Either | Closes a channel |
| [`set_target`](#set_target) | Pool to miner | Sets the share target |
| [`new_mining_job`](#new_mining_job) | Pool to miner | Sends a job to a standard channel |
| [`new_extended_mining_job`](#new_extended_mining_job) | Pool to miner | Sends a job to an extended channel |
| [`set_new_prev_hash`](#set_new_prev_hash) | Pool to miner | Starts mining on a new previous block |
| [`set_custom_mining_job`](#set_custom_mining_job) | Miner to pool | Proposes a job built by the miner |
| [`set_custom_mining_job_success`](#set_custom_mining_job_success) | Pool to miner | Accepts the job |
| [`set_custom_mining_job_error`](#set_custom_mining_job_error) | Pool to miner | Refuses the job |
| [`submit_shares`](#submit_shares) | Miner to pool | Submits shares |
| [`submit_shares_success`](#submit_shares_success) | Pool to miner | Acknowledges shares |
| [`submit_shares_error`](#submit_shares_error) | Pool to miner | Rejects shares |
| [`reconnect`](#reconnect) | Pool to miner | Moves the miner to another server |

## 2. Connection

### setup_connection

Opens the connection, with the subprotocol, the range of versions and
the flags of the features the miner supports.

### setup_connection_success

Accepts the connection, with the version and flags in use.

### setup_connection_error

Refuses the connection, with the reason.

### reconnect

Asks the miner to reconnect, to the given server and port.

## 3. Channels

### open_standard_mining_channel

Opens a channel in which the miner varies only the header, with its
nominal hash rate and maximum target.

### open_standard_mining_channel_success

Accepts the standard channel, with its identifier, target and
extranonce prefix.

### open_standard_mining_channel_error

Refuses the standard channel, with the reason.

### open_extended_mining_channel

Opens a channel in which the miner also varies part of the coinbase,
with the size of the extranonce it needs.

### open_extended_mining_channel_success

Accepts the extended channel, with its identifier, target and extranonce
prefix and size.

### open_extended_mining_channel_error

Refuses the extended channel, with the reason.

### update_channel

Updates a channel's nominal hash rate and maximum target.

### update_channel_error

Refuses the update, with the reason.

### close_channel

Closes a channel, with the reason.

## 4. Work

### set_target

Sets the target of the shares a channel submits.

### new_mining_job

Sends a job to a standard channel: its merkle root and version.

### new_extended_mining_job

Sends a job to an extended channel: the coinbase around the extranonce,
the merkle path and the version.

### set_new_prev_hash

Starts mining on a new previous block, with its hash, time and target,
for a job already sent.

### set_custom_mining_job

Proposes a job whose transactions the miner chose.

### set_custom_mining_job_success

Accepts the miner's job.

### set_custom_mining_job_error

Refuses the miner's job, with the reason.

### submit_shares

Submits shares: the channel, the job, the nonce, the time and the
version, and on an extended channel the extranonce.

### submit_shares_success

Acknowledges the shares accepted since the last acknowledgement.

### submit_shares_error

Rejects a share, with the reason.
