"""Render architecture/md/*.md into architecture/*.html using the site chrome.

Usage: python tools/build-architecture.py [--mermaid URL]

The anti-mirror script and the logo are lifted from node-performance.html so
the pages share one copy of each. Mermaid diagrams are emitted as
<div class="mermaid"> and rendered client-side by mermaid.min.js.
"""
import html
import os
import re
import sys

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "architecture", "md")
OUT = os.path.join(ROOT, "architecture")
CHROME = os.path.join(ROOT, "node-performance.html")
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"

PAGES = [
    ("index", "Architecture"),
    ("00-overview", "Overview"),
    ("01-event-bus", "Event bus"),
    ("02-chaser-header", "Chaser header"),
    ("03-chaser-download", "Chaser download"),
    ("04-chaser-validate", "Chaser validate"),
    ("05-chaser-confirm", "Chaser confirm"),
    ("06-sessions-and-protocols", "Sessions and protocols"),
    ("07-header-protocols", "Header protocols"),
    ("08-block-out-protocols", "Block out protocols"),
    ("09-filter-out-70015", "Filter out 70015"),
    ("10-tx-protocols", "Tx protocols"),
    ("11-chaser-transaction", "Chaser transaction"),
    ("12-periphery-chasers", "Periphery chasers"),
]
SLUGS = {name for name, _ in PAGES}

STYLE = """
  :root {
    color-scheme: dark;
    --paper: #272822; --surface: #1f211c;
    --ink: #ededed; --ink-2: #cfcfcf; --ink-3: #6a7282;
    --rule: #3a3c33; --rule-soft: #2e302a;
    --accent: #c85637; --heading: #ffa022;
    --mono: ui-monospace, "SF Mono", "Cascadia Mono", "Segoe UI Mono", Menlo, Consolas, monospace;
    --sans: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
    --shadow: 0 1px 2px rgba(0,0,0,.4), 0 8px 24px -16px rgba(0,0,0,.8);
  }
  body { background: var(--paper); color: var(--ink); font-family: var(--sans); font-size: 15px; line-height: 1.55; -webkit-font-smoothing: antialiased; }
  .wrap { max-width: 1120px; margin: 0 auto; padding: 0 24px 96px; }
  .logo { width: 132px; height: auto; display: block; }
  .mast { padding: 56px 0 28px; border-bottom: 2px solid var(--ink); display: flex; flex-direction: column; gap: 14px; }
  .eyebrow { font-family: var(--mono); font-size: 11px; letter-spacing: .18em; text-transform: uppercase; color: var(--accent); font-weight: 600; }
  h1 { color: var(--heading); font-family: var(--mono); font-size: clamp(28px, 4.4vw, 44px); font-weight: 600; letter-spacing: -.02em; line-height: 1.1; text-wrap: balance; margin: 0; }
  .lede { max-width: 66ch; color: var(--ink-2); font-size: 16px; }
  .lede strong { color: var(--ink); font-weight: 600; }
  a { color: var(--accent); }
  :focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  .menu { display: flex; flex-wrap: wrap; gap: 6px 18px; margin: 0 0 28px; padding: 10px 0; border-top: 1px solid var(--rule-soft); border-bottom: 1px solid var(--rule-soft); font-family: var(--mono); font-size: 12px; letter-spacing: .08em; text-transform: uppercase; }
  .menu a { color: var(--ink-2); text-decoration: none; }
  .menu a:hover, .menu a:focus { color: var(--heading); }
  .menu a.here { color: var(--heading); }
  .menu.site { margin-bottom: 0; border-bottom: 0; }
  .menu.site + .menu { margin-top: 0; }
  .foot { border-top: 2px solid var(--ink); padding-top: 20px; margin-top: 48px; color: var(--ink-2); font-size: 13.5px; max-width: 72ch; display: flex; flex-direction: column; gap: 10px; }
  .pager { display: flex; justify-content: space-between; gap: 18px; margin: 40px 0 0; font-family: var(--mono); font-size: 12.5px; }

  .doc p, .doc ul, .doc ol, .doc blockquote, .doc h2, .doc h3, .doc h4 { max-width: 86ch; }
  .doc h2 { color: var(--heading); font-family: var(--mono); font-size: 20px; font-weight: 600; letter-spacing: -.015em; margin: 44px 0 12px; scroll-margin-top: 16px; }
  .doc h3 { color: var(--heading); font-family: var(--mono); font-size: 15.5px; font-weight: 600; margin: 30px 0 10px; scroll-margin-top: 16px; }
  .doc h4 { color: var(--ink); font-family: var(--mono); font-size: 14px; font-weight: 600; margin: 22px 0 8px; scroll-margin-top: 16px; }
  .doc p { margin: 0 0 14px; }
  .doc ul, .doc ol { margin: 0 0 14px; padding-left: 26px; }
  .doc li { margin: 3px 0; }
  .doc li::marker { color: var(--ink-3); }
  .doc hr { border: 0; border-top: 1px solid var(--rule-soft); margin: 36px 0; }
  .doc code { font-family: var(--mono); font-size: 12.5px; color: var(--ink); background: var(--surface); border: 1px solid var(--rule-soft); border-radius: 2px; padding: 0 4px; overflow-wrap: anywhere; }
  .doc pre { background: var(--surface); border: 1px solid #c856374d; border-radius: 3px; padding: 12px 14px; margin: 0 0 18px; overflow-x: auto; font-family: var(--mono); font-size: 12.5px; line-height: 1.5; color: var(--ink); }
  .doc pre code { background: none; border: 0; padding: 0; font-size: inherit; }
  .doc blockquote { margin: 0 0 18px; padding: 10px 16px; border-left: 3px solid var(--accent); background: var(--surface); color: var(--ink-2); border-radius: 0 3px 3px 0; }
  .doc blockquote p:last-child { margin-bottom: 0; }
  .doc blockquote strong { color: var(--ink); }
  .doc blockquote blockquote { margin-top: 10px; border-left-color: var(--ink-3); }
  .doc em { color: var(--ink); }

  .scroller { overflow-x: auto; border: 1px solid #c856374d; border-radius: 3px; background: var(--surface); margin: 0 0 18px; }
  .doc table { border-collapse: collapse; width: 100%; font-size: 13px; }
  .doc th { font-family: var(--mono); font-size: 10px; letter-spacing: .1em; text-transform: uppercase; color: var(--ink-3); font-weight: 600; text-align: left; padding: 9px 14px; border-bottom: 1px solid var(--rule); white-space: nowrap; }
  .doc td { padding: 7px 14px; border-bottom: 1px solid var(--rule-soft); vertical-align: baseline; }
  .doc tr:last-child td { border-bottom: none; }
  .doc td code { white-space: nowrap; }

  .mermaid { background: var(--surface); border: 1px solid #c856374d; border-radius: 3px; padding: 14px; margin: 0 0 18px; overflow-x: auto; text-align: center; }
  .mermaid svg { max-width: 100%; height: auto; cursor: zoom-in; }
  .lightbox { position: fixed; inset: 0; z-index: 10; background: rgba(0,0,0,.92); overflow: auto; padding: 24px; cursor: zoom-out; }
  .lightbox[hidden] { display: none; }
  .lightbox svg { display: block; margin: 0 auto; max-width: none !important; height: auto; }
  .mermaid:not([data-processed]) { font-family: var(--mono); font-size: 12px; text-align: left; white-space: pre; color: var(--ink-3); }
  .mermaid p, .mermaid span, .mermaid div { margin: 0; max-width: none; }

  @media (max-width: 760px) {
    .wrap { padding: 0 14px 72px; }
    .doc th, .doc td { padding: 6px 8px; }
    .doc table { font-size: 12px; }
  }
"""


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def chrome():
    page = read(CHROME)
    guard = re.search(r"<script>\n\(function \(\) \{\n  'use strict';\n  var CANONICAL.*?</script>", page, re.S).group(0)
    logo = re.search(r"<svg\s.*?</svg>", page, re.S).group(0)
    return guard, logo


def github_slug(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def extract_mermaid(md):
    blocks = []

    def stash(m):
        blocks.append(m.group(1).replace("\\n", "<br/>"))
        return "\n\nMERMAIDBLOCK%d\n\n" % (len(blocks) - 1)

    md = re.sub(r"```mermaid\n(.*?)```", stash, md, flags=re.S)
    return md, blocks


def restore_mermaid(body, blocks):
    def put(m):
        return '<div class="mermaid">\n%s</div>' % html.escape(blocks[int(m.group(1))], quote=False)

    return re.sub(r"<p>MERMAIDBLOCK(\d+)</p>", put, body)


def fix_links(body):
    def fix(m):
        target = m.group(1)
        name, _, anchor = target.partition("#")
        if name == "Architecture":
            name = "index"
        if name not in SLUGS:
            return m.group(0)
        return 'href="%s.html%s"' % (name, "#" + anchor if anchor else "")

    return re.sub(r'href="([^"/:]+)"', fix, body)


def add_heading_ids(body):
    seen = {}

    def ident(m):
        level, attrs, text = m.group(1), m.group(2), m.group(3)
        slug = github_slug(text)
        n = seen.get(slug, 0)
        seen[slug] = n + 1
        if n:
            slug = "%s-%d" % (slug, n)
        return '<h%s id="%s"%s>%s</h%s>' % (level, slug, attrs, text, level)

    return re.sub(r"<h([2-6])([^>]*)>(.*?)</h\1>", ident, body, flags=re.S)


def wrap_tables(body):
    return re.sub(r"<table>.*?</table>", lambda m: '<div class="scroller">%s</div>' % m.group(0), body, flags=re.S)


def loosen_lists(md):
    out, fenced, prev = [], False, ""
    for line in md.split("\n"):
        if line.startswith("```"):
            fenced = not fenced
        elif not fenced and re.match(r"\s*([-*+]|\d+\.)\s", line) and prev.strip() and not re.match(r"\s*([-*+]|\d+\.|>)\s", prev):
            out.append("")
        out.append(line)
        prev = line
    return "\n".join(out)


def split_title(md):
    m = re.match(r"# (.*)\n", md)
    title = m.group(1).strip()
    body = md[m.end():]
    return title, body


def lede(title):
    # "NN — `thing` (detail)" -> plain title text without code ticks.
    return title.replace("`", "")


def menu(current):
    items = []
    for name, label in PAGES:
        cls = ' class="here"' if name == current else ""
        items.append('    <a href="%s.html"%s>%s</a>' % (name, cls, html.escape(label)))
    return "\n".join(items)


def pager(current):
    names = [n for n, _ in PAGES]
    i = names.index(current)
    prev = '<a href="%s.html">&larr; %s</a>' % PAGES[i - 1] if i > 0 else "<span></span>"
    nxt = '<a href="%s.html">%s &rarr;</a>' % PAGES[i + 1] if i + 1 < len(PAGES) else "<span></span>"
    return '<nav class="pager">%s%s</nav>' % (prev, nxt)


def render(name, md, guard, logo, mermaid_src):
    title, body_md = split_title(md)
    body_md, blocks = extract_mermaid(loosen_lists(body_md))
    converter = markdown.Markdown(extensions=["tables", "fenced_code"])
    body = converter.convert(body_md)
    body = restore_mermaid(body, blocks)
    body = fix_links(body)
    body = add_heading_ids(body)
    body = wrap_tables(body)
    page_title = "Libbitcoin Node Architecture" if name == "index" else "Libbitcoin Node Architecture: " + lede(title)
    description = "Source-anchored architecture documentation for libbitcoin-node: chasers, the event bus, sessions and peer protocols."
    h1 = html.escape(lede(title)) if name != "index" else "Node Architecture"
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(page_title)s</title>
<meta name="description" content="%(description)s">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<link rel="canonical" href="https://libbitcoin.info/architecture/%(name)s.html">
%(guard)s
<meta property="og:type" content="website">
<meta property="og:site_name" content="libbitcoin">
<meta property="og:url" content="https://libbitcoin.info/architecture/%(name)s.html">
<meta property="og:title" content="%(page_title)s">
<meta property="og:description" content="%(description)s">
<meta property="og:image" content="https://libbitcoin.info/card.png">
<meta property="og:image:secure_url" content="https://libbitcoin.info/card.png">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="2400">
<meta property="og:image:height" content="1260">
<meta property="og:image:alt" content="Libbitcoin is Coming &mdash; a Bitcoin full node and query server speaking Electrum, bitcoind, btcd, ZeroMQ, Stratum and the peer protocol.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(page_title)s">
<meta name="twitter:description" content="%(description)s">
<meta name="twitter:image" content="https://libbitcoin.info/card.png">
<meta name="twitter:image:alt" content="Libbitcoin is Coming &mdash; a Bitcoin full node and query server.">
<style>%(style)s</style>
</head>
<body>

<div class="wrap">
  <header class="mast">
    <a href="../" aria-label="libbitcoin.info">
    %(logo)s
    </a>
    <div class="eyebrow">Bitcoin full node and query server</div>
    <h1>%(h1)s</h1>
    <p class="lede">
      Source-anchored architecture documentation for <strong>libbitcoin-node</strong>:
      the chasers, the event bus, sessions and peer protocols.
    </p>
  </header>

  <nav class="menu site">
    <a href="../index.html">Home</a>
    <a href="../interfaces.html">Server interfaces</a>
    <a href="../interface-performance.html">Interface performance</a>
    <a href="../node-performance.html">Node performance</a>
    <a href="index.html" class="here">Node architecture</a>
    <a href="../team.html">Team</a>
  </nav>
  <nav class="menu">
%(menu)s
  </nav>

  <article class="doc">
%(body)s
  </article>

  %(pager)s

  <div class="lightbox" id="lightbox" hidden></div>

  <p class="foot">
    <span>Adapted from the libbitcoin-node wiki architecture pages by <a href="https://github.com/rsantacroce">rsantacroce</a>.</span>
    <span>Copyright &copy; 2011-2026 libbitcoin developers</span>
  </p>
</div>
<script>
(function () {
  var box = document.getElementById('lightbox');
  function open(svg) {
    var copy = svg.cloneNode(true);
    var view = (svg.getAttribute('viewBox') || '').split(/\s+/);
    var width = parseFloat(view[2]) || svg.getBoundingClientRect().width;
    copy.style.width = Math.max(width, 0) + 'px';
    copy.removeAttribute('height');
    box.innerHTML = ''; box.appendChild(copy); box.hidden = false;
  }
  function close() { box.hidden = true; box.innerHTML = ''; }
  document.addEventListener('click', function (e) {
    var svg = e.target.closest('.mermaid svg');
    if (svg) open(svg);
  });
  box.addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
})();
</script>
<script src="%(mermaid)s"></script>
<script>
mermaid.initialize({
  startOnLoad: true,
  theme: 'dark',
  securityLevel: 'loose',
  htmlLabels: false,
  flowchart: { htmlLabels: false },
  fontFamily: 'ui-monospace, "SF Mono", "Cascadia Mono", "Segoe UI Mono", Menlo, Consolas, monospace',
  sequence: { useMaxWidth: true, actorFontFamily: 'ui-monospace, "SF Mono", "Cascadia Mono", "Segoe UI Mono", Menlo, Consolas, monospace', noteFontFamily: 'ui-monospace, "SF Mono", "Cascadia Mono", "Segoe UI Mono", Menlo, Consolas, monospace', messageFontFamily: 'ui-monospace, "SF Mono", "Cascadia Mono", "Segoe UI Mono", Menlo, Consolas, monospace', actorFontSize: 13, noteFontSize: 13, messageFontSize: 13 },
  themeVariables: {
    fontFamily: 'ui-monospace, "SF Mono", "Cascadia Mono", "Segoe UI Mono", Menlo, Consolas, monospace',
    fontSize: '13px',
    background: '#1f211c',
    primaryColor: '#3a3c33',
    primaryTextColor: '#ededed',
    primaryBorderColor: '#c85637',
    lineColor: '#cfcfcf',
    secondaryColor: '#2e302a',
    tertiaryColor: '#272822',
    noteBkgColor: '#2e302a',
    noteTextColor: '#ededed',
    noteBorderColor: '#6a7282',
    actorBkg: '#3a3c33',
    actorBorder: '#c85637',
    actorTextColor: '#ededed',
    signalColor: '#cfcfcf',
    signalTextColor: '#ededed',
    labelBoxBkgColor: '#2e302a',
    labelBoxBorderColor: '#6a7282',
    labelTextColor: '#ededed',
    loopTextColor: '#ededed',
    activationBkgColor: '#c85637',
    activationBorderColor: '#ffa022',
    sequenceNumberColor: '#272822',
    edgeLabelBackground: '#272822',
    clusterBkg: '#272822',
    clusterBorder: '#6a7282',
    titleColor: '#ffa022'
  }
});
</script>
</body>
</html>
""" % dict(page_title=page_title, description=description, name=name, guard=guard, logo=logo,
           style=STYLE, h1=h1, menu=menu(name), body=body, pager=pager(name), mermaid=mermaid_src)


def check_links(pages):
    ids = {name: set(re.findall(r' id="([^"]+)"', body)) for name, body in pages.items()}
    bad = []
    for name, body in pages.items():
        article = re.search(r'<article class="doc">(.*?)</article>', body, re.S).group(1)
        for href in re.findall(r'href="([^"]+)"', article):
            if href.startswith(("http", "../", "#", "mailto")):
                if href.startswith("#") and href[1:] not in ids[name]:
                    bad.append((name, href))
                continue
            target, _, anchor = href.partition("#")
            target = target[:-5] if target.endswith(".html") else target
            if target not in ids:
                bad.append((name, href))
            elif anchor and anchor not in ids[target]:
                bad.append((name, href))
    return bad


def main():
    mermaid_src = MERMAID
    if "--mermaid" in sys.argv:
        mermaid_src = sys.argv[sys.argv.index("--mermaid") + 1]
    guard, logo = chrome()
    pages = {}
    for name, _ in PAGES:
        md = read(os.path.join(SRC, name + ".md"))
        pages[name] = render(name, md, guard, logo, mermaid_src)
        write(os.path.join(OUT, name + ".html"), pages[name])
        print("wrote", name + ".html")
    for name, href in check_links(pages):
        print("BROKEN LINK in %s: %s" % (name, href))


if __name__ == "__main__":
    main()
