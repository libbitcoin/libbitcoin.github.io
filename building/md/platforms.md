# Platform support

## 1. Platforms

| Platform | Architecture | Libbitcoin | Bitcoin Core |
| -------- | ------------ | ---------- | ------------ |
| Linux | x64 | ✔ CI | ✔ CI |
| Linux | x86 (32-bit) | ✔ | ✔ CI |
| Linux | arm64 | ● | ● |
| Linux | arm32 | ✔ | ✔ CI |
| Linux | s390x (big-endian) | ✔ CI | ✔ |
| macOS | x64 | ● | ● |
| macOS | arm64 | ✔ CI | ✔ CI |
| Windows | x64 | ✔ CI | ✔ CI |
| Windows | x86 (32-bit) | ✔ CI | No target |
| Windows | arm64 | ● | No target |

## 2. Compilers

| Platform | Compiler | Libbitcoin | Bitcoin Core |
| -------- | -------- | ---------- | ------------ |
| Linux | GCC | ✔ CI (13, 14, 15 and 16) | ✔ CI (12, 14 and 15) |
| Linux | Clang | ✔ CI (18 and 19) | ✔ CI (17, 19 and 23) |
| macOS | Apple Clang (Xcode) | ✔ CI | ✔ CI |
| Windows | MSVC (Visual Studio 2026) | ✔ CI | ✔ CI |
| Windows | Clang (clang-cl, with Visual Studio) | ● | No target |
| Windows | MinGW-w64 GCC | No target | ✔ CI (cross compiled from Linux) |

## 3. Build systems

| Build system | Libbitcoin | Bitcoin Core |
| ------------ | ---------- | ------------ |
| Autotools | ✔ CI (Linux, macOS) | No target |
| CMake | ✔ CI (Linux, macOS) | ✔ CI (Linux, macOS, Windows) |
| Visual Studio | ✔ CI (Windows) | No target |
| Install scripts | ✔ CI (Linux, macOS, Windows) | No target |
| Guix (reproducible release builds) | WIP (Linux, macOS, Windows) | ✔ (Linux, macOS, Windows) |

## 4. Platform market share

![Operating system share of desktops, laptops and servers, and architecture share](../performance/desktop-share.png)

## 5. Notes

- ✔ CI: built and tested on every change.
- ● Built and tested outside of CI.
- ✔ Expected to build: the toolchain supports it.
- No target: no documented build or CI for the platform.

POWER, RISC-V and BSD are not shown. Compiler versions are those built in CI.
Bitcoin Core is shown from its build files and CI configuration at master
(October 2026).
