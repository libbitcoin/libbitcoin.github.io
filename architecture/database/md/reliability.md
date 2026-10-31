# 01 — Reliability

> Companion to [`00-overview`](overview) and [`04-storage`](storage).
>
> The store is **fail-stop and recoverable**. Under the assumptions every
> system must make, it either holds exactly what was written or it is
> condemned and returned to a known-good state. It never opens a store
> whose contents it cannot vouch for, and it never repairs one.
>
> Citations are to libbitcoin-database master at `10e63cfe`, relative to
> `include/bitcoin/database/`, and to libbitcoin-server where marked.

---

## 1. Terms

The common phrase "a reliable store" bundles properties that have to be
kept apart.

| Term | Meaning |
| ---- | ------- |
| Reliability | A rate: how often a component fails. |
| Fail-stop | A shape: when a component fails, it stops detectably. It never returns wrong data as good. |
| Fail-partial | The alternative: a failed component may keep running and return wrong or stale data as good. |
| Crash consistency | After a hard shutdown, the store is always in a state its contract allows. |
| Recoverable | A stop is not terminal: the store can be returned to a known-good state. |

A component that halts every week is fail-stop and unreliable. One that
runs for years and then silently serves stale data is reliable and
fail-partial, and it is the second that destroys data, because every
layer above it was built on failures being announced.

---

## 2. Assumptions

Two assumptions underlie every claim on this page. Neither is particular
to libbitcoin. No software can do without them.

- **Fail-stop hardware.** Software runs on its hardware, so it cannot
  certify that hardware. Any check it makes, a checksum, a comparison, a
  re-validation, executes on the same processor and memory and reads the
  same storage it would be checking. Hardware fail-stop is therefore
  assumed, not constructed. Drives, controllers and ECC memory
  approximate it well, because their detection sits outside the part
  that fails.
- **Correct software in normal operation.** A defect that writes wrong
  state through a clean shutdown produces a well-formed store. No
  mechanism inside the store can see it, for the same reason: the check
  would share the defect.

Everything that follows holds under these two assumptions, and only
under them.

### 2.1 Fail-stop hardware is working hardware

"Working hardware" has a precise meaning here: every fault below the
software either does not occur or surfaces as a detectable stop, an error
return or a halt, and never as wrong data returned as good. With correct
software above it, that leaves no path by which an error can enter the
store unannounced. Each failure is either absent (software, by
assumption) or announced (hardware, by assumption).

The assumption covers the whole substrate the software touches, not only
the drive. A fail-stop drive beneath memory without ECC still admits
silent error, because data can change after the drive has delivered it
correctly. ECC memory, interface CRCs and drive-internal ECC each buy
fail-stop behavior for their own segment.

### 2.2 What no layer can add

The fail-stop property cannot be conferred from above.

- **Drive firmware** sits inside the failure domain it would certify.
  Firmware defects are themselves a main source of fail-partial
  behavior: lost writes acknowledged as complete, misdirected writes,
  stale reads.
- **Software checks** (page checksums, scrubbing, re-validation) execute
  on the processor and memory they would be checking. They shrink the
  surface for undetected error, but what remains is exactly what
  fail-stop excludes, wrong data accepted as good. A checksum also
  blesses whatever the code computed, so it cannot see the software's own
  errors either.

So software checks are probabilistic mitigation, not a guarantee. A store
that assumes fail-stop hardware and does not checksum is not omitting a
protection. It declines a permanent cost for a check that cannot deliver
the property it suggests.

### 2.3 Masking

A component that is always correct and never stops would be stronger than
fail-stop. No single device can guarantee it.

- **Masking is finite.** Every masking mechanism is redundancy within a
  bound: an error-correcting code corrects up to its distance, a mirror
  survives one loss. Past the bound, a code used for correction can
  miscorrect, decoding to the wrong value and returning it as good. The
  same redundancy buys either more masking or more detection, and pushing
  a device toward never stopping moves its failures toward fail-partial.
- **No physical object is unconditionally available.** Power loss or
  destruction stops any device. Fail-stop survives even that, since
  destruction is a stop, which makes it the strongest model a single
  device can hold.

Continued correct service through faults requires redundancy across
independent failure domains, and its guarantee is conditional on a fault
budget.

### 2.4 RAID

RAID is that redundancy across drives, and it assumes fail-stop members.
A member that stops is an erasure at a known location, so the array
reconstructs it from the others and keeps serving. A code that corrects
*n* erasures corrects only *n*/2 errors at unknown locations, so the
announcement is worth twice the redundancy.

Normal reads do not check parity, so a fail-partial member's wrong data
passes through. A parity update computed from it writes the error into
the parity, and a later rebuild restores it with confidence. RAID masks
the stops of fail-stop members and does nothing for silent faults.

### 2.5 Running bs on the hardware

`bs` requires fail-stop hardware and nothing more:

- An announced hardware error stops `bs`, either as a storage fault
  (§5) or by ending the process. Either way `flush.lock` remains and the
  store is condemned (§3).
- ECC memory is the part of the substrate most often missing. Without
  it, the assumption of §2 does not hold for memory.
- RAID beneath the store, or a mirrored volume, masks a drive that stops,
  so `bs` keeps running through it. It adds availability, not
  correctness. The store's guarantee is the same with or without it.
- Checksumming filesystems and scrubbing reduce the chance of silent
  hardware error. They are worth having on doubtful hardware, but they
  do not change the guarantee either.

---

## 3. The guarantee: fail-stop by construction

The store does not ask whether its contents after a crash are valid.
That question has no reliable answer. It asks whether the store **closed
cleanly**, which is decidable.

- **Open** creates `flush.lock` and holds it, with an exclusive OS
  process lock, for as long as the store is open
  (`impl/store/store_open.ipp:37-45`).
- **Close** flushes every table, records each body's count in its head,
  and removes `flush.lock` only if no storage faulted
  (`impl/store/store_close.ipp:89-96`). A fault returns
  `error::integrity` and leaves the lock in place.
- **At open, a present `flush.lock` means the store did not close
  cleanly.** It is not opened. Only restore accepts it
  (`impl/store/store_restore.ipp:41-46`), and the server routes startup
  there automatically (`server:console/executor_runner.cpp:128-131`).

The predicate never depends on code that ran during the crash, so it
cannot be wrong about the crash. It deliberately over-approximates: some
condemned stores were in fact intact. That availability cost is what
keeps the guarantee free of exceptions.

The clean-close state itself is sound because the store admits only two
kinds of durable change, each consistent at any instant a fault can
strike:

1. **Atomic directory renames** on one volume: snapshot promotion and
   rotation, all-old or all-new.
2. **Append-only body writes with logical truncation**: content below
   any recorded count never changes once written, so every body state
   that can exist on disk is a valid extension of every recorded count.

Mutable state lives in heads, which are replaced only as a whole
([`04 §6`](storage)). Every deletion that matters is an atomic rename.
Non-atomic deletion touches only directories already defined as garbage.

> **Invariant (Reliability-1).** A store opens only if it closed cleanly,
> and a store that closed cleanly holds exactly what was written.

> **Invariant (Reliability-2).** No snapshot directory that restore could
> prefer is ever modified in place.

---

## 4. Recovery

A condemned store is returned to a state whose correctness rests on
something other than the damaged store:

- **Restore from a snapshot.** The store keeps one snapshot, its heads
  as of a quiescent point. Restore prefers `/primary`, falls back to
  `/secondary` only when a crash interrupted the snapshot that was
  replacing it, and truncates every body to the counts the snapshot
  recorded (`impl/store/store_restore.ipp:60-86`, [`04 §6`](storage)).
  Because bodies are append-only, those counts describe a state that
  existed exactly.
- **Recreate and resync.** With no snapshot, restore recreates the store
  in place and the node rebuilds it from the network
  (`impl/store/store_restore.ipp:79-82`).

Both paths end in a state the store did not have to vouch for. The
snapshot was taken while the store was known good. The network is an
independent source.

> **Invariant (Reliability-3).** Recovery never trusts content of the
> condemned store beyond the counts recorded by a snapshot taken at a
> quiescent point.

### 4.1 Why not repair

Repair is not a choice the design declines. It is not possible, because
nothing can certify a repaired store as correct.

- **The store cannot vouch for itself.** Any check of its contents
  shares fate with those contents.
- **Full validation of the whole chain is not an authority either.** It
  proves that the data satisfies the consensus rules, not that the store
  holds what was written. It runs over the suspect store. Indexes,
  associations and derived state can agree with each other and with the
  rules and still be wrong.
- **The hardware cannot be checked by software running on it** (§2).

A repaired store would be trusted on no grounds at all. Rollback to a
known-good state, or a rebuild from the source, is the only recovery
there is.

---

## 5. Runtime faults

Faults while running are announced, never absorbed.

- **Disk full** is recoverable. The storage records the space it needed,
  the node suspends, and once space is freed a reload resumes service
  without condemning the store ([`04 §4`](storage)).
- **Any other storage fault** implies a code or hardware error, outside
  the assumptions of §2. Corruption of the store itself is excluded by
  construction (§3), so a fault is never ambiguous. It is latched as the first error code and
  cannot be cleared (`impl/memory/mmap.ipp:227-239`). The node stops
  using the store, reports the fault, and close leaves `flush.lock` in
  place. The next start will restore, but restoring before the cause is
  found is not a good idea. The fault means an assumption failed, and
  until the code or hardware is fixed, restore and resync run on the same
  platform with none of the guarantees above.

---

## 6. Compared with Bitcoin Core

Bitcoin Core keeps its chain state in LevelDB. Under the same two
assumptions, it can offer no comparable guarantee.

- **LevelDB is fail-partial, and corrupts on good hardware.** Chrome
  ships LevelDB and SQLite side by side across the same machines, drives
  and power loss. LevelDB corrupts at rates that forced dedicated
  recovery machinery, and SQLite does not. Bitcoin Core's chain state
  corruption after power loss on ordinary machines fits the same
  pattern. The faults follow the software, not the hardware.
- **Its recovery repairs the only copy.** Log recovery stops at the
  first bad record and discards everything after it. `RepairDB` keeps
  what it can parse and drops the rest. `ReplayBlocks` reconciles the
  chain state from the damaged store itself. Each result is then
  trusted, with no authority to check it against.
- **Its integrity checks certify nothing.** The startup `VerifyDB`
  examines the last 6 blocks by default, reading them and their undo
  data from the same suspect store and comparing them with chain state
  from the same process. A pass shows only that the parts agree with
  each other. It certifies neither the rest of the store nor even the
  blocks it examined. A full-depth run over every block has the same
  flaw.
- **Its errors are ambiguous.** A corruption error implies one of three
  causes: bad hardware, bad software, or corruption of the store itself
  (for example by uncontrolled process termination).
  Because LevelDB is not crash consistent, the third is always possible,
  so the error cannot say which occurred. Every recovery available, an
  in-place repair, `-reindex` from the block files on the same disk, or
  even a full resync from the network, assumes the store was the cause.
  None can rule out the other two, so each may resume on the hardware or
  software that caused the error.

| | libbitcoin | Bitcoin Core |
| --- | --- | --- |
| Failure model of the store | fail-stop | fail-partial |
| After a hard shutdown | clean close or condemned, decided without examining contents | examined, repaired, then trusted |
| After a reported error | bad hardware or software, since the store cannot corrupt itself | bad hardware, bad software or store corruption, indistinguishable |
| Recovery | snapshot restore or rebuild | repair, reindex or resync, each assuming store corruption |
| Recovered store rests on | a snapshot taken while known good, or the network | the damaged store's own contents, unless resynchronized |

---

## 7. The network is the redundancy

A single component can be at best fail-stop and recoverable. Keeping
service through faults requires redundancy across independent failure
domains, and redundancy is only sound over members that fail by
stopping, since it must know which member failed.

Bitcoin already provides that redundancy: thousands of independent
nodes, any one of which can stop while the rest serve. The network is
the array and nodes are its members, and like RAID (§2.4) its contract
holds only over members that stop rather than lie. For a node, the
correct design is therefore exactly fail-stop and recoverable. Masking
faults inside the node would duplicate, conditionally and less well,
what the network provides as a whole.

---

## Cross-references

- [`04-storage`](storage) — snapshot, restore, prune, disk full and
  locking in detail
- [`00-overview`](overview) — append-only bodies and publication
