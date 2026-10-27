# Stratum v1

<div class="banner"><strong>Stratum is planned for version 5.</strong></div>

Stratum v1 is the mining pool protocol in common use, by which a pool
gives mining work to miners and receives their shares. Messages are
JSON-RPC 1.0, one per line, over TCP/S.

## 1. Messages

| Message | Direction | Purpose |
| ------- | --------- | ------- |
| [`mining.configure`](#miningconfigure) | Miner to pool | Negotiates extensions, such as version rolling |
| [`mining.subscribe`](#miningsubscribe) | Miner to pool | Subscribes to work |
| [`mining.authorize`](#miningauthorize) | Miner to pool | Authorizes a worker |
| [`mining.set_difficulty`](#miningset_difficulty) | Pool to miner | Sets the share difficulty |
| [`mining.notify`](#miningnotify) | Pool to miner | Sends a job |
| [`mining.submit`](#miningsubmit) | Miner to pool | Submits a share |
| [`mining.extranonce.subscribe`](#miningextranoncesubscribe) | Miner to pool | Accepts changes of extranonce |
| [`mining.extranonce.unsubscribe`](#miningextranonceunsubscribe) | Miner to pool | Declines changes of extranonce |
| [`client.reconnect`](#clientreconnect) | Pool to miner | Moves the miner to another server |
| [`client.hello`](#clienthello) | | |
| [`client.rejected`](#clientrejected) | | |

## 2. Session

### mining.configure

Negotiates protocol extensions before subscribing (BIP310), such as
version rolling, by which the miner varies bits of the block version.

### mining.subscribe

Subscribes to work. The result gives the extranonce prefix assigned to
the miner and the size of the extranonce it varies.

### mining.authorize

Authorizes a worker, by name and password, to submit shares.

### mining.extranonce.subscribe

Accepts later changes of the extranonce prefix from the pool.

### mining.extranonce.unsubscribe

Declines later changes of the extranonce prefix.

### client.reconnect

Asks the miner to reconnect, to the given server and port, after a
wait.

### client.hello

To be documented with the implementation.

### client.rejected

To be documented with the implementation.

## 3. Work

### mining.set_difficulty

Sets the difficulty of the shares the miner submits, from the next job.

### mining.notify

Sends a job: the previous block hash, the two parts of the coinbase
around the extranonce, the merkle branch, the version, the target and
the time, and whether earlier jobs are void.

### mining.submit

Submits a share: the worker, the job, the extranonce varied by the
miner, the time and the nonce, and with version rolling the version
bits.
