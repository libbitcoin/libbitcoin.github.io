# libbitcoin-build

libbitcoin-build is a maintainer tool. Building `bs` does not require it:
everything it produces is committed to each repository. It is needed only
to change the build files themselves, such as adding a source file, a
target, a dependency, a build option or a CI job.

## Purpose

Every libbitcoin repository is built by three build systems (autotools,
CMake and Visual Studio), tested by the same CI matrix, and installed by
the same scripts. libbitcoin-build generates all of those files from one
description, so that they stay consistent across the build systems and
across the repositories.

It covers six repositories: libbitcoin-system, libbitcoin-network,
libbitcoin-database, libbitcoin-node, libbitcoin-server and
libbitcoin-explorer.

## Breadth

For each repository it generates:

| Area | Files |
| ---- | ----- |
| Autotools | `builds/gnu/configure.ac`, `Makefile.am`, the pkg-config `.pc.in`, and the test runner |
| CMake | `builds/cmake/CMakeLists.txt`, `CMakePresets.json` and the package config |
| Visual Studio | the solution, every `.vcxproj` and `.vcxproj.filters`, property sheets, NuGet configuration and the debugger visualizers |
| Install scripts | `install-gnu.sh`, `install-cmake.sh`, `install-presets.sh` and `build-msvc.cmd` |
| CI | the GitHub Actions workflows: `ci.yml`, `ci-expanded.yml` and `version-tag.yml` |
| Editors | the VS Code workspace and settings |
| Sources | the aggregate include header and `version.hpp` |
| Repository | `.gitignore` and `CODEOWNERS` |

It also fixes the versions every build uses. These include the C++
standard, Boost for autotools and CMake, the Boost NuGet package for
Visual Studio, the MSVC toolset, and the compilers and runner images of
the CI matrix (see [Build systems and toolchains](toolchains)).

README build instructions are not generated.

## Operation

The description is a single XML manifest, `version4.xml`. It declares each
repository's targets (libraries, tests and binaries), their source roots,
options, dependencies, compilers and CI jobs, along with the shared
dependency, preset, build option and toolchain definitions.

Templates written in [iMatix GSL](https://github.com/zeromq/gsl) turn the
manifest into the files above. The tool runs in three steps:

1. Generate every artifact into `output/version4`.
2. Copy the static Visual Studio property sheets and scripts.
3. Copy the output over the sibling repository checkouts beside the
   libbitcoin-build checkout.

```
$ ./generate4.sh
```

On Windows, `generate4.cmd` does the same, and accepts repository names to
limit the copy, for example `generate4.cmd libbitcoin-node`.

GSL builds from source on Linux and macOS (it needs PCRE), and is
available as a NuGet package on Windows.

### Source files

Source lists are not kept in the manifest. The generator reads them from
the sibling checkouts on disk, scanning each target's source roots. So:

- **Adding a source file** under an existing root needs no manifest
  change: add the file and regenerate. CMake finds new files by itself.
- **Adding a source root or a target** needs a manifest change.
- **Do not hand-edit** `Makefile.am` or the `.vcxproj` files. The
  generator also gives files that share a name distinct object names,
  which hand edits miss.

### Requirements of a run

- All six repositories must be checked out beside libbitcoin-build. A
  missing repository or directory stops the run partway.
- The scan reads the working trees, not git. Untracked files are
  included, and an empty directory inside a scanned tree empties the
  lists it would have filled. Clean the trees before regenerating.
- The copy overlays files and never deletes them. A file the generator no
  longer produces must be removed from the repository by hand.
