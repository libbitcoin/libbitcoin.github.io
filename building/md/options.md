# Build options

Options are given to the install scripts, which pass them to every
library they build. The autotools form is `--enable-<name>` or
`--with-<name>`, the CMake form is `-D<name>=ON`, and Visual Studio uses
the `Option-<name>` property.

## 1. Install script options

`install-gnu.sh`, `install-cmake.sh` and `install-presets.sh` accept:

| Option | Purpose |
| ------ | ------- |
| `--prefix=<path>` | Install location (default `/usr/local`). Not used by the presets script. |
| `--build-preset=<name>` | CMake preset (presets script only, required). |
| `--build-config=<debug\|release>` | Debug (`-Og -g1`, assertions on) or release (`-O3`, assertions off). |
| `--build-link=<dynamic\|static>` | Build shared or static libraries (default both). |
| `--build-src-dir=<path>` | Where sources are cloned (default the current directory). |
| `--build-obj-dir=<path>` | Where objects are built (default `obj` in the current directory). |
| `--build-use-local-src` | Use existing source directories instead of cloning. |
| `--build-full-repositories` | Clone full history (default is a shallow clone). |
| `--build-skip-tests` | Do not build or run the tests. |
| `--build-skip-test-run` | Build the tests without running them. |
| `--build-parallel=<n>` | Number of parallel jobs (default the number of CPUs). |
| `--build-post-install-clean` | Remove dependency build files after installing. |
| `--hardware-optimized` | Optimize for the build machine's CPU (`-march=native -mtune=native`), with `--build-config`. See [Hardware options](#2-hardware-options). |
| `--noninteractive` | Do not prompt. |
| `--verbose` | Display the commands run. |

Any other option is passed to each library's configure step, which is how
the options below are given.

## 2. Hardware options

Each option compiles code that uses an instruction set extension. A `bs`
built with an option runs only on CPUs that have the extension. Run
`bs --hardware` on the target machine to see which it has, and do not
enable an option it lacks.

All are off by default. `--hardware-optimized` (§1) enables every
extension of the build machine's CPU instead.

> **Portability:** a build with `--hardware-optimized` runs only on CPUs
> that have every instruction set extension of the machine it was built
> on. To build for other machines, omit it, and enable only the
> extensions they all have.

### x86

| Option | Instructions |
| ------ | ------------ |
| `--enable-sse41` | SSE4.1 |
| `--enable-avx2` | AVX2 (implies AES-NI) |
| `--enable-avx512` | AVX-512 (F, BW, VL) (implies AVX2 and AES-NI) |
| `--enable-avxifma` | AVX-IFMA (implies AVX2, SHA extensions and AES-NI) |
| `--enable-avx512ifma` | AVX-512 IFMA (implies AVX-512, AVX2, SHA extensions and AES-NI) |
| `--enable-shani` | SHA extensions (implies AES-NI) |
| `--enable-sha512` | SHA512 extensions (implies AVX2) |
| `--enable-aesni` | AES-NI and PCLMULQDQ |
| `--enable-vaes` | VAES and VPCLMULQDQ (implies AES-NI and AVX2) |

### ARM

| Option | Instructions |
| ------ | ------------ |
| `--hardware-sha2` | ARMv8 SHA-1 and SHA-256 (implies AES) |
| `--hardware-sha3` | ARMv8.2 SHA-3, used for SHA-512 (implies SHA-1/SHA-256 and AES) |
| `--hardware-aes` | ARMv8 AES and PMULL |

The ARM options are install script options. Each option and the options
it implies combine into one target flag, `-march=armv8-a+<extensions>`
(`armv8.2-a` with `--hardware-sha3`), added to `CFLAGS` and `CXXFLAGS`.
For example, `--hardware-sha2` builds with `-march=armv8-a+aes+sha2`, and
`--hardware-sha3` with `-march=armv8.2-a+aes+sha2+sha3`. They cannot be
combined with `--hardware-optimized`.

The configure and CMake options `--enable-sha2`, `--enable-sha3` and
`--enable-aes` add no flags, and imply the same options as their install
script options. Each checks that the compiler flags enable its extension,
and configure fails if they do not. When building without the install
script, give your own `-march` or `-mcpu` in `CFLAGS` and `CXXFLAGS`,
including every implied extension, with the matching `--enable` options.

### GPU

| Option | Default | Purpose |
| ------ | ------- | ------- |
| `--with-cuda` | on | NVIDIA GPU batch signature verification |

GPU support needs no CUDA toolkit to build. `bs` loads the NVIDIA driver
when it starts, and uses the CPU when there is no driver or GPU. Only
the libbitcoin-system scripts accept `--without-cuda` (`-Dwith-cuda=OFF`),
including its `build-msvc.cmd`. The scripts of the other repositories
build libbitcoin-system with GPU support. In Visual Studio,
`/p:Option-cuda=false` disables it in any build.

## 3. Feature options

| Option | Default | Purpose |
| ------ | ------- | ------- |
| `--with-tests` | on | Build the test suites. |
| `--with-console` | on | Build `bs`. |
| `--with-web` | on | Compile the web pages into `bs`. Without it, `bs` serves pages only from a configured path. |
| `--with-self-tests` | off | Compile the built-in store tests into `bs`, which enable its `-g`/`--get` and `-p`/`--put` options and the `[t]est built-in case` console menu entry. |
| `--with-verbose` | off | Compile in verbose logging (`LOGV`), in libbitcoin-network and every library and binary built on it. Debug builds enable it by default. |
| `--with-performance-tests` | off | Compile the libbitcoin-system performance tests. |
| `--with-slow-tests` | off | Compile the slow libbitcoin-system tests: scrypt, PBKDF2, the encrypted key tests, the bloom and sieve filter tests and a 1 GiB SHA vector. |
| `--enable-ndebug` | on | Compile assertions out. `--build-config` sets it. |
| `--enable-isystem` | off | Include the headers of libbitcoin dependencies with `-isystem` in place of `-I`, which silences their warnings. |

## 4. Visual Studio

The instruction set, GPU, `--with-web`, `--with-self-tests`,
`--with-verbose`, `--with-performance-tests`, `--with-slow-tests` and
`--with-secp256k1` options are `Option-<name>` properties on the project
property pages, or `/p:Option-<name>=true` (or `false`) on the
`build-msvc.cmd` or `msbuild` command line. The others have no property:
the tests and `bs` are projects in the solution, and the Release
configurations define `NDEBUG`. For example, an
AVX-512 build:

```
$ builds\msvc\build-msvc.cmd --build-src-dir .. --build-config StaticRelease --build-use-local-src /p:Option-avx512=true
```

Windows x64 and Win32 builds target AVX2 by default, which can be
lowered (see [Windows](windows#4-instruction-set)).

## 5. External libraries

There is no required external dependency, and the Visual Studio
projects use no NuGet package. libbitcoin implements secp256k1 and TLS
itself, although secp256k1 can be replaced by an external library with the
same public interface.

### secp256k1

| Option | Default | Purpose |
| ------ | ------- | ------- |
| `--with-secp256k1` | on | Use libbitcoin's native secp256k1 interface. |

`--without-secp256k1` (`-Dwith-secp256k1=OFF`) compiles out the native
interface and links an installed library with the libsecp256k1 interface
in its place, such as
[bitcoin-core/secp256k1](https://github.com/bitcoin-core/secp256k1) 0.8.0
or later, or UltrafastSecp256k1. Batch verification remains internal.

- **Autotools and CMake.** The library is found through pkg-config or
  CMake. `--build-libsecp256k1` makes the install script build
  bitcoin-core/secp256k1 from source, with its ellswift, recovery and
  schnorrsig modules, along with the other dependencies. It is used only
  with `--without-secp256k1`.
- **Visual Studio.** `/p:Option-secp256k1=false` compiles out the native
  interface, and the library must be added to the link.

## 6. Link-time optimization

No build system enables link-time optimization (LTO), and it is not
recommended with any toolchain. In measurements of the libbitcoin-system
performance tests (November 2026), no form of LTO made secp256k1
signature verification faster, and verification dominates the time `bs`
spends validating blocks. With MSVC, LTO made `bs` substantially slower.

| Compiler | LTO flags | secp256k1 verify time | Other effects |
| -------- | --------- | --------------------- | ------------- |
| MSVC v145 | `/GL` `/LTCG` | +19% | SHA-256 and SHA-512 hashing 10-85x slower (SHA-NI unchanged), ChaCha20-Poly1305 17x slower. `bs.exe` 7% larger, and each `bs.exe` link takes about 3 minutes instead of 1. |
| MSVC v145 | `/GL` `/LTCG` `/Ob3` | -2% | The same result as `/Ob3` without LTO. `bs.exe` 9% larger. |
| Clang 18 | `-flto=thin` | no change | Hashing of small inputs 3-16% faster, SHA-1 of 1 MB 10-12% slower. 13% more code, 11% longer test build. |
| Clang 18 | `-flto` | no change | AES and the secp256r1 and secp384r1 curves 4-7% faster. Test build takes twice as long. |
| GCC 15 | `-flto=auto` | no change | secp256r1 signing and verification, used by TLS, 20% slower. 21% less code. |

Each time is relative to a build by the same compiler without LTO:
`StaticRelease` for MSVC, and a static `-O3` release build for Clang and
GCC. A positive change is slower. MSVC was measured on an AMD
Threadripper PRO 9985WX, and Clang and GCC on an AMD Ryzen 7 7735HS.

### MSVC

The Visual Studio projects define `ReleaseLTCG`, `ReleaseLEXE` and
`DebugLTCG` configurations, but no solution configuration selects them.
With `/GL`, MSVC inlines functions only during the final link. By then
the functions that libbitcoin forces inline have already been expanded
into their callers, and MSVC no longer inlines even functions of one or
two instructions, such as array element access and integer casts, which
compilation without `/GL` inlines. In `bs.exe`, calls to such functions
increase from about 3,000 to about 57,500. Adding `/Ob3` (aggressive
inlining) to an LTO build removes most of these calls. That restores
`StaticRelease` performance but does not improve on it, and `/Ob3`
without LTO performs the same.
