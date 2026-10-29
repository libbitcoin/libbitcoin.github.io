# Test practices

Test code follows the [Style guide](style) except where this page differs.
**A test file reads as a declarative list of facts**, so anything that
makes it harder to scan, or that would itself need testing, is excluded.

## 1. Scope

| Level | Scope |
|---|---|
| unit | A method or function, isolated to the extent practical. |
| component | A group of units, such as a class. |
| functional | A feature group, such as client-server communication. |

- `BC_ASSERT` paths are unreachable by design and are not tested.
- Acceptance tests are the server's Python suite in `endpoints/`, run
  against a live node (see [Test architecture](../test/index)).

## 2. Files and structure

- `test/` mirrors `src/`, with one test file per source file, of the same
  name.
- Include the shared header by relative path, then any mocks or fixtures:

```cpp
#include "../test.hpp"
#include "../mocks/chunk_storage.hpp"
```

- The suite is named for the file, with a `_tests` suffix:
  `BOOST_AUTO_TEST_SUITE(hashmap_tests)`, or
  `BOOST_FIXTURE_TEST_SUITE(query_address_tests, test::directory_setup_fixture)`.
- Group cases by method under an implementation-style banner:

```cpp
// record hashmap
// ----------------------------------------------------------------------------
```

- **Leave a blank line before `BOOST_AUTO_TEST_SUITE_END()`.**
- Put shared helpers in `test/mocks` or a fixture, in namespace `test`.
  File-local helpers are `static` free functions, not anonymous namespaces.
- Reach protected members through an accessor subclass (for example
  `chaser_accessor`) that re-exports the base constructor and members,
  never by changing production visibility.
- Use `TEST_DIRECTORY` and `TEST_PATH` (each test's own path) with
  `test::directory_setup_fixture` for anything that touches the
  filesystem.

## 3. Test names

Name a case `subject__method__condition__expectation`, joining the parts
with double underscores:

```cpp
BOOST_AUTO_TEST_CASE(hashmap__enabled__empty_slab_one_bucket__true)
BOOST_AUTO_TEST_CASE(query_address__get_balance__turbo_block1a_address0_confirmed_blocks__expected)
```

- Where an error code applies, the expectation is that code
  (`..._invalid_parameter`).
- Keep names as short as their siblings.
- Describe the condition in libbitcoin vocabulary. Wire error names may
  appear as the outcome (`confirmed_unspent__verify_already_in_utxo_set`).

## 4. Lines: never wrap inside a test case

**This is the main difference from production code.**

- Inside a `BOOST_AUTO_TEST_CASE` body, **never wrap a line**, however
  long. Each assertion and each call is one line.
- Shorten lines with named locals. Each nested call inside an assertion
  becomes a local, and the assertion collapses to one line:

```cpp
// Right.
const auto hash = bitcoin_hash(data);
const auto fingerprint = to_fingerprint(hash);
BOOST_REQUIRE_EQUAL(fingerprint, expected);

// Wrong.
BOOST_REQUIRE_EQUAL(to_fingerprint(bitcoin_hash(
    data)), expected);
```

- The same applies to `static_assert`: hoist the operands into named
  `constexpr` values.
- Two declarations are exceptions. A declaration of elements may span lines
  with balanced braces, and a long hex literal may continue across lines
  as adjacent string literals:

```cpp
const hashes roots
{
    test::root01,
    test::root23
};

const auto block = base16_chunk(
    "02000000b51eb76f7cfd89ef4be99b0c7ea3e009ffbf33643661a0fc29354e010000"
    "000029cac78dd1eb1575de815d371bc652c47fcf6f15557bbd02b449513bb46de6f3");
```

- **Outside test case bodies the 80-column rule still applies.** Helper
  functions, mocks and fixture declarations wrap like production code.

## 5. No control flow

**Tests contain no `if`, `else`, `for`, `while` or ternary.** This includes
fixtures and lambdas inside tests. A test with branches needs a test of its
own.

- Write a small enumerable range out in full, with numbered locals
  (`value1` through `value12`), never as a loop.
- Where iteration is unavoidable, use standard algorithms: `std::generate`
  for pattern buffers, `std::copy_n` for fills,
  `BOOST_REQUIRE_EQUAL_COLLECTIONS` for verification, and `std::for_each`
  over `std::iota` ids to spawn and join threads. Worker threads only
  record results; the assertions run after the join.
- Count conditions arithmetically, not with a branch:
  `faults += to_int<size_t>(!!ec);`.
- The one sanctioned loop is over an embedded table of reference vectors.
- Write generated test data out literally.

## 6. Assertions

- `BOOST_REQUIRE*` is the default: the first failure stops the case.
  `BOOST_CHECK*` appears in files that are dense lists of independent facts
  (for example system's `filter/bloom.cpp` and database's
  `query/merkle.cpp`), where reporting every failure at once helps. Match
  the file you are editing.
- Use `BOOST_REQUIRE_EQUAL` for anything streamable, including
  `hash_digest`, `data_chunk` and `data_array`. `test.hpp` supplies
  `operator<<` for `data_slice`, `std::vector` and `std_array`, so a
  failure prints both values. Reserve `BOOST_REQUIRE(a == b)` for types
  with no stream operator (`script`, `enum class` values).
- Success is `BOOST_REQUIRE(!ec)`. Failure is `BOOST_REQUIRE(ec)`, or
  `BOOST_REQUIRE_EQUAL(ec, error::query_canceled)` where the test proves a
  specific error.
- Keep each statement with its assertions. For longer tests, separate
  setup, action and verification groups with blank lines, and do not
  interleave them.

## 7. Comments

**Comment almost nothing.** The test name and the code are the
documentation.

- Comment only what neither the name nor the code can carry: for example,
  that a published filter carries a count prefix, so the expected bytes
  are the body alone.
- A test file needs few comments beyond its section banners.
- The source of a set of reference vectors is worth a comment. Narrative
  blocks are not.

## 8. Pre-commit checklist for agents

1. **No wraps** in any `BOOST_AUTO_TEST_CASE` body. This flags
   continuation lines for review:
   `git diff -U0 -- test | grep -E '^\+\s{8,}\S' | grep -vE '^\+\s*(BOOST_|//|")'`.
2. **No control flow.** This should print nothing:
   `git diff -U0 -- test | grep -nE '^\+.*\b(if|for|while|else)\b|\?.*:'`.
3. **Names** follow `subject__method__condition__expectation`, at sibling
   length.
4. **`BOOST_REQUIRE_EQUAL`** is used wherever the operands are streamable.
5. **Comments.** A few at most, none narrative.
6. A blank line precedes `BOOST_AUTO_TEST_SUITE_END()`.
7. The suite passes.
