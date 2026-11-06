# Toolchains

## 1. Build systems

| Build system | Files | Platforms | Install script |
| ------------ | ----- | --------- | -------------- |
| Autotools | `builds/gnu` | Linux, macOS | `install-gnu.sh` |
| CMake | `builds/cmake` | Linux, macOS | `install-cmake.sh`, `install-presets.sh` |
| Visual Studio | `builds/msvc/vs2026` | Windows | `build-msvc.cmd` |

All three build the same targets: the library, its tests and `bs`. They
are generated from one description by [libbitcoin-build](libbitcoin-build),
so their options and sources match.

### Autotools

Requires autoconf, automake, libtool and pkg-config. Each library
installs a pkg-config file, and the next library finds it through
`pkg-config`, including the compiler flags for the hardware options it
was built with.

### CMake

Requires CMake 3.30 or later. The presets are:

| Preset | Configuration | Link |
| ------ | ------------- | ---- |
| `nix-gnu-debug-static` | Debug | Static |
| `nix-gnu-debug-shared` | Debug | Shared |
| `nix-gnu-release-static` | Release | Static |
| `nix-gnu-release-shared` | Release | Shared |

### Visual Studio

Requires Visual Studio 2026 (MSVC toolset v145). The solution exposes the
`StaticDebug` and `StaticRelease` configurations for x64, Win32 and
ARM64. There are no package dependencies.

### MinGW-w64

Windows x64 binaries can also be built on Linux with MinGW-w64 and
autotools. `install-gnu.sh` cross-compiles when `CC` and `CXX` name the
MinGW compilers and `--host=x86_64-w64-mingw32` is given. With GCC:

```
$ CC=x86_64-w64-mingw32-gcc-posix CXX=x86_64-w64-mingw32-g++-posix ./builds/gnu/install-gnu.sh --prefix=$HOME/mingw --build-config=release --build-link=static --host=x86_64-w64-mingw32
```

With Clang (llvm-mingw):

```
$ CC=x86_64-w64-mingw32-clang CXX=x86_64-w64-mingw32-clang++ ./builds/gnu/install-gnu.sh --prefix=$HOME/mingw --build-config=release --build-link=static --host=x86_64-w64-mingw32
```

The tests are built for Windows, so they run on Windows, not on the build
machine.

## 2. Language

All libraries are C++20, with no compiler extensions.

## 3. Compilers tested in CI

Every change is built and tested on a subset of these. The expanded
matrix, run on demand, builds every compiler below in all four
combinations of debug or release and static or shared, with each of its
build systems.

| Compiler | Version | Platform | Build systems |
| -------- | ------- | -------- | ------------- |
| GCC | 13 | Ubuntu 24.04 x64 | Autotools, CMake, presets |
| GCC | 14 | Ubuntu 24.04 x64 | Autotools, CMake, presets |
| GCC | 15 | Ubuntu 24.04 x64 | Autotools, CMake, presets |
| GCC | 16 | Ubuntu 24.04 x64 | Autotools, CMake, presets |
| Clang | 18 | Ubuntu 24.04 x64 | Autotools, CMake, presets |
| Clang | 19 | Ubuntu 24.04 x64 | Autotools, CMake, presets |
| Apple clang | current Xcode | macOS, Apple silicon | Autotools, CMake |
| MSVC | v145 (Visual Studio 2026) | Windows x64 | Visual Studio |
| Clang (clang-cl) | Included with Visual Studio 2026 | Windows x64 | Visual Studio |
| MinGW-w64 GCC | 13 | Ubuntu 26.04 x64, for Windows x64 | Autotools |
| MinGW-w64 Clang | 13 | Ubuntu 26.04 x64, for Windows x64 | Autotools |

GCC 15 and 16 come from the Ubuntu toolchain PPA. The macOS and Windows
runners use the current GitHub images, so their exact compiler versions
follow those images.

## 4. Release builds

Release binaries are built with CMake on Linux and macOS and with Visual
Studio on Windows, statically linked to libbitcoin, in
variants for each set of hardware options, for example:

| Platform | Compiler | Variants |
| -------- | -------- | -------- |
| Linux x64 (glibc) | Clang 18 | AVX2, with SHA-NI, AVX-IFMA and AVX-512 combinations |
| Linux x64 (musl) | Alpine GCC | The same, fully static |
| Linux ARM64 | GCC 14 | Baseline, SHA-2, SHA-3 |
| macOS ARM64 | Apple clang | SHA-2, SHA-3, AES |
| macOS x64 | Apple clang | AVX2, SSE4.1, AES-NI |
| Windows x64 | MSVC v145 | AVX2, with SHA-NI, AVX-IFMA and AVX-512 combinations |
| Windows ARM64 | MSVC v145 | Baseline, SHA-2, SHA-3 |

On Linux glibc builds, the C library remains dynamic. The musl builds
have no dynamic dependencies.

## 5. Deterministic builds

| Toolchain | Builds | Reference |
| --------- | ------ | --------- |
| Guix | The release builds, in a Guix environment | [Build Status](status#2-releases) |
| Double Build | A release build, built twice on separate runners and compared by hash | [Deterministic builds](../architecture/build/deterministic) |

## 6. CUDA

No CUDA toolchain is required. The GPU verification kernels are part of
the source, as compressed PTX (`src/crypto/secp256k1/cuda/ptx.cpp` in
libbitcoin-system). At run time `bs` loads the NVIDIA driver library
(`nvcuda.dll` on Windows, `libcuda.so.1` on Linux), which compiles the
PTX for the installed GPU. `--with-cuda` is on by default, and applies
on x64 and arm64, except on macOS.
