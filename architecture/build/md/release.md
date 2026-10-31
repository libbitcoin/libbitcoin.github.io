# Release builds

<div class="banner"><strong>Release builds are a work in progress.</strong></div>

The published builds of `bs` are made by two GitHub Actions workflows,
both run by hand: one tags each repository with a version, and one
builds, signs and publishes the server from those tags.

```mermaid
flowchart LR
    tag["version-tag\neach repository"] --> validate["validate-tags"]
    validate --> build["build-candidates\none job per build"]
    build --> sign["sign\napproval"]
    sign --> publish["publish\napproval"]
```

## 1. Version tags

Each of libbitcoin-system, -database, -network, -node and -server has a
`version-tag.yml` workflow. Its inputs are a branch (`master` by default),
a tag description and a tag suffix. It computes the version from the
branch:

| Part | Source |
| ---- | ------ |
| Major | `LIBBITCOIN_VERSION_MAJOR` in `builds/cmake/CMakeLists.txt` |
| Minor | `LIBBITCOIN_VERSION_MINOR` in `builds/cmake/CMakeLists.txt` |
| Patch | The number of commits on the branch (`git rev-list --count HEAD`) |

The tag is `v<major>.<minor>.<patch>` followed by the suffix, and is
created as an annotated tag and pushed. The workflow fails if the tag
already exists.

## 2. Build to Release

`manual-release.yml`, in libbitcoin-server, takes a tag for each of the
five repositories, and an optional suffix for the release title. Its four
jobs run in order.

### 2.1 validate-tags

Checks out each repository at its tag, and fails unless each tag exists
as a tag (not a branch or commit).

### 2.2 build-candidates

One job for each build, all from the same tags. Each checks out the five
repositories side by side and builds `bs` with the server's install
script, using the local sources (`--build-use-local-src`) and skipping
the tests (`--build-skip-tests`):

| Toolchain | Script | Configuration |
| --------- | ------ | ------------- |
| CMake (Linux, macOS) | `builds/cmake/install-cmake.sh` | `release`, `static`, with `--build-boost` |
| Visual Studio (Windows) | `builds/msvc/build-msvc.cmd` | `StaticRelease`, toolset `v145`, `vs2026` |

| Build | Runner | Compiler | Target | Options |
| ----- | ------ | -------- | ------ | ------- |
| `bs-linux-x64` | `ubuntu-24.04` | clang 18 | `x86-64-v3` | avx2, sse41 |
| `bs-linux-x64-shani` | `ubuntu-24.04` | clang 18 | `x86-64-v3` | shani, avx2, sse41 |
| `bs-linux-x64-avxifma` | `ubuntu-24.04` | clang 18 | `x86-64-v3` | avxifma, shani, avx2, sse41 |
| `bs-linux-x64-avx512ifma` | `ubuntu-24.04` | clang 18 | `x86-64-v3` | avx512ifma, shani, avx2, sse41 |
| `bs-linux-arm64` | `ubuntu-24.04-arm` | gcc 14 | `armv8-a` | |
| `bs-linux-arm64-crypto` | `ubuntu-24.04-arm` | gcc 14 | `armv8-a+crypto` | sha |
| `bs-linux-arm64-sha3` | `ubuntu-24.04-arm` | gcc 14 | `armv8.2-a+crypto+sha3` | sha, sha3 |
| `bs-musl-x64` | Alpine 3.22 | gcc | `x86-64-v3` | avx2, sse41 |
| `bs-musl-x64-shani` | Alpine 3.22 | gcc | `x86-64-v3` | shani, avx2, sse41 |
| `bs-musl-x64-avxifma` | Alpine 3.22 | gcc | `x86-64-v3` | avxifma, shani, avx2, sse41 |
| `bs-musl-x64-avx512ifma` | Alpine 3.22 | gcc | `x86-64-v3` | avx512ifma, shani, avx2, sse41 |
| `bs-macos-arm64` | `macos-latest` | Apple Clang | `apple-m1`, macOS 13.3 | sha3, sha, aes |
| `bs-macos-x64` | `macos-26-intel` | Apple Clang | `x86-64-v3`, macOS 13.3 | avx2, sse41, aesni |
| `bs-windows-x64` | `windows-latest` | MSVC | x64 | avx2, sse41 |
| `bs-windows-x64-shani` | `windows-latest` | MSVC | x64 | shani, avx2, sse41 |
| `bs-windows-x64-avxifma` | `windows-latest` | MSVC | x64 | avxifma, shani, avx2, sse41 |
| `bs-windows-x64-avx512ifma` | `windows-latest` | MSVC | x64 | avx512ifma, shani, avx2, sse41 |
| `bs-windows-arm64` | `windows-11-vs2026-arm` | MSVC | ARM64 | |
| `bs-windows-arm64-crypto` | `windows-11-vs2026-arm` | MSVC | ARM64 | sha |
| `bs-windows-arm64-sha3` | `windows-11-vs2026-arm` | MSVC | ARM64 | sha, sha3 |

Every x64 build assumes AVX2 and SSE4.1 (`x86-64-v3`) as the baseline of
its architecture.

Linux builds link the C++ and GCC runtimes statically
(`-static-libstdc++ -static-libgcc`); musl builds also link the C library
statically (`--static`). Windows builds end in `.exe`.

After the build, each job:

1. copies `bs` to its build name,
2. removes any embedded RPATH/RUNPATH (`patchelf`, glibc Linux builds),
3. strips symbols (all but Windows),
4. runs `--version` and `--hardware`, and shows the linkage (`ldd`,
   `readelf -d`, `otool -L`),
5. uploads the build as an artifact, kept for one day.

### 2.3 sign

Runs in the `release` environment, which holds the signing key and its
passphrase as secrets, and does not start until a maintainer approves it.
It downloads every build, imports the key into a
temporary keyring, and writes a detached, armored signature beside each
build (`<build>.asc`). It then deletes the key and the keyring, imports
the public key, and fails unless every signature verifies as a good
signature. The builds and signatures are uploaded as one artifact.

### 2.4 publish

Also in the `release` environment, and also waits for approval. It creates a release at the server
tag (with the suffix, if any), as a draft prerelease, with the builds and
their signatures as its assets. Existing assets are not overwritten. The
release notes link the tag of each of the five repositories it was built
from, and show the public key that signed it.

The draft is public once a maintainer publishes it.
