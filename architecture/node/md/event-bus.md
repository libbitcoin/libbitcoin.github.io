# 01 — Event Bus

> Companion to [`00-overview`](overview). This is the authoritative,
> source-verified reference for every `chase` enumerator: payload, issuer
> sites, handler sites, and known discrepancies with the inline
> `chase.hpp` documentation.
>
> Every fact below is grep-derived against master at `79eeac6a`.
> Methodology and queries are in [§4](#4-methodology) so any future change
> can be re-verified mechanically.

---

## 1. Subscriber model

### 1.1 Storage

```
event_subscriber_ : full_node                     // include/bitcoin/node/full_node.hpp:223
   = network::desubscriber<object_key, event_value>   // define.hpp:78
```

A `desubscriber` is the libbitcoin-network primitive that combines pub/sub
with explicit unsubscription via a key. All subscribers share one bus.

### 1.2 Typed payloads

`event_value` is a `std::variant` with one alternative per `chase`
enumerator, declared in enum order in `namespace chases`
(`include/bitcoin/node/chase.hpp`). Each payload struct carries a
`static constexpr chase id` and zero or one field:

| Field          | Type            | Events                                                                                      |
| -------------- | --------------- | ------------------------------------------------------------------------------------------- |
| —              |                 | `start`, `space`, `suspend`, `resume`, `unfull`, `stale`, `stop`                            |
| `height`       | `height_t`      | `snap`, `bump`, `checked`, `windowed`, `valid`, `template_`                                 |
| `branch_point` | `height_t`      | `purge`, `headers`, `regressed`, `disorganized`                                             |
| `channel`      | `object_t`      | `starved`, `split`, `stall`                                                                 |
| `count` / `sequence` | `count_t` | `download` / `report`                                                                       |
| `link`         | `header_t`      | `unchecked`, `unvalid`, `confirmable`, `unconfirmable`, `block`, `pruned`, `organized`, `reorganized` |
| `link`         | `transaction_t` | `transaction`                                                                               |

A `static_assert(is_chase_ordered(...))` guarantees the variant index equals
the enumerator, so `to_chase(value)` is `static_cast<chase>(value.index())`
and `to_payload<chase::X>(value)` is a `std::get` by that index.

> **Invariant (Bus-0).** An event cannot carry the wrong payload type: the
> payload struct *is* the event. Handlers switch on `to_chase(value)` and
> read `to_payload<chase::X>(value).field`.

### 1.3 Subscribe protocol

There are two subscribe APIs, both eventually owning state on the
`full_node` strand:

| API                                                       | Used by   | Strand discipline                                              |
| --------------------------------------------------------- | --------- | -------------------------------------------------------------- |
| `subscribe_chase(notifier) → object_key` (sync)           | chasers, `session_outbound` | Caller must already be on `full_node` strand |
| `subscribe_chase(notifier, completer)` (async)            | protocols | Posts to `full_node` strand internally; completer fires there  |

Chaser subscription path (`include/bitcoin/node/chasers/chaser.hpp:106-107`,
`src/chasers/chaser.cpp:96-99`):
```
chaser::subscribe_chase
  → full_node::subscribe_chase(handler)          // src/full_node.cpp:252-258
    → event_subscriber_.subscribe(handler, key)
```
Each chaser subscribes exactly once, in its `start()`, via
`SUBSCRIBE_CHASE(handle_chase, _1, _2)` (`chaser.hpp:188-189`). The
`handle_chase` body runs on the node strand and `POST`s the work to the
chaser's own strand.

Protocol subscription path (`src/protocols/protocol.cpp:183-232`):
```
protocol::subscribe_chase
  → session::subscribe_chase(handler, complete)  // src/sessions/session.cpp:114-118
    → full_node::subscribe_chase(handler, complete) // src/full_node.cpp:260-275
      → posts to strand → do_subscribe_chase
        → event_subscriber_.subscribe(handler, key)
        → complete(ec, key)   → protocol::handle_subscribe stores key_
                               → handle_subscribed posts subscribed() to channel strand
```
The async variant exists because a protocol is constructed on its channel
strand, not the node strand, so it must hop across. Subscription is
asynchronous, so a protocol may miss events emitted before it completes
(the source notes this at every protocol subscription site).

### 1.4 Notify protocol

```
chaser/protocol calls notify(ec, chases::X{...})
   → full_node::notify posts to strand           // src/full_node.cpp:222-227
     → do_notify on strand
        → event_subscriber_.notify(ec, value)     // :230-234
           → each subscriber's handle_chase runs here and POSTs to its own strand
```
`notify_one(key, ...)` (`:236-250`) delivers to a single subscriber by key;
it is used for `chase::split` (targeting the slowest channel) and for
`chase::stop` on unsubscribe.

### 1.5 Unsubscribe semantics

`full_node::unsubscribe_chase(key)` does not remove the entry; it sends a
single `chases::stop` to that subscriber only
(`src/full_node.cpp:277-280`). The subscriber's `handle_chase` returns
`false` on `chase::stop`, and the `desubscriber` interprets that as
removal. So:

> **Invariant (Bus-1).** A `false` return from `handle_chase` means
> "remove me". Every chaser returns `false` on `chase::stop` and when
> `closed()`; protocols return `false` when `stopped()`.

> **Invariant (Bus-2).** The bus is torn down only in `full_node::do_close`,
> which broadcasts `chases::stop` to all subscribers
> (`src/full_node.cpp:149`). After that point no further `notify` will
> deliver.

---

## 2. Verified event reference

Notation:
- **Issuer** is every `notify(... chases::X{...})` or
  `notify_one(... chases::X{...})` call site that is not commented out.
  Direct self-calls of `handle_chase` (not through the bus) are listed
  as *self*.
- **Handler** is every `case chase::X:` arm that is not commented out.
- Discrepancies with the `chase.hpp` inline doc are flagged ⚠.

### 2.1 Work shuffling

| Event       | Issuer (file:line)                                                                                   | Handler (file:line)                                                                                    |
| ----------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `start`     | `src/full_node.cpp:112` (`do_run`, direct `do_notify`)                                               | `chaser_download.cpp:132`, `chaser_validate.cpp:122`, `chaser_confirm.cpp:92`                             |
| `space`     | `src/full_node.cpp:319` (`fault` when `query_.is_full()`)                                            | `chaser_storage.cpp:83`                                                                                |
| `snap`      | **none** ⚠ — chase.hpp says issued by `confirm`; no live issuer                                      | `chaser_snapshot.cpp:123`                                                                              |
| `bump`      | `chaser_header.cpp:379` (first current strong header, and first after each regression); `chaser_validate_batch.cpp:419` (silent batch drained) ⚠; *self*: `chaser_validate.cpp:297`, `chaser_confirm.cpp:292` | `chaser_download.cpp:133`, `chaser_validate.cpp:123`, `chaser_confirm.cpp:93` |
| `suspend`   | `src/full_node.cpp:310` (`suspend`, with `error::suspended_channel`); `chaser_header.cpp:562` (after `do_disorganize`) ⚠ | `protocol_observer.cpp:77` (only)                                                  |
| `resume`    | `src/full_node.cpp:301` (after `net::resume`)                                                        | `chaser_download.cpp:131`, `chaser_validate.cpp:128`, `chaser_confirm.cpp:91`                             |
| `unfull`    | `chaser_storage.cpp:168` (reload from disk full succeeded, before `resume`)                           | `chaser_validate.cpp:101` (latched before the suspension gate)                                         |
| `starved`   | `protocol_block_in_31800.cpp:426`                                                                    | `chaser_download.cpp:123`                                                                                 |
| `split`     | `chaser_download.cpp:243` (via `notify_one` to the slowest channel)                                     | `protocol_block_in_31800.cpp:107`                                                                      |
| `stall`     | `chaser_download.cpp:248`                                                                               | `protocol_block_in_31800.cpp:114`                                                                      |
| `purge`     | `chaser_download.cpp:359`                                                                               | `protocol_block_in_31800.cpp:122`                                                                      |
| `report`    | **external** — issued by the executor in libbitcoin-server                                           | `protocol_block_in_31800.cpp:137`                                                                      |

Discrepancy notes:
- ⚠ **`bump`**: chase.hpp says issued by 'organize'. `chaser_validate` also
  issues it when a silent-payment bank drains, because the blocks of that
  bank may now be confirmable (`chaser_validate_batch.cpp:418-419`).
- ⚠ **`suspend`** is also issued by `chaser_header` after a
  disorganization (`chaser_header.cpp:558-562`), to reset all connections.
- ⚠ **`snap`** has no live issuer anywhere in this repo. Treat as dormant.

### 2.2 Candidate chain

| Event          | Issuer (file:line)                                                      | Handler (file:line)                                                                |
| -------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `headers`      | `chaser_header.cpp:385` (every current strong organize)                 | `chaser_download.cpp:157`                                                             |
| `download`     | `chaser_download.cpp:417` (`do_headers`), `:463` (`do_put_hashes`)         | `protocol_block_in_31800.cpp:129`                                                  |
| `regressed`    | `chaser_header.cpp:326`                                                 | `chaser_download.cpp:143`, `chaser_validate.cpp:151`, `chaser_confirm.cpp:103`        |
| `disorganized` | `chaser_header.cpp:559`                                                 | `chaser_download.cpp:149`, `chaser_validate.cpp:157`, `chaser_confirm.cpp:109`        |

### 2.3 Check / Identify

| Event       | Issuer (file:line)                                                                  | Handler (file:line)                                                                       |
| ----------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `checked`   | `protocol_block_in_31800.cpp:352`; `chaser_transaction.cpp:466` (compact block fill) | `chaser_download.cpp:138`, `chaser_validate.cpp:136` (also clears `window_archived_` at `:109`) |
| `unchecked` | `protocol_block_in_31800.cpp:325`; `chaser_transaction.cpp:673` (compact block with an invalid tx) | `chaser_header.cpp:150` (gated on `database.mark_unconfirmable`)              |
| `windowed`  | `chaser_download.cpp:403` (position reached the last requested height)                 | `chaser_validate.cpp:107` (latch) and `:141` (drain batches, called directly)              |

### 2.4 Accept / Connect

| Event     | Issuer (file:line)                                                                              | Handler (file:line)                                                    |
| --------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `valid`   | `chaser_validate.cpp:375` (`notify_block`; reached directly and from the batch drain's `mark_valids`) | `chaser_download.cpp:162`, `chaser_confirm.cpp:98`                  |
| `unvalid` | `chaser_validate.cpp:367` (`notify_block`; suppressed at startup)                               | `chaser_header.cpp:159` (gated on `database.mark_unconfirmable`)       |

### 2.5 Confirm (block)

| Event           | Issuer (file:line)        | Handler (file:line)                                            |
| --------------- | ------------------------- | -------------------------------------------------------------- |
| `confirmable`   | `chaser_confirm.cpp:368`  | None (chase.hpp agrees: "handled by none")                     |
| `unconfirmable` | `chaser_confirm.cpp:361`  | `chaser_header.cpp:168` (gated on `database.mark_unconfirmable`) |

### 2.6 Confirm (chain) and Mining

| Event           | Issuer (file:line)                                       | Handler (file:line)                                                                                                                                                 |
| --------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `block`         | `chaser_confirm.cpp:462` (`announce`, only when confirmed chain is current) | `chaser_snapshot.cpp:115`, `session_outbound.cpp:73`, `protocol_block_out_106.cpp:80`, `protocol_header_out_70012.cpp:71`, `protocol_transaction_out_70013.cpp:80` ⚠ |
| `pruned`        | `chaser_snapshot.cpp:166` (prune on first current block)  | `chaser_transaction.cpp:89`                                                                                                                                         |
| `stale`         | `chaser_confirm.cpp:523` (stale timer expiry)            | `session_outbound.cpp:74`, `protocol_transaction_out_70013.cpp:81` ⚠                                                                                                |
| `organized`     | `chaser_confirm.cpp:420` (`set_organized`)               | `chaser_transaction.cpp:79`, `chaser_template.cpp:76` ⚠                                                                                                             |
| `reorganized`   | `chaser_confirm.cpp:386` (`set_reorganized`)             | `chaser_transaction.cpp:84`, `chaser_template.cpp:77` ⚠                                                                                                             |
| `transaction`   | `chaser_transaction.cpp:241` (pooled from a reorganized block), `:378` (submitted package), `:620`, `:648` (compact fill) | `chaser_template.cpp:75`, `protocol_transaction_out_106.cpp:94` |
| `template_`     | `chaser_template.cpp:155` (each completed template build) | (miners, external)                                                                                                                                                  |

Discrepancies:
- ⚠ **`block`**: chase.hpp lists `protocol_header/block_out`.
  `chaser_snapshot` (one-shot prune trigger), `session_outbound`
  (connection count) and `protocol_transaction_out_70013` (fee filter
  refresh) are also live consumers.
- ⚠ **`stale`**: chase.hpp lists `protocol_transaction_out`;
  `session_outbound` also consumes it.
- ⚠ **`organized`**, **`reorganized`**: chase.hpp lists `transaction`;
  `chaser_template` also consumes both, to rebuild the template when the
  confirmed chain changes.

### 2.7 Stop

| Event  | Issuer (file:line)                                                                                                                                  | Handler                  |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| `stop` | `full_node::unsubscribe_chase` via `notify_one` (`src/full_node.cpp:279`); `full_node::do_close` via `event_subscriber_.stop(...)` (`:149`)          | Every chaser & protocol  |

---

## 3. Verified issuer / handler diagram

One node per *actual* source location rather than per chase.hpp comment.

```mermaid
flowchart LR
    FN[full_node]
    HDR[chaser_header]
    CHK[chaser_download]
    VAL[chaser_validate]
    CNF[chaser_confirm]
    TX[chaser_transaction]
    PIN["protocol_block_in_31800"]

    SNP[chaser_snapshot]
    STG[chaser_storage]
    TPL[chaser_template]
    MIN["miners (external)"]
    OBS[protocol_observer]
    SOUT[session_outbound]
    POUT_B["protocol_block_out_106"]
    POUT_H["protocol_header_out_70012"]
    POUT_T["protocol_transaction_out_106 / 70013"]

    FN -- "start, resume" --> CHK
    FN -- "start, resume" --> VAL
    FN -- "start, resume" --> CNF
    FN -- "space" --> STG
    FN -- "suspend" --> OBS
    HDR -- "headers, bump, regressed, disorganized" --> CHK
    HDR -- "bump, regressed, disorganized" --> VAL
    HDR -- "bump, regressed, disorganized" --> CNF
    HDR -- "suspend (after disorganize)" --> OBS
    PIN -- "checked" --> CHK
    PIN -- "checked" --> VAL
    PIN -- "unchecked" --> HDR
    PIN -- "starved" --> CHK
    CHK -- "download, split, stall, purge" --> PIN
    CHK -- "windowed" --> VAL
    VAL -- "valid" --> CHK
    VAL -- "valid" --> CNF
    VAL -- "unvalid" --> HDR
    VAL -- "bump (silent drain)" --> CHK
    CNF -- "unconfirmable" --> HDR
    CNF -- "block" --> SNP
    CNF -- "organized, reorganized" --> TPL
    CNF -- "block, stale" --> SOUT
    CNF -- "block" --> POUT_B
    CNF -- "block" --> POUT_H
    CNF -- "block, stale" --> POUT_T
    CNF -- "organized, reorganized" --> TX
    TX -- "checked, unchecked (compact fill)" --> CHK
    TX -- "transaction" --> TPL
    TX -- "transaction" --> POUT_T
    SNP -- "pruned" --> TX
    TPL -- "template_" --> MIN
    STG -- "unfull" --> VAL

    style HDR stroke:#4f8dff,stroke-width:2px
    style CNF stroke:#ff2357,stroke-width:2px
    style VAL stroke:#ff2357,stroke-width:2px
    style CHK stroke:#ff2357,stroke-width:2px
```

`chase::confirmable` has no consumer and `chase::snap` has no issuer,
so they are omitted.

---

## 4. Methodology

The tables above were generated by these greps from repo root:

```sh
# Issuers (all notify and notify_one sites)
grep -rn 'notify\(_one\)\?(' src include | grep 'chases::'

# Direct self-calls that bypass the bus
grep -rn 'handle_chase(.*chases::' src

# Handlers
grep -rn 'case chase::' src include | grep -v '////'

# Subscription sites
grep -rn 'SUBSCRIBE_CHASE\|subscribe_chase' src
```

To recheck after source changes, run the same set and diff against the
tables here. Any new row must come with its source citation, and any
deletion should be cross-referenced with this doc to ensure no downstream
spec assumes the old behaviour.

---

## 5. Specification view

A formal model can treat the bus as follows.

**Processes.** Each chaser and each event-subscribing protocol is a
process `P` with:
- a single inbox typed `(code, event_value)`
- a private state space `Σ_P`
- a deterministic transition `δ_P : Σ_P × (code, event_value) → Σ_P × Output_P`
- where `Output_P` is a finite set of `notify` calls and outbound
  asynchronous actions (e.g. DB writes).

**Bus.** The bus is broadcast-with-filter: every `notify(ec, v)` is
delivered to every subscriber, and each subscriber's `handle_chase`
inspects `to_chase(v)` to decide whether to act. `notify_one` is a
point-to-point exception used only for `split` and `stop`.

**Invariants worth proving.**
1. *Liveness of stop*: after `full_node::do_close`, every process
   eventually reaches a terminal state. (Follows from Bus-2 + the universal
   `case chase::stop: return false;`.)
2. *Disorganize convergence*: every `chase::regressed`/`disorganized` is
   eventually responded to by the consuming chasers' "rewind" branches
   (`chaser_download.cpp:344-360`, `chaser_validate.cpp:179-186`,
   `chaser_confirm.cpp:131-134`) before the next forward event is processed.
3. *No spurious validation*: `chase::valid` is emitted only from
   `chaser_validate::notify_block` (`chaser_validate.cpp:375`), after either
   full validation, bypass processing, or batch verification of the height.
4. *Confirm uniqueness*: `chase::confirmable`, `unconfirmable`,
   `organized`, `reorganized`, `block`, `stale` all have a single issuer
   (`chaser_confirm`). Confirmation is centralized.
5. *Two archivers*: `chase::checked` and `chase::unchecked` have exactly
   two issuers — the download protocol and the compact block fill in
   `chaser_transaction` — and both write the block association before
   emitting (docs 06 §5.6, 11 §3).

**Dormant events (do not model as live).**
- `chase::snap` — handler exists, no issuer.
- `chase::report` — issuer is the executor (external, libbitcoin-server).
- `chase::confirmable` — issued, no handler.

---

## Cross-references

- [`00-overview`](overview) §3 (concurrency model) and §4
  (high-level event table).
- [`02-chaser-header`](header-chaser) — the state machine
  that emits `bump`, `regressed`, `disorganized`, `headers`, `suspend`.
- [`04-chaser-validate`](validation-chaser) — the unique issuer of `valid`
  / `unvalid`.
- [`11-chaser-transaction`](transaction-chaser) — the issuer of
  `transaction` and the second issuer of `checked`/`unchecked`.
