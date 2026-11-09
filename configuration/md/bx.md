# BX Settings

## 1. The configuration file

Bitcoin Explorer (`bx`) runs with built-in mainnet defaults, and reads no
configuration file unless one is given. Every command accepts
`-c <path>` (`--config <path>`), or the path can be set in the `BX_CONFIG`
environment variable:

```
$ bx fetch-height --config bx.cfg
$ export BX_CONFIG=~/bx.cfg
$ bx fetch-height
```

A command line option takes precedence over a configuration setting.
The file uses the same syntax as the `bs` configuration file
([Configuration File](file)).

## 2. Displaying settings

`bx settings` prints every setting with the value in effect, in
configuration file form:

```
$ bx settings --config bx.cfg
```

## 3. Settings

| Setting | Default | Purpose |
| ------- | ------- | ------- |
| `wallet.witness_version` | `0` | The witness version. |
| `wallet.witness_address_prefix` | `bc` | The witness address prefix. |
| `wallet.wif_version` | `128` | The wallet import format (WIF) key version. |
| `wallet.hd_public_version` | `76067358` | The HD public key version (`xpub`). |
| `wallet.hd_secret_version` | `76066276` | The HD private key version (`xprv`). |
| `wallet.pay_to_public_key_hash_version` | `0` | The pay-to-public-key-hash address version. |
| `wallet.pay_to_script_hash_version` | `5` | The pay-to-script-hash address version. |
| `wallet.transaction_version` | `1` | The version of transactions `bx` creates. |
| `wallet.rule_fork_flags` | `4294967295` | The consensus rule forks applied to scripts, all by default. |
| `server.url` | `http://mainnet.libbitcoin.net:8181` | The `bs` native interface used by the `fetch-*` commands. |
| `server.connect_retries` | `0` | The number of times to retry contacting the server. |
| `server.connect_timeout_seconds` | `5` | The time limit for each step of a request. |

A `fetch-*` command also accepts a server URL on its command line, which
takes precedence over `server.url`.

## 4. Testnet and a local server

The `[wallet]` settings select the encodings of keys and addresses. For
testnet3, with a local `bs` serving its native interface
([Block explorer](setups#6-block-explorer)):

```ini
[wallet]
witness_address_prefix = tb
wif_version = 239
hd_public_version = 70617039
hd_secret_version = 70615956
pay_to_public_key_hash_version = 111
pay_to_script_hash_version = 196

[server]
url = http://127.0.0.1:18180
```

The same `[wallet]` settings apply to testnet4, testnet5 and signet, and to regtest
with `bcrt` as its witness address prefix. The server port is the `bs`
native port on the chain: `18180` on testnet3, `48180` on testnet4,
`58180` on testnet5, `38180` on signet and `28180` on regtest ([Conventional Ports](ports)).
