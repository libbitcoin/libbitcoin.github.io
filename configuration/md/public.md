# Public Servers

## 1. Libbitcoin servers

The libbitcoin project runs two public `bs` servers:

| Host | Address |
| ---- | ------- |
| [wormer.libbitcoin.net](http://wormer.libbitcoin.net:8180) | 72.65.246.83 |
| [carmine.libbitcoin.net](http://carmine.libbitcoin.net:8180) | 72.65.246.84 |

Both have two AMD EPYC 7F32 processors (Zen 2), 16 cores and 32
threads in all, and no GPU. A `--hardware-optimized` build on either
reports ([Command Line](command-line)):

```
$ bs --hardware
Hardware configuration (x64)...
aesni....... platform:1 compiled:1.
vaes........ platform:0 compiled:0.
shani....... platform:1 compiled:1.
sha512...... platform:0 compiled:0.
sse41....... platform:1 compiled:1.
avx2........ platform:1 compiled:1.
avx512...... platform:0 compiled:0.
avxifma..... platform:0 compiled:0.
avx512ifma.. platform:0 compiled:0.
cuda........ platform:0 compiled:1.
```

Each address serves mainnet, testnet3 and testnet4. Every chain accepts
inbound P2P connections and serves these client services on its
default ports (clear / secure):

| Service | mainnet | testnet3 | testnet4 |
| ------- | ------- | -------- | -------- |
| P2P network | 8333 | 18333 | 48333 |
| Native web and REST | 8180 / 8143 | 18180 / 18143 | 48180 / 48143 |
| Bitcoind RPC and REST | 8280 / 8243 | 18280 / 18243 | 48280 / 48243 |
| Bitcoind ZMQ | 8380 / 8343 | 18380 / 18343 | 48380 / 48343 |
| BTCD RPC | 8480 / 8443 | 18480 / 18443 | 48480 / 48443 |
| Electrum | 8580 / 8543 | 18580 / 18543 | 48580 / 48543 |
| Sparrow | 8680 / 8643 | 18680 / 18643 | 48680 / 48643 |
| Esplora | 8780 / 8743 | 18780 / 18743 | 48780 / 48743 |

## 2. Running a public server

A public server needs a DNS name for its address, a TLS certificate for
that name, and a CurveZMQ key pair. This example uses
`node.example.com` on Linux.

**1. Get a TLS certificate.** [Let's Encrypt](https://letsencrypt.org)
issues free certificates that clients trust without configuration.
[Certbot](https://certbot.eff.org) proves control of the name by
answering on port 80, which `bs` does not use. Open port 80 to the
machine, then:

```
$ sudo certbot certonly --standalone --key-type ecdsa \
    --elliptic-curve secp256r1 -d node.example.com
```

`bs` accepts ECDSA keys on P-256 or P-384, not RSA. Certbot writes the
certificate chain and its key to `/etc/letsencrypt/live/node.example.com/`,
readable only by root. Copy them where `bs` runs, owned by its user:

```
$ sudo install -o bitcoin -m 600 \
    /etc/letsencrypt/live/node.example.com/fullchain.pem \
    /etc/letsencrypt/live/node.example.com/privkey.pem ~bitcoin/
```

**2. Renew it.** Let's Encrypt certificates last 90 days, and certbot
renews them automatically, again over port 80. `bs` reads its
certificates when it starts, so each renewal must copy the new files and
restart `bs`. Certbot runs a deploy hook after each renewal; place the
`install` command above, followed by the restart, in
`/etc/letsencrypt/renewal-hooks/deploy/bs.sh`.

> **Note.** `bx` is not quite ready yet. The commands used here are not
> yet available in a `bx` release.

**3. Create the CurveZMQ key pair.** `bx curve-new` makes a server secret
key from 256 bits of entropy. `bx dice-rolls` gives the number of
throws, 256 for a coin, and `bx dice-entropy` converts them. Flip a coin
that many times, write the flips down as one string of digits (heads 1,
tails 0), and convert them:

```
$ bx dice-rolls --sides 2 --bits 256
$ bx dice-entropy --sides 2 1101001110...
$ bx curve-new <entropy>
$ bx curve-public '<secret key>'
```

A die of up to 16 sides also works. Write each roll as one 0-based digit,
using `a` to `f` above 9, and give its sides to both commands. For
example, a six-sided die takes `--sides 6` and 102 rolls. `dice-entropy`
rejects a sequence that would bias the entropy, which must then be
rolled again.

`curve-new` prints the secret key and `curve-public` its public key, both
Z85 encoded. Z85 includes `#`, which a configuration file reads as a
comment, so `curve-new` reports `The entropy produced an invalid key.`
when either key contains one, and the coin must be flipped again. Quote
the keys on the command line, as they contain shell characters.

**4. Configure the services.** Bind each service on every adapter, clear
and secure, with the certificate and key from step 1 and the ZMQ secret
key from step 3:

```ini
[inbound]
bind = 0.0.0.0:8333
bind = [::]:8333

[electrum]
bind = 0.0.0.0:8580
bind = [::]:8580
safe = 0.0.0.0:8543
safe = [::]:8543
cert_path = fullchain.pem
key_path = privkey.pem

[bitcoind_zmq]
bind = 0.0.0.0:8380
bind = [::]:8380
safe = 0.0.0.0:8343
safe = [::]:8343
key = <secret key>
```

The other client services follow `[electrum]`, each on its own ports
([Conventional Ports](ports)). With no `bitcoind_zmq.cert` lines, any ZMQ client may connect.
Leave `[admin]` on the local machine ([Admin site](setups#5-admin-site)).

**5. Publish the ZMQ public key.** TLS clients verify the server by its
certificate, but a CurveZMQ client must already hold the server's public
key. Publish the `curve-public` key beside the server's name and ports,
for clients to configure as the server key. Never publish the secret key.
