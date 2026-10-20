# libbitcoin-node — Architecture documentation

This is a top-down, source-anchored description of libbitcoin-node. It is
also written to support a **formal-verification effort**, which needs
state machines, invariants, pre/post-conditions, and a clear bus-vs.-store
ownership model.

The architectural concepts (parallel block download, sequential chasers
following concurrent download and validation, validation bypass by
checkpoints and milestones, append-only store writes with small copyable
indexes, and quiescence for snapshot, remap and shutdown) are from the
2021 [design document](libbitcoin-v4-node-design.pdf) for the version 4 node.

Every behavioural claim is anchored with `file:line` references into the
C++ source so it can be re-verified or re-derived if source drifts. The
citations in this revision were verified against libbitcoin-node master at
commit `a5173475` (2026-10-20), with `chaser_check` renamed to `chaser_download` (node branch `download`, `ea1e1264`).

---

## The 13 documents

| #  | File                                                                      | Topic                                                                       |
| -- | ------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| 00 | [`00-overview`](overview)                                        | Top-down map: layer stack, object graph, threading model, lifecycle         |
| 01 | [`01-event-bus`](event-bus)                                      | Every `chase` event with verified issuer/handler sites; methodology         |
| 02 | [`02-chaser-header`](header-chaser)                              | Header organize state machine, tree pruning, disorganize; 15 `organizeN` fault sites |
| 03 | [`03-chaser-download`](download-chaser)                                | Block-download orchestration; race_all purge barrier; σ slow-peer detector; download window |
| 04 | [`04-chaser-validate`](validation-chaser)                          | Consensus validation; own threadpool; batched signature and silent-payment verification; 12 `validateN` fault sites |
| 05 | [`05-chaser-confirm`](confirmation-chaser)                            | Order-based consensus check + confirmed-chain writer; stale timer; 12 `confirmN` fault sites |
| 06 | [`06-sessions-and-protocols`](sessions-and-protocols)            | Sessions, the protocol attach tree, `protocol_block_in_31800`                |
| 07 | [`07-header-protocols`](header-protocols)                        | Header in/out at 31800, 70012 and 70014 (compact blocks); prove-then-archive sync |
| 08 | [`08-block-out-protocols`](block-out-protocols)                  | Block out at 106, 70001, 70012 and 70014; streaming send loop; `not_found` |
| 09 | [`09-filter-out-protocol`](filter-out-protocol)                        | BIP157/158 client filters; three request types                              |
| 10 | [`10-tx-protocols`](transaction-protocols)                                | Tx in/out ladder at 106, 60002, 70001, 70013 and 70016                      |
| 11 | [`11-chaser-transaction`](transaction-chaser)                    | The transaction pool: package submission, compact block fill, scan starts; 9 `transactionN` fault sites |
| 12 | [`12-periphery-chasers`](periphery-chasers)                      | `chaser_snapshot`, `chaser_storage`, `chaser_template`, `chaser_estimate`    |

---

## Recommended reading orders

### For a new contributor
Read in order: **00 → 01 → 02 → 03 → 04 → 05** for the consensus
pipeline, then **06 → 07/08** for the corresponding peer protocols, then
**10 → 11** for the transaction pool. Skim 09 and 12 as needed.

### For a formal-verification reader
**01** is foundational — the `chase` events are the inter-process
interface. Then **02 §3, §5, §7** (organize state machine, disorganize
state machine, error-code → proof-obligation list), **04 §4–§7**
(validate consensus, batching, error inventory), **05 §4–§8** (confirm
algorithm, rollback atomicity, error inventory). The numbered
invariants throughout (`Validate-Backlog-1`, `Confirm-Rollback-1`,
etc.) are the recommended target set for a TLA+/Alloy spec.

### For a peer-protocol implementer
**00 §7** for the network-layer overview, then **06** for the
attach tree, then read whichever versioned family you need
(**07** for headers and compact blocks, **08** for blocks, **09** for
filters, **10** for tx).

---

## Conventions used throughout

### File:line citations
Every non-trivial behavioural claim has a `path/to/file.cpp:N` (or
`.hpp`, `.ipp`) citation. If you change source, run
`grep -rn 'pattern' src include` from the repo root to find new
locations and update the citation.

### Numbered invariants
Each doc names its invariants in the form `Topic-N` (e.g.
`Validate-Bypass-1`, `Confirm-Rollback-1`). The intent is that a
formal-spec encoding can cite them stably. Major invariant
families:

| Prefix          | Doc                              | Roughly                                            |
| --------------- | -------------------------------- | -------------------------------------------------- |
| `Concurrency-*` | 00                               | Strand discipline across the node                  |
| `Lifecycle-*`   | 00                               | start/run/close ordering                            |
| `Store-*`       | 00                               | Suspend/resume around store maintenance             |
| `Bus-*`         | 01                               | Subscription/unsubscription semantics               |
| `Organize-*`    | 02                               | Header organize state machine                       |
| `Download-*`       | 03                               | Download orchestration                              |
| `Validate-*`    | 04                               | Consensus validation and batching                   |
| `Confirm-*`     | 05                               | Confirmation + order-based consensus                |
| `Session-*`, `Attach-*`, `Protocol-*`, `Observer-*`, `Performer-*`, `BlockIn-*`, `HeaderIn-*`, `HeaderOut-*`, `Compact-*`, `Anti-Echo-*`, `BlockOut-*`, `Filter-*`, `TxIn-*`, `TxOut-*` | 06–10 | Network layer |
| `Pool-*`        | 11                               | Transaction pool                                    |
| `Snapshot-*`, `Storage-*`, `Estimate-*`, `Periphery-*` | 12 | Periphery chasers |

### Mermaid diagrams
All diagrams use Mermaid (sequence, flowchart, stateDiagram-v2,
classDiagram).

### "Spec view" / "Implementation notes" / "Notes for the formal model"
Most subsystem docs have these three closing sections. They are the
distilled-for-export view of each subsystem.

---

## Honest caveats

1. **No build verification.** Citations are textual. They were
   re-grepped during writing but the code has not been built or
   executed during this documentation effort. A version drift
   between source and docs is possible.
2. **`block.accept` / `block.connect` semantics** live in
   libbitcoin-system, not this repo. Docs 02/04/05 describe the
   *sequencing* of those calls, not their content. The consensus
   surface is delegated to libbitcoin-system documentation.
3. **Store consistency** is treated as an oracle. Every numbered
   `organizeN`/`validateN`/`confirmN`/`transactionN` fault is documented
   as a proof obligation against store-consistency invariants supplied by
   libbitcoin-database. A full proof would require importing those.
4. **Discrepancies with `chase.hpp` comments**: the inline event-bus
   doc in `chase.hpp` has a few stale entries (incomplete handler lists,
   dormant events). All are flagged in
   [`01-event-bus`](event-bus) with `⚠` and discussed in
   §2 of that doc.
5. **Stub subsystems**: `chaser_template` is a stub. The doc describes
   its wiring and intended design but notes clearly that current
   behaviour is "no-op".
6. **Database-side batching.** The signature and silent-payment batch
   tables, their verification kernels (CPU or GPU) and the pooled-block
   validation query live in libbitcoin-database and libbitcoin-system.
   Doc 04 describes the node's bank/drain protocol around them, not the
   kernels.

---

## Coverage map

```
libbitcoin-node
├── src/
│   ├── full_node.cpp ........................ 00
│   ├── configuration.cpp / settings.cpp ..... (mentioned in 00, not detailed)
│   ├── error.cpp ............................ 00 §9
│   ├── estimator.cpp ........................ 12 §4 (interface only)
│   │
│   ├── chasers/
│   │   ├── chaser.cpp ....................... 00 §3 (base; per-doc as needed)
│   │   ├── chaser_header.cpp ................ 02
│   │   ├── chaser_download.cpp ................. 03
│   │   ├── chaser_validate.cpp .............. 04
│   │   ├── chaser_validate_parallel.cpp ..... 04 §4
│   │   ├── chaser_validate_batch.cpp ........ 04 §5
│   │   ├── chaser_validate_capture.cpp ...... 04 §5
│   │   ├── chaser_confirm.cpp ............... 05
│   │   ├── chaser_transaction.cpp ........... 11
│   │   ├── chaser_template.cpp .............. 12 §3
│   │   ├── chaser_estimate.cpp .............. 12 §4
│   │   ├── chaser_snapshot.cpp .............. 12 §1
│   │   └── chaser_storage.cpp ............... 12 §2
│   │
│   ├── sessions/
│   │   ├── session.cpp ...................... 06 §1
│   │   ├── session_inbound.cpp .............. 06 §1.3
│   │   ├── session_outbound.cpp ............. 06 §1.4
│   │   └── session_manual.cpp ............... 06 §1 (typedef)
│   │
│   ├── channels/
│   │   └── channel_peer.cpp ................. 07 §8 (announcement cache)
│   │
│   └── protocols/
│       ├── protocol.cpp ..................... 06 §3
│       ├── protocol_peer.cpp ................ 06 §3; 07 §8 anti-echo
│       ├── protocol_observer.cpp ............ 06 §3.2
│       ├── protocol_performer.cpp ........... 06 §4
│       │
│       ├── protocol_block_in_31800.cpp ...... 06 §5
│       ├── protocol_block_out_106.cpp ....... 08 §2
│       ├── protocol_block_out_70001.cpp ..... 08 §3
│       ├── protocol_block_out_70012.cpp ..... 08 §4
│       ├── protocol_block_out_70014.cpp ..... 08 §5
│       │
│       ├── protocol_header_in_31800.cpp ..... 07 §2
│       ├── protocol_header_in_70012.cpp ..... 07 §3
│       ├── protocol_header_in_70014.cpp ..... 07 §4
│       ├── protocol_header_out_31800.cpp .... 07 §5
│       ├── protocol_header_out_70012.cpp .... 07 §6
│       ├── protocol_header_out_70014.cpp .... 07 §7
│       │
│       ├── protocol_filter_out_70015.cpp .... 09
│       ├── protocol_transaction_in_106.cpp .. 10 §2
│       ├── protocol_transaction_in_70001.cpp  10 §2
│       ├── protocol_transaction_in_70013.cpp  10 §2
│       ├── protocol_transaction_in_70016.cpp  10 §2
│       ├── protocol_transaction_out_106.cpp . 10 §3
│       ├── protocol_transaction_out_60002.cpp 10 §3
│       ├── protocol_transaction_out_70001.cpp 10 §3
│       ├── protocol_transaction_out_70013.cpp 10 §3
│       └── protocol_transaction_out_70016.cpp 10 §3
│
└── include/bitcoin/node/
    ├── full_node.hpp ........................ 00
    ├── chase.hpp ............................ 00 §4; 01 (verified against source)
    ├── events.hpp ........................... 00 §4 (metrics enum)
    ├── error.hpp ............................ 00 §9
    ├── settings.hpp ......................... 00 §10
    ├── estimator.hpp ........................ 12 §4
    └── impl/sessions/session_peer.ipp ....... 06 §2
```

Files **not** detailed (treated as "use as documented"):
- `configuration.cpp` / `settings.cpp` / `parser.cpp` — configuration
- `messages/` headers — wire types from libbitcoin-network
- `block_arena.hpp` / `block_memory.hpp` — arena allocator (not currently
  wired into channel construction; see 00 §8)

---

## How to update these docs after source changes

1. Run the verification greps from
   [`01-event-bus §4`](event-bus#4-methodology) to detect
   bus-graph drift.
2. For per-chaser docs, the relevant invariants reference specific
   `file:line`s — re-grep those when their files change.
3. The error inventories in each chaser doc (`organizeN`,
   `validateN`, `confirmN`, `transactionN`, `batchN`, `estimates_*`) are
   exhaustive at the time of writing — any new `error::<chaser>N` entry
   should add a row.
4. The attach tree in
   [`06 §2.3`](sessions-and-protocols#23-attach_protocolschannel--session_peeripp71-190)
   should be re-checked whenever `session_peer.ipp` is modified.
5. Update the verification commit at the top of this page.
