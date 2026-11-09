# Download BS

<div class="banner"><strong>Version 4 release preview builds are planned for early November 2026.</strong> Until then, build <code>bs</code> from source (see <a href="../start/index.html">Quick Start</a>).</div>

<p class="download"><a href="https://github.com/libbitcoin/libbitcoin-server/releases">Download Bitcoin Server</a></p>

Builds of `bs` are published on the libbitcoin-server
[releases page](https://github.com/libbitcoin/libbitcoin-server/releases),
one for each platform and hardware level, each with a signature. There is
no installer and there are no dependencies, just a single executable file.

## 1. A release

Each release lists the version of each library it was built from, and the
key that signed its builds. Its assets are the builds, each with a
signature file of the same name, ending in `.asc`:

```
bs-linux-x64
bs-linux-x64.asc
bs-linux-x64-shani
bs-linux-x64-shani.asc
...
```

## 2. Selecting a build

A build is named `bs-<platform>-<architecture>`, followed by the
extension level it is built for, if any. Windows builds end in `.exe`.

| Platform | Runs on |
| -------- | ------- |
| `linux` | Linux (glibc) |
| `macos` | macOS |
| `windows` | Windows |

| Build | Also uses |
| ----- | --------- |
| `x64` | |
| `x64-shani` | SHA extensions |
| `x64-avxifma` | SHA extensions, AVX-IFMA |
| `x64-avx512ifma` | SHA extensions, AVX-512 IFMA |
| `arm64` | |
| `arm64-sha2` | ARMv8 SHA-2, AES |
| `arm64-sha3` | ARMv8 SHA-2, AES, ARMv8.2 SHA-3 |

Linux and Windows have every build above. macOS has one build for each
architecture: `arm64`, which uses ARMv8 SHA-2, SHA-3 and AES, and `x64`,
which uses AES-NI.

A build runs only on a CPU that has every extension it uses, and is
faster for using them. To select one, run the build without an extension
level, which runs on any CPU of its architecture, with `--hardware`:

```
$ bs-linux-x64 --hardware
```

It lists the extensions of the CPU. Use the build whose extensions are
all among them, preferring `avx512ifma` to `avxifma`, and either to
`shani`. For example, a CPU with SHA extensions and AVX-512 IFMA uses
`bs-linux-x64-avx512ifma`. For what each extension does, see
[Hardware options](../building/options#2-hardware-options).

The list ends with CUDA, for batch signature verification on an NVIDIA
GPU:

```
cuda........ platform:1 compiled:1.
cuda ecc.... platform:1 enabled:1.
```

`platform:1` means the NVIDIA driver reports a supported device, and
`compiled:1` that the build includes CUDA, as the Linux and Windows
builds do and the macOS builds do not. The driver is loaded when `bs`
runs, so a build with CUDA also runs without a GPU. The `cuda ecc` line
appears only when a device is present, and shows whether it supports
error correcting memory and whether that is enabled (see
[GPU error correction](../configuration/#gpu-error-correction)).
`bx hardware` prints the same list.

## 3. Verifying a build

Verify a build before running it. A build is verified by its signature,
made with the libbitcoin release key. The signature proves the build is
the one released only if the key is obtained apart from the release:
whoever could replace a build could also replace a key published beside
it.

### 3.1 The release key

Import the key from this page, not from a release:

```
-----BEGIN PGP PUBLIC KEY BLOCK-----

mDMEaekBLRYJKwYBBAHaRw8BAQdAOTBxJVknNMnoYLrlsZ7Cs8R2Nk3ES6Z9uUUU
uhkKrUC0H0xpYmJpdGNvaW4gPG1pZW5rcGhpQGdtYWlsLmNvbT6ItQQTFgoAXRYh
BMQDUCNIi2ZttpwL2fN9153pcb2bBQJp6QEtGxSAAAAAAAQADm1hbnUyLDIuNSsx
LjEyLDIsMQIbAwUJA3TGEwULCQgHAgIiAgYVCgkICwIEFgIDAQIeBwIXgAAKCRDz
fded6XG9mzzsAP9ietyeTpq3wdKNaDM9+KeQ+LSv+bpItphJ+dWJ+F++0QD8DXrM
vmKCsMcp00fa8l79rNFCSlTT9tBwp5Wv29pJRw64OARp6QEtEgorBgEEAZdVAQUB
AQdAMIFjrHMSxEwCkiN7FeUPxC7xk0w1MKuQbTX4YGT6JE0DAQgHiJoEGBYKAEIW
IQTEA1AjSItmbbacC9nzfded6XG9mwUCaekBLRsUgAAAAAAEAA5tYW51MiwyLjUr
MS4xMiwyLDECGwwFCQN0xhMACgkQ833XnelxvZvI8QEAmpEPcK27HA/dQXz2TuVB
hILewCE+IkkegW6iXc1Fx1YA+wQb0HWHA05INf+QEm6rmG4ax7mDnZyCPjVVJENa
DpAL
=vA2l
-----END PGP PUBLIC KEY BLOCK-----
```

Save it as `libbitcoin.asc`, or download [libbitcoin.asc](libbitcoin.asc),
import it, and check its fingerprint:

```
$ gpg --import libbitcoin.asc
$ gpg --fingerprint
```

| Key | Value |
| --- | ----- |
| Fingerprint | `C403 5023 488B 666D B69C 0BD9 F37D D79D E971 BD9B` |
| Type | ed25519, created 2026-04-22, expires 2028-02-22 |

Import the key once, and keep it. Every later release is signed with the
same key, so a build that does not verify against the key already held
is not a libbitcoin release, whatever key its release shows.

This site and the releases are both hosted by the libbitcoin GitHub
organization. For a check independent of it, compare the fingerprint
with one published elsewhere by the project's maintainers.

### 3.2 The signature

Verify the build against its signature:

```
$ gpg --verify bs-linux-x64.asc bs-linux-x64
```

A good build reports `Good signature from "Libbitcoin"`, with the
fingerprint above. Any other result means the file is not the one
released, and should not be run. On Windows, `gpg` is provided by
[Gpg4win](https://www.gpg4win.org).

### 3.3 The hash

The releases page also shows the SHA-256 of each file:

| Platform | Command |
| -------- | ------- |
| Linux | `sha256sum bs-linux-x64` |
| macOS | `shasum -a 256 bs-macos-arm64` |
| Windows | `certutil -hashfile bs-windows-x64.exe SHA256` |

## 4. Running a build

On Linux and macOS, make the build executable, and rename it if
convenient:

```
$ chmod +x bs-linux-x64
$ mv bs-linux-x64 bs
```

On macOS, a downloaded file is quarantined, and is refused until the
quarantine is removed:

```
$ xattr -d com.apple.quarantine bs-macos-arm64
```

Then continue from [Quick Start §2](../start/index#2-sync).
