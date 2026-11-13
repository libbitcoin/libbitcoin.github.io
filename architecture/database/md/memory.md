# 05 — Memory

> Companion to [`04-storage`](storage).
>
> [`04-storage`](storage) treats a storage as a file with a chain of
> sizes, a remap lock and a lifecycle. This page is the level below it:
> how each map holds its file in memory on each platform, how pages
> become resident and are released, and how the maps respond to the
> memory of the machine. Citations here are to libbitcoin-database
> commit `cc149c1d` (2026-11-13).

---

## 1. Two backends

A storage is an `mmap<Widths...>` over one of two backends, selected at
compile time (`memory/mstage.hpp:24-29`):

| Backend | Platforms | Model |
| ------- | --------- | ----- |
| native | Windows | The file is mapped shared, and the operating system pages it between memory and disk (`impl/memory/mmap_native.ipp`). |
| staging | Linux, macOS, BSD | The map is built from anonymous memory and file mappings that `bs` manages itself (`impl/memory/mmap_staging.ipp`, `mmap_body.ipp`, `mmap_head.ipp`). |

Windows mapped-file behavior is the model that staging emulates
(`memory/mstage.hpp:24-29`). On Windows a written page is the file's
page, and the system writes it back and drops it as memory requires.
The staging backend keeps written rows in anonymous memory, writes them
to the file itself, and maps the file where rows no longer change.

Each map runs one worker thread, which wakes once a second
(`impl/memory/mmap_private.ipp:333-392`). The worker performs the
background work of its kind of map: settling and eviction for bodies,
write-back and touch passes for heads, and cache release.

## 2. Bodies and heads

The two kinds of storage ([`02-primitives`](primitives)) are mapped
differently, because they are written differently:

| Storage | Written | POSIX mode | Windows |
| ------- | ------- | ---------- | ------- |
| Every body | Appended, then never changed | staged | native |
| The strong and envelope heads | Appended in link order | shared | native |
| Every other head | Updated in place, at random | managed | native |

The modes are chosen by the store when it constructs each table
(`store.hpp:328-369`, `impl/store/store.ipp:29-138`). A head appended in
link order goes cold behind its top, so it maps its file directly, and
its pages can be dropped like a body's (`store.hpp:367-369`).

## 3. Address space

A POSIX map reserves address space, four times its capacity, as an
inaccessible anonymous mapping, and commits pages within the reservation
as the map grows (`impl/memory/mmap_staging.ipp:179-228`,
`src/memory/mstage.cpp:46-50`). Growth within the reservation does not
move the map. When the reservation is exhausted, a larger one is
reserved, the unsettled rows are copied into it, and the old one is
released (`impl/memory/mmap_staging.ipp:275-447`). There is no
`mremap`.

A commitment is admitted only if memory remains for it. Linux and BSD
probe for `headroom` bytes beyond the commitment; macOS computes free
and inactive memory, swap slack and free space on the swap volume
(`src/memory/mstage.cpp:59-120`).

Windows grows a map by unmapping it and mapping the larger file
(`src/memory/mman.cpp:143-152`).

On both, the file is extended before the map, by `fallocate` on Linux,
`F_PREALLOCATE` on macOS, `posix_fallocate` on BSD and `SetEndOfFile`
on Windows (`impl/memory/mmap_private.ipp:276-326`,
`src/memory/mman.cpp:272-426`), after a check that the volume has the
extension plus `headroom` free (`impl/memory/mmap_private.ipp:254-273`).
A refused extension is the disk-full condition of
[`04 §4`](storage). At close every file is truncated to its logical size.

## 4. Staged bodies

A staged body has two parts, divided at the settled size
([`04 §1`](storage)):

```
0                   settled                      logical
| file mapping      | anonymous memory           |
| read only, clean  | written rows, not yet in   |
| droppable         | the file                   |
```

- **Writing.** Rows are written to anonymous memory. Nothing is written
  to the file until the rows settle or the store flushes.
- **Settling.** The worker writes the oldest unsettled rows to the file
  with `pwrite`, then replaces that part of the map with a read-only
  mapping of the file (`impl/memory/mmap_body.ipp:83-121, 301-339`). A
  settled page is a clean file page, which the system can drop and read
  back without writing it. On a machine with 32 GiB or less, settled
  pages are also marked cold, so the system reclaims them first
  (`memory/mmap.hpp:258-264`).
- **Pace.** Settling drains continuously while the system reports memory
  pressure or the unsettled backlog exceeds a quarter of memory, and
  otherwise proceeds a chunk at a time
  (`impl/memory/mmap_body.ipp:225-295`).
- **Throttle.** A writer waits while a body's unsettled rows exceed an
  eighth of memory, so writes cannot outrun settling
  (`impl/memory/mmap_body.ipp:188-213`).
- **Eviction.** When free memory falls below an eighth of memory, the
  worker evicts settled pages in sweeps over the recently settled rows:
  `MADV_PAGEOUT` on Linux, `msync` with `MS_INVALIDATE` elsewhere
  (`impl/memory/mmap_body.ipp:346-380`, `src/memory/mstage.cpp:247-267`).
  On Linux eviction stops while the store is caught up (§8)
  (`impl/memory/mmap_body.ipp:261-266`).
- **Loading.** A body is loaded by mapping its settled prefix from the
  file and reading the unsettled remainder back into anonymous memory
  (`impl/memory/mmap_staging.ipp:151-265`).

## 5. Heads

### 5.1 Managed (POSIX)

A managed head is a resident copy of the head file, with a bitmap of
dirty pages (`impl/memory/mmap_head.ipp`).

- **Install.** The head is installed lazily, mapped from the file and
  copied to anonymous memory in 1 MiB segments as writers first touch
  them (`impl/memory/mmap_head.ipp:37-90, 185-252`). A newly created head
  is written to the file with its fill and installed from it, so the
  fill is never resident (`:135-179`).
- **Write-back.** A writer marks the pages it changes. The worker
  writes dirty pages to the file in coalesced runs, and drains the head
  completely after a minute without writes (`:280-353, 372-538`).
- **Residency.** Under low memory the worker revisits every head page
  every four seconds, reading only pages still resident, so the system
  keeps the heads in memory ahead of the bodies (`:425-458`). On macOS
  the head is wired instead, and cold clean segments are returned to the
  file under scarcity while caught up (`src/memory/mstage.cpp:205-229`,
  `impl/memory/mmap_head.ipp:471-650`).
- **Sharing.** While caught up, a drained head may map its file writable,
  as a shared head does, and returns to the managed copy when writes
  resume at a high rate (`:391-401, 755-816`).

### 5.2 Shared (POSIX)

The strong and envelope heads map their files writable
(`impl/store/store.ipp:76, 106`). Written pages are written back by
the system, and by `msync` at flush.

### 5.3 Windows

Every map is a shared view of its file. The worker of each head raises
the process working set floor to three quarters of memory, and under low
memory reads one byte of every head page every four seconds, so the
system keeps the heads in the working set
(`impl/memory/mmap_native.ipp:234-280`, `src/memory/mman.cpp:205-213`).

## 6. Memory tiers

The thresholds above derive from installed memory, read at run time
(`memory/mmap.hpp:249-294`). Page size is also read at run time, and
nothing assumes 4 KiB pages.

| Fraction of memory | Use |
| ------------------ | --- |
| 1/4 | Unsettled backlog that drives settling |
| 1/8 | Free memory below which bodies evict and heads are touched; the writer throttle |
| 1/32 | Backlog at which settling proceeds in steps |
| 1/256, at most 256 MiB | Growth chunk of a staged body |

## 7. Cold block reads

A block read that produces wire-serialized bytes (`get_wire_block`)
first pages in the block (`impl/query/archive/wire_reader.ipp:269,
291-415`). This is the read used by validation and confirmation and by
every service that returns a serialized block. A read that builds a
block object does not page in.

- **Regions.** A block is up to six regions, found from its first and
  last transaction: its tx rows, its input rows and sequences, its
  output rows, and its input and output bytes.
- **Residency check.** The first and last page of each region are
  checked: `mincore` on POSIX, `QueryWorkingSetEx` on Windows
  (`src/memory/utilities.cpp:130-147, 386-404`).
- **Prefetch.** If any region is not resident, all are prefetched:
  `MADV_WILLNEED` on POSIX, in 128 KiB steps on Linux to match the
  kernel's readahead window, and one `PrefetchVirtualMemory` call on
  Windows (`:149-163, 406-429`).

Body files are opened for random access, so a fault on a cold page reads
one page. Without prefetch a cold block is read a page at a time; with
it, the block is read in large requests that queue together at the
device. On Windows the check is for the process working set, so a page
cached by the system but not in the working set is also prefetched,
which maps it without a disk read.

`database.cold_reads` limits how many cold blocks may prefetch at once.
A cold read waits for a slot; a warm read never waits. The default, 0,
is no limit (`impl/store/store.ipp:206-210`).

## 8. Cache release

While the store is caught up, the body workers release cached rows until
neither of two limits is exceeded
(`impl/memory/mmap_private.ipp:408-451`):

| Setting | Exceeded when |
| ------- | ------------- |
| `database.memory_reserve` | Free physical memory is below this many bytes |
| `database.memory_ceiling` | The resident memory of `bs` is above this many bytes |

Release sweeps the rows in chunks, at most one lap per check. Heads are
never released. Each limit is disabled at 0, the default; with both
disabled, no release work is done (on Windows no worker starts for the
bodies at all).

| Platform | Release | Resident memory (ceiling) | A later read of a released row |
| -------- | ------- | ------------------------- | ------------------------------ |
| Windows | `VirtualUnlock`, out of the working set | working set size | A fault, without a disk read while the system caches the page |
| Linux | `MADV_PAGEOUT` of settled rows | `/proc/self/statm` | A disk read |
| macOS | `msync` with `MS_INVALIDATE` | `task_info` resident size | A disk read |
| BSD | as macOS | not measured, so the ceiling never applies | A disk read |

The store is caught up when the candidate and confirmed chains are the
same height and the top header is at most 20 minutes old
(`store.hpp:187`, `impl/store/store.ipp:360-452`). The code calls this
state current, but it is not the node's current, the user-facing state
that gates services: the node tests only the top of one chain, against
`node.currency_window_minutes`, so the node can be current while the
store is not caught up. The store passes each change to every
map. The limits are a control for sharing a machine with other programs,
to keep memory free for them or to bound the footprint of `bs`.

## 9. Durability

| Platform | Flush |
| -------- | ----- |
| POSIX | Staged bodies `pwrite` their unsettled rows, shared heads `msync`, and managed heads write their dirty pages; then `fsync`, or `F_FULLFSYNC` on macOS (`impl/memory/mmap_staging.ipp:40-78`). |
| Windows | `FlushViewOfFile`, then `FlushFileBuffers` (`impl/memory/mmap_native.ipp:39-60`). |

Background settling and write-back do not sync. A flush is the only
point at which a map is durable, and the ordering of flushes across
maps is the store's ([`04 §5`](storage)).

## 10. Settings

| Setting | Default | Effect |
| ------- | ------- | ------ |
| `database.cold_reads` | `0` | Concurrent cold block prefetches, 0 unlimited (§7) |
| `database.memory_reserve` | `0` | Free memory restored by cache release while caught up, 0 disables (§8) |
| `database.memory_ceiling` | `0` | Resident memory of `bs` above which cache is released while caught up, 0 disables (§8) |
| `table.*.size` | per table | Minimum file provision ([`04 §1.1`](storage)) |
| `table.*.rate` | per table | Growth beyond the requirement ([`04 §1.1`](storage)) |

The commitment and disk `headroom` (256 MiB) and the access advice of
each map are fixed by the store (`memory/settings.hpp:34-74`,
`store.hpp:328-361`).

---

## Cross-references

- [`02-primitives`](primitives) — heads and bodies
- [`04-storage`](storage) — sizes, the remap lock, disk full and flush
- [Performance Settings](../../configuration/performance.html) — the
  memory settings
