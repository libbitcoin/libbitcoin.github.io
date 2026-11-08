# Platform coverage

## 1. Platforms

| Platform | Architecture | Libbitcoin | Bitcoin Core |
| -------- | ------------ | ---------- | ------------ |
| Linux | x64 | ✔ CI | ✔ CI |
| Linux | x86 (32-bit) | ✔ CI | ✔ CI |
| Linux | arm64 | ✔ CI | ✔ |
| Linux | arm32 | ✔ CI | ◑ CI |
| Linux | s390x (big-endian) | ✔ CI | ● |
| Linux | ppc64le | ✔ CI | ● |
| Linux | ppc64 (big-endian) | ✔ CI | ● |
| macOS | x64 | ✔ CI | ✔ |
| macOS | arm64 | ✔ CI | ✔ CI |
| Windows | x64 | ✔ CI | ✔ CI |
| Windows | x86 (32-bit) | ✔ CI | No target |
| Windows | arm64 | ✔ CI | No target |
| FreeBSD | x64 | ◑ CI | ◑ CI |
| OpenBSD | x64 | ◑ CI | ◑ CI |
| NetBSD | x64 | ◑ CI | ◑ CI |

Linux is tested under both glibc and musl. The BSD tests have all been
verified outside of CI, and `bs` has not been performance tuned on BSD.
NetBSD requires GCC 13 or later from pkgsrc.

All libraries and Bitcoin Explorer (`bx`) are supported on 32-bit
platforms, however Bitcoin Server (`bs`) requires 64-bit.

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

## 3. Build systems

| Build system | Libbitcoin | Bitcoin Core |
| ------------ | ---------- | ------------ |
| Autotools | ✔ CI (Linux, macOS) | No target |
| CMake | ✔ CI (Linux, macOS, Windows) | ✔ CI (Linux, macOS, Windows) |
| Visual Studio | ✔ CI (Windows) | No target |

## 4. Build scripts

| Build script | Libbitcoin | Bitcoin Core |
| ------------ | ---------- | ------------ |
| `install-gnu.sh` | ✔ CI (Linux, macOS) | No target |
| `install-cmake.sh` | ✔ CI (Linux, macOS) | No target |
| `install-presets.sh` | ✔ CI (Linux, Windows) | No target |
| `build-msvc.cmd` | ✔ CI (Windows) | No target |

## 5. Developer libraries

| Platform | Library | system | database | network | node | server | Bitcoin Core |
| -------- | ------- | ------ | -------- | ------- | ---- | ------ | ------------ |
| Linux | Static | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ● |
| Linux | Shared | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI |
| macOS | Static | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ● |
| macOS | Shared | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI |
| Windows | Static | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI |
| Windows | DLL | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI | ✔ CI |

Bitcoin Core's experimental validation library is not released, or called by `bitcoind`.

## 6. Executables

| Platform | Linkage | Libbitcoin | Bitcoin Core |
| -------- | ------- | ---------- | ------------ |
| Linux | Static | ✔ CI | ✔ CI |
| Linux | Dynamic | ✔ CI | ✔ CI |
| macOS | Static | ✔ CI | ✔ CI |
| macOS | Dynamic | ✔ CI | ✔ CI |
| Windows | Static | ✔ CI | ✔ CI |
| Windows | Dynamic | ✔ CI | ✔ CI |

## 7. Installers

| Platform | Libbitcoin | Bitcoin Core |
| -------- | ---------- | ------------ |
| Linux | single file executable | tar (22 files) |
| macOS | single file executable | tar (20 files) |
| Windows | single file executable | zip (19 files), NSIS installer (13 files, 5 shortcuts, 15 registry values) |

## 8. Platform market share

![Operating system share of desktops, laptops and servers, and architecture share](../performance/desktop-share.png)

## 9. Notes

- ✔ CI: built and tested on every change.
- ◑ CI: built on every change, tests not run.
- ✔ Built and tested outside of CI.
- ● Expected to build: the toolchain supports it.
- No target: no documented build or CI for the platform.

Compiler versions are those built in CI.
Bitcoin Core is shown from its build files and CI configuration at master
(October 2026).
