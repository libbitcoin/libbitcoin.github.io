# Commands

<div class="banner"><strong>Bitcoin Explorer (<code>bx</code>) for version 4 is in development.</strong> Commands may be incomplete or change before release.</div>

Bitcoin Explorer (`bx`) is the libbitcoin command line client. Its
commands work offline, on keys, addresses, transactions, scripts and
encodings, and online, querying a libbitcoin server. It is built on
libbitcoin-explorer, which depends on libbitcoin-system alone (see
[Developers](../developers/index)).

Each command is run as `bx <command>`, with `bx <command> --help`
describing its arguments. Commands read their main argument from the
command line or from standard input, so they can be piped together. For
example, the key at BIP32 path `m/0'/1` of a seed, and its legacy and
segwit addresses:

```
$ bx hd-new 000102030405060708090a0b0c0d0e0f | bx hd-private --hard --index 0 | bx hd-private --index 1 | bx hd-to-ec | bx ec-to-public
03501e454bf00751f24b1b489aa925215d66af2234e3891c3b21a52bedb3cd711c

$ bx ec-to-address 03501e454bf00751f24b1b489aa925215d66af2234e3891c3b21a52bedb3cd711c
1JQheacLPdM5ySCkrZkV66G2ApAXe1mqLj

$ bx ec-to-witness bc 03501e454bf00751f24b1b489aa925215d66af2234e3891c3b21a52bedb3cd711c
bc1qhm6697d9d2224vfyt8mj4kw03ncec7a7fdafvt
```

## 1. Commands

109 commands, by category:

| Category | Commands |
| -------- | -------- |
| [Wallet](#2-wallet) | 31 |
| [Key encryption](#3-key-encryption) | 9 |
| [Stealth](#4-stealth) | 3 |
| [Transaction](#5-transaction) | 8 |
| [Messaging](#6-messaging) | 2 |
| [Online](#7-online) | 26 |
| [Encoding](#8-encoding) | 12 |
| [Hash](#9-hash) | 6 |
| [Math](#10-math) | 10 |
| [Meta](#11-meta) | 2 |

## 2. Wallet

| Command | Description |
| ------- | ----------- |
| `address-decode` | Convert a payment address to its component parts. |
| `address-embed` | Create a pay-to-public-key-hash payment address with an embedded record of binary data. WARNING: any coin spent to this address is lost. |
| `address-encode` | Convert a RIPEMD160 value to a payment address. |
| `address-to-key` | Derive the payments search key of a payment address. |
| `dice-entropy` | Convert a sequence of dice rolls to Base16 data. |
| `ec-decompress` | Decompress a compressed EC public key. |
| `ec-new` | Create a new Base16 EC private key from entropy. |
| `ec-to-address` | Create a pay-to-public-key-hash address from an EC public key. |
| `ec-to-public` | Derive the EC public key of an EC private key. Defaults to the compressed public key format. |
| `ec-to-wif` | Convert an EC private key to a WIF private key. The result associates with the compressed public key format by default. |
| `ec-to-witness` | Create a BIP173 pay-to-witness-public-key-hash address from an EC public key. |
| `electrum-decode` | Convert an Electrum mnemonic to its numeric entropy. Entropy round-trips with the electrum-new command. |
| `electrum-new` | Create an Electrum mnemonic from entropy. After the mnemonic is created, entropy round-trips with the electrum-decode command. |
| `electrum-to-seed` | Convert an Electrum dictionary-based mnemonic to a wallet seed. Entropy cannot be derived from the seed. WARNING: mnemonic should be created from properly generated entropy. |
| `hd-new` | Create a new HD (BIP32) private key from entropy. |
| `hd-private` | Derive a child HD (BIP32) private key from another HD private key. |
| `hd-public` | Derive a child HD (BIP32) public key from another HD public or private key. |
| `hd-to-ec` | Convert a HD (BIP32) public or private key to the equivalent EC public or private key. |
| `hd-to-public` | Derive the HD (BIP32) public key of a HD private key. |
| `mnemonic-decode` | Convert a BIP39 mnemonic to its numeric entropy. |
| `mnemonic-encode` | Convert numeric entropy to its BIP39 mnemonic. |
| `mnemonic-to-seed` | Convert a BIP39 dictionary-based mnemonic to a wallet seed. Entropy cannot be derived from the seed. WARNING: mnemonic should be created from properly generated entropy. |
| `qrcode` | Create a square QRCODE TIFF file for a payment address. |
| `script-to-address` | Create a BIP16 pay-to-script-hash address from a script. |
| `script-to-key` | Derive the payments search key of an output script. |
| `script-to-witness` | Create a BIP173 pay-to-witness-script-hash address from a script. |
| `uri-decode` | Decompose a Bitcoin URI into its parts. |
| `uri-encode` | Compose a Bitcoin URI from specified parts. |
| `wif-to-ec` | Convert a WIF private key to an EC private key. |
| `wif-to-public` | Derive the EC public key from a WIF private key. |
| `witness-to-key` | Derive the payments search key of a witness address. |

## 3. Key encryption

| Command | Description |
| ------- | ----------- |
| `ec-to-ek` | Encrypt an EC private key as an encrypted private key (BIP38). |
| `ek-address` | Create a payment address derived from an intermediate passphrase token (BIP38). |
| `ek-new` | Create an encrypted private key from an intermediate passphrase token (BIP38). |
| `ek-public` | Create an encrypted public key from an intermediate passphrase token (BIP38). |
| `ek-public-to-address` | Extract the payment address of an encrypted public key (BIP38). |
| `ek-public-to-ec` | Extract the EC public key of an encrypted public key (BIP38).  |
| `ek-to-address` | Extract the payment address of an encrypted private key (BIP38). |
| `ek-to-ec` | Recover the EC private key from an encrypted private key (BIP38). |
| `token-new` | Create an intermediate passphrase token for deferred encrypted key generation (BIP38). |

## 4. Stealth

| Command | Description |
| ------- | ----------- |
| `stealth-public` | Derive the stealth public key necessary to address and to identify a stealth payment. |
| `stealth-secret` | Derive the stealth private key necessary to spend a stealth payment. |
| `stealth-shared` | Derive the secret shared between an ephemeral key pair and a scan key pair. Provide scan SECRET and ephemeral PUBKEY, or ephemeral SECRET and scan PUBKEY. |

## 5. Transaction

| Command | Description |
| ------- | ----------- |
| `input-set` | Assign a script to an existing transaction input. |
| `input-sign` | Create an endorsement for a transaction input. |
| `input-validate` | Validate a transaction input endorsement. |
| `script-decode` | Decode a script to plain text tokens. |
| `script-encode` | Base16 encode a plain text script. |
| `tx-decode` | Decode a Base16 transaction. |
| `tx-encode` | Encode an unsigned transaction as Base16. |
| `tx-sign` | Sign a set of transactions using a private key. Output is suitable for sending to Bitcoin network. |

## 6. Messaging

| Command | Description |
| ------- | ----------- |
| `message-sign` | Create a message signature. |
| `message-validate` | Validate a message signature. |

## 7. Online

| Command | Description |
| ------- | ----------- |
| `broadcast-tx` | Broadcast a transaction to the Bitcoin network via the Bitcoin peer-to-peer network. |
| `fetch-balance` | Get the balance in satoshi of a payment address. Requires a Libbitcoin server connection. |
| `fetch-block` | Get the block from the specified hash or height. Height is ignored if both are specified. Requires a Libbitcoin server connection. |
| `fetch-block-hashes` | Get the block from the specified hash or height. Height is ignored if both are specified. Requires a Libbitcoin server connection. |
| `fetch-block-height` | Get the block height from the specified hash. Requires a Libbitcoin server connection. |
| `fetch-filter` | Retrieve compact filters from a Libbitcoin server. |
| `fetch-filter-checkpoint` | Retrieve compact filter checkpoint from a Libbitcoin server. |
| `fetch-filter-headers` | Retrieve compact filter headers from a Libbitcoin server. The distance between provided height and hash must be strictly less than 2000. |
| `fetch-header` | Get the block header from the specified hash or height. Height is ignored if both are specified. Requires a Libbitcoin server connection. |
| `fetch-height` | Get the last block height. Requires a Libbitcoin server connection. |
| `fetch-history` | Get list of output points, values, and spends for a payment key. Requires a Libbitcoin server connection. |
| `fetch-public-key` | Get the EC public key of the address, if it exists on the blockchain. Requires a Libbitcoin server connection. |
| `fetch-tx` | Get a transaction by its hash. Requires a Libbitcoin server connection. |
| `fetch-tx-index` | Get the block height and index of a transaction. Requires a Libbitcoin server connection. |
| `fetch-utxo` | Get enough unspent transaction outputs from a payment address to pay a number of satoshi. Requires a Libbitcoin server connection. |
| `get-filter-checkpoint` | Retrieve compact filter checkpoint from a single Bitcoin network node. |
| `get-filter-headers` | Retrieve compact filter headers from a single Bitcoin network node. The distance between provided height and hash must be strictly less than 2000. |
| `get-filters` | Retrieve compact filters from a single Bitcoin network node. The distance between provided height and hash must be strictly less than 100. |
| `put-tx` | Broadcast a transaction to the Bitcoin network via a single Bitcoin network node. |
| `send-tx` | Broadcast a transaction to the Bitcoin network via a Libbitcoin server. |
| `subscribe-block` | Watch the network for all blocks. Requires a Libbitcoin server connection. |
| `subscribe-tx` | Watch the network for all transactions. Requires a Libbitcoin server connection. |
| `validate-tx` | Determine if a transaction is valid for submission to the blockchain. Requires a Libbitcoin server connection. |
| `version` | Fetch and display the libbitcoin server and client versions. Requires a Libbitcoin server connection. |
| `watch-key` | Watch the network for transactions in which a payment key participates. Requires a Libbitcoin server connection. |
| `watch-tx` | Watch the network for a transaction by hash. Requires a Libbitcoin server connection. |

## 8. Encoding

| Command | Description |
| ------- | ----------- |
| `base16-decode` | Convert a Base16 value to binary data. |
| `base16-encode` | Convert binary data to Base16. |
| `base32-decode` | Convert a Base32 value to binary data. |
| `base32-encode` | Convert binary data to Base32. |
| `base58-decode` | Convert a Base58 value to Base16. |
| `base58-encode` | Convert a Base16 value to Base58. |
| `base64-decode` | Convert a Base64 value to binary data. |
| `base64-encode` | Convert binary data to Base64. |
| `bech32-decode` | Validate the bech32 checksum of Base16 data and recover its witness prefix, version and program. |
| `bech32-encode` | Add a prefix, version byte and checksum to a Base32 witness program. |
| `checked-decode` | Validate the bitcoin checksum of Base16 data and recover its version and payload. |
| `checked-encode` | Add a version byte and bitcoin checksum to Base16 data. |

## 9. Hash

| Command | Description |
| ------- | ----------- |
| `bitcoin160` | Perform a RIPEMD160 hash of a SHA256 hash of Base16 data. |
| `bitcoin256` | Perform a SHA256 hash of a SHA256 hash of Base16 data and then reverse the byte order. |
| `ripemd160` | Perform a RIPEMD160 hash of Base16 data. |
| `sha160` | Perform a SHA160 (also known as SHA-1) hash of Base16 data. |
| `sha256` | Perform a SHA256 hash of Base16 data. |
| `sha512` | Perform a SHA512 hash of Base16 data. |

## 10. Math

| Command | Description |
| ------- | ----------- |
| `btc-to-satoshi` | Convert BTC to satoshi. |
| `cert-new` | Create a Base85 Curve ZMQ private key for use with a Libbitcoin server. WARNING: entropy is obtained from the underlying platform. |
| `cert-public` | Derive a Base85 Curve ZMQ public key for use with a Libbitcoin server. |
| `ec-add` | Calculate the EC function POINT + (SECRET * curve-generator-point). |
| `ec-add-secrets` | Calculate the EC function (SECRET + SECRET) % curve-order. |
| `ec-multiply` | Calculate the EC product (POINT * SECRET). |
| `ec-multiply-secrets` | Calculate the EC function (SECRET * SECRET) % curve-order. |
| `match-neutrino-address` | Determine whether the provided client filter probabilistically matches the provided payment address. |
| `match-neutrino-script` | Determine whether the provided client filter probabilistically matches the provided script. |
| `satoshi-to-btc` | Convert satoshi to BTC. |

## 11. Meta

| Command | Description |
| ------- | ----------- |
| `help` | Get the list of commands. |
| `settings` | Display the loaded configuration settings. |
