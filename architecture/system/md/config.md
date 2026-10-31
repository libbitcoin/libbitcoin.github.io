# Config

The `config` module provides the text forms of libbitcoin values and the
machinery that reads them from a command line, environment variables and a
configuration file. Each value type converts to and from a string through
stream operators, which is the interface `boost::program_options` uses to parse
and display option values. The parser, setting and printer classes build on
`boost::program_options` to load, describe and print the options of an application
such as `bs` or `bx`. Paths are relative to `include/bitcoin/system/` in
[libbitcoin-system](https://github.com/libbitcoin/libbitcoin-system), at
master `0cd57fcf` (2026-10-27).

## 1. Value types

### 1.1 Stream round trip

Every value type has the same shape: construction from its native value,
construction from a string (which throws on malformed text), an implicit
conversion back to the native value, and a friend pair of stream operators
in the same text format (`config/hash256.hpp`):

```cpp
class BC_API hash256 final
{
public:
    typedef std::vector<hash256> list;

    hash256() NOEXCEPT;
    hash256(hash_digest&& value) NOEXCEPT;
    hash256(const hash_digest& value) NOEXCEPT;
    hash256(const std::string& base16) THROWS;

    std::string to_string() const NOEXCEPT;

    operator const hash_digest&() const NOEXCEPT;
    operator uint256_t() const NOEXCEPT;

    friend std::istream& operator>>(std::istream& stream,
        hash256& argument) THROWS;
    friend std::ostream& operator<<(std::ostream& stream,
        const hash256& argument) NOEXCEPT;

private:
    hash_digest value_;
};
```

Extraction reports failure by throwing `istream_exception` with the
offending text. The string constructor delegates to extraction, so both
paths share one decoder. `hash256` and `hash160` use the reversed byte order
of displayed hashes (`decode_hash`, `encode_hash`).

### 1.2 Chain object wrappers

`block`, `header`, `transaction`, `input`, `output`, `point` and `script`
derive from the corresponding `chain::` class, so a parsed option is the
chain object itself. Block, header and transaction text is the base16 wire
serialization, and extraction rejects an object that does not deserialize
as valid (`src/config/header.cpp`):

```cpp
std::istream& operator>>(std::istream& stream, header& argument) THROWS
{
    std::string base16{};
    stream >> base16;

    data_chunk bytes{};
    if (!decode_base16(bytes, base16))
        throw istream_exception(base16);

    argument = chain::header{ bytes };

    if (!argument.is_valid())
        throw istream_exception(base16);

    return stream;
}
```

Script text is the opcode mnemonic form; construction from a `data_chunk`
takes the serialized script instead. Points, inputs and outputs are colon
delimited tuples (`point::delimiter`):

| Type | Text form |
| ---- | --------- |
| `point` | `txhash:index` |
| `input` | `txhash:index[:sequence]`, sequence defaults to `max_input_sequence` |
| `output` | `script:value` |

### 1.3 Network addresses

`authority`, `endpoint` and `url` parse host and port text, with IPv6 hosts
in bracketed literal form. `authority` holds an IP address, port and CIDR
suffix (`[IPv6]|IPv4[:port][/cidr]`), and its equality treats a zero port as
any port and a nonzero CIDR as subnet containment. `endpoint` holds a host
name or address with an optional port (`[scheme://]host[:port]`), and `url`
also retains the scheme. Both provide `to_local()`, which replaces a `*`
host with `localhost`. The free functions in `config/utilities.hpp` implement
the shared parsing and the denormalization of IPv4-mapped IPv6 addresses to
native IPv4. All four address types and `version` specialize `std::hash`
over their string form.

## 2. Settings

### 2.1 Chain parameters

`system::settings` (`settings.hpp`) holds the consensus parameters of a
network, populated by its `chain::selection` constructor (mainnet, testnet3,
testnet4, regtest, signet). Three of its members are config types, so they
are set from configuration text through the same stream operators:

```cpp
config::block genesis_block{};
config::script signet_challenge{};
```

```cpp
config::hash256 minimum_work{};
```

### 2.2 Bound settings

`config/setting.hpp` declares option values that are bound to a member of a
settings object and take that member's value at declaration as their
default. `setting_value<Type>` is a `program_options` `typed_value<Type>` that
also implements `printable`, so the current and default values of an option
can be reported as text:

```cpp
template <typename Type>
class setting_value
  : public boost::program_options::typed_value<Type>,
    public printable
{
public:
    setting_value(Type* store, bool secret=false) THROWS;

    string_list values() const NOEXCEPT override;

    std::string default_text() const NOEXCEPT override;

    void xparse(boost::any& value_store,
        const string_list& new_tokens) const THROWS override;
```

The factory `setting(&store)` declares a displayed setting and
`secret(&store)` one whose value is withheld: a secret reports one empty
value and empty default text. For integral types, `xparse` accepts comma
digit grouping (`1,000,000`) through `ungroup`. `is_configured` is true when
a variable was set by the command line, environment or configuration file,
and false when it is unset or holds its declared default.

`path` and `base85` provide a `program_options` `validate` overload that
assigns the token directly, since stream extraction cannot produce an empty
token. `path` extraction also reads the full line, so paths may contain
spaces.

## 3. Parsing and help

`parser` is an abstract base for an application's option parser. A derived
class supplies four sets of metadata, and the base loads each source into
one retained `variables_map`:

| Pure virtual | Source |
| ------------ | ------ |
| `load_options()` | Named command line options |
| `load_arguments()` | Positional command line arguments |
| `load_environment()` | Environment variables, under a name prefix |
| `load_settings()` | Configuration file settings, loaded once and retained |

`load_configuration_variables` reads the file named by a path option. With
no file it parses an empty stream, which populates the declared defaults.

`printer` serializes the same metadata as command line help
(`commandline`) or as a configuration settings listing (`settings`). It
normalizes each option into a `parameter` (long and short names, position,
argument limit, description, values), and `parameter::description` replaces
`{}` in an option's description with the default text of its bound setting.

## 4. Config objects

| Object | Value | Text form |
| ------ | ----- | --------- |
| `base2` | `binary` | Binary digits |
| `base16` | `data_chunk` | Hex |
| `base32` | `data_chunk` | RFC 4648 base32 |
| `base32b` | `data_chunk` | Base32 in the bech32 alphabet |
| `base58` | `data_chunk` | Base58 |
| `base64` | `data_chunk` | Base64 |
| `base85` | `data_chunk` | Z85, four byte aligned, such as keys |
| `byte` | `uint8_t` | Decimal, not a character |
| `hash160` | `short_hash` | Reversed hex |
| `hash256` | `hash_digest` | Reversed hex |
| `block` | `chain::block` | Base16 |
| `header` | `chain::header` | Base16 |
| `transaction` | `chain::transaction` | Base16 |
| `script` | `chain::script` | Mnemonic |
| `point` | `chain::point` | `txhash:index` |
| `input` | `chain::input` | `txhash:index[:sequence]` |
| `output` | `chain::output` | `script:value` |
| `authority` | Address, port and CIDR | `[IPv6]` or `IPv4`, `[:port][/cidr]` |
| `endpoint` | Scheme, host and port | `[scheme://]host[:port]` |
| `url` | Scheme, host and port | `[scheme://]host[:port]` |
| `version` | Up to four numeric segments, ordered | `major.minor[.subminor[.patch]]` |
| `path` | Filesystem path | UTF-8, may be empty or contain spaces |

## 5. Other libraries

Other libraries of the stack provide config objects in the same pattern,
each round-tripping through its stream operators.

| Library | Object | Value |
| ------- | ------ | ----- |
| libbitcoin-network | `address` | A peer address with timestamp and services, for connection and the hosts file |
| libbitcoin-network | `authority`, `endpoint` | The system `authority` and `endpoint`, extended with the P2P message address types |
| libbitcoin-network | `credential` | An HTTP basic authorization credential and its methods, `username:password[:method[,method]...]` |
| libbitcoin-explorer | `address`, `algorithm`, `btc`, `byte`, `bytes`, `ec_private`, `electrum`, `endorsement`, `hd_key`, `language`, `sighash`, `signature`, `witness`, `wrapper` | The argument types of `bx` commands |
