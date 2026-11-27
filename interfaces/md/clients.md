# Client Compatibility

The interfaces of `bs` are drop-ins for the interfaces of other servers,
so that existing clients can use `bs` unchanged. These matrices show,
for each client, the interfaces it uses and how it fares on each against
`bs`: first the clients that have been run against `bs`, then those that
use the same interfaces but have not yet been tested.

| Cell | Result |
| :-: | ------ |
| <span class="works">✔</span> | Works: the client did its job end to end. |
| <span class="partial">◑</span> | Partial: some of its features fail. |
| <span class="blocked">✘</span> | Blocked: it fails. |
| <span class="retest">↻</span> | Retest: the failure is fixed in `bs`, and the client has not been run again. |
| <span class="expected">○</span> | Expected: untested, but every method the client uses is served. |
| <span class="no">⊘</span> | No: the client requires methods on that interface that `bs` does not serve, such as bitcoind's wallet methods (see [Node wallet clients](#node-wallet-clients)). |

A blank cell is an interface the client does not use.

## 1. Tested

Results are for the `bs` master branch on the date given, on mainnet.
Each client links to its notes (§3).

| Client | Kind | Version | Date | [Native](native) | [Electrum](electrum) | [Sparrow](sparrow) | [Bitcoind<br>JSON-RPC](bitcoind-rpc) | [Bitcoind<br>REST](bitcoind-rest) | [ZMQ](zeromq) | [BTCD](btcd) | [Esplora](esplora) | [P2P](p2p) |
| ------ | ---- | ------- | ---- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [BDK](#bdk) | Wallet library | 4.0.0 | <span class="nw">2026-11-22</span> | | <span class="works" title="Works">✔</span> | | <span class="blocked" title="Blocked">✘</span> | | | | <span class="works" title="Works">✔</span> | <span class="works" title="Works">✔</span> |
| [Bitcoin Core](#bitcoin-core) | Peer | 31.0 | <span class="nw">2026-10-17</span> | | | | | | | | | <span class="works" title="Works">✔</span> |
| [BTCPay Server](#btcpay-server) | Payment processor | 2.4.7 | <span class="nw">2026-11-22</span> | | | | <span class="works" title="Works">✔</span> | | | | | <span class="works" title="Works">✔</span> |
| [Core Lightning](#core-lightning) | Lightning node | 26.06.10 | <span class="nw">2026-11-22</span> | | | | <span class="works" title="Works">✔</span> | | | | | |
| [Electrum](#electrum) | Wallet | 4.8.4 | <span class="nw">2026-11-23</span> | | <span class="partial" title="Partial">◑</span> | | | | | | | |
| [Fulcrum](#fulcrum) | Electrum server | 2.1.3 | <span class="nw">2026-10-16</span> | | | | <span class="blocked" title="Blocked">✘</span> | | <span class="works" title="Works">✔</span> | | | |
| [kassiber](#kassiber) | Accounting | 0.22.78 | <span class="nw">2026-11-06</span> | | <span class="works" title="Works">✔</span> | | <span class="no" title="No">⊘</span> | | | | <span class="blocked" title="Blocked">✘</span> | |
| [lnd](#lnd) | Lightning node | 0.21.8 | <span class="nw">2026-11-23</span> | | | | <span class="works" title="Works">✔</span> | | <span class="works" title="Works">✔</span> | <span class="partial" title="Partial">◑</span> | | <span class="works" title="Works">✔</span> |
| [mempool](#mempool) | Explorer | 3.3.2 | <span class="nw">2026-11-21</span> | | <span class="works" title="Works">✔</span> | | <span class="works" title="Works">✔</span> | | | | | |
| [SatSage](#satsage) | Wallet analysis | 1.0.2 | <span class="nw">2026-11-23</span> | <span class="works" title="Works">✔</span> | <span class="partial" title="Partial">◑</span> | | <span class="works" title="Works">✔</span> | | | | | <span class="works" title="Works">✔</span> |
| [Sparrow Wallet](#sparrow-wallet) | Wallet | | <span class="nw">2026-10</span> | | <span class="works" title="Works">✔</span> | <span class="works" title="Works">✔</span> | | | | | | |
| [Specter Desktop](#specter-desktop) | Wallet | 2.3.0 | <span class="nw">2026-11-16</span> | | <span class="works" title="Works">✔</span> | | <span class="no" title="No">⊘</span> | | | | | |

## 2. Untested

Expected compatibility, from each client's source or documentation. It
is not a test.

| Client | Kind | [Native](native) | [Electrum](electrum) | [Sparrow](sparrow) | [Bitcoind<br>JSON-RPC](bitcoind-rpc) | [Bitcoind<br>REST](bitcoind-rest) | [ZMQ](zeromq) | [BTCD](btcd) | [Esplora](esplora) | [P2P](p2p) |
| ------ | ---- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [Alby Hub](https://albyhub.com) | Lightning node | | | | | | | | <span class="expected" title="Expected">○</span> | |
| [Aqua](https://aqua.net) | Wallet | | <span class="expected" title="Expected">○</span> | | | | | | | |
| [Ashigaru Dojo](https://ashigaru.rs) | Wallet backend | | <span class="expected" title="Expected">○</span> | | <span class="expected" title="Expected">○</span> | | <span class="expected" title="Expected">○</span> | | | |
| [BitBoxApp](https://bitbox.swiss/app/) | Hardware wallet app | | <span class="expected" title="Expected">○</span> | | | | | | | |
| [Bitkit](https://bitkit.to) | Lightning wallet | | <span class="expected" title="Expected">○</span> | | | | | | | |
| [Blixt](https://blixtwallet.com) | Lightning wallet | | | | | | | | | <span class="expected" title="Expected">○</span> |
| [Blockstream app](https://blockstream.com/app/) | Wallet | | <span class="expected" title="Expected">○</span> | | | | | | | |
| [BlueWallet](https://bluewallet.io) | Wallet | | <span class="expected" title="Expected">○</span> | | | | | | | |
| [BTC RPC Explorer](https://github.com/janoside/btc-rpc-explorer) | Explorer | | <span class="expected" title="Expected">○</span> | | <span class="expected" title="Expected">○</span> | | | | | |
| [btcwallet](https://github.com/btcsuite/btcwallet) | Wallet daemon | | | | | | | <span class="partial" title="Partial">◑</span> | | |
| [electrs](https://github.com/romanz/electrs) | Electrum server | | | | <span class="blocked" title="Blocked">✘</span> | | | | | <span class="expected" title="Expected">○</span> |
| [Fedimint](https://fedimint.org) | Federation | | <span class="expected" title="Expected">○</span> | | <span class="expected" title="Expected">○</span> | | | | <span class="expected" title="Expected">○</span> | |
| [Floresta](https://github.com/getfloresta/Floresta) | Utreexo node | | | | | | | | | <span class="no" title="No">⊘</span> |
| [LDK Node](https://lightningdevkit.org) | Lightning library | | <span class="expected" title="Expected">○</span> | | <span class="expected" title="Expected">○</span> | <span class="expected" title="Expected">○</span> | | | <span class="expected" title="Expected">○</span> | |
| [Liana](https://wizardsardine.com/liana/) | Wallet | | <span class="expected" title="Expected">○</span> | | <span class="no" title="No">⊘</span> | | | | | |
| [Nunchuk](https://nunchuk.io) | Wallet | | <span class="expected" title="Expected">○</span> | | | | | | | |
| [ord](https://github.com/ordinals/ord) | Index | | | | <span class="expected" title="Expected">○</span> | | | | | |
| [Phoenix](https://phoenix.acinq.co) | Lightning wallet | | <span class="expected" title="Expected">○</span> | | | | | | | |
| [Stack Wallet](https://stackwallet.com) | Wallet | | <span class="expected" title="Expected">○</span> | | | | | | | |
| [Trezor Suite](https://trezor.io/trezor-suite) | Hardware wallet app | | <span class="expected" title="Expected">○</span> | | | | | | | |
| [Wasabi Wallet](https://wasabiwallet.io) | Wallet | | | | <span class="expected" title="Expected">○</span> | | | | | <span class="expected" title="Expected">○</span> |
| [Zeus](https://zeusln.com) | Lightning wallet | | | | | | | | | <span class="expected" title="Expected">○</span> |

Custodial wallets, and wallets bound to their provider's backend, have
no server setting and are not listed. Node platforms such as Umbrel,
Start9 and RaspiBlitz host a node and its clients rather than connect
to one.

[Stratum v1](stratum-v1) clients are mining devices and proxies, such as
Bitaxe (AxeOS), cgminer and Braiins OS. [Stratum v2](stratum-v2) is
planned for version 5; its clients include the Stratum V2 reference
translator.

## 3. Notes

### lnd

**bitcoind backend:** wallet creation, `newaddress` (P2WKH, NP2WKH,
P2TR), restart with addresses, graph sync and channel validation, and
wallet recovery work. ZMQ blocks arrive within a second of validation.

**neutrino backend:** recovery of a wallet from 2019 (366,000 blocks) took
about 15 minutes and found every reference transaction. Requires a store
created with `node.provide_filters`.

**btcd backend:** the chain syncs, but once the wallet has an address, lnd
calls the deprecated [`rescan`](btcd#rescan) with addresses, which `bs`
does not serve, and the wallet never finishes syncing. Two client changes
replace `rescan` with `loadtxfilter` and `rescanblocks`, as btcd
recommends:
[btcsuite/btcwallet#1515](https://github.com/btcsuite/btcwallet/pull/1515)
and [lightningnetwork/lnd#11583](https://github.com/lightningnetwork/lnd/pull/11583),
both open. With them, a 368,000-block wallet rescan found the same 397
transactions as the neutrino backend, and the lnd integration suite gives
identical results against btcd with and without them.

**Retest with 0.21.8:** sync, `newaddress` and restart work on the
bitcoind and neutrino backends, and the chain notifier delivered every
confirmation and spend notification for pool transactions when their
block arrived. Republishing a transaction that is already pooled or
confirmed (`wallet publishtx`) succeeds on the bitcoind and btcd
backends, as the [btcd](btcd) interface reports btcd's reject reasons.

### Sparrow Wallet

Wallets load, and silent payment wallets are scanned and notified over
`blockchain.silentpayments.subscribe`. Requires the address index, and
for silent payments `node.silent_start_height`.

### Specter Desktop

In Spectrum mode (Spectrum 0.8.0), Specter negotiates protocol 1.4. A
watch-only BIP84 wallet imported by descriptor, with 600 receive and
change addresses, synced 285 confirmed transactions, every one at the
same height as a public Electrum server reports for the same addresses,
and the same balance. Spectrum makes its requests one at a time, so its
sync time grows with the round trip time to the server. In Core mode
Specter keeps its wallets in the node, which requires bitcoind's wallet
methods.

### Electrum

A watch-only wallet of 45 addresses (P2PKH, P2SH, P2WPKH, P2WSH, P2TR,
from 2015 to the pool, up to 150 transactions each) synced in 30
seconds. All 541 transactions it shared with a public Electrum server
were identical in amount, fee, height, position and confirmations, the
confirmed balance matched, and the wallet verified every header and
merkle proof.

Sending was tested on testnet5, with testnet5 added to Electrum
([eynhaender/electrum](https://github.com/eynhaender/electrum/tree/feature/testnet5)).
The wallet received coins, broadcast a payment through `bs`, which
relayed it to other nodes within 20 seconds, and replaced it with a
higher fee (RBF). The wallet showed the correct history and balance
after the replacement confirmed.

Partial for the pool: `blockchain.scripthash.get_balance` reports no
unconfirmed amount. A replaced transaction stays in the `bs` pool next
to its replacement, so `get_mempool` lists both and `listunspent`
returns the outputs of both. A transaction that has left the pool, such
as the loser of a double spend or a replaced transaction after its
replacement confirms, is still reported as unconfirmed by
`get_history`, `get_mempool` and `listunspent`. Electrum itself drops
such conflicts, but clients that rely on `listunspent` or `get_mempool`
see outputs that cannot confirm.

### SatSage

A tax and holding period analyzer for xpub wallets. Each interface was
compared with a public Electrum server, for an address with 127 unspent
outputs and the history of a BIP84 wallet (300 addresses).

**Native REST:** SatSage recognizes `bs` by `libbitcoin` in the
`server.version` name and finds the address index in
[`configuration`](native#configuration). The outputs of the address,
their transactions and their previous outputs were identical, 127 of 127.

**Electrum:** the outputs and transactions of the address were identical,
and 146 of the 148 history entries. In the other two, SatSage names as
the spender a transaction that lost a double spend and has left the `bs`
pool, which `bs` still reports as unconfirmed (see [Electrum](#electrum)),
in place of the confirmed one.

**Bitcoind JSON-RPC:** `scantxoutset` returned the same 127 outputs, from
the address index, and `getrawtransaction` the same transactions.

**P2P:** SatSage scans client filters and fetches the matching blocks
from `bs` as its only peer. The scan was stopped after the newest blocks
and the first 16,000 blocks from the SegWit height. Each of the 7 outputs
it found is on the public server, and its one false positive was
discarded.

Its import of xpubs from a node wallet (`listdescriptors`) requires a
node wallet.

### kassiber

**Electrum:** 436 of 436 transactions identical to a public Fulcrum
server, with amounts, fees and timestamps. **Esplora:** a client fault.
The client computes script hashes in Electrum byte order, reversed, for
Esplora's `/scripthash/` paths, which take them unreversed, so it finds
no transactions on any Esplora server. **Bitcoind JSON-RPC:** requires bitcoind
wallet methods (`createwallet`, `importdescriptors`, `listwallets`).

### Fulcrum

Fulcrum requires a `Content-Length` header on each bitcoind JSON-RPC response, and
`bs` sends single responses with chunked transfer encoding, which
HTTP/1.1 allows. With a test build that sized single responses, Fulcrum
indexed half of mainnet (to height 483,000) at about 9 blocks a second,
with ZMQ block notifications. `bs` serves the Electrum interface itself,
so Fulcrum is not needed in front of it.

### BTCPay Server

BTCPay Server 2.4.7 with NBXplorer 2.6.23, whose indexer reads the chain
and pool over P2P and checks them over bitcoind JSON-RPC. NBXplorer
synced, and the store, wallet, invoice addresses and the UTXO rescan of
an xpub (`scantxoutset`, identical outputs to Bitcoin Core) worked. Every
five minutes NBXplorer tests its pending transactions with
[`testmempoolaccept`](bitcoind-rpc#testmempoolaccept), and `bs` gives
Bitcoin Core's reject reasons for pooled, confirmed and conflicted
transactions, so pending payments stay pending. NBXplorer warns that it
is not whitelisted by the node, which is harmless.

### mempool

The mempool backend in its `electrum` mode, which reads blocks,
transactions and the pool over bitcoind JSON-RPC and addresses over Electrum.
It indexed the latest blocks, followed new ones, loaded the pool and
served fee recommendations. Against mempool.space: block headers,
transaction lists, transactions, their hex and merkle proofs, the
confirmation status of transactions, fee recommendations, projected
blocks and the 126 unspent outputs of an address all identical.

The pool loaded without errors and held the same transactions as the
`bs` pool (17,054). For 40 sampled pool transactions the fee, weight,
size and status matched [`getmempoolentry`](bitcoind-rpc#getmempoolentry),
and the ancestors and descendants matched
[`getmempoolancestors`](bitcoind-rpc#getmempoolancestors) and
[`getmempooldescendants`](bitcoind-rpc#getmempooldescendants), except
where `bs` holds two spends of one output: mempool links one spender,
so it lists one relative fewer. Address pool totals are zero, as the
Electrum balance reports no unconfirmed amount.

The differences from mempool.space are those of this backend mode,
and the same with Bitcoin Core: spent outputs without the spending
transaction, address totals without output counts (received shows the
balance, sent shows zero), address histories in pages of 10, and no
block status. Each page reads the full address history, so an address
of 462,000 transactions exceeds the frontend's 60 s timeout, although
`bs` answers its history in under 4 s. The pool held fewer transactions
than mempool.space, which reflects the pool of the node, not the
interface; it was within 10% of the pool of Bitcoin Core 32.1 on the
same host.

The `esplora` mode of mempool, which lifts these limits, is not
supported. It calls endpoints of mempool's own electrs fork that are not
part of the [Esplora](esplora) API. `bs` serves `POST /internal/txs`,
`POST /internal/mempool/txs` and the two `/internal/txs/outspends`
lookups, but not `GET /internal/mempool/txs` (the pool in pages),
`GET /internal/block/{hash}/txs` or `GET /address/{address}/txs/summary`.

The backend makes one request per transaction, and per input for its
previous output, one after another, so it should run close to the node:
at a round trip of 186 ms one block took several minutes, on the same
host about a second.

### Core Lightning

Core Lightning calls `bitcoin-cli` for `getnetworkinfo`,
`getblockchaininfo`, `getblockhash`, `getblock`, `estimatesmartfee`,
`getmempoolinfo`, `gettxout`, `sendrawtransaction` and `getpeerinfo`,
and requires amounts with exactly eight decimal places. Against an
instance of the same version on Bitcoin Core 32.1: startup, chain
height, fee rates, `newaddr`, `getrawblockbyheight`, `getutxout` (found
and spent), `getchaininfo`, and `sendrawtransaction` of pooled and
confirmed transactions all gave the same results. Core Lightning logs
an unusual fee rate where the `bs` estimate for 100 blocks exceeds that
for 12 blocks.

### BDK

With `bdk-cli`, full scans of BIP84 and BIP86 test wallets.
**Electrum** and **Esplora:** 285 and 32 transactions, identical in
content, heights, balance and next unused address to the public
Blockstream servers. **P2P:** a light client on `bdk_kyoto` 0.17, with
`bs` as its only peer, found the same transactions from client filters
(with a wallet lookahead of 250, as the default of 25 drops some), and
`bs` filters are byte-identical to BIP158 filters rebuilt from the
blocks. Kyoto requests header announcements (`sendheaders`) before its
header sync is complete, and drops a peer whose announcement of a new
block does not connect to its partial chain, so a sync from a single
peer can stop when a block arrives.

**Bitcoind JSON-RPC:** `bs` sends its responses with chunked transfer
encoding, and the default transport of the Rust `jsonrpc` crate, used
by `bitcoincore-rpc`, does not read chunked responses. A client change
that uses the crate's `minreq` transport is open:
[bitcoindevkit/bdk-cli#392](https://github.com/bitcoindevkit/bdk-cli/issues/392).

### Bitcoin Core

A differential test fed the same blocks, valid and invalid, to `bs` and
to Bitcoin Core over P2P: 15 of 15 decisions identical. Reorganization
tests against Bitcoin Core on regtest (depths 1 to 1000, ties, double
spends, restarts mid-reorganization): 35 of 35 passed.

### Untested clients

Electrum wallets negotiate protocol 1.4 to 1.6, and `bs` serves 1.0
through 1.7. electrs reads bitcoind JSON-RPC with the `simple_http`
transport of the Rust `jsonrpc` crate, which does not read the chunked
responses of `bs` (see [BDK](#bdk)), and refuses a node that reports
`pruned`. Wasabi, Zeus and Blixt require client filters. LDK Node reads blocks over bitcoind REST with bitcoind JSON-RPC for the rest.
Bitkit takes an Electrum server over TCP or TLS. Aqua takes one for
bitcoin only over TLS, with a certificate valid for the host name.
Alby Hub's built-in node (LDK) takes an Esplora server
(`LDK_ESPLORA_SERVER`), and Alby Hub can instead use an lnd or Core
Lightning node.
ord's index and server are expected to work, and `ord wallet` requires a
node wallet. Floresta requires Utreexo proofs from its peers.

### Node wallet clients

Some clients keep their wallet in the node, and call bitcoind's wallet
methods to create it, import descriptors or addresses, list and lock
unspent outputs, fund, sign and send. `bs` does not implement the
wallet methods (see [bitcoind JSON-RPC](bitcoind-rpc#11-methods-not-served)), and
these clients have no other backend, so they cannot be run on `bs`:

| Client | Kind | Wallet methods required |
| ------ | ---- | ----------------------- |
| [Eclair](https://github.com/ACINQ/eclair) | Lightning node | `fundrawtransaction`, `walletprocesspsbt`, `listunspent`, `lockunspent`, `getnewaddress`, `sendtoaddress`, … |
| [JoinMarket](https://github.com/JoinMarket-Org/joinmarket-clientserver) | Coinjoin | `importmulti` (legacy wallet), or `importdescriptors` in JoinMarket-NG, and `listunspent` |

Liana, Specter Desktop and kassiber also need a node wallet on bitcoind JSON-RPC,
and work over Electrum instead, so they stay in the matrices with **No**
on bitcoind JSON-RPC.

Floresta's **No** is unrelated: it requires Utreexo proofs from its P2P
peers, which `bs` does not provide.
