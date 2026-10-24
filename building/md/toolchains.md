# Build systems and toolchains

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
ARM64. Dependencies are NuGet packages, restored into `.nuget\packages`
in the source directory.

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

GCC 15 and 16 come from the Ubuntu toolchain PPA. The macOS and Windows
runners use the current GitHub images, so their exact compiler versions
follow those images.

## 4. Boost

| Build system | Boost | Source |
| ------------ | ----- | ------ |
| Autotools, CMake | 1.86.0 (minimum) | Downloaded and built by `--build-boost` |
| Visual Studio | 1.91.0 | NuGet package `libbitcoin-boost` |

libbitcoin uses only Boost's header libraries, so `--build-boost` builds
no Boost binaries.

## 5. Release builds

Release binaries are built with CMake on Linux and macOS and with Visual
Studio on Windows, statically linked to libbitcoin and Boost, in
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
