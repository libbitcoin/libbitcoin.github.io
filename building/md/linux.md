# Linux

Ubuntu 24.04 is the reference platform. CI builds and tests on it with
GCC 13 through 16 and Clang 18 and 19 (see
[Toolchains](toolchains)). Other distributions work
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
$ ./builds/gnu/install-gnu.sh --prefix=$HOME/libbitcoin --build-config=release --build-link=static
```

The script clones libbitcoin-system, libbitcoin-database,
libbitcoin-network and libbitcoin-node. It then builds, tests and installs
each in order, ending with libbitcoin-server.
The result is `$HOME/libbitcoin/bin/bs`.

`bx` is built the same way from libbitcoin-explorer, whose script clones
libbitcoin-system and libbitcoin-network:

```
$ git clone https://github.com/libbitcoin/libbitcoin-explorer
$ cd libbitcoin-explorer
$ ./builds/gnu/install-gnu.sh --prefix=$HOME/libbitcoin --build-config=release --build-link=static
```

The result is `$HOME/libbitcoin/bin/bx`. Every script and option on this
page applies to both.

The dependencies are cloned into the current directory. Add
`--build-src-dir=<path>` to put them elsewhere, `--build-skip-tests`
to skip the test suites, and `--build-skip-test-run` to build the test
suites without running them.

The default prefix, `/usr/local`, requires `sudo` for the install step.
A prefix in the home directory does not.

## 3. CMake

The CMake script takes the same options:

```
$ ./builds/cmake/install-cmake.sh --prefix=$HOME/libbitcoin --build-config=release --build-link=static
```

## 4. CMake presets

A preset selects the configuration and link by name:
`nix-gnu-debug-static`, `nix-gnu-debug-shared`, `nix-gnu-release-static`
or `nix-gnu-release-shared`.

```
$ ./builds/cmake/install-presets.sh --build-preset=nix-gnu-release-static
```

The presets script chooses the install location itself, and the result
is `prefix/<preset>/bin/bs` under the source directory.

## 5. Compiler and flags

The scripts use the compilers named by `CC` and `CXX`:

```
$ CC=clang-19 CXX=clang++-19 ./builds/gnu/install-gnu.sh --prefix=$HOME/libbitcoin --build-config=release --build-link=static
```

`CFLAGS` and `CXXFLAGS` are kept and passed to every library.

Hardware extensions are enabled with the hardware options, for example
the ARM crypto extensions of a Raspberry Pi 5:

```
$ ./builds/gnu/install-gnu.sh --prefix=$HOME/libbitcoin --build-config=release --build-link=static --hardware-sha2 --hardware-aes
```

See [Build options](options) for the hardware options.
