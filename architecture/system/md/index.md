# System Architecture

libbitcoin-system is the base of the stack. It has no dependency other than
Boost (headers only), and every other library builds on it. It implements
Bitcoin's primitives and rules: its own hash functions and cryptography,
the script machine, the consensus rules of the chain, and the encodings,
serialization and wallet types that applications need. These pages
describe the design of its major modules. Paths are relative to
`include/bitcoin/system/` in
[libbitcoin-system](https://github.com/libbitcoin/libbitcoin-system), at
master `0cd57fcf` (2026-10-27).

## 1. Modules

| Page | Module | Covers |
| ---- | ------ | ------ |
| [Chain](chain) | `chain/` | Validation stages, context and forks, chain state, the compact number, population |
| [Config](config) | `config/` | Text-serializable configuration types |
| [Crypto](crypto) | `crypto/` | Ciphers, authenticated encryption, elliptic curves, secret sharing, entropy |
| [Hash](hash) | `hash/`, `intrinsics/` | Hash functions and constructions; templates over specifications, one code path for scalar and vector, selection at compile time |
| [Machine](machine) | `machine/` | The script machine: the stack language, the variant stack, allocation, dispatch, signature capture |
| [Math](math) | `math/` | `constexpr`, type-constrained integral arithmetic and casts |
| [Radix](radix) | `radix/` | Base encodings |
| [Stream](stream) | `stream/` | Devices and streams, fast streams, error state |
| [Streamers](streamers) | `stream/streamers/` | The reader and writer interfaces, streamers, and hash writers |
| [Unicode](unicode) | `unicode/` | UTF-8 everywhere, conversion, normalization |
| [Wallet](wallet) | `wallet/` | Keys, addresses and mnemonics |
