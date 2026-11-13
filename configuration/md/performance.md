# Performance Settings

The defaults suit most machines. These are the settings that most affect
sync and query speed.

## 1. Processor

| Setting | Default | Purpose |
| ------- | ------- | ------- |
| `network.threads` | `0` | Threads that run the network: peer and client connections. `0` uses one per hardware thread, at most 32. |
| `node.threads` | `0` | Threads that validate blocks. `0` uses one per hardware thread, which is two per core on a processor with hyperthreading (SMT). |
| `node.thread_priority` | `true` | Run validation threads at high priority, ahead of other programs. `false` leaves them at normal priority. |
| `node.memory_priority` | `true` | Keep the process at normal memory priority. `false` lowers it, so the operating system reclaims its memory first. |
| `database.turbo` | `true` | Allow a single client query to use all processors, so large queries return sooner. |

## 2. Signature verification and silent payment indexing

When a sufficient GPU is available, signatures are verified, and silent
payment transactions indexed, in batches on the GPU, which is much faster
than on a CPU. Run
`bs -w` to see whether a GPU is available, and which processor features
apply.

| Setting | Default | Purpose |
| ------- | ------- | ------- |
| `node.use_gpu` | `true` | Use the GPU when one is available, for signature verification, silent payment indexing and silent payment scans. |
| `node.batch_verify` | `1,000,000` | Signatures verified in each GPU batch. `0` disables GPU verification. |
| `node.batch_silent` | `1,000,000` | Silent payment transactions indexed in each GPU batch. `0` disables GPU indexing. |
| `database.gpu_scan_minimum` | `65,536` | Smallest silent payment scan, in transactions, sent to the GPU. Smaller scans run on the CPU, where they return sooner. |

### GPU error correction

A GPU that supports error correcting (ECC) memory but has it off shows
`cuda ecc.... platform:1 enabled:0` in `bs -w`. Turn it on with
`nvidia-smi`, as root on Linux or from an administrator prompt on
Windows:

```
$ sudo nvidia-smi -e 1
```

The change takes effect after a reboot, after which `bs -w` shows
`enabled:1`. `nvidia-smi -q -d ECC` shows the current and pending
modes, `-i <index>` selects one GPU of several, and `-e 0` turns error
correction off. On many cards it also reduces the memory available.
`platform:0` means the device has no error correcting memory, and there
is nothing to enable.

## 3. Network

| Setting | Default | Purpose |
| ------- | ------- | ------- |
| `node.maximum_concurrency` | `50,000` | Blocks downloaded concurrently. Blocks arrive out of order, and this window lets download run ahead of validation. `0` is unlimited. |
| `outbound.connections` | `100` | Outgoing peer connections while syncing. More peers may be required to saturate a high bandwidth network connection. |
| `outbound.current_connections` | `10` | Outgoing peer connections once the chain is current, when fewer are needed. `0` keeps `outbound.connections`. |

## 4. Memory

| Setting | Default | Purpose |
| ------- | ------- | ------- |
| `database.cold_reads` | `0` | Blocks read from disk at once. A block read that is not in memory prefetches the whole block in large reads; this limits how many may prefetch together. `0` is unlimited, which keeps the most requests queued at the disk. |
| `database.memory_reserve` | `0` | Free memory, in bytes, kept for other programs once the store is caught up. While free memory is below it, `bs` releases cached block data. `0` disables. |
| `database.memory_ceiling` | `0` | Resident memory, in bytes, that `bs` stays under once the store is caught up. While above it, `bs` releases cached block data. `0` disables. Not available on BSD. |

The reserve and ceiling act only on block and transaction data (table
bodies), never on the indexes (table heads). They act only while the
store is caught up: every candidate block is confirmed and the top block
is at most 20 minutes old. This is stricter than the node being current
(`node.currency_window_minutes`), which tests only the age of the top
block. A released page is read again from disk when it is next needed
(on Windows, from the system cache while it remains there). They are
controls for sharing a machine with other programs, not a speedup
([Database Memory](../architecture/database/memory.html#8-cache-release)).

## 5. NUMA balancing (multi-socket Linux)

On a Linux machine with more than one NUMA node (usually a machine with
more than one CPU socket), disable the kernel's automatic NUMA balancing
before you run `bs`. Ubuntu and most other distributions turn it on by
default whenever the machine has more than one node.

Check the node count and the current setting (`1` is on, `0` is off):

```
$ lscpu | grep NUMA
$ cat /proc/sys/kernel/numa_balancing
```

Disable it for the whole machine, both now and after reboots:

```
$ echo 'kernel.numa_balancing = 0' | sudo tee /etc/sysctl.d/90-numa-balancing.conf
$ sudo sysctl --system
```

If you can't change the setting for the whole machine, start `bs` with
interleaved memory placement instead:

```
$ numactl --interleave=all bs --config bs.cfg
```

**Why it matters.** With balancing on, the kernel repeatedly unmaps pages
of a running process to sample which NUMA node is reading them, then
moves each page to the node that reads it most. `bs` maps its store into
memory and reads and writes it from many threads running on every
socket. Pages that both nodes use keep getting sampled and moved, and the
kernel's page-migration walks and lock spinning take the CPU time that
validation needs.

**Measured on stratton.** stratton has 2× Xeon E5-2683 v4 (32 cores, 64
threads, 2 NUMA nodes) and 256 GB RAM, running Ubuntu 26.04 with Linux
7.0. Download time is measured from the first block to height 345,000.
Each row is a set of identical runs:

| Configuration | Runs | Download time (s) | Slow runs |
| ------------- | ---- | ----------------- | --------- |
| Balancing on (default) | 8 | 261 to 305 when fast; 443, 494 and more than 1,137 when slow | 3 |
| Balancing on, `numactl --interleave=all` | 8 | 211 to 257 | 0 |
| Balancing off (`kernel.numa_balancing = 0`) | 8 | 235 to 264 | 0 |

With balancing on, about a third of all runs were slow. In the slow
periods, the kernel's page migration took 40 to 59% of `bs` CPU time,
and SHA-256 hashing took only 1 to 5%. In fast periods, migration took 0
to 2%.

Machines with a single NUMA node are not affected.
