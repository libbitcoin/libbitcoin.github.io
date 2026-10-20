# 01 — Primitives (heads, bodies, maps)

> Companion to [`00-overview`](00-overview) and [`02-tables`](02-tables).
>
> Every table in the store is an instance of a small set of templates in
> `include/bitcoin/database/primitives/`. A table is a **head** and a
> **body**, each backed by its own storage (file). The head is the small,
> fixed or slowly growing part that indexes the body; the body holds the
> elements and is append-only. A **map** template pairs one head type with
> one body type and exposes the query interface.
>
> Citations are to libbitcoin-database master at `d29fa3df`, relative to
> `include/bitcoin/database/`.

| Template            | Head          | Body                  | Lookup                     | Store tables |
| ------------------- | ------------- | --------------------- | -------------------------- | ------------ |
| `hashmap`           | `hashhead`    | record or slab        | search by key              | header, tx, duplicate, wtxid |
| `hashmaps`          | `hashhead`    | keyed record + records | search by key, then link  | ins, outs, pool |
| `arraymap`          | `arrayhead`   | record or slab        | index by dense integer     | txs, prevout, filter_bk, filter_tx |
| `arraymaps`         | `arrayhead`   | records               | index, then link           | scan |
| `nomap`             | `nohead`      | record or slab        | link only                  | input, output, spends, scan_prefix, batch banks |
| `nomaps`            | `nohead`      | records               | link only                  | ecdsa, schnorr, silent banks |
| `headmap`           | (is the head) | none                  | index into the head        | candidate, confirmed, strong, state, envelope |

![Head types](figures/heads.png)

---

## 1. Links and keys

### 1.1 `linkage<Size, Bits>`

A link is an unsigned integer of `Size` bytes, of which the low `Bits` are
significant (`primitives/linkage.hpp:32-66`). The all-ones value of `Bits`
is `terminal`, which is both the null link and the mask used to read a link
out of wider bytes. Serialization is non-endian.

A link is a **record ordinal** in a record body (position = link × row
size) and a **byte offset** in a slab body. Because a slab consumes the link
domain by bytes, slab links are wider: input, output, txs, prevout and
filter_tx all use 5-byte links, while most record tables use 3 or 4 bytes.

Several links are deliberately narrower than their bytes so that a flag can
be merged into the spare bit wherever the link is stored
(`tables/schema.hpp:105`, `:135`, `:181`):

| Link     | Bytes / bits | Freed bit carries                                     |
| -------- | ------------ | ----------------------------------------------------- |
| header   | 3 / 23       | the strong index's "positive" flag (`strong.hpp`)     |
| tx       | 4 / 31       | the coinbase flag in prevout and spends records        |
| output   | 5 / 39       | the outs "excluded" flag (op_return or oversize)       |

> **Invariant (Link-1).** `terminal` is never a valid element link. Every
> walk, iterator and head lookup stops on terminal, and a terminal bucket
> is an empty bucket.

### 1.2 Keys

A key is a fixed-width byte array (a hash), a `chain::point`
(hash and index), or a `keys::search<Width>` that stores only `Width`
bytes and verifies a match against the element itself
(`primitives/keys.hpp:30-53`). A zero-width search key stores no key bytes
at all: the outs (address) and wtxid tables find candidates by bucket and
confirm them against the output script or the pool's witness hash.

Bucket selection takes the low eight bytes of the key modulo the bucket
count, which is uniform because the keys are already hashes. A point mixes
its index into the hash with FNV-1a, and a null-index (coinbase) point is
always bucket zero (`impl/primitives/keys.ipp`, `bucket`, `hash`). The
bucket filter draws its entropy (`thumb`) from the key bytes that follow
the bucket bytes, so the two do not overlap.

---

## 2. Heads

### 2.1 `hashhead<Link, Key, CellSize>`

The head file is `[body count][cell 0 .. cell buckets-1]`, every slot one
cell wide (`primitives/hashhead.hpp:171-179`). The bucket count is fixed at
creation and recorded in the store envelope, so a store keeps its geometry
across configuration changes. A new head is filled with ones (all buckets
terminal).

A cell holds the link of the bucket's newest element in its low
`Link::bits`. When `CellSize` is wider than the link, the remaining high
bits are a **bucket filter**: a small bloom filter over the keys pushed into
the bucket (`hashhead.hpp:43-48`).

![Hash head cell](figures/hash-cell.png)

- **Push** computes the new cell (new link, filter OR the key's k bits) and
  installs it with a compare-exchange loop, so the filter can never lag the
  conflict stack. The element's `next` is written from the observed top and
  fenced before the exchange publishes it (`impl/primitives/hashhead.ipp`, `set_cell`, `next_cell`).
  A word-aligned cell is a lock-free atomic; an unaligned cell is guarded
  by a mutex.
- **Search** first tests the key's k bits against the cell. If any is clear
  the key is not in the bucket and no body memory is touched (`screened`).
- **k** is derived from the expected element count and bucket count
  (`optimal_k`), and the envelope's stored value overrides it at open, so a
  store keeps the k it was built with.

Only three tables have spare cell bits, and so a working filter:

![Hash head cells of the store](figures/hash-cells.png)

> **Invariant (Head-Hash-1).** A cell's filter is a superset of the keys
> reachable from its link. A clear filter bit is therefore a proof of
> absence, and a set bit only a possibility.

### 2.2 `arrayhead<Link, Align>`

The same `[body count][bucket ...]` layout, but the bucket index is the key
itself, a dense integer such as a header link (`primitives/arrayhead.hpp:29-111`).
There is no hash and no conflict list. The head expands as keys grow,
through the storage's growth path. Each bucket is read and written
atomically: as an atomic word when the bucket is integral-sized, otherwise
under a head mutex held only for the copy (`impl/primitives/arrayhead.ipp:142-210`).
`Align` pads each bucket to a full word; every store table uses
`align = false`.

### 2.3 `nohead<Link>`

A single cell holding the body count, and nothing else
(`primitives/nohead.hpp:29-82`). The body is reachable only by links that
other tables hold.

### 2.4 `headmap<Link, Cell, Value>`

A head-only table: the head file is an array of cells with no count cell and
no body (`primitives/headmap.hpp:30-195`). The logical file size is the
count, so publishing the size publishes the newest cell. A value is either a
link (masked to terminal) or an opaque integer no wider than the cell. A
cell size of `max_size_t` makes the head a byte-addressed slab (used only by
the envelope).

![Head map](figures/headmap.png)

Because a headmap has no body, its whole content is in the head, and it is
restored with the heads at snapshot (`impl/primitives/headmap.ipp:51-62`).

---

## 3. Bodies

`bodys<Link, Key, Sizes...>` wraps a storage and converts between links and
positions (`primitives/body.hpp:29-120`). Each row is a set of records, one
per size and one file per record, all addressed by the same link. A body of
one record, `body<Link, Key, Size>`, is the special case `bodys` of one
size, and is what most tables use.

- **Records**: position = link × record size, in each record's own file
  (`memory/mmaps.hpp`). Allocation is unified across the record files under
  one lock.
- **Slab** (one record of `Size == max_size_t`): position = link. Elements
  carry no length prefix; each element's own serialization (typically a
  varint count) determines its extent, so an empty element is not
  storable.

Allocation reserves space and advances the logical size before the element
is written; the element becomes reachable only when something publishes its
link (a head push, or a foreign key written in another table).

> **Invariant (Body-1).** Bodies are append-only. The only exceptions are
> wholesale: batch banks are truncated to zero per batch, and prune
> reclaims the prevout, pool, spends, wtxid and batch bodies
> (`impl/store/store_prune.ipp`).

---

## 4. Maps

### 4.1 `hashmap`

A hash head over a body whose elements are `[next][key][value]`
(`primitives/hashmap.hpp:38-275`). Elements in a bucket form a stack
through `next`, newest first.

![Hash map](figures/hashmap.png)

- **Two-phase commit.** `allocate` and `set` write a complete element with
  its `next` unset, and `commit` pushes it onto the bucket. Until the
  commit the element is unreachable by search, so a reader can never see a
  partly written element (`set`, `commit`, `put` = all three).
- **Search.** `first` / `find` screen the cell, then walk the stack
  comparing stored keys (`impl/primitives/hashmap.ipp:519-538`).
- **Duplicates.** Keys are not unique. `it(key)` returns an `iterator` that
  walks the whole conflict stack, skipping keys that do not match
  (`primitives/iterator.hpp`). This is the multimap of the 2021 design.
- **Get by link.** `get(link)` bypasses the head entirely, so a hashmap is
  a key-link bimap: search by key yields the link, and the link is a
  foreign key that other tables store.

Slab hashmaps (variable elements, byte-offset links) are supported by the
template; the store uses record hashmaps throughout and keeps variable data
in no maps and array maps.

![Hash map over a slab](figures/hashmap-slab.png)

> **Invariant (Map-Hash-1).** An element is searchable if and only if its
> commit completed, and once searchable it remains so (heads are never
> popped, only cleared wholesale by prune or restore).

> **Caution.** An iterator holds the body's shared remap lock until it is
> released. Writing to the same table while holding one will deadlock
> against the remap that the write's growth requires
> (`primitives/iterator.hpp:29-41`, `impl/query/query.ipp:50-58`). Reads
> through the iterator use its own accessor (`get(iterator, ...)`).

### 4.2 `arraymap`

An array head over a body: `at(key)` reads the bucket and `get` reads the
element (`primitives/arraymap.hpp:36-125`). `put(key, element)` appends the
element and stores its link into the bucket, expanding the head as needed.
Buckets are mutable, so a key can be repointed while the old element stays
in the body unreachable.

![Array map](figures/arraymap.png)

In the store every array map is keyed by **header link**: txs (block to its
transactions), prevout (block to its spent-output cache), filter_bk and
filter_tx (block to its BIP157 header and BIP158 filter). These replace the
search that the 2021 design needed for Header→Txs: the header link is
already known, so the association is a direct index.

### 4.3 `nomap`

A no head over a body, addressed only by link (`primitives/nomap.hpp:29-148`).
Inputs and outputs are slab no maps: a transaction's inputs and outputs are
found through foreign keys held by ins and outs, never by search.

![No map](figures/nomap.png)

### 4.4 Multi-record forms: `hashmaps`, `arraymaps`, `nomaps`

The three maps are general over record(s); `hashmap`, `arraymap` and
`nomap` are the case of record(1)
(`primitives/hashmaps.hpp:28-317`, `arraymaps.hpp`, `nomaps.hpp`). In a
hashmaps, record zero is keyed and searched; the other records are read by
the same row link. A query that needs one record reads only that record's
file, which keeps hot data dense in memory.

![Records](figures/records.png)

| Table   | Form       | Records (width)                                          |
| ------- | ---------- | -------------------------------------------------------- |
| ins     | hashmaps   | point, keyed (39), sequence (13)                         |
| outs    | hashmaps   | address, keyed (4, or 0 when address indexing is off), puts (5) |
| pool    | hashmaps   | context, keyed (38), id0..id3 (8 each)                   |
| scan    | arraymaps  | identity (4), point (33), outputs (7)                    |
| ecdsa   | nomaps     | identity (6), message (32), key (33), signature (64)     |
| schnorr | nomaps     | identity (3), message (32), key (32), signature (64)     |
| silent  | nomaps     | identity (4), sum (33), hash (32), outputs (7)           |

---

## 5. Notes for the formal model

- Each map is a pair (head, body) of byte arrays plus a logical size. All
  publication is either a single atomic cell store (head) or a size store
  (headmap, body count), so the reachable state is always a prefix-closed
  subset of the written state.
- The hash head is a set of per-bucket stacks with a monotone filter per
  stack. Search is `filter ⊇ keys(stack)` then a linear walk.
- The array head and headmap are total functions from a dense domain to
  links, mutable pointwise; the bodies they reference are append-only.

---

## Cross-references

- [`02-tables`](02-tables) — every store table, with its map type and sizes
- [`03-storage`](03-storage) — the storage under heads and bodies, remap,
  disk full and snapshot
