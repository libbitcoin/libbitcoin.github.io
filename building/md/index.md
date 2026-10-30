# Building bs

`bs` is built from libbitcoin-server and the four libraries it depends on:
libbitcoin-system, libbitcoin-database, libbitcoin-network and
libbitcoin-node. An install script builds and installs all five in
order, along with Boost where needed.

## 1. Choosing a build

| Platform | Build system | Script | Page |
| -------- | ------------ | ------ | ---- |
| Linux | Autotools or CMake | `install-gnu.sh`, `install-cmake.sh`, `install-presets.sh` | [Linux](linux) |
| macOS | Autotools or CMake | `install-gnu.sh`, `install-cmake.sh` | [macOS](macos) |
| Windows | Visual Studio | `build-msvc.cmd` | [Windows](windows) |

The three build systems produce the same `bs`. CMake and autotools are
equivalent on Linux and macOS. CMake presets select a configuration by
name.

## 2. Supported platforms

| | x64 | x86 (32-bit) | arm64 | arm32 | s390x (big-endian) |
| --- | --- | --- | --- | --- | --- |
| **Linux** | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI |
| **macOS** | ✔ CI | Obsolete | ✔ CI | N/A | N/A |
| **Windows** | ✔ CI | ✔ CI | ✔ CI | Obsolete | N/A |

- ✔ CI: built and tested on every change.
- ● Built and tested outside of CI.
- ✔ Expected to build: the toolchain supports it.
- Obsolete: no current toolchain targets it.
- N/A: the platform does not exist on that architecture.

BSD, Cygwin, and MinGW are not supported.

[Platform support](platforms) compares platforms, compilers and build
systems with Bitcoin Core.

## 3. Supported compilers

| Platform | Compilers | Build systems |
| -------- | --------- | ------------- |
| Linux | GCC 13 to 16, Clang 18 and 19 | Autotools, CMake, CMake presets |
| macOS | Apple Clang (Xcode) | Autotools, CMake |
| Windows | MSVC v145 (Visual Studio 2026), Clang (clang-cl, with Visual Studio) | Visual Studio, MSBuild |

## 4. What every build needs

- A C++20 compiler. The versions tested in CI are listed in
  [Build systems and toolchains](toolchains).
- Boost 1.86.0 or later. The Linux and macOS scripts download and install
  it with `--build-boost`. Visual Studio restores it as a NuGet package.
- Git, to fetch the libbitcoin sources.

Nothing else is required (see [Build options](options)).

## 5. Quick start

On Linux or macOS, a static release build installed under
`~/libbitcoin`, optimized for the build machine:

```
$ git clone https://github.com/libbitcoin/libbitcoin-server
$ cd libbitcoin-server
$ ./builds/gnu/install-gnu.sh --prefix=$HOME/libbitcoin --build-boost --build-config=release --build-link=static --hardware-optimized
```

The result is `~/libbitcoin/bin/bs`. On Windows, see [Windows](windows).

## 6. Hardware options

By default `bs` is built for the baseline instruction set of its
architecture (AVX2 by default on Windows, which can be lowered). Options such as `--enable-avx2` or `--enable-shani` make it
faster on CPUs that have those instructions, and unable to run on CPUs
that do not. `--hardware-optimized` enables all that the build machine
supports, so its `bs` runs only on CPUs with the same extensions. Run
`bs --hardware` on the target machine to see what it supports, and see
[Build options](options).

## 7. Pages

- [Linux](linux), [macOS](macos) and [Windows](windows): prerequisites
  and steps for each platform.
- [Build options](options): the install script options and the build
  options shared by all three build systems.
- [Build systems and toolchains](toolchains): autotools, CMake and
  Visual Studio, and the compilers and Boost versions tested in CI.
- [Platform support](platforms): platforms, compilers and build systems
  compared with Bitcoin Core.
- [libbitcoin-build](libbitcoin-build): the generator behind the build
  files, for maintainers.
