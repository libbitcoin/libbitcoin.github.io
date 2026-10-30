# Test Architecture

How libbitcoin is tested: code built for testability, the kinds of test,
the platforms each change is tested on, and how coverage is measured. The
mechanics of writing a test are in [Test practices](../developers/testing).

## 1. Testability

Code is written to be tested through its own interface. There are no test
hooks: no test-only branches, no conditional compilation for tests, and no
access granted to tests that other callers do not have. Mocks and fakes
are injected to alter and detect behavior:

- **Mocks.** A test derives a mock from the class under test, or from one
  it depends on, and overrides what it alters or detects
  (`mock_channel_peer`, `mock_proxy`, `mock_settings`).
- **Fakes.** A test substitutes a working implementation of a dependency,
  such as the in-memory `chunk_storage` fake for the store's memory-mapped
  files.
- **Settings.** Behavior that depends on configuration is driven by the
  settings object the code already takes.

## 2. Kinds of test

| Kind | Scope | Suite |
|---|---|---|
| unit | A method or function, isolated to the extent practical. | Boost, in each repository's `test/` |
| component | A group of units, such as a class. | Boost, in each repository's `test/` |
| functional | A feature group, such as client-server communication. | Boost, in each repository's `test/` |
| performance | The speed of a unit or component. | Boost, in each repository's `test/`, disabled by default |
| acceptance | Each server interface, as a client uses it. | Python, in libbitcoin-server's `endpoints/`, against a live node |

The Boost suites run in every CI job, except the performance tests, which
are compiled only when `HAVE_PERFORMANCE_TESTS` is defined. The acceptance
suite is customer acceptance: it exercises each interface of a running `bs`
as its clients do, over its own protocols.

## 3. One thing, named

A test case tests one thing, and its name states that thing: the method,
the condition and the expected result. A failing test is then a diagnosis.

## 4. Reference vectors

Tests establish correctness, using reference vectors wherever they exist.

| Source | Vectors | Repositories |
|---|---|---|
| BIP-21 | URI scheme | explorer |
| BIP-32 | HD wallets, test vectors 1, 2 and 5 | system, explorer |
| BIP-38 | Encrypted private keys | system, explorer |
| BIP-39 | Mnemonics (trezor python-mnemonic, bip32JP Japanese) | system |
| BIP-143 | Segwit v0 signature hash | system |
| BIP-158 | Compact block filters | system |
| BIP-173 | Bech32 addresses, valid and invalid | system |
| BIP-174, BIP-370 | PSBT, PSBT v2 | system, server |
| BIP-324 | ElligatorSwift, v2 transport packet encoding | system, network |
| BIP-340 | Schnorr signatures | system |
| BIP-341 | Taproot signature hash and wallet vectors | system |
| BIP-352 | Silent payments, send and receive | system, database, node, server |
| BIP-380, BIP-386 | Descriptor checksums, `tr()` descriptors | system, server |
| RFC 2202, RFC 4231 | HMAC-SHA1, HMAC-SHA256 and HMAC-SHA512 | system |
| RFC 4648 | Base16, base32 and base64 encodings | system, explorer |
| RFC 5869 | HKDF | system |
| RFC 6070, RFC 7914 | PBKDF2 and scrypt | system |
| RFC 6979 | Deterministic ECDSA (P-256) | system |
| RFC 7617 | HTTP basic authentication | network |
| RFC 7748 | X25519 | system, network, server |
| RFC 8439 | ChaCha20, Poly1305 and their AEAD | system |
| RFC 8448 | TLS 1.3 handshake traces | network |
| FIPS 180-4, CAVP | SHA-1 and SHA-2, including SHA-512/224 and SHA-512/256 | system, explorer |
| FIPS 197, SP 800-38A | AES and its modes | system |
| FIPS 202 | SHA-3 | system |
| Wycheproof | secp256k1 ECDSA, P-256 and P-384 ECDSA and ECDH, AES-GCM | system |
| SLIP-39 | Shamir mnemonics (trezor python-shamir-mnemonic) | system |
| Unicode | `NormalizationTest.txt` | system |
| RIPEMD | RIPEMD-128 and RIPEMD-160 reference vectors | system |
| eSTREAM, NaCl | Salsa20, XSalsa20-Poly1305 | system |
| Bitcoin Core | Script tests, valid and invalid, by fork | system |
| Bitcoin Core | `key_io_valid.json`, `blockfilters.json`, MuHash, descriptors | system, network, server |
| Electrum | Electrum mnemonics, v1 and current | system |
| ElectrumX | Merkle proofs with `cp_height`, block headers | database, server |
| Bitcoin Wiki | P2P message samples, wallet import format | network, explorer |

## 5. Continuous integration

Every change is built and tested by CI (GitHub Actions) before review.
Each library repository runs the same matrix. The gate runs on push and
pull request, and the expanded matrix, run on demand, covers every
compiler in all combinations of debug or release and static or shared (see
[Continuous integration](../build/index#6-continuous-integration) and
[Compilers tested in CI](../building/toolchains#3-compilers-tested-in-ci)).

Each CI job runs the same install script published for end-user builds
(see [Building](../building/index)), so CI verifies the build scripts as
well as the build. All build artifacts, for every build system and
including the install scripts, are generated from templates and
configurable metadata (see [Build architecture](../build/index)).

| Platform | Architecture | Word | Byte order | Compilers | Build systems |
|---|---|---|---|---|---|
| Linux (Ubuntu 24.04) | x64 | 64 | little | GCC 13 to 16, Clang 18 and 19 | Autotools, CMake, presets |
| Linux (Ubuntu 24.04) | x86 (32-bit) | 32 | little | GCC | Autotools |
| Linux (Ubuntu 24.04) | arm64 | 64 | little | GCC | Autotools |
| Linux (Ubuntu 24.04) | arm32 | 32 | little | GCC | Autotools |
| Linux (Ubuntu 24.04) | s390x | 64 | big | GCC, cross compiled, tested in QEMU | Autotools |
| macOS | arm64 (Apple silicon) | 64 | little | Apple clang (current Xcode) | Autotools, CMake |
| macOS | x64 (Intel) | 64 | little | Apple clang (current Xcode) | Autotools, CMake |
| Windows | x64 | 64 | little | MSVC v145, Clang (clang-cl) | Visual Studio |
| Windows | x86 (Win32) | 32 | little | MSVC v145 | Visual Studio |
| Windows | arm64 | 64 | little | MSVC v145 | Visual Studio |

## 6. Build status

The current master of each repository:

| Repository | CI | Coverage |
|---|---|---|
| [libbitcoin-system](https://github.com/libbitcoin/libbitcoin-system) | [![CI](https://github.com/libbitcoin/libbitcoin-system/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-system/actions/workflows/ci.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-system/master)](https://coveralls.io/github/libbitcoin/libbitcoin-system?branch=master) |
| [libbitcoin-database](https://github.com/libbitcoin/libbitcoin-database) | [![CI](https://github.com/libbitcoin/libbitcoin-database/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-database/actions/workflows/ci.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-database/master)](https://coveralls.io/github/libbitcoin/libbitcoin-database?branch=master) |
| [libbitcoin-network](https://github.com/libbitcoin/libbitcoin-network) | [![CI](https://github.com/libbitcoin/libbitcoin-network/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-network/actions/workflows/ci.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-network/master)](https://coveralls.io/github/libbitcoin/libbitcoin-network?branch=master) |
| [libbitcoin-node](https://github.com/libbitcoin/libbitcoin-node) | [![CI](https://github.com/libbitcoin/libbitcoin-node/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-node/actions/workflows/ci.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-node/master)](https://coveralls.io/github/libbitcoin/libbitcoin-node?branch=master) |
| [libbitcoin-server](https://github.com/libbitcoin/libbitcoin-server) | [![CI](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-server/actions/workflows/ci.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-server/master)](https://coveralls.io/github/libbitcoin/libbitcoin-server?branch=master) |
| [libbitcoin-explorer](https://github.com/libbitcoin/libbitcoin-explorer) | [![CI](https://github.com/libbitcoin/libbitcoin-explorer/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-explorer/actions/workflows/ci.yml) | [![Coverage](https://img.shields.io/coveralls/github/libbitcoin/libbitcoin-explorer/master)](https://coveralls.io/github/libbitcoin/libbitcoin-explorer?branch=master) |
| [libbitcoin-build](https://github.com/libbitcoin/libbitcoin-build) | [![CI](https://github.com/libbitcoin/libbitcoin-build/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/libbitcoin/libbitcoin-build/actions/workflows/ci.yml) | |

## 7. Coverage

**Line coverage.** A GCC debug job in each repository's CI (GitHub
Actions) is built with `--coverage`, and its lcov output is reported to
[Coveralls](https://coveralls.io/github/libbitcoin/libbitcoin-system),
excluding the paths listed in the repository's `coverage` element of the
build model.

**Constant time.** A libbitcoin-system job in the expanded matrix runs the
secp256k1 constant-time tests under [valgrind](https://valgrind.org/), which reports any branch or
memory access that depends on secret data.

**Fuzzing.** libbitcoin-system is a module of
[bitcoinfuzz](https://github.com/bitcoinfuzz/bitcoinfuzz), a differential
fuzzer that runs the same inputs through several Bitcoin implementations
and reports where their results differ.

**Mutation testing.** Coverage shows which code ran, not whether a test
would fail if it were wrong. Mutation testing changes the code and checks
that a test fails. libbitcoin-system is tested on
[MutantHub](https://mutanthub.space/projects/libbitcoin/libbitcoin-system).
