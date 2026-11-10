# Community Servers

## 1. Libbitcoin servers

The libbitcoin community maintains two public `bs` servers:

<div id="server-status"></div>

| Host | Address | mainnet | testnet3 | testnet4 | testnet5 |
| ---- | ------- | ------- | -------- | -------- | -------- |
| wormer.libbitcoin.net | 72.65.246.83 | – | – | – | – |
| carmine.libbitcoin.net | 72.65.246.84 | – | – | – | – |

<div id="server-details"></div>

| Host | Chain | Top | Address index | Client filters | Unpruned Above |
| ---- | ----- | --- | ------------- | -------------- | ------------ |
| [wormer.libbitcoin.net](https://wormer.libbitcoin.net:8143) | mainnet | – | – | – | – |
| [wormer.libbitcoin.net](https://wormer.libbitcoin.net:18143) | testnet3 | – | – | – | – |
| [wormer.libbitcoin.net](https://wormer.libbitcoin.net:48143) | testnet4 | – | – | – | – |
| [wormer.libbitcoin.net](https://wormer.libbitcoin.net:58143) | testnet5 | – | – | – | – |
| [carmine.libbitcoin.net](https://carmine.libbitcoin.net:8143) | mainnet | – | – | – | – |
| [carmine.libbitcoin.net](https://carmine.libbitcoin.net:18143) | testnet3 | – | – | – | – |
| [carmine.libbitcoin.net](https://carmine.libbitcoin.net:48143) | testnet4 | – | – | – | – |
| [carmine.libbitcoin.net](https://carmine.libbitcoin.net:58143) | testnet5 | – | – | – | – |

<div id="server-scan"></div>

| Service | mainnet | testnet3 | testnet4 | testnet5 |
| ------- | ------- | -------- | -------- | -------- |
| P2P network | 8333 / 8333 | 18333 / 18333 | 48333 / 48333 | 18353 / 18353 |
| ZMQ | 8380 / 8343 | 18380 / 18343 | 48380 / 48343 | 58380 / 58343 |
| Native web and REST | 8180 / 8143 | 18180 / 18143 | 48180 / 48143 | 58180 / 58143 |
| Bitcoind RPC and REST | 8280 / 8243 | 18280 / 18243 | 48280 / 48243 | 58280 / 58243 |
| BTCD RPC | 8480 / 8443 | 18480 / 18443 | 48480 / 48443 | 58480 / 58443 |
| Electrum | 8580 / 8543 | 18580 / 18543 | 48580 / 48543 | 58580 / 58543 |
| Sparrow | 8680 / 8643 | 18680 / 18643 | 48680 / 48643 | 58680 / 58643 |
| Esplora | 8780 / 8743 | 18780 / 18743 | 48780 / 48743 | 58780 / 58743 |

<style>
.scan-host { margin: 1.4em 0 .4em; font-family: var(--mono); }
#server-scan a { color: inherit; }
#server-scan .scan-up { color: var(--yes, #00bb7f); font-weight: 600; }
#server-scan .scan-down { color: var(--rejected, #ff2357); font-weight: 600; }
#server-scan .scan-wait, #server-status + .scroller .scan-wait { color: var(--ink-3); }
#server-status + .scroller .scan-up { color: var(--yes, #00bb7f); font-weight: 600; }
#server-status + .scroller .scan-down { color: var(--rejected, #ff2357); font-weight: 600; }
#server-details + .scroller table { table-layout: fixed; min-width: 640px; }
#server-details + .scroller th:first-child { width: 25%; }
#server-details + .scroller .scan-up { color: var(--yes, #00bb7f); font-weight: 600; }
#server-details + .scroller .scan-down { color: var(--rejected, #ff2357); font-weight: 600; }
.scan-some { color: var(--partial, #ffa022); font-weight: 600; }
</style>

<script>
(function () {
  var marker = document.getElementById("server-scan");
  if (!marker || !window.fetch || !window.AbortController) return;
  var scroller = marker.nextElementSibling;
  if (!scroller || !scroller.querySelector("table")) return;
  var hosts = ["wormer.libbitcoin.net", "carmine.libbitcoin.net"];
  var http = ["Native web and REST", "Bitcoind RPC and REST", "BTCD RPC", "Electrum", "Sparrow", "Esplora"];
  var genesis = {
    mainnet: "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
    testnet3: "000000000933ea01ad0ee984209779baaec3ced90fa3f408719526f8d77f4943",
    testnet4: "00000000da84f2bafbbc53dee25a72ae507ff4914b867c565be350b0da8bf043",
    testnet5: "000000000001bd3ade1e24d07c1a3677d4868c34f2f1696fa419e3b9f061b1e0"
  };
  var paths = {
    "Native web and REST": "/v1/block/height/0?format=json",
    "Bitcoind RPC and REST": function (chain) { return "/rest/block/" + genesis[chain] + ".json"; },
    "Esplora": function (chain) { return "/block/" + genesis[chain]; }
  };
  var electrum = [
    { jsonrpc: "2.0", id: 0, method: "server.version", params: ["libbitcoin.org", "1.4"] },
    { jsonrpc: "2.0", id: 1, method: "blockchain.block.header", params: [0] }
  ];
  var requests = {
    "Electrum": electrum,
    "Sparrow": electrum,
    "BTCD RPC": function (chain) { return { jsonrpc: "1.0", id: 1, method: "getblock", params: [genesis[chain], 2] }; }
  };

  function open(target, body) {
    var view = window.open("about:blank", "_blank");
    var show = function (text, type) {
      if (!view) return;
      var blob = new Blob([text], { type: type });
      view.location.href = URL.createObjectURL(blob);
    };
    fetch(target, { method: "POST", headers: { "Content-Type": "text/plain" }, body: JSON.stringify(body) })
      .then(function (response) { return response.text(); })
      .then(function (text) { show(text, "application/json"); }, function () {
        if (view) view.location.href = failure("unreadable", target);
      });
  }
  var missing = new URL("../404.html", location.href).href;

  function failure(reason, target) {
    return missing + "?reason=" + reason + "&url=" + encodeURIComponent(target);
  }
  var cache = {};

  function url(host, port, path) {
    var scheme = String(port).slice(-2) === "43" ? "https" : "http";
    return scheme + "://" + host + ":" + port + (path || "/");
  }

  function probe(host, port, path) {
    var key = host + ":" + port;
    if (cache[key]) return cache[key];
    var abort = new AbortController();
    var timer = setTimeout(function () { abort.abort(); }, 8000);
    cache[key] = fetch(url(host, port, path), { mode: "no-cors", cache: "no-store", signal: abort.signal })
      .then(function () { return "up"; }, function () { return abort.signal.aborted ? "timeout" : "failed"; })
      .then(function (state) { clearTimeout(timer); return state; });
    return cache[key];
  }

  var tally = {};
  var status = document.getElementById("server-status");
  var summary = status && status.nextElementSibling;
  var chains = [].map.call(scroller.querySelectorAll("thead th"), function (th) { return th.textContent.trim(); });

  function count(host, chain, promise) {
    var key = host + " " + chain;
    var entry = tally[key] || (tally[key] = { total: 0, up: 0, done: 0 });
    entry.total++;
    promise.then(function (state) {
      entry.done++;
      if (state === "up") entry.up++;
      show(host, chain, entry);
    });
  }

  function show(host, chain, entry) {
    if (!summary) return;
    summary.querySelectorAll("tbody tr").forEach(function (row) {
      if (row.cells[0].textContent.trim() !== host) return;
      var head = [].map.call(summary.querySelectorAll("thead th"), function (th) { return th.textContent.trim(); });
      var cell = row.cells[head.indexOf(chain)];
      if (!cell) return;
      cell.textContent = entry.up + " of " + entry.total;
      cell.className = entry.done < entry.total ? "scan-wait" :
        entry.up === entry.total ? "scan-up" : entry.up ? "scan-some" : "scan-down";
      cell.title = entry.up + " of " + entry.total + " checked ports answered";
    });
  }

  var details = document.getElementById("server-details");
  var table = details && details.nextElementSibling;
  if (table) {
    var offsets = { mainnet: 0, testnet3: 10000, testnet4: 40000, testnet5: 50000 };
    var mark = function (cell, text, state) { cell.textContent = text; cell.className = state; };
    var yes = function (cell, value) { mark(cell, value ? "Yes" : "No", value ? "scan-up" : "scan-down"); };
    table.querySelectorAll("tbody tr").forEach(function (row) {
      var host = row.cells[0].textContent.trim();
      var chain = row.cells[1].textContent.trim();
      var base = "https://" + host + ":" + (8143 + offsets[chain]);
      var get = function (target) {
        return fetch(base + target, { cache: "no-store" }).then(function (response) {
          if (!response.ok) throw new Error(response.status);
          return response.text();
        });
      };
      get("/v1/top?format=json").then(function (text) {
        row.cells[2].textContent = Number(text).toLocaleString("en-US");
      }, function () {});
      get("/v1/configuration?format=json").then(function (text) {
        var config = JSON.parse(text);
        var store = config.store || config;
        yes(row.cells[3], store.address);
        yes(row.cells[4], store.filter);
        if (store.pruned) mark(row.cells[5], Number(store.pruned).toLocaleString("en-US"), "scan-some");
        else mark(row.cells[5], "Genesis", "scan-up");
      }, function () {});
    });
  }

  hosts.forEach(function (host) {
    var heading = document.createElement("p");
    heading.className = "scan-host";
    heading.textContent = host;
    var copy = scroller.cloneNode(true);
    marker.appendChild(heading);
    marker.appendChild(copy);
    copy.querySelectorAll("tbody tr").forEach(function (row) {
      var cells = row.querySelectorAll("td");
      var service = cells[0].textContent.trim();
      var checked = http.indexOf(service) >= 0;
      var path = paths[service];
      var request = requests[service];
      for (var i = 1; i < cells.length; i++) {
        var ports = cells[i].textContent.split("/").map(function (t) { return t.trim(); });
        cells[i].textContent = "";
        var chain = chains[i];
        ports.forEach(function (port, j) {
          var where = typeof path === "function" ? path(chain) : path;
          var body = typeof request === "function" ? request(chain) : request;
          if (j) cells[i].appendChild(document.createTextNode(" / "));
          var span = document.createElement(where || request ? "a" : "span");
          span.textContent = port;
          if (where || request) {
            span.target = "_blank";
            span.rel = "noopener";
          }
          if (where) span.href = url(host, port, where);
          if (request) {
            span.href = url(host, port);
            span.addEventListener("click", function (event) {
              event.preventDefault();
              if (span.dataset.reason) window.open(failure(span.dataset.reason, url(host, port)), "_blank");
              else open(url(host, port), body);
            });
          }
          cells[i].appendChild(span);
          if (!checked || port.slice(-2) !== "43") return;
          span.className = "scan-wait";
          var result = probe(host, port, where);
          count(host, chains[i], result);
          result.then(function (state) {
            var up = state === "up";
            span.className = up ? "scan-up" : "scan-down";
            if (!up) span.dataset.reason = state;
            if (!up && where) span.href = failure(state, url(host, port, where));
            span.title = up ? "Answered" : "No answer";
          });
        });
      }
    });
  });
  scroller.style.display = "none";
})();
</script>

Both have two AMD EPYC 7F32 processors (Zen 2), 16 cores and 32
threads in all, and no GPU.

A `--hardware-optimized` build on either reports
([Command Line](command-line)):

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

## 2. Running a community server

A community server needs a DNS name for its address, a TLS certificate for
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

[zmq]
bind = 0.0.0.0:8380
bind = [::]:8380
safe = 0.0.0.0:8343
safe = [::]:8343
key = <secret key>
```

The other client services follow `[electrum]`, each on its own ports
([Conventional Ports](ports)). With no `zmq.cert` lines, any ZMQ client may connect.
Leave `[admin]` on the local machine ([Admin site](setups#5-admin-site)).

**5. Allow web pages.** The HTTP services accept cross-origin requests
from web pages on other sites ([CORS](https://fetch.spec.whatwg.org/#http-cors-protocol)).
With no `origin` setting, a service accepts a request from any page and
returns the page's origin in `Access-Control-Allow-Origin`, so a block
explorer or wallet hosted elsewhere can query the server from a browser.
To admit only particular sites, list them:

```ini
[native]
origin = explorer.example.org:443
```

Each `origin` is a host and port, without a scheme. A service with an
`origin` list also refuses the pages it serves itself, unless its own host
and port are listed.

A request from any other page is then refused. Requests that carry no
`Origin`, such as those from wallets and command line tools, are not
affected. `allow_opaque_origin` admits pages opened as local files
([HTTP services](services#4-http-services)).

**6. Publish the ZMQ public key.** TLS clients verify the server by its
certificate, but a CurveZMQ client must already hold the server's public
key. Publish the `curve-public` key beside the server's name and ports,
for clients to configure as the server key. Never publish the secret key.
