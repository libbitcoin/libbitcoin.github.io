# Linux

Ubuntu 24.04 is the reference platform. CI builds and tests on it with
GCC 13 through 16 and Clang 18 and 19 (see
[Build systems and toolchains](toolchains)). Other distributions work
with the equivalent packages.

## 1. Prerequisites

```
$ sudo apt install build-essential git autoconf automake libtool pkg-config curl
```

CMake builds also require CMake 3.30 or later. Ubuntu 24.04 ships an
older version, so install a current one from
[cmake.org](https://cmake.org/download/).

## 2. Autotools

```
$ git clone https://github.com/libbitcoin/libbitcoin-server
$ cd libbitcoin-server
$ ./builds/gnu/install-gnu.sh --prefix=$HOME/libbitcoin --build-boost --build-config=release --build-link=static
```

The script downloads Boost 1.86.0 and clones libbitcoin-system,
libbitcoin-database, libbitcoin-network and libbitcoin-node. It then
builds, tests and installs each in order, ending with libbitcoin-server.
The result is `$HOME/libbitcoin/bin/bs`.

The dependencies are cloned into the current directory. Add
`--build-src-dir=<path>` to put them elsewhere, `--build-skip-tests`
to skip the test suites, and `--build-skip-test-run` to build the test
suites without running them.

The default prefix, `/usr/local`, requires `sudo` for the install step.
A prefix in the home directory does not.

## 3. CMake

The CMake script takes the same options:

```
$ ./builds/cmake/install-cmake.sh --prefix=$HOME/libbitcoin --build-boost --build-config=release --build-link=static
```

## 4. CMake presets

A preset selects the configuration and link by name:
`nix-gnu-debug-static`, `nix-gnu-debug-shared`, `nix-gnu-release-static`
or `nix-gnu-release-shared`.

```
$ ./builds/cmake/install-presets.sh --build-preset=nix-gnu-release-static --build-boost
```

The presets script chooses the install location itself, and the result
is `prefix/<preset>/bin/bs` under the source directory.

## 5. Compiler and flags

The scripts use the compilers named by `CC` and `CXX`:

```
$ CC=clang-19 CXX=clang++-19 ./builds/gnu/install-gnu.sh --prefix=$HOME/libbitcoin --build-boost --build-config=release --build-link=static
```

`CFLAGS` and `CXXFLAGS` are kept and passed to every library. This is
how to target a specific CPU, for example a Raspberry Pi 5:

```
$ CFLAGS="-mcpu=cortex-a76+crypto" CXXFLAGS="-mcpu=cortex-a76+crypto" ./builds/gnu/install-gnu.sh --prefix=$HOME/libbitcoin --build-boost --build-config=release --build-link=static
```

See [Build options](options) for the hardware options.
