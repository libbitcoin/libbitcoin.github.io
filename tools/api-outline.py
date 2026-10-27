"""Generate the Developers API outline pages from each library's master headers.

The libbitcoin repositories are read from the directory that contains this
site's repository (or API_SOURCE), at their libbitcoin/master remote-tracking
branch (or API_REF), which is not fetched here. Each library
gets api/<library>/md/index.md and a page per top-level header
directory (module). Each header links to GitHub master, and records its
blob hash with a permalink to that version.
"""
import html, os, re, subprocess, collections

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.environ.get("API_SOURCE", os.path.dirname(SITE))
LIBS = [
    ("system", "System", "Bitcoin primitives: blocks, transactions, scripts and their execution, hashes and cryptography, keys, addresses and wallets, encodings and serialization."),
    ("database", "Database", "The store: memory-mapped tables, and the queries over them."),
    ("network", "Network", "Connections and protocols: the P2P network, and HTTP, websocket, JSON-RPC, TLS and ZMQ services."),
    ("node", "Node", "The full node: sync, validation and confirmation, and the transaction pool."),
    ("server", "Server", "The client interfaces of Bitcoin Server (bs)."),
    ("explorer", "Explorer", "The commands of Bitcoin Explorer (bx)."),
]
REF = os.environ.get("API_REF", "libbitcoin/master")
GITHUB = "https://github.com/libbitcoin/libbitcoin-%s/blob/%s/%s"
DECL = re.compile(r"^[ \t]*(?:template\s*<[^;{]*>\s*)?(class|struct)\s+(?:[A-Z_]+_API\s+)?(\w+)\s*(?:final\s*)?(?::[^;{]*)?\{", re.M)
ENUM = re.compile(r"^[ \t]*enum\s+(class\s+)?(\w+)\s*(?::\s*[\w:]+\s*)?\{", re.M)


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args), capture_output=True,
        text=True, encoding="utf-8", errors="replace").stdout


def declarations(text):
    text = re.sub(r"//[^\n]*", "", text)
    found = [(m.start(), m.group(1), m.group(2)) for m in DECL.finditer(text)]
    found += [(m.start(), "enum", m.group(2)) for m in ENUM.finditer(text)]
    out, seen = [], set()
    for _, kind, name in sorted(found):
        if name not in seen and not name.startswith("_"):
            seen.add(name)
            out.append((kind, name))
    return out


def entry(lib, path, decls, blob, commit):
    source = "include/bitcoin/%s/%s" % (lib, path)
    lines = ['<div class="api">',
             '<div class="api-inc"><a href="%s">#include &lt;bitcoin/%s/%s&gt;</a>'
             '<a class="api-ver" href="%s" title="blob %s">%s</a></div>' % (
                 GITHUB % (lib, "master", source), lib, html.escape(path),
                 GITHUB % (lib, commit, source), blob, blob[:8])]
    if decls:
        lines.append('<dl class="api-decl">')
        for kind, name in decls:
            lines.append('<div><dt>%s</dt><dd>%s</dd></div>' % (kind, html.escape(name)))
        lines.append('</dl>')
    lines.append('</div>')
    return "\n".join(lines) + "\n"


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def main():
    for lib, title, provides in LIBS:
        repo = os.path.join(SRC, "libbitcoin-" + lib)
        commit = git(repo, "rev-parse", REF).strip()
        sha = commit[:8]
        base = "include/bitcoin/%s/" % lib
        blobs = {}
        for line in git(repo, "ls-tree", "-r", REF, base).splitlines():
            meta, path = line.split(chr(9), 1)
            blobs[path] = meta.split()[2]
        files = [f for f in sorted(blobs) if f.endswith(".hpp") and "/impl/" not in f]
        modules = collections.OrderedDict()
        root = []
        for f in sorted(files):
            rel = f[len(base):]
            (root if "/" not in rel else modules.setdefault(rel.split("/", 1)[0], [])).append(rel)
        decls = {rel: declarations(git(repo, "show", REF + ":" + base + rel))
                 for rel in root + [h for hs in modules.values() for h in hs]}
        out = os.path.join(SITE, "api", lib, "md")

        page = ["# %s" % title, "",
                "%s The library is `libbitcoin-%s`, in namespace `libbitcoin::%s`." % (provides, lib, lib), "",
                "> The API reference is in progress. This outline follows the header",
                "> hierarchy of libbitcoin-%s at [`%s`](https://github.com/libbitcoin/libbitcoin-%s/tree/%s)." % (lib, sha, lib, commit), "",
                "```cpp", "#include <bitcoin/%s.hpp>" % lib, "```", "",
                "## 1. Modules", "", "| Module | Headers | Types |", "| ------ | ------- | ----- |"]
        for module, headers in modules.items():
            count = sum(len(decls[h]) for h in headers)
            page.append("| [`%s`](%s) | %d | %d |" % (module, module, len(headers), count))
        page += ["", "## 2. Root headers", ""]
        for rel in root:
            page += ["### %s" % rel, "", entry(lib, rel, decls[rel], blobs[base + rel], commit)]
        write(os.path.join(out, "index.md"), "\n".join(page))

        for module, headers in modules.items():
            page = ["# %s" % module, "",
                    "The `%s` module of libbitcoin-%s." % (module, lib), "",
                    "```cpp", "#include <bitcoin/%s/%s/%s.hpp>" % (lib, module, module)
                    if "%s/%s.hpp" % (module, module) in headers else "// <bitcoin/%s/%s/...>" % (lib, module), "```", ""]
            groups = collections.OrderedDict()
            for h in headers:
                groups.setdefault(h.rsplit("/", 1)[0], []).append(h)
            for n, (group, members) in enumerate(groups.items(), 1):
                page += ["## %d. %s" % (n, group), ""]
                for h in members:
                    page += ["### %s" % h.rsplit("/", 1)[1], "", entry(lib, h, decls[h], blobs[base + h], commit)]
            write(os.path.join(out, module + ".md"), "\n".join(page))
        print(lib, sha, len(files), "headers,", len(modules), "modules")


if __name__ == "__main__":
    main()
