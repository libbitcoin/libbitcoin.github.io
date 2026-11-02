# Platform coverage

## 1. Platforms

| Platform | Architecture | Libbitcoin | Bitcoin Core |
| -------- | ------------ | ---------- | ------------ |
| Linux | x64 | ✔ CI | ✔ CI |
| Linux | x86 (32-bit) | ✔ CI | ✔ CI |
| Linux | arm64 | ✔ CI | ✔ |
| Linux | arm32 | ✔ CI | ✔ CI |
| macOS | x64 | ✔ CI | ✔ |
| macOS | arm64 | ✔ CI | ✔ CI |
| Windows | x64 | ✔ CI | ✔ CI |
| Windows | x86 (32-bit) | ✔ CI | No target |
| Windows | arm64 | ✔ CI | No target |

On 32-bit platforms the full stack builds and passes its tests, and `bx`
is supported, but `bs` is not.

## 2. Compilers

| Platform | Compiler | Libbitcoin | Bitcoin Core |
| -------- | -------- | ---------- | ------------ |
| Linux | GCC | ✔ CI (13, 14, 15 and 16) | ✔ CI (12, 14 and 15) |
| Linux | Clang | ✔ CI (18 and 19) | ✔ CI (17, 19 and 23) |
| macOS | Apple Clang (Xcode) | ✔ CI (Xcode 26.6) | ✔ CI (Xcode 26.3) |
| Windows | MSVC (Visual Studio 2026) | ✔ CI (v145) | ✔ CI (v145) |
| Windows | Clang (clang-cl, with Visual Studio) | ✔ CI (18.11) | No target |
| Windows | MinGW-w64 GCC | ✔ CI (13) | ✔ CI (14) |
| Windows | MinGW-w64 Clang | ✔ CI (13) | No target |

## 3. Executables

| Platform | Linkage | Libbitcoin | Bitcoin Core |
| -------- | ------- | ---------- | ------------ |
| Linux | Static | ✔ CI | ✔ CI |
| Linux | Dynamic | ✔ CI | ✔ CI |
| macOS | Static | ✔ CI | ✔ CI |
| macOS | Dynamic | ✔ CI | ✔ CI |
| Windows | Static | ✔ CI | ✔ CI |
| Windows | Dynamic | ✔ CI | ✔ CI |

## 4. Libraries

| Platform | Library | system | database | network | node | server | Bitcoin Core |
| -------- | ------- | ------ | -------- | ------- | ---- | ------ | ------------ |
| Linux | Static | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ● |
| Linux | Shared | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI |
| macOS | Static | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ● |
| macOS | Shared | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI |
| Windows | Static | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI |
| Windows | DLL | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI |

Bitcoin Core's experimental library is not released, or called by `bitcoind`.

## 5. Build systems

| Build system | Libbitcoin | Bitcoin Core |
| ------------ | ---------- | ------------ |
| Autotools | ✔ CI (Linux, macOS) | No target |
| CMake | ✔ CI (Linux, macOS, Windows) | ✔ CI (Linux, macOS, Windows) |
| Visual Studio | ✔ CI (Windows) | No target |
| Build script | ✔ CI (Linux, macOS, Windows) | No target |

## 6. Platform market share

![Operating system share of desktops, laptops and servers, and architecture share](../performance/desktop-share.png)

## 7. Notes

- ✔ CI: built and tested on every change.
- ✔ Built and tested outside of CI.
- ● Expected to build: the toolchain supports it.
- No target: no documented build or CI for the platform.

POWER, RISC-V, s390x and BSD are not shown. Compiler versions are those built in CI.
Bitcoin Core is shown from its build files and CI configuration at master
(October 2026).
