# Store Migration

## 1. Migration

A new release of `bs` may change the schema of the store. `bs` migrates an
existing store to the schema compiled into it, so the store need not be
rebuilt. The oldest store that can be migrated is schema 4.0.30. A store
older than that, or newer than the binary (written by a later build), is
refused with "store schema version mismatch" and is not changed. Such a
store must be recreated.

| From | To | Change |
| ---- | -- | ------ |
| 4.0.30 | 4.0.31 | The transaction pool tables (`pool`, `spends` and `wtxid`, and the pool and spends indexes) are discarded and created empty, sized by the current configuration as for a new store. The pool refills from the network. Headers, transactions, inputs, outputs and indexes are unchanged. |
| 4.0.31 | 4.0.32 | The `require_witness` setting is added to the settings stored at creation, from the current configuration. |
| 4.0.32 | 4.0.33 | Each pruned block, and each of its transactions, is flagged as pruned in place, so queries refuse them by flag ([Querying pruned blocks](setups#querying-pruned-blocks)). The coinbase of a block pruned before this step remains without its script. |
| 4.0.33 | 4.0.34 | The store records the last block applied to the transaction pool; a migrated store records none. |

A store is migrated through each step in turn. Settings stored at
creation still override configured settings, except where a step takes a
configured value, as above. To recreate the pool tables larger, set the
`[table.pool]` and `[table.wtxid]` bucket settings before migrating
([Store Settings](store)).

The snapshot that follows migration takes time in proportion to the size
of the store.

## 2. Before migrating

- **Snapshots are deleted.** Migration deletes all existing snapshots
  before it changes the store, since they hold the old schema. A
  snapshot of the migrated store is taken when migration completes.
- **An interruption is not recoverable.** The store is fault locked while
  it is changed. If migration fails or is interrupted (such as by power
  loss or a killed process), the fault lock remains and `bs` refuses to
  open the store. The store must then be recreated. A failure before the
  store is changed, such as an unsupported schema, leaves it unchanged.
- **The store must have closed cleanly.** Migration is refused if a flush
  lock or fault lock is present.

## 3. Migrating with `--transform`

```
$ bs -t
```

`-t` (`--transform`) migrates the store in the configured directory,
takes a snapshot of the migrated store, and exits. A store already at the
compiled schema is reported as current and not changed:

```
Database schema 4.0.32 is current.
```

## 4. Migrating at startup

Every command that opens the store (a normal run, `--information`,
`--backup` and so on) first checks its schema. When the store can be
migrated, an interactive `bs` prompts:

```
Database schema 4.0.30 must be migrated to compiled schema 4.0.32.
Existing snapshots are deleted and an interruption is not recoverable.
Press <enter> to migrate the store now.
Enter 'c' to stop without changing the store.
```

Enter migrates the store, opens it, takes a snapshot, and continues. `c`
stops without changing the store:

```
Database not migrated, start with --accept or run --transform.
```

With `-a` (`--accept`), `bs` migrates without prompting. A daemon or
service is not interactive, so without `-a` it stops with the same
message and does not migrate.

## 5. Log lines

```
Database schema 4.0.30 is migrating to compiled schema 4.0.32.
Database schema 4.0.30 migrated to compiled schema 4.0.32 in {n} secs.
Snapshot is started.
Snapshot complete in {n} secs.
```

A failure is logged with its error, and leaves the store fault locked:

```
Database schema 4.0.30 failed to migrate with error '{message}'.
```
