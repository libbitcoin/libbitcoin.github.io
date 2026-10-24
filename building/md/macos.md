# macOS

macOS builds use the same scripts as Linux, with Apple clang from Xcode.
CI builds and tests with the current Xcode on Apple silicon (see
[Build systems and toolchains](toolchains)).

## 1. Prerequisites

Install the Xcode command line tools, then the build tools from
[Homebrew](https://brew.sh):

```
$ xcode-select --install
$ brew install autoconf automake libtool pkg-config cmake
```

## 2. Build

```
$ git clone https://github.com/libbitcoin/libbitcoin-server
$ cd libbitcoin-server
$ ./builds/gnu/install-gnu.sh --prefix=$HOME/libbitcoin --build-boost --build-config=release --build-link=static
```

The result is `$HOME/libbitcoin/bin/bs`. CMake works the same way with
`./builds/cmake/install-cmake.sh` and the same options. The scripts use
`clang` and `clang++` by default.

The notes in [Linux](linux) about the source directory, skipping tests
and passing compiler flags apply on macOS too.

## 3. Hardware options

On Apple silicon, `--enable-sha`, `--enable-sha3` and `--enable-aes`
enable the ARM crypto instructions, which every M-series CPU has. On
Intel Macs, use the x86 options (see [Build options](options)).

GPU acceleration is not available on macOS.
