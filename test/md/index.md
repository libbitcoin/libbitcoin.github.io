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

## 4. Public vectors

Tests establish correctness, using public vectors wherever they exist:
BIPs, RFCs, NIST, Wycheproof, and the consensus vectors shared across
Bitcoin implementations.

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
| Linux (QEMU) | s390x | 64 | big | GCC, cross compiled, tested in QEMU | Autotools |
| macOS | arm64 (Apple silicon) | 64 | little | Apple clang (current Xcode) | Autotools, CMake |
| Windows | x64 | 64 | little | MSVC v145 | Visual Studio |
| Windows | x86 (Win32) | 32 | little | MSVC v145 | Visual Studio |

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
