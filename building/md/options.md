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
| `--hardware-optimized` | Optimize for the build machine's CPU (`-march=native -mtune=native`), with `--build-config`. See [Hardware options](#2-hardware-options). |
| `--build-post-install-clean` | Remove dependency build files after installing. |
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
| `--enable-avx2` | AVX2 |
| `--enable-avx512` | AVX-512 (F, BW, VL) |
| `--enable-avxifma` | AVX-IFMA (implies AVX2) |
| `--enable-avx512ifma` | AVX-512 IFMA (implies AVX-512 VL) |
| `--enable-shani` | SHA extensions |
| `--enable-sha512` | SHA512 extensions (implies AVX2) |
| `--enable-aesni` | AES-NI and PCLMULQDQ |
| `--enable-vaes` | VAES and VPCLMULQDQ (implies AES-NI and AVX2) |

### ARM

| Option | Instructions |
| ------ | ------------ |
| `--enable-sha2` | ARMv8 SHA-1 and SHA-256 |
| `--enable-sha3` | ARMv8.2 SHA-3, used for SHA-512 |
| `--enable-aes` | ARMv8 AES and PMULL |

The ARM options combine into one target flag, `-march=armv8-a+<extensions>`
(`armv8.2-a` with `--enable-sha3`). For example, `--enable-sha2
--enable-aes --enable-sha3` builds with `-march=armv8.2-a+sha2+aes+sha3`.
An ARM option cannot be combined with `-march` or `-mcpu` in `CFLAGS` or
`CXXFLAGS`, and the build fails if both are given. Use either the options
or your own `-march` or `-mcpu`. `-mtune` can be used with either.

### GPU

| Option | Default | Purpose |
| ------ | ------- | ------- |
| `--enable-cuda` | on | NVIDIA GPU batch signature verification |

GPU support needs no CUDA toolkit to build. `bs` loads the NVIDIA driver
when it starts, and uses the CPU when there is no driver or GPU. Disable
it with `--disable-cuda` in any build script, including `build-msvc.cmd`
(`-Denable-cuda=OFF`, `/p:Option-cuda=false`).

## 3. Feature options

| Option | Default | Purpose |
| ------ | ------- | ------- |
| `--with-tests` | on | Build the test suites. |
| `--with-console` | on | Build `bs`. |
| `--with-embedded` | on | Embed the web interfaces in `bs`. |
| `--enable-ndebug` | on | Compile assertions out. `--build-config` sets it. |
| `--enable-isystem` | off | Include the headers of libbitcoin dependencies with `-isystem` in place of `-I`, which silences their warnings. |

## 4. Visual Studio

The instruction set, GPU, `--with-embedded` and `--with-secp256k1`
options are `Option-<name>` properties on the project property pages, or
`/p:Option-<name>=true` on the `build-msvc.cmd` or `msbuild` command line.
The others have no property: the tests and `bs` are projects in the
solution, and the Release configurations define `NDEBUG`. For example, an
AVX-512 build:

```
$ builds\msvc\build-msvc.cmd --build-src-dir .. --build-config StaticRelease --build-use-local-src /p:Option-avx512=true
```

Windows x64 and Win32 builds target AVX2 by default, which can be
lowered (see [Windows](windows#4-instruction-set)).

## 5. External libraries

There is no required external dependency. libbitcoin implements
secp256k1 and TLS itself, although secp256k1 can be replaced by an
external library with the same public interface.

### secp256k1

| Option | Default | Purpose |
| ------ | ------- | ------- |
| `--with-secp256k1` | off | Use [bitcoin-core/secp256k1](https://github.com/bitcoin-core/secp256k1) 0.8.0 or later. |

The option replaces the calls made through the libsecp256k1 interface, so
any other implementation of that interface can be linked in its place.
Batch verification remains internal.

- **Autotools and CMake.** `--build-secp256k1` makes the install script
  build it from source, with its ellswift, recovery and schnorrsig
  modules, along with the other dependencies. Otherwise it must be
  installed where the build can find it (`-Dwith-secp256k1=ON` for
  CMake).
- **Visual Studio.** `/p:Option-secp256k1=true` links the
  `secp256k1_vc145` NuGet package.

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
