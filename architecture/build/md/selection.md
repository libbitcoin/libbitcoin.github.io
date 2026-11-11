# Build Selection

How the release builds of Bitcoin Server (`bs`) are divided by hardware
extension, how each build is named, and how the `selector` finds the build
for a machine. The builds are made by the release workflow
([Release builds](release)) and installed by the packages
([Packaging](packaging)).

## 1. Floors

Each architecture has a floor, the lowest target any build is compiled
for. A build that uses a hardware extension is compiled for the lowest
architecture level that every processor with that extension is known to
reach, so its target can be above the floor.

| Architecture | Floor |
| ------------ | ----- |
| x64 | `x86-64` (x86-64-v1) |
| arm64 | `armv8-a` (ARMv8.0-A) |

## 2. Tags

A tag names a hardware extension that the builds differentiate. Each tag
is a build option. Enabling a tag also enables the extensions it ensures,
so a build compiles in every extension of its tags, including the ones
the tags ensure.

| Tag | Architecture | Compiles in | Target |
| --- | ------------ | ----------- | ------ |
| `sse41` | x64 | sse41 | `x86-64` |
| `shani` | x64 | shani, aesni | `x86-64-v2` |
| `avx2` | x64 | avx2, aesni | `x86-64-v3` |
| `avxifma` | x64 | avxifma, avx2, shani, aesni | `x86-64-v3` |
| `avx512` | x64 | avx512, avx2, aesni | `x86-64-v4` |
| `avx512ifma` | x64 | avx512ifma, avx512, avx2, shani, aesni | `x86-64-v4` |
| `sha2` | arm64 | sha2, aes | `armv8-a+aes+sha2` |
| `sha3` | arm64 | sha3, sha2, aes | `armv8.2-a+aes+sha2+sha3` |

SSE4.1 is part of every x64 target from `x86-64-v2`, and NEON is part of
the arm64 floor. AES is not a tag: it is compiled in by each tag that
ensures it. The `sha3` tag is set with the `+sha3` architecture extension,
which also provides the SHA-512 instructions which libbitcoin uses.

## 3. Relations

| Relation | Tags | Rule |
| -------- | ---- | ---- |
| Supersedence | `avx512` > `avx2` > `sse41` | A name carries only the highest of the three. |
| Exclusion | `avx512ifma`, `avxifma` | A name never carries both. A processor with both uses the `avx512ifma` build, which does not compile in avxifma. |
| Implication | `avxifma` ⇒ `avx2`, `shani` | A name with `avxifma` omits `avx2` and `shani`. |
| Implication | `avx512ifma` ⇒ `avx512`, `shani` | A name with `avx512ifma` omits `avx512` and `shani`. |
| Implication | `sha3` ⇒ `sha2` | A name with `sha3` omits `sha2`. |

## 4. Builds

A build is named `bs-<os>-<arch>` followed by its tags, each preceded by a
hyphen, in the order of the table below. `<os>` is `linux`, `macos` or
`windows`, and `<arch>` is `x64` or `arm64`. Windows builds end in
`.exe`. Each of the 13 builds below is made for each of the three
operating systems, 39 in all.

| Tags in name | Target | Options | Compiles in |
| ------------ | ------ | ------- | ----------- |
| x64, none | `x86-64` | | |
| `-sse41` | `x86-64` | `sse41` | sse41 |
| `-shani` | `x86-64-v2` | `shani` | shani, aesni |
| `-avx2` | `x86-64-v3` | `avx2` | avx2, aesni |
| `-avx2-shani` | `x86-64-v3` | `avx2`, `shani` | avx2, shani, aesni |
| `-avxifma` | `x86-64-v3` | `avxifma` | avxifma, avx2, shani, aesni |
| `-avx512` | `x86-64-v4` | `avx512` | avx512, avx2, aesni |
| `-avx512-shani` | `x86-64-v4` | `avx512`, `shani` | avx512, avx2, shani, aesni |
| `-avx512-avxifma` | `x86-64-v4` | `avx512`, `avxifma` | avx512, avx2, avxifma, shani, aesni |
| `-avx512ifma` | `x86-64-v4` | `avx512ifma` | avx512ifma, avx512, avx2, shani, aesni |
| arm64, none | `armv8-a` | | |
| `-sha2` | `armv8-a+aes+sha2` | `sha2` | sha2, aes |
| `-sha3` | `armv8.2-a+aes+sha2+sha3` | `sha3` | sha3, sha2, aes |

Builds for macOS arm64 are tuned for Apple M1 (`-mtune=apple-m1`), and all
others for a generic processor (`-mtune=generic`).

## 5. Selection

The `selector` reports a tag only when the processor has the extension
and also has every extension and architecture level that the tag's build
is compiled for. A processor that has an extension at a lower level than
its build assumes is therefore never directed to that build.

| Tag | Reported when the processor has |
| --- | ------------------------------- |
| `sse41` | SSE4.1 |
| `shani` | SHA extensions, x86-64-v2 and AES-NI |
| `avx2` | AVX2, x86-64-v3 and AES-NI |
| `avx512` | AVX-512 (F, BW, VL), x86-64-v4 and AES-NI |
| `avxifma` | AVX-IFMA, and the `avx2` and `shani` tags |
| `avx512ifma` | AVX-512 IFMA, and the `avx512` and `shani` tags |
| `sha2` | NEON SHA2 and NEON AES |
| `sha3` | NEON SHA3, LSE and the `sha2` tag |

The name is formed from the reported tags by these rules, in order:

| Part | Rule |
| ---- | ---- |
| x64 | `avx512ifma` if reported. Otherwise the first of `avx512` and `avx2` reported, with `avx2` omitted when `avxifma` is reported, followed by the first of `avxifma`, `shani` and `sse41` reported, with `sse41` omitted when `avx2` or `avx512` is reported. |
| arm64 | `sha3` if reported, otherwise `sha2` if reported. |

For example:

| Processors | Tags reported | Build |
| ---------- | ------------- | ----- |
| AMD K10 | | `bs-linux-x64` |
| Intel Nehalem to Ivy Bridge | `sse41` | `bs-linux-x64-sse41` |
| Intel Goldmont, Goldmont Plus | `sse41`, `shani` | `bs-linux-x64-shani` |
| Intel Haswell to Comet Lake | `sse41`, `avx2` | `bs-linux-x64-avx2` |
| AMD Zen to Zen 3, Intel Alder Lake, Raptor Lake | `sse41`, `avx2`, `shani` | `bs-linux-x64-avx2-shani` |
| Intel Lunar Lake, Arrow Lake, Sierra Forest | `sse41`, `avx2`, `shani`, `avxifma` | `bs-linux-x64-avxifma` |
| Intel Skylake-SP, Cascade Lake | `sse41`, `avx2`, `avx512` | `bs-linux-x64-avx512` |
| Intel Ice Lake, Tiger Lake, Sapphire Rapids, AMD Zen 4, Zen 5 | `sse41`, `avx2`, `avx512`, `shani`, `avx512ifma` | `bs-linux-x64-avx512ifma` |
| Raspberry Pi 4 (Cortex-A72, no cryptographic extensions) | | `bs-linux-arm64` |
| Raspberry Pi 5 (Cortex-A76), AWS Graviton2 | `sha2` | `bs-linux-arm64-sha2` |
| Apple M1 and later, AWS Graviton3 | `sha2`, `sha3` | `bs-macos-arm64-sha3` |

## 6. Selector

The `selector` of libbitcoin-system is built at the floor, with no tags,
so that it runs on every processor of its architecture.

| Build | Host |
| ----- | ---- |
| `selector-linux-x64` | `x86_64-linux-gnu` |
| `selector-linux-arm64` | `aarch64-linux-gnu` |
| `selector-macos-x64` | `x86_64-apple-darwin` |
| `selector-macos-arm64` | `arm64-apple-darwin` |
| `selector-windows-x64.exe` | `x86_64-pc-windows-msvc` |
| `selector-windows-arm64.exe` | `aarch64-pc-windows-msvc` |

| Command | Prints |
| ------- | ------ |
| `selector` | The reported tags, one per line |
| `selector bs` | The name of the build for the machine |
| `selector bs <release>` | The download address of that build: `https://github.com/libbitcoin/libbitcoin-server/releases/download/<release>/<name>` |

`bs --hardware` and `bx hardware` print, for each extension, whether the
processor has it (platform) and whether the binary compiles it in
(compiled), followed by the name of the build for the processor and the
name of the build that matches the binary:

```text
build....... platform:bs-linux-x64-avx2-shani compiled:bs-linux-x64-avx2-shani.
```

## 7. Packages

The deb packages, the Windows installers and the Docker image each hold
the `selector` and two builds. Each build requires a set of tags, and the
package uses the first build whose required tags are all reported by the
`selector`, at install for a deb or an installer, and at each start for
the image.

| Package | Architecture | Builds (required tags) |
| ------- | ------------ | ---------------------- |
| deb, Docker | x64 | `bs-linux-x64-avx2-shani` (`avx2`, `shani`), `bs-linux-x64` (none) |
| deb, Docker | arm64 | `bs-linux-arm64-sha2` (`sha2`), `bs-linux-arm64` (none) |
| Windows installer | x64 | `bs-windows-x64-avx2-shani.exe` (`avx2`, `shani`), `bs-windows-x64.exe` (none) |
| Windows installer | arm64 | `bs-windows-arm64-sha2.exe` (`sha2`), `bs-windows-arm64.exe` (none) |
| Homebrew | x64 | `bs-macos-x64-avx2` |
| Homebrew | arm64 | `bs-macos-arm64-sha3` |

The Homebrew formula holds one build per architecture, with no
`selector`. Every Mac supported by macOS 13.3 has the tags of its
build.
