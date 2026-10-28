# Style guide

This guide applies to libbitcoin source code. Test code follows it except
where [Test practices](testing) says otherwise.

**The code is the specification.** Where this guide and the surrounding
code disagree, match the surrounding code and raise the discrepancy.
Never restyle code you are not otherwise changing.

## 1. Files

**License header.** Every hand-written source file begins with the AGPL
header, `Copyright (c) 2011-2026 libbitcoin developers`, copied verbatim
from an existing file. Generated files carry libbitcoin-build's own header
(`2014-2026 libbitcoin-<repo> developers (see COPYING)`); it changes only
through regeneration.

### Kinds of file

| Kind | Location | Holds |
|---|---|---|
| `.hpp` | `include/bitcoin/<repo>/<directory>/` | Declarations, plus inline bodies only when short. |
| `.ipp` | `include/bitcoin/<repo>/impl/<directory>/` | Template and inline definitions, included at the foot of their `.hpp`. |
| `.cpp` | `src/<directory>/` | Non-template definitions. |

Include guards spell the path:
`LIBBITCOIN_DATABASE_PRIMITIVES_HASHMAP_HPP`, and `..._IPP` for an `.ipp`.
Do not use `#pragma once`.

A templated class defines `TEMPLATE` and `CLASS` after its declaration,
includes the `.ipp`, then undefines them:

```cpp
} // namespace database
} // namespace libbitcoin

#define TEMPLATE template <class Link, class Key, size_t RowSize, size_t CellSize>
#define CLASS hashmap<Link, Key, RowSize, CellSize>

#include <bitcoin/database/impl/primitives/hashmap.ipp>

#undef CLASS
#undef TEMPLATE

#endif
```

In the `.ipp`, each definition is `TEMPLATE` on its own line, followed by
`<return> CLASS::name(...) NOEXCEPT`.

### Namespaces

One namespace per line, each closed with a comment. Do not use anonymous
namespaces; file-local helpers are `static` free functions.

```cpp
namespace libbitcoin {
namespace network {

} // namespace network
} // namespace libbitcoin
```

### Includes

Headers may not form an inclusion cycle, so the header dependencies of a
library form a directed acyclic graph. These rules keep it that way, and
apply to every `.hpp` and `.ipp`. A `.cpp` cannot create a cycle, but
generally follows them.

1. **Common headers.** Each directory has a common header that includes
   the directory (for example `data/data.hpp`, `log/log.hpp`). Code outside
   the directory includes the common header, never an individual header
   inside it. Code inside the directory never includes its own common
   header, which would be a cycle, and includes its siblings explicitly,
   never assuming one arrives through another.
2. **`define.hpp`** is the library's root common header, included by every
   header outside the root directory. The root headers are chained into
   it, and are not included directly anywhere else.
3. **Dependency order.** Each library's `src/define.cpp` lists the order
   of its root chain and of its directories, in the form
   `/channels : /interfaces /net`. Each entry names only its highest
   dependencies. A cycle is broken by including one file, noted as
   `[sessions/session.hpp]`, or by a forward declaration, noted as
   `[forward: net]`.
4. A `.cpp` includes its own header first, then a blank line, then the
   rest. Any standard header comes first, then the libbitcoin
   headers, sorted, `define.hpp` among them.
5. **Never include the standard headers that libbitcoin-system's
   `define.hpp` provides:** `<algorithm> <array> <cstddef> <cstdint>
   <functional> <istream> <ostream> <iostream> <iterator> <limits>
   <memory> <stdexcept> <string> <string_view> <type_traits> <utility>
   <variant> <vector>`.
6. Repo aggregates (`bitcoin/database.hpp` and the like), `.vcxproj` and
   `.filters` files, `Makefile.am`, `configure.ac`, and the CMake and CI
   files are **generated** by [libbitcoin-build](../building/libbitcoin-build).
   Adding, moving or deleting a source file means regenerating them and
   committing the result with the change. Never hand-edit them.

## 2. Naming

| Kind | Form | Example |
|---|---|---|
| Types, functions, variables | `snake_case` | `get_top_confirmed` |
| Private data members | trailing underscore | `body_`, `negative_` |
| Type aliases | `snake_case`, a `_t` suffix allowed | `data_chunk`, `settings_t` |
| Shared pointers | nested `ptr` and `cptr` | `channel::ptr` |
| Template parameters | `PascalCase` | `Link`, `RowSize` |
| Macros | `UPPER_CASE` | `SUBSCRIBE_ESPLORA` |
| Async completions | `handle_*` | `handle_receive_post` |
| Platform guards | `HAVE_*`, naming the platform meant | `HAVE_LINUX`, not `HAVE_POSIX`, for Linux-only code |

### Vocabulary

These rules bind identifiers, comments, test names and commit messages.
Wire names from other protocols, such as `getchaintips` or
`bestblockhash`, stay as written.

| Use | Never |
|---|---|
| top | tip |
| unspent | utxo |
| output | coin (except "coinbase") |
| input, output | vin, vout |
| output script, input script | scriptPubKey, scriptSig |
| bitcoind (or satoshi in some older references) | Core, Bitcoin Core |
| tx pool (all unconfirmed transactions) | mempool, mem_pool |

Quick check:
`grep -nEi '\bcore\b|\bvin\b|\bvout\b|scriptpubkey|scriptsig|\btip\b|\butxo\b|mem_?pool'`.

## 3. Declarations

- Every function is `NOEXCEPT`. Exported classes carry the library's
  export macro: `BC_API` (system), `BCD_API` (database), `BCT_API`
  (network), `BCN_API` (node), `BCS_API` (server), `BCX_API` (explorer).
- State copy and move semantics with the macros `DEFAULT_COPY_MOVE`,
  `DEFAULT_COPY_MOVE_DESTRUCT`, `DELETE_COPY_MOVE` and
  `DELETE_COPY_MOVE_DESTRUCT`. The `_DESTRUCT` forms declare a virtual
  destructor, so use them only for polymorphic classes.
- Write a default function parameter without spaces
  (`size_t expected=zero`), and a default template parameter with them
  (`typename Byte = uint8_t`).
- Order class sections as `public`, `protected`, then `private`. Within a
  section put types first, then methods, then data members. Data members
  come last, after operators, and are never mixed in among methods.
- Declaration order in the `.hpp` equals definition order in the
  `.ipp` or `.cpp`.
- **Parameter order.** Out-parameters and mutable references come first.
  The completion handler comes last.
- **The bool out-parameter contract.** `false` means the out-parameter was
  not set. Never return `true` when the input is absent, and never build a
  default into the helper. For optional input, compose a finder (`false`
  means absent) with a parser (`false` means malformed), and initialize the
  default at the caller.
- **Enums for foreign API values.** Use an unscoped enum with an explicit
  underlying type and explicit values, qualified at the point of use. Put
  each enumerator's doc on a `///` line above it, never as a trailing
  comment.

```cpp
enum block_verbosity : size_t
{
    /// Serialized block as hex.
    hex = 0,

    /// Block with txids.
    object = 1
};

if (verbosity == block_verbosity::hex)
```

### Header docs

A `///` comment is a single line saying what the member does, in the style
of its siblings. Headers stay lean, with no explanation beyond that. In a
member list that has no comments, a new member also goes in bare.

Header section banners use triple slashes:

```cpp
    /// Setup, not thread safe.
    /// -----------------------------------------------------------------------

    bool create() NOEXCEPT;
```

Implementation section banners use double slashes and run to column 80:

```cpp
// not thread safe
// ----------------------------------------------------------------------------
```

## 4. Layout

- Indent four spaces, never tabs. Braces go on their own lines (Allman).
- **Limit lines to 80 columns.** The limit may be bent slightly when one
  line reads better than a wrap.
- Base classes and constructor initializers start on a continuation line
  indented two spaces with `:`.

```cpp
class BCT_API channel
  : public proxy
{
```

```cpp
TEMPLATE
CLASS::hashmap(storage& header, storage& body, const Link& buckets,
    size_t expected) NOEXCEPT
  : head_(header, buckets, expected), body_(body)
{
}
```

- **Do not wrap call arguments.** Shorten the line instead: hoist named
  locals, or put `using in_t = input_link::integer;` aliases at the top of
  the function. Wrapping a signature is fine.
- **Braced initializers fit on one line, or stand alone.** Never wrap from
  inside a brace pair.

```cpp
// Right.
item =
{
    messages::peer::unspecified_timestamp,
    messages::peer::service::node_none, address, port
};

// Wrong.
item = { messages::peer::unspecified_timestamp,
    messages::peer::service::node_none, address, port };
```

- A body of one statement is unbraced (`if (stopped())` and `return;` on
  two lines). **A macro body is always braced**, because a multi-statement
  expansion escapes an unbraced conditional:

```cpp
if (!is_zero(minimum))
{
    SEND(fee_filter{ minimum }, handle_send, _1);
}
```

- In a multi-clause condition put one clause per line, and leave a blank
  line between a computed condition and the `if` that consumes it.
- Align `=` (or `+=`) across a run of related assignments. Order
  declaration groups from short to long.
- A function's opening lines (`using`, the first locals) form one block,
  with no blank line separating them.
- Put the success path inside braces and let failure fall through to a
  single `return`, rather than piling up guard returns, where that reads
  better. Keep logically distinct exits as separate returns rather than
  one compound ternary.
- **No sandwiches.** Do not wedge a statement between macro invocations, or
  a comment between paired lines. Group each statement with its
  assertions, and separate groups with blank lines.
- **DRY by judgment.** Repeating a large expression back to back is a
  defect. A small repetition that reads better is fine.

## 5. Comments

Default to **no comment**.

- Comment only a non-obvious invariant the code cannot state, of the same
  gravity as anything else the code leaves unstated. If there are several,
  name all of them or none.
- **Never** record the change, the fix, a rejected alternative, a reference
  implementation, or a conversation. Git history and review hold those.
  Ask: would this comment exist if the code had been written this way from
  the start, by someone who never saw how it came to be?
- A comment applies to what is immediately below it. A blank line after the
  comment widens its scope to the section that follows.
- A commented magic literal becomes a named `constexpr`, and the comment
  moves to the constant.
- Write `// TODO: ...` only for real deferred work.

## 6. Types and numbers

**Never use `static_cast` for integer conversion.** Pick the system cast
whose name states what is certain and what is possible:

| Cast | Size | Sign |
|---|---|---|
| `narrow_cast` | narrower | same |
| `sign_cast` | not narrower | changes |
| `narrow_sign_cast` | narrower | changes |
| `wide_cast` | wider | same |
| `wide_sign_cast` | wider | changes |
| `possible_narrow_cast` | may narrow | same |
| `possible_sign_cast` | not narrower | may change |
| `possible_narrow_sign_cast` | may narrow | changes |
| `possible_sign_narrow_cast` | narrower | may change |
| `possible_narrow_and_sign_cast` | may narrow | may change |

Classify the conversion from what the standard fixes, never from the
compiler in front of you. For floating point, use `to_integer` and
`to_floating`. For `bool`, use `to_int`.

- **Use promotion-free math.** For sub-int operands use `add<T>`,
  `subtract<T>` and `is_add_overflow<T>` (in the target type), and
  `is_lesser` and `is_greater`. For mixed types use `greater` and
  `lesser`, never `std::max` or `std::min`, which require both arguments
  of one type. `size_t` and `uint64_t` are different types; never assume a
  64-bit build.
- Use `is_zero(x)`, `is_nonzero(x)`, `is_one(x)`, `zero`, `one`, `two`,
  `add1` and `sub1` rather than raw literals and `== 0`.
- Add a literal suffix (`_size`, `_u64`) only where it establishes a type.
  A value that already matches its parameter type takes no suffix.
- Derive constants from domain constants: `ec_xonly_size * two`, not `64`.
- Use `size_t` for the system's own quantities, and an explicit width for
  wire and disk fields and external totals.
- Arithmetic templates are constrained to unsigned types. Do not declare
  signed overloads.
- Prefix OS and global symbols with `::`: `::CloseHandle`,
  `::GetSystemInfo`.
- A `.cpp` takes `using namespace system;` and names system symbols
  unqualified. Headers qualify with `system::`. Base-namespace utilities
  (`zero`, `is_zero`, `std_vector`) are never written `system::`. Keep a
  `using namespace` at the narrowest scope possible.
- **The C++20 contract holds both ways.** Code that exceeds C++20 is fixed
  in the code. A compiler that rejects conforming C++20 gets upgraded; the
  code is not contorted around it.

## 7. Errors and assertions

- **Never collapse error conditions.** When you expect a specific failure,
  test for that one (`errno == ENOSPC`). Every other failure is a different
  condition, normally a fault.
- Functions return a `code` (`error::success` or a specific value) or
  `bool`. Callers test `if (const auto ec = f())`.
- `BC_ASSERT` declares a condition unreachable by design. It is
  documentation, not runtime behavior. Convert an unreachable guard into
  `BC_ASSERT` when the guard would otherwise appear to hide a defect.
- Suppress a warning with `BC_PUSH_WARNING(NAME)` and `BC_POP_WARNING()`,
  scoped as narrowly as possible.

## 8. Asynchrony and design

- **Write continuations as named handlers, not lambdas.** Bind a private
  `handle_*` method with the network macros (`BIND(handle_x, _1)`,
  `POST(...)`), which bind it to a shared pointer to the object. Small
  lambdas are fine. Nested capture chains are not.
- A stranded method begins with `BC_ASSERT(stranded());`.
- Apply `std::move` to handoffs consistently, including trivially copyable
  types. A move into a `const&` destination gains nothing: fix the handler
  signature instead. Pass one `shared_ptr` across a strand, not a list of
  values derived from it.
- **Pass conditions as parameters, not as held state.** Do not set a member
  around a synchronous call, and never set a flag for a later asynchronous
  step to consume.
- **Trigger the existing path; do not write a parallel one.** If new code
  repeats the tail of an existing operation, call that operation instead.
  Reuse system primitives (`config::version`, `is_ascii_number`, the
  extractors) rather than writing bespoke parsing.

## 9. Commits

- **One subject line, short, imperative, ending in a period.** No body, and
  no trailers of any kind, including `Co-Authored-By` and tool attribution.
  For example: `Return the found link from hashmap find_link.`
- The subject names the change, not its rationale.
- Each commit is one logical change. It includes its regenerated build
  artifacts and its tests.

## 10. Pre-commit checklist for agents

Run these against the diff before committing.

1. **Wrapped calls and initializers.** No argument list is wrapped, and no
   braced list is wrapped from inside the braces.
2. **Comments.** Each added comment passes the "written this way from the
   start" test in section 5. Delete any that narrate the change.
3. **Includes.** No forbidden standard headers, no individual header from
   another directory, and nothing out of dependency order:
   `git diff -U0 | grep '^+#include <'`, then check each path.
4. **Vocabulary.** Run the grep in section 2 over the added lines.
5. **Casts and math.** No `static_cast<` on integers, no `std::max` or
   `std::min` on mixed types, and no `== 0`:
   `git diff -U0 | grep -E '^\+.*(static_cast<|std::(max|min)\(| == 0\b)'`.
6. **Macro bodies.** Every macro under a conditional is braced.
7. **`NOEXCEPT`.** Present on every new function.
8. **Generated files.** Regenerated through libbitcoin-build if any file
   was added, moved or deleted.
9. **Tests.** Added or updated per [Test practices](testing), and the
   suite passes.
10. **Commit message.** One line, a period, no trailer.
