# Conventional Ports

Every service has an assigned port on each chain, clear and secure. A
service listens only on the addresses given by its `bind` and `safe`
settings ([Listening](services#1-listening)), so the examples on this page give them explicitly.

The P2P network uses its convention on each chain, so peers find the
node without configuration. Each libbitcoin service uses its own block,
`8N80` for clear connections and `8N43` for secure (TLS), so that `bs` can run
beside `bitcoind`, Electrum servers and Esplora on one machine without
conflict.

| Service | Section | Clear | Secure |
| ------- | ------- | ----- | ------ |
| P2P network | `[inbound]` | 8333 | 8333 |
| Admin web | `[admin]` | 8080 | 8043 |
| Native web and REST | `[native]` | 8180 | 8143 |
| Bitcoind RPC and REST | `[bitcoind]` | 8280 | 8243 |
| ZMQ | `[zmq]` | 8380 | 8343 |
| BTCD RPC | `[btcd]` | 8480 | 8443 |
| Electrum | `[electrum]` | 8580 | 8543 |
| Sparrow | `[sparrow]` | 8680 | 8643 |
| Esplora | `[esplora]` | 8780 | 8743 |
| Stratum v1 | `[stratum_v1]` | 8880 | 8843 |
| Stratum v2 | `[stratum_v2]` | 8980 | – |

P2P has no separate secure port. BIP324 encryption is negotiated on the
same port, and offered when `node.provide_privacy` is set. ZMQ's secure
port uses CurveZMQ.

On the test chains the service ports move by a fixed offset, and the P2P
port follows its network's convention:

| Chain | Service offset | Services | P2P |
| ----- | -------------- | -------- | --- |
| mainnet | 0 | 8043–8980 | 8333 |
| testnet3 | +10000 | 18043–18980 | 18333 |
| regtest | +20000 | 28043–28980 | 18444 |
| signet | +30000 | 38043–38980 | 38333 |
| testnet4 | +40000 | 48043–48980 | 48333 |
| testnet5 | +50000 | 58043–58980 | 18353 |

To use a service as a drop-in replacement, bind it to the port its
clients expect instead:

```ini
[bitcoind]
bind = 127.0.0.1:8332
bind = [::1]:8332

[btcd]
safe = 127.0.0.1:8334
safe = [::1]:8334

[electrum]
bind = 0.0.0.0:50001
safe = 0.0.0.0:50002

[esplora]
bind = 127.0.0.1:3000
bind = [::1]:3000
```

A section may list several `bind` and `safe` lines, and listens on all
of them. This Electrum server accepts clients on its default ports and
on the conventional ones, over IPv4 and IPv6:

```ini
[electrum]
bind = 0.0.0.0:8580
bind = [::]:8580
bind = 0.0.0.0:50001
bind = [::]:50001
safe = 0.0.0.0:8543
safe = [::]:8543
safe = 0.0.0.0:50002
safe = [::]:50002
connections = 100
cert_path = server.pem
key_path = server.key
```

And this RPC interface listens on the local machine and on one private
network address only:

```ini
[bitcoind]
bind = 127.0.0.1:8280
bind = [::1]:8280
bind = 192.168.0.10:8280
connections = 10
credential = user:password
```
