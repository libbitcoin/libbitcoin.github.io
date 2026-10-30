# Windows

Windows builds use Visual Studio 2026 (MSVC toolset v145). CI builds and
tests the static debug and release configurations on x64.

## 1. Prerequisites

- **Visual Studio 2026** with the *Desktop development with C++*
  workload. The Community edition is sufficient.
- **Git.**
- **nuget.exe**, from [nuget.org](https://www.nuget.org/downloads), on
  the `PATH`.

Build from a *Developer Command Prompt for VS 2026*, which puts
`msbuild` on the `PATH`.

## 2. Build with the script

Clone the five repositories side by side:

```
$ mkdir libbitcoin
$ cd libbitcoin
$ git clone https://github.com/libbitcoin/libbitcoin-system
$ git clone https://github.com/libbitcoin/libbitcoin-database
$ git clone https://github.com/libbitcoin/libbitcoin-network
$ git clone https://github.com/libbitcoin/libbitcoin-node
$ git clone https://github.com/libbitcoin/libbitcoin-server
```

Then build all five:

```
$ cd libbitcoin-server
$ builds\msvc\build-msvc.cmd --build-src-dir .. --build-config StaticRelease --build-platform x64 --build-use-local-src
```

The script restores the NuGet packages, including Boost, and builds
libbitcoin-system, libbitcoin-database, libbitcoin-network,
libbitcoin-node and libbitcoin-server in order, then runs the tests. The
result is `bin\x64\Release\v145\static\bs.exe`.

| Option | Values |
| ------ | ------ |
| `--build-config` | `StaticRelease` or `StaticDebug` (required) |
| `--build-platform` | `x64` (default), `ARM64` or `Win32` |
| `--build-skip-tests` | Do not build or run the tests |
| `--disable-cuda` | Build without GPU support (`/p:Option-cuda=false`) |
| `--build-symbols` | `default`, `disabled` or `public-only` |

Other arguments are passed to `msbuild`. Build options are set as
properties, for example `/p:Option-cuda=false` (see
[Build options](options)).

## 3. Build in Visual Studio

Open `builds\msvc\vs2026\libbitcoin-server.sln`. It contains
libbitcoin-server, its tests and `bs`, and references the other four
libraries in their sibling directories. Select `StaticRelease` or
`StaticDebug` and build. NuGet packages are restored on the first build.

Build options are on each project's property pages, under
*Configuration Properties*.

## 4. Instruction set

Windows x64 and Win32 builds target AVX2 by default, so such a `bs.exe`
requires a CPU with AVX2 (Intel Haswell, AMD Excavator or later). This
is only a default, set by `Option-arch`, and can be lowered for an older
CPU, for example to AVX or SSE2:

```
$ builds\msvc\build-msvc.cmd --build-src-dir .. --build-config StaticRelease --build-use-local-src /p:Option-arch=StreamingSIMDExtensions2
```

| `Option-arch` | Instructions |
| ------------- | ------------ |
| `StreamingSIMDExtensions2` | SSE2 |
| `AdvancedVectorExtensions` | AVX |
| `AdvancedVectorExtensions2` | AVX2 (default) |
| `AdvancedVectorExtensions512` | AVX-512 |

An extension option raises it as needed: `Option-sse41` to at least AVX,
`Option-avx2`, `Option-avxifma`, `Option-vaes` or `Option-sha512` to
AVX2, and `Option-avx512` to AVX-512.

## 5. Machine options

Options given on the command line apply to one build, and options set on
the property pages are saved in the project files. To set options for
every build on a machine, put them in a `Directory.Build.props` file in
the directory that holds the cloned repositories (`libbitcoin` above).
MSBuild imports this file into every project below its directory, so the
options apply to all five libraries, whether built by `build-msvc.cmd` or
in Visual Studio. The file is outside the repositories and is never
checked in.

For example, an AVX-512 machine with IFMA, AES-NI, VAES and the SHA
extensions:

```xml
<?xml version="1.0" encoding="utf-8"?>
<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <PropertyGroup>
    <Option-arch>AdvancedVectorExtensions512</Option-arch>
    <Option-avx512ifma>true</Option-avx512ifma>
    <Option-avxifma>false</Option-avxifma>
    <Option-aesni>true</Option-aesni>
    <Option-vaes>true</Option-vaes>
    <Option-sha>true</Option-sha>
    <Option-cuda>true</Option-cuda>
  </PropertyGroup>
</Project>
```

A property not set in the file keeps its default, and a `/p:` property
on the command line overrides the file. The build prints the resulting
options at the start of each library's build.
