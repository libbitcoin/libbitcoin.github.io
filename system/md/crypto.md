# Crypto

The cryptography, from AES to secp256k1, is implemented in the library
itself. It follows the design of the
[hash](hash) module: class templates over specifications, written once over
the `f` operators, so that the same source compiles to scalar code or to
vector code over the extensions the build targets.

Paths are relative to `include/bitcoin/system/` in
[libbitcoin-system](https://github.com/libbitcoin/libbitcoin-system), at
master `0cd57fcf` (2026-10-27).

## 1. Algorithms

| Group | Algorithms | Location |
| ----- | ---------- | -------- |
| Ciphers | AES-128 and AES-256 (CTR, CBC decryption), ChaCha20, FSChaCha20 (BIP324), Salsa20 | `crypto/aes/`, `crypto/` |
| Authentication | Poly1305, GHASH | `crypto/poly1305.hpp`, `crypto/aes/ghash.hpp` |
| Authenticated encryption | AES-GCM, ChaCha20-Poly1305, FSChaCha20-Poly1305, XSalsa20-Poly1305 | `crypto/` |
| Elliptic curves | secp256k1 (ECDSA, Schnorr, ElligatorSwift, batch verification, silent payment scanning), secp256r1, secp384r1, X25519 | `crypto/secp256k1/`, `crypto/nist/`, `crypto/x25519.hpp` |
| Signature parsing | DER and lax DER (BIP66) | `crypto/der_parser.hpp` |
| Secret sharing | Shamir over GF(256), RS1024 checksum (SLIP-0039) | `crypto/shamir/` |
| Entropy | `maybe_random` (`std::random_device`) | `crypto/maybe_random.hpp` |

The template families are instantiated by specification
(`crypto/algorithms.hpp`):

```cpp
// FIPS 197 (AES)
using aes128     = aes::algorithm<aes::k128>;
using aes256     = aes::algorithm<aes::k256>;

// SEC 1, RFC 6979 (NIST curves)
using secp256r1  = nist::algorithm<nist::p256>;
using secp384r1  = nist::algorithm<nist::p384>;

// SLIP-0039 (Shamir)
using shamir128  = shamir::algorithm<shamir::k128>;
using shamir256  = shamir::algorithm<shamir::k256>;
```

## 2. Native, vector and constant time

Each cipher has a native path where the build targets the dedicated
instructions, and otherwise a portable path written over the `f` operators
and extended words, as the hash functions are. The selection is at compile
time, by the same `have_*` flags and `if constexpr`
(see [Hash](hash#4-selection-at-compile-time)).

| Algorithm | Native | Portable |
| --------- | ------ | -------- |
| AES | AES-NI, VAES (x86-64), Crypto extension (ARM) | Constant-time bitsliced blocks, vectorized across 64 bit lanes |
| GHASH | PCLMULQDQ (x86-64), PMULL (ARM) | Constant-time carryless multiplication |
| ChaCha20 | | One block per 32 bit lane of an extended word |
| secp256k1 field | | One field element per 64 bit lane of an extended word, with 52 bit fused multiply-add (IFMA) where available |

The AES template takes the same `Native` and `Vector` parameters as the
SHA template (`crypto/aes/algorithm.hpp`):

```cpp
static constexpr auto use_aes = Native && bc::have_aes && bc::have_128;
static constexpr auto use_vaes = use_aes && bc::have_vaes;
static constexpr auto use_128 = Vector && bc::have_128;
static constexpr auto use_256 = Vector && bc::have_256;
static constexpr auto use_512 = Vector && bc::have_512;
```

Secret key operations are constant time: the bitsliced AES, the GHASH
multiplication, signing and key derivation on the NIST curves, and field
and scalar inversion on secp256k1 by fixed exponent.

Constant time is tested only in part. The secp256k1 secret key operations
(key derivation, secret and point tweaks, ECDSA and Schnorr signing, and
ElligatorSwift key creation and exchange) are tested under Valgrind
memcheck (`test/crypto/secp256k1/ctime.cpp`): each secret is marked
undefined, so a branch or memory access that depends on it is reported as
an error. These tests run in one CI build, a GCC debug build with the
`--with-valgrind` option, so they cover neither optimized builds, which
may introduce secret-dependent branches, nor other compilers or platforms.
The other constant time code, including AES, GHASH and the NIST curves, is
constant time by construction but not tested for it.

## 3. secp256k1

`secp256k1::algorithm` (`crypto/secp256k1/algorithm.hpp`) implements the
curve's arithmetic in the library, using the 5x52 field representation of
bitcoin-core/secp256k1. Its field operations are templates over the word
type, integral or extended, so the same arithmetic computes one element or
one element per 64 bit lane:

```cpp
/// secp256k1 arithmetic over integral or extended integral words.
/// Extended words compute one element per 64 bit lane.
```

On it are built ECDSA and BIP340 Schnorr signing and verification,
ElligatorSwift encoding (BIP324), multi-scalar multiplication
(`impl/crypto/secp256k1/algorithm_pippenger.ipp`), and Bernstein-Yang
safegcd inversion. The generator tables used for multiplication by the
generator are `constexpr`, computed by the compiler
(`crypto/secp256k1/tables.hpp`).

The batch types (`crypto/secp256k1/batch/`) verify many ECDSA or Schnorr
signatures at once, and scan for silent payments (BIP352), over the lanes
of the extended words. Script execution feeds them through
[signature capture](machine#8-signature-capture).

## 4. Other curves

`nist::algorithm` implements ECDSA over the short Weierstrass curves with
a = -3, secp256r1 and secp384r1, with deterministic nonces (RFC 6979), for
the X.509 certificate support (`x509/`). X25519 implements the
Diffie-Hellman function over Curve25519 (RFC 7748).

## 5. Entropy

`maybe_random` draws on `std::random_device`, which may or may not obtain
its values from the operating system or hardware, and whose values may or
may not be random. The standard permits a deterministic implementation, and
there has been one in wide use: MinGW's seeded a Mersenne Twister with a
fixed value, so every run produced the same sequence. This was observed at
least as early as 2013, and was not fixed until years later
([GCC bug 85494](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=85494)).
Since the quality of the source cannot be known, it is named for what it
is, and
is used only for ephemeral values such as network session keys and
address selection, never for wallet seeds. The [wallet](wallet) takes all
entropy from its caller.

`maybe_random` was formerly `pseudo_random`. Both names state that the
output is not known to be random, but some took `pseudo_random` to mean
truly random, and used it for seeds despite explicit warnings against that. It
has therefore been renamed, and the `bx seed` command that exposed it has
been removed (see
[CVE-2023-39910](https://github.com/libbitcoin/libbitcoin-explorer/wiki/CVE-2023-39910)).
