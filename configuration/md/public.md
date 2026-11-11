# Community Servers

## 1. Libbitcoin servers

The libbitcoin community maintains two public `bs` servers. Both have
two AMD EPYC 7F32 processors (Zen 2), 16 cores and 32 threads in all,
and no GPU.

<div id="server-status"></div>

| Host | Address | mainnet | testnet3 | testnet4 | testnet5 |
| ---- | ------- | ------- | -------- | -------- | -------- |
| wormer.libbitcoin.net | 72.65.246.83 | – | – | – | – |
| carmine.libbitcoin.net | 72.65.246.84 | – | – | – | – |

<div id="server-details"></div>

| Host | Network | Top | Turbo<br>(parallel queries) | Address index (Genesis) | Client filters (Genesis) | Silent Payments From | Whole Blocks<br>From |
| ---- | ----- | --- | ----- | ------------- | -------------- | --------------- | ------------ |
| [wormer](https://wormer.libbitcoin.net:8143) | mainnet | – | – | – | – | – | – |
| [wormer](https://wormer.libbitcoin.net:18143) | testnet3 | – | – | – | – | – | – |
| [wormer](https://wormer.libbitcoin.net:48143) | testnet4 | – | – | – | – | – | – |
| [wormer](https://wormer.libbitcoin.net:58143) | testnet5 | – | – | – | – | – | – |
| [carmine](https://carmine.libbitcoin.net:8143) | mainnet | – | – | – | – | – | – |
| [carmine](https://carmine.libbitcoin.net:18143) | testnet3 | – | – | – | – | – | – |
| [carmine](https://carmine.libbitcoin.net:48143) | testnet4 | – | – | – | – | – | – |
| [carmine](https://carmine.libbitcoin.net:58143) | testnet5 | – | – | – | – | – | – |

<div id="server-p2p"></div>

| Host | Network | Protocol version | Serves blocks from | Tx relay (BIP37) | Witness node (BIP144) | Address gossip (BIP155) | Compact blocks (BIP152) | Client filters (BIP157) | P2P encryption (BIP324) | Mempool message (BIP35) | Wtxid relay (BIP339) |
| ---- | ------- | ---------------- | ----------------- | -------------- | ------ | ------- | ----------------------- | ------------------- | ----------------------- | -------------------- | --------------- |
| wormer | mainnet | – | – | – | – | – | – | – | – | – | – |
| wormer | testnet3 | – | – | – | – | – | – | – | – | – | – |
| wormer | testnet4 | – | – | – | – | – | – | – | – | – | – |
| wormer | testnet5 | – | – | – | – | – | – | – | – | – | – |
| carmine | mainnet | – | – | – | – | – | – | – | – | – | – |
| carmine | testnet3 | – | – | – | – | – | – | – | – | – | – |
| carmine | testnet4 | – | – | – | – | – | – | – | – | – | – |
| carmine | testnet5 | – | – | – | – | – | – | – | – | – | – |

<div id="server-scan"></div>

| Service | mainnet | testnet3 | testnet4 | testnet5 |
| ------- | ------- | -------- | -------- | -------- |
| P2P | 8333 / 8333 | 18333 / 18333 | 48333 / 48333 | 18353 / 18353 |
| ZMQ | 8380 / 8343 | 18380 / 18343 | 48380 / 48343 | 58380 / 58343 |
| Native | 8180 / 8143 | 18180 / 18143 | 48180 / 48143 | 58180 / 58143 |
| Bitcoind | 8280 / 8243 | 18280 / 18243 | 48280 / 48243 | 58280 / 58243 |
| BTCD | 8480 / 8443 | 18480 / 18443 | 48480 / 48443 | 58480 / 58443 |
| Electrum | 8580 / 8543 | 18580 / 18543 | 48580 / 48543 | 58580 / 58543 |
| Sparrow | 8680 / 8643 | 18680 / 18643 | 48680 / 48643 | 58680 / 58643 |
| Esplora | 8780 / 8743 | 18780 / 18743 | 48780 / 48743 | 58780 / 58743 |

To connect to a secure ZMQ port, a client must be configured with the server's public key:

<div id="zmq-keys"></div>

| Host | ZMQ base85 public key |
| ---- | --------------------- |
| wormer.libbitcoin.net | `>XrBaljAIXUrrCt(y^(i-@2mUY-4]lj=:DSoFWns` |
| carmine.libbitcoin.net | `ihZy(J.QWwNe(L9uUMyI8GH0<vW=kHJ9PLdBle8:` |

<style>
#server-scan .scroller th { white-space: normal; vertical-align: bottom; }
#server-scan .scroller th, #server-scan .scroller td { padding-left: 5px; padding-right: 5px; white-space: nowrap; }
#server-scan .scroller th:first-child { position: relative; padding-top: 2.4em; }
#server-scan .scroller td:nth-child(n+3) { font-family: var(--mono); font-size: 12px; font-weight: 300; line-height: 18px; text-align: center; }
#server-scan .scroller th:nth-child(n+3) { text-align: center; }
#server-scan .scroller td:nth-child(n+3) > :is(a, span) { display: inline-block; width: 5ch; text-align: right; vertical-align: top; }
#server-scan .table-title { position: absolute; top: 10px; left: 8px; color: var(--ink); }
.doc .tip, #server-scan span[title]:not([title=""]) { cursor: default; text-decoration: underline dotted; text-underline-offset: 3px; }
#server-scan a { color: inherit; text-decoration: none; }
#server-scan a:hover { text-decoration: underline; }
#server-scan .scan-up { color: var(--yes, #00bb7f); }
#server-scan .scan-down { color: var(--rejected, #ff2357); }
#server-scan .scan-wait, #server-status + .scroller .scan-wait { color: var(--ink-3); }
#server-status + .scroller .scan-up { color: var(--yes, #00bb7f); font-weight: 600; }
#server-status + .scroller .scan-down { color: var(--rejected, #ff2357); font-weight: 600; }
#server-details + .scroller table { table-layout: fixed; min-width: 640px; }
#server-details + .scroller th { white-space: normal; vertical-align: bottom; }
#server-details + .scroller th:first-child, #server-p2p + .scroller th:first-child, #server-scan .scroller th:first-child { width: 72px; }
#server-details + .scroller th:nth-child(2), #server-p2p + .scroller th:nth-child(2), #server-scan .scroller th:nth-child(2) { width: 72px; }
#server-details + .scroller :is(th, td):nth-child(-n+2), #server-p2p + .scroller :is(th, td):nth-child(-n+2), #server-scan .scroller :is(th, td):nth-child(-n+2) { padding-left: 8px; padding-right: 8px; }
#server-p2p + .scroller td:first-child { white-space: nowrap; }
#server-details + .scroller .scan-up { color: var(--yes, #00bb7f); font-weight: 600; }
#server-details + .scroller .scan-down { color: var(--rejected, #ff2357); font-weight: 600; }
#server-p2p + .scroller table { min-width: 760px; }
#server-p2p + .scroller th { white-space: normal; vertical-align: bottom; }
#server-p2p + .scroller th, #server-p2p + .scroller td { padding-left: 8px; padding-right: 8px; }
#server-p2p + .scroller .scan-up { color: var(--yes, #00bb7f); font-weight: 600; }
#server-details + .scroller th:first-child, #server-p2p + .scroller th:first-child { position: relative; }
#server-details + .scroller .table-title, #server-p2p + .scroller .table-title { position: absolute; top: 10px; left: 8px; color: var(--ink); }
.scan-some { color: var(--partial, #ffa022); font-weight: 600; }
#zmq-keys + .scroller .copy { position: static; margin-left: .6em; padding: 3px; vertical-align: middle; }
</style>

<script>
(function () {
  var marker = document.getElementById("zmq-keys");
  if (!marker || !navigator.clipboard) return;
  marker.nextElementSibling.querySelectorAll("td code").forEach(function (code) {
    var button = document.createElement("button");
    button.type = "button";
    button.className = "copy";
    button.title = "Copy";
    button.setAttribute("aria-label", "Copy");
    button.innerHTML = '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><rect x="5.5" y="5.5" width="8.5" height="8.5" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M10.5 5.5V3.5a1.5 1.5 0 0 0-1.5-1.5H3.5A1.5 1.5 0 0 0 2 3.5V9a1.5 1.5 0 0 0 1.5 1.5h2" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>';
    button.addEventListener("click", function () {
      navigator.clipboard.writeText(code.textContent).then(function () {
        button.classList.add("done");
        button.title = "Copied";
        setTimeout(function () { button.classList.remove("done"); button.title = "Copy"; }, 1500);
      });
    });
    code.parentNode.appendChild(button);
  });
})();
</script>

<script>
(function () {
  function hint(cell, text) {
    var span = cell.querySelector(".tip");
    if (!text) {
      if (span) cell.textContent = span.textContent;
      return;
    }
    if (!span) {
      span = document.createElement("span");
      span.className = "tip";
      while (cell.firstChild) span.appendChild(cell.firstChild);
      cell.appendChild(span);
    }
    span.title = text;
  }
  var marker = document.getElementById("server-scan");
  if (!marker || !window.fetch || !window.AbortController) return;
  var scroller = marker.nextElementSibling;
  if (!scroller || !scroller.querySelector("table")) return;
  var hosts = ["wormer.libbitcoin.net", "carmine.libbitcoin.net"];
  var http = ["Native", "Bitcoind", "BTCD", "Electrum", "Sparrow", "Esplora"];
  var genesis = {
    mainnet: "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
    testnet3: "000000000933ea01ad0ee984209779baaec3ced90fa3f408719526f8d77f4943",
    testnet4: "00000000da84f2bafbbc53dee25a72ae507ff4914b867c565be350b0da8bf043",
    testnet5: "000000000001bd3ade1e24d07c1a3677d4868c34f2f1696fa419e3b9f061b1e0"
  };
  var paths = {
    "Native": "/v1/block/height/0?format=json",
    "Bitcoind": function (chain) { return "/rest/block/" + genesis[chain] + ".json"; },
    "Esplora": function (chain) { return "/block/" + genesis[chain]; }
  };
  var electrum = [
    { jsonrpc: "2.0", id: 0, method: "server.version", params: ["libbitcoin.org", "1.4"] },
    { jsonrpc: "2.0", id: 1, method: "blockchain.block.header", params: [0] }
  ];
  var requests = {
    "Electrum": electrum,
    "Sparrow": electrum,
    "BTCD": function (chain) { return { jsonrpc: "1.0", id: 1, method: "getblock", params: [genesis[chain], 2] }; }
  };

  function popup(target) {
    return window.open(target, "server-query", "popup,width=540,height=450");
  }

  function pretty(text) {
    try {
      return JSON.stringify(JSON.parse(text), null, 2);
    } catch (e) {
      try {
        return text.split("\n").filter(function (line) { return line.trim(); })
          .map(function (line) { return JSON.stringify(JSON.parse(line), null, 2); }).join("\n");
      } catch (e2) {
        return text;
      }
    }
  }

  function escape(text) {
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function open(target, body, title) {
    if (target.indexOf("http:") === 0) {
      popup(body === undefined ? target : failure("insecure", target));
      return;
    }
    var view = popup("about:blank");
    var show = function (text) {
      if (!view) return;
      var page = "<!doctype html><meta charset=\"utf-8\"><title>" + escape(title) +
        "</title><style>:root{color-scheme:light dark}body{margin:0}" +
        "pre{margin:0;padding:12px;font:13px/1.4 ui-monospace,Consolas,monospace}</style><pre>" +
        escape(pretty(text)) + "</pre>";
      var blob = new Blob([page], { type: "text/html;charset=utf-8" });
      view.location.href = URL.createObjectURL(blob);
    };
    var options = body === undefined ? { cache: "no-store" } :
      { method: "POST", headers: { "Content-Type": "text/plain" }, body: JSON.stringify(body) };
    fetch(target, options)
      .then(function (response) { return response.text(); })
      .then(show, function () {
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
      hint(cell, entry.up + " of " + entry.total + " checked ports answered");
    });
  }

  var details = document.getElementById("server-details");
  var table = details && details.nextElementSibling;
  if (table) {
    var offsets = { mainnet: 0, testnet3: 10000, testnet4: 40000, testnet5: 50000 };
    var mark = function (cell, text, state, tip) { cell.textContent = text; cell.className = state; hint(cell, tip); };
    var taproot = { mainnet: 709632, testnet3: 2011968, testnet4: 0, testnet5: 0 };
    var window_ = 24 * 60 * 60 * 1000;
    var tops = {};
    var agree = function (chain, row, hash) {
      var seen = tops[chain] || (tops[chain] = []);
      seen.push({ row: row, hash: hash });
      if (!seen.some(function (top) { return top.hash !== seen[0].hash; })) return;
      var tip = "The hosts have different top blocks: " + seen.map(function (top) {
        return top.row.cells[0].textContent.trim() + " " + top.hash.slice(0, 16) + "…";
      }).join(", ");
      seen.forEach(function (top) { top.row.cells[1].className = "scan-down"; hint(top.row.cells[1], tip); });
    };
    var yes = function (cell, value, name) { mark(cell, value ? "Yes" : "No", value ? "scan-up" : "scan-down", value ? "" : "The " + name + " is not enabled"); };
    var title = function (scroller, text) {
      var cell = scroller && scroller.querySelector("thead th");
      if (!cell) return;
      var label = document.createElement("span");
      label.className = "table-title";
      label.textContent = text;
      cell.insertBefore(label, cell.firstChild);
    };
    title(table, "Store");
    title(document.getElementById("server-p2p").nextElementSibling, "P2P");
    var p2p = document.getElementById("server-p2p");
    var peers = {};
    if (p2p && p2p.nextElementSibling) p2p.nextElementSibling.querySelectorAll("tbody tr").forEach(function (row) {
      peers[row.cells[0].textContent.trim() + ".libbitcoin.net " + row.cells[1].textContent.trim()] = row;
    });
    var feature = function (cell, value) { mark(cell, value ? "Yes" : "No", value ? "scan-up" : "scan-some"); };
    var currency = {};
    var gated = [3, 4, 5, 7, 8, 10, 11];
    var settle = function (key, current) {
      var entry = currency[key] || (currency[key] = {});
      if (current !== undefined) entry.current = current;
      else entry.features = true;
      if (!entry.features || entry.current !== false || !peers[key]) return;
      gated.forEach(function (index) {
        var cell = peers[key].cells[index];
        if (cell.className !== "scan-up") return;
        cell.className = "scan-some";
        hint(cell, "Inactive until current");
      });
    };
    var features = function (row, node, network, store) {
      mark(row.cells[2], String(network.protocol_maximum), "");
      hint(row.cells[2], "Protocol versions " + network.protocol_minimum + " to " + network.protocol_maximum);
      if (!node.blocks) mark(row.cells[3], "No", "scan-some");
      else if (node.limited) mark(row.cells[3], (Number(store.pruned) + 1).toLocaleString("en-US"), "scan-some");
      else mark(row.cells[3], "Genesis", "scan-up");
      feature(row.cells[4], network.relay);
      feature(row.cells[5], node.witness);
      feature(row.cells[6], network.address);
      feature(row.cells[7], network.compact);
      feature(row.cells[8], node.filters);
      feature(row.cells[9], node.privacy);
      feature(row.cells[10], network.memory_pool);
      feature(row.cells[11], network.witness_tx);
    };
    table.querySelectorAll("tbody tr").forEach(function (row) {
      var host = row.cells[0].textContent.trim() + ".libbitcoin.net";
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
        return get("/v1/block/height/" + Number(text) + "/header?format=json");
      }).then(function (text) {
        var header = JSON.parse(text);
        var current = header.timestamp * 1000 >= Date.now() - window_;
        settle(host + " " + chain, current);
        row.cells[2].className = current ? "scan-up" : "scan-some";
        hint(row.cells[2], "Top block time " + new Date(header.timestamp * 1000).toISOString());
        agree(chain, row, header.hash);
      }, function () {});
      get("/v1/configuration?format=json").then(function (text) {
        var config = JSON.parse(text);
        var store = config.store || config;
        if (peers[host + " " + chain]) {
          features(peers[host + " " + chain], config.node || {}, config.network || {}, store);
          settle(host + " " + chain);
        }
        mark(row.cells[3], store.turbo ? "Yes" : "No", store.turbo ? "scan-up" : "scan-some");
        yes(row.cells[4], store.address, "address index");
        yes(row.cells[5], store.filter, "client filter index");
        if (store.silent === null) mark(row.cells[6], "No", "scan-some", "The silent payment index is not enabled");
        else {
          var silent = Math.max(Number(store.silent), taproot[chain]);
          mark(row.cells[6], silent ? silent.toLocaleString("en-US") : "Genesis", silent === taproot[chain] ? "scan-up" : "scan-some");
        }
        if (store.pruned) mark(row.cells[7], (Number(store.pruned) + 1).toLocaleString("en-US"), "scan-some");
        else mark(row.cells[7], "Genesis", "scan-up");
      }, function () {});
    });
  }

  var services = [].map.call(scroller.querySelectorAll("tbody tr"), function (row) {
    return [].map.call(row.cells, function (cell) { return cell.textContent.trim(); });
  });
  var merged = scroller.cloneNode(true);
  var head = merged.querySelector("thead tr");
  var body = merged.querySelector("tbody");
  head.innerHTML = "";
  body.innerHTML = "";
  ["Host", "Network"].concat(services.map(function (row) { return row[0]; })).forEach(function (text) {
    var th = document.createElement("th");
    th.textContent = text;
    head.appendChild(th);
  });
  var label = document.createElement("span");
  label.className = "table-title";
  label.textContent = "Ports";
  head.cells[0].insertBefore(label, head.cells[0].firstChild);
  marker.appendChild(merged);
  hosts.forEach(function (host) {
    for (var i = 1; i < chains.length; i++) {
      var row = body.insertRow();
      row.insertCell().textContent = host.split(".")[0];
      row.insertCell().textContent = chains[i];
      services.forEach(function (entry) {
        var cell = row.insertCell();
        var service = entry[0];
        var checked = http.indexOf(service) >= 0;
        var path = paths[service];
        var request = requests[service];
        var chain = chains[i];
        var ports = entry[i].split("/").map(function (t) { return t.trim(); });
        ports.forEach(function (port, j) {
          var where = typeof path === "function" ? path(chain) : path;
          var payload = typeof request === "function" ? request(chain) : request;
          var name = host.split(".")[0];
          var title = name.charAt(0).toUpperCase() + name.slice(1) + " " + service + " " + chain.charAt(0).toUpperCase() + chain.slice(1) + " Genesis" + (port.slice(-2) === "43" ? " (Secure)" : " (Clear)");
          if (j) cell.appendChild(document.createTextNode(" / "));
          var span = document.createElement(where || request ? "a" : "span");
          span.textContent = port;
          if (where || request) {
            span.href = url(host, port, where);
            span.addEventListener("click", function (event) {
              event.preventDefault();
              if (span.dataset.reason) popup(failure(span.dataset.reason, span.href));
              else open(span.href, payload, title);
            });
          }
          cell.appendChild(span);
          if (!checked || port.slice(-2) !== "43") return;
          span.className = "scan-wait";
          var result = probe(host, port, where);
          count(host, chain, result);
          result.then(function (state) {
            var up = state === "up";
            span.className = up ? "scan-up" : "scan-down";
            if (!up) span.dataset.reason = state;
            span.title = up ? "Answered" : state === "timeout" ? "No answer within 8 seconds" : "The connection failed or was refused";
          });
        });
      });
    }
  });
  scroller.style.display = "none";
})();
</script>

A `--hardware-optimized` build on either server reports
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
build....... platform:bs-linux-x64-avx2-shani compiled:bs-linux-x64-avx2-shani.
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
`origin` list admits the pages it serves itself only when the request's
`Host` is in its `host` list, so list the service's own name there, which
also protects it from DNS rebinding.

A request from any other page is then refused. Requests that carry no
`Origin`, such as those from wallets and command line tools, are not
affected. `allow_opaque_origin` admits pages opened as local files
([HTTP services](services#4-http-services)).

**6. Publish the ZMQ public key.** TLS clients verify the server by its
certificate, but a CurveZMQ client must already hold the server's public
key. Publish the `curve-public` key beside the server's name and ports,
for clients to configure as the server key. Never publish the secret key.
