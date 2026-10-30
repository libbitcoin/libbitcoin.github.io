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
| `--build-boost` | Download and install Boost 1.86.0. Only its headers are used, so its build step compiles nothing. |
| `--build-src-dir=<path>` | Where sources are cloned (default the current directory). |
| `--build-obj-dir=<path>` | Where objects are built (default `obj` in the current directory). |
| `--build-use-local-src` | Use existing source directories instead of cloning. |
| `--build-full-repositories` | Clone full history (default is a shallow clone). |
| `--build-skip-tests` | Do not build or run the tests. |
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
| `--enable-sha` | ARMv8 SHA-1 and SHA-256 |
| `--enable-sha3` | ARMv8.2 SHA-3, used for SHA-512 |
| `--enable-aes` | ARMv8 AES and PMULL |

On ARM, a CPU flag in `CFLAGS` and `CXXFLAGS`, such as
`-mcpu=cortex-a76+crypto`, enables the same code as these options (see
[Linux](linux)).

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

## 4. Visual Studio

The instruction set, GPU, `--with-embedded`, `--with-ssl` and
`--with-secp256k1` options are
`Option-<name>` properties on the project property pages, or
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

The Boost headers are the only required external dependency. libbitcoin implements
secp256k1 and TLS itself, and either can be replaced by an external
library.

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
  `secp256k1_vc145` NuGet package, which is restored with the Boost
  package.

### OpenSSL

The embedded TLS library (`--with-ssl`, on by default) is used only for
TLS, by the secure service endpoints. `--without-ssl`
(`-Dwith-ssl=OFF`, `/p:Option-ssl=false`) omits it, and TLS then
requires an external OpenSSL, which Boost.Asio uses in its place.

The build scripts and project files have no option for OpenSSL, and no
package of it is maintained, so its paths must be added to the build by
hand: OpenSSL's include directory must be on the include path of every
library and executable built, and `libssl` and `libcrypto` must be linked
into every executable.

**Autotools.** Set `CPPFLAGS`, `LDFLAGS` and `LIBS` for the install
script, for example:

```
$ CPPFLAGS="-I/opt/openssl/include" LDFLAGS="-L/opt/openssl/lib" LIBS="-lssl -lcrypto" ./install-gnu.sh --without-ssl ...
```

**Visual Studio.** An OpenSSL NuGet package may work, though none is
maintained or tested with libbitcoin. Alternatively add the paths in a
`Directory.Build.props` file (see [Windows](windows#5-machine-options)):

```xml
<ItemDefinitionGroup>
  <ClCompile>
    <AdditionalIncludeDirectories>C:\openssl\include;%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
  </ClCompile>
  <Link>
    <AdditionalLibraryDirectories>C:\openssl\lib;%(AdditionalLibraryDirectories)</AdditionalLibraryDirectories>
    <AdditionalDependencies>libssl.lib;libcrypto.lib;%(AdditionalDependencies)</AdditionalDependencies>
  </Link>
</ItemDefinitionGroup>
```
