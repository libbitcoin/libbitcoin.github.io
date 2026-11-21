# Store Settings

## 1. Store table sizing (`[table.*]`)

The `[table.*]` settings are advanced and generally do not need to be
changed. Each table has some of these settings:

| Setting | Purpose |
| ------- | ------- |
| `buckets` | The number of buckets in the table head. For a searched (hashmap) table, more buckets mean shorter searches and a larger head. `0` disables an optional table. |
| `expected` | The expected entry count of a hashmap table, from which its bucket count is derived ([Bucket autotuning](#2-bucket-autotuning)). |
| `size` | The minimum allocation of the table body, in bytes. |
| `rate` | The percentage by which the table body grows when it fills. |

The defaults depend on the network. Mainnet's are sized for 950,000
blocks, and a test chain's are much smaller (`bs -n regtest -s` shows
them). A body grows as needed, so `size` and `rate` only shape its
allocation and can be changed at any time. The bucket counts of the
hashmap tables are fixed when the store is created
([Settings fixed at store creation](#3-settings-fixed-at-store-creation)).

The common changes are:

- disabling the address index ([Disable the address index](setups#13-disable-the-address-index));
- enabling client filters ([Client filters (BIP157/158)](setups#12-client-filters-bip157158));
- sizing for a test chain, as on the [Testnet3](testnet3),
  [Testnet4](testnet4), [Testnet5](testnet5), [Signet](signet) and [Regtest](regtest) pages.

`bs -k` and `bs -l` report bucket fill and collisions on an existing
store.

## 2. Bucket autotuning

The hashmap tables (`header`, `tx`, `ins`, `outs`, `pool` and `wtxid`)
derive their bucket count from their `expected` entry count and the
installed memory, unless `buckets` is configured. The ratio of entries to
buckets is the load factor. More buckets shorten searches but enlarge
the table heads, which must generally be held in memory during initial
sync.

| Installed memory | Load factor | Address index (`outs`) |
| ---------------- | ----------- | ---------------------- |
| 8 GB or less | 7.5 | 50 |
| 32 GB or more | 2.5 | 5 |

Between 8 and 32 GB the load factor falls in proportion to the memory.
So a store created on a smaller machine uses less memory for its heads,
and one created on a larger machine searches faster. The `strong` table
has one bucket per expected transaction (`table.tx.expected`), whatever
the memory. A configured `buckets` value replaces the derived count, and
`0` disables an optional table. `bs -s` shows the counts derived on the
machine it runs on.

## 3. Settings fixed at store creation

Some settings are captured in the store when it is created, in its
envelope, and govern that store from then on. The general rules are that
hashmap bucket counts cannot be changed (would require table rewrites),
optional indexation cannot be altered (would result in hidden gaps), and
consensus rules cannot be modified (would result in an inconsistent
chain).

Each time `bs` opens an existing store (or restores one), it compares the
captured values with the configuration. Where a setting differs, the
store's value is used for that run, and the configured value is ignored.
The configuration file is not changed. Each overridden setting is logged
by name:

```
Database envelope [milestone] overrides configuration.
```

The captured settings are:

| Section | Settings |
| ------- | -------- |
| `[bitcoin]` | `network`, the chain parameters, soft fork activations, the milestone, the top checkpoint and `signet_challenge` |
| `[forks]` | all |
| `[database]` | `interval_depth` |
| `[table.*]` | `buckets` of `header`, `tx`, `ins`, `outs`, `duplicate`, `pool` and `wtxid` |
| `[node]` | `limited_blocks`, `provide_filters`, `require_witness` and `silent_start_height` |

The values captured are those in effect when the store is created, not
only those in the configuration file:

- **Network defaults.** Any of these settings that is not configured
  takes the selected network's default, and that default is captured.
- **Derived bucket counts.** A bucket count that is not configured is
  derived from the table's `expected` count and the installed memory
  ([Bucket autotuning](#2-bucket-autotuning)), and the derived count is captured. So
  the same configuration creates different stores on machines with
  different memory, and a store moved to another machine keeps its
  counts.

A different top checkpoint is logged but not replaced. To change any of
these settings, create a new store. The setups that depend on them, from
milestone sync and pruning to client filters and disabling the address
index, take effect only on a new store.

The optional indexes are decided at creation:

| Index | Indexed when the store is created with |
| ----- | -------------------------------------- |
| Client filters | `node.provide_filters = true` |
| Silent payments | `node.silent_start_height` below its default |
| Address | `table.outs.buckets` above 0 (the default) |

The tables of an index not enabled at creation are created empty. A
store created with client filters can stop serving them, with
`provide_filters = false`, which only drops the service bit. On a store
created without them, `provide_filters = true` stops `bs` at startup with
`client filters are not indexed by the store`.

The store's values are applied before the configuration is checked, so
checks such as `client filters require unpruned blocks` test the store's
values, and `bs -s` shows them for an existing store.

## 4. Schema migration

A store records the schema of the `bs` that created it. A store of the
compiled schema opens as is. A store of an older schema is migrated to the
compiled schema, as described on [Store Migration](migration).

## 5. Fault lock

A fault of the node, such as a failure to write the store, fault locks
the store. The node does not resume, and on the next start `bs` refuses to
open the store, as does `--restore`:

```
The application (or underlying operating system or hardware) produced an unrecoverable error prior to shutdown. The cause is not knowable to the application.
```

A fault locked store must be recreated.
