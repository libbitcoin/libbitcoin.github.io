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
| `--build-boost` | Download and build Boost 1.86.0. |
| `--build-src-dir=<path>` | Where sources are cloned (default the current directory). |
| `--build-obj-dir=<path>` | Where objects are built (default `obj` in the current directory). |
| `--build-use-local-src` | Use existing source directories instead of cloning. |
| `--build-full-repositories` | Clone full history (default is a shallow clone). |
| `--build-skip-tests` | Do not build or run the tests. |
| `--build-parallel=<n>` | Number of parallel jobs (default the number of CPUs). |
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

All are off by default.

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
| `--enable-sha` | ARMv8 SHA-1 and SHA-256 |
| `--enable-sha3` | ARMv8.2 SHA-3, used for SHA-512 |
| `--enable-aes` | ARMv8 AES and PMULL |

On ARM, a CPU flag in `CFLAGS` and `CXXFLAGS`, such as
`-mcpu=cortex-a76+crypto`, enables the same code as these options (see
[Linux](linux)). On x86, `-march=native` does the same for the build
machine.

### GPU

| Option | Default | Purpose |
| ------ | ------- | ------- |
| `--enable-cuda` | on | NVIDIA GPU batch signature verification |

GPU support needs no CUDA toolkit to build. `bs` loads the NVIDIA driver
when it starts, and uses the CPU when there is no driver or GPU. Disable
it with `--disable-cuda` (`-Denable-cuda=OFF`, `/p:Option-cuda=false`).

## 3. Feature options

| Option | Default | Purpose |
| ------ | ------- | ------- |
| `--with-tests` | on | Build the test suites. |
| `--with-console` | on | Build `bs`. |
| `--with-embedded` | on | Embed the web interfaces in `bs`. |
| `--with-ssl` | on | Build the embedded TLS library, used by secure service endpoints. |
| `--enable-ndebug` | on | Compile assertions out. `--build-config` sets it. |
| `--enable-isystem` | off | Treat Boost headers as system headers, which silences their warnings. |

secp256k1 is part of libbitcoin and needs no option.

## 4. Visual Studio

The same options are `Option-<name>` properties on the project property
pages, or `/p:Option-<name>=true` on the `build-msvc.cmd` or `msbuild`
command line. For example, an AVX-512 build:

```
$ builds\msvc\build-msvc.cmd --build-src-dir .. --build-config StaticRelease --build-use-local-src /p:Option-avx512=true
```

Windows x64 and Win32 builds target AVX2 by default.
