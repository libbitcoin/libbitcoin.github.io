# Streamers

Streamers are the typed read and write layer of the
[stream](stream) module. A streamer wraps a stream and reads or writes
Bitcoin's serialized forms: little and big endian integers, variable length
integers, hashes, byte vectors and strings. Every chain type serializes and
deserializes through them. Paths are relative to `include/bitcoin/system/`
in [libbitcoin-system](https://github.com/libbitcoin/libbitcoin-system), at
master `0cd57fcf` (2026-10-27).

## 1. Interfaces

The streamers implement three abstract interfaces
(`stream/streamers/interfaces/`), with short aliases (`stream/streamers.hpp`):

```cpp
using flipper = byteflipper;
using reader = bytereader;
using writer = bytewriter;
```

The chain types take these interfaces, `reader&` to deserialize and
`writer&` to serialize, so a chain type is independent of the streamer and
of the stream beneath it. The same `to_data(writer&)` writes to a
`std::ostream`, to a fast stream over a byte buffer, or into a hash.

| Group | `reader` | `writer` |
| ----- | -------- | -------- |
| Integers | `read_2_bytes_little_endian` to `read_8_bytes_little_endian`, big endian forms, `read_byte`, `peek_byte` | The corresponding `write_*` |
| Variable integers | `read_variable`, `read_size(limit)` | `write_variable` |
| Hashes | `read_mini_hash`, `read_short_hash`, `read_hash`, `read_long_hash`, and shared pointer forms | `write_bytes` |
| Bytes | `read_bytes()` (remaining), `read_bytes(size)`, into a buffer, and shared pointer forms | `write_bytes` |
| Strings | `read_string(limit)`, `read_string_buffer(size)`, `read_line` | `write_string`, `write_string_buffer`, `write_line` |
| Control | `skip_bytes`, `rewind_bytes`, `get_read_position`, `set_position`, `set_limit`, `is_exhausted`, `invalidate` | `flush`, `get_write_position` |
| State | `operator bool` | `operator bool` |

A failed read or write invalidates the streamer, and every later operation
is a no-op that returns a zero or empty value. A deserializer reads its
whole object and tests the streamer once at the end (see
[Stream](stream#3-error-state)).

## 2. Streamer classes

Each streamer is a class template over its stream type
(`stream/streamers/`):

| Streamer | Reads or writes |
| -------- | --------------- |
| `byte_reader`, `byte_writer` | Bytes |
| `byte_flipper` | Bytes, read and write over one `iostream` |
| `bit_reader`, `bit_writer`, `bit_flipper` | Bit fields |
| `hex_reader`, `hex_writer` | Base16 text on the stream, bytes at the interface |
| `sha256_writer` | Bytes into a SHA-256 hash, written to the stream on `flush` |
| `sha256x2_writer` | Bytes into a double SHA-256 (Bitcoin) hash |
| `sha256t_writer<Tag>` | Bytes into a tagged SHA-256 hash |

## 3. Aliases

The combinations of streamer and stream are named by namespace in
`stream/streamers.hpp`, for each direction and form: `read::bytes`,
`read::bits`, `read::base16`, `write::bytes`, `write::bits`,
`write::base16`, and `hash::sha256`, `hash::sha256x2`, `hash::sha256t`.
Within each:

| Alias | Stream |
| ----- | ------ |
| `istream`, `ostream` | A `std::istream` or `std::ostream` |
| `fast` | A fast `system::istream<>` or `system::ostream<>` |
| `copy` | A standard stream over a copy device on a buffer, by `make_streamer` |
| `push`, `text`, `data` | A standard stream that inserts into a container, a `std::string` or a `data_chunk` |

A chain type constructed from bytes wraps them in a fast stream and a fast
reader (`src/chain/transaction.cpp`):

```cpp
transaction::transaction(const data_slice& data, bool witness) NOEXCEPT
  : transaction(stream::in::fast(data), witness)
{
}

transaction::transaction(stream::in::fast&& stream, bool witness) NOEXCEPT
  : transaction(read::bytes::fast(stream), witness)
{
}
```

## 4. Hash writers

A hash writer is a `writer`, so any object that serializes can be hashed by
serializing it into one. The serialization is never materialized: each
write is absorbed into the hash, and `flush` writes the digest to the
underlying stream. A header's hash is computed by serializing the header
into a double SHA-256 writer over a fast stream on the digest
(`src/chain/header.cpp`):

```cpp
hash_digest header::hash() const NOEXCEPT
{
    if (hash_)
        return *hash_;

    hash_digest digest;
    stream::out::fast stream{ digest };
    hash::sha256x2::fast sink{ stream };
    to_data(sink);
    sink.flush();
    return digest;
}
```

Transaction identifiers and signature hashes are computed the same way.
