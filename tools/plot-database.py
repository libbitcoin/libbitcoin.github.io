"""Draw the libbitcoin-database head and table type figures.

Usage: python tools/plot-database.py

Writes database/figures/*.png in the style of the performance charts.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "database", "figures")

BG = "#1a1a19"
INK = "#f0efec"
INK2 = "#c9c8c4"
MUTED = "#8b8a86"
RULE = "#3a3a37"
CELL = "#262624"
BLUE = "#3987e5"
ORANGE = "#d85a28"
LIGHT = "#ec8b40"
GOLD = "#f2b660"
GREEN = "#3fae7a"
MONO = "DejaVu Sans Mono"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": INK,
    "figure.facecolor": BG,
    "savefig.facecolor": BG,
})


def figure(title, width=22.5, height=12.75, xmax=100, ymax=56):
    fig = plt.figure(figsize=(width / 2.0, height / 2.0), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, xmax)
    ax.set_ylim(ymax, 0)
    ax.axis("off")
    ax.text(2.5, 2.6, title, fontsize=15, color=INK, va="center")
    return fig, ax


def note(ax, lines, y):
    for i, line in enumerate(lines):
        ax.text(1.5, y + i * 1.7, line, fontsize=9.5, color=MUTED, va="center")


def box(ax, x, y, w, h, text="", fc=CELL, ec=RULE, color=INK, size=9.5,
        mono=True, weight="normal", lw=1.0, ha="center"):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, lw=lw))
    if text != "":
        tx = x + w / 2 if ha == "center" else x + 0.6
        ax.text(tx, y + h / 2, text, fontsize=size, color=color, ha=ha,
                va="center", family=MONO if mono else "DejaVu Sans",
                weight=weight)


def label(ax, x, y, text, color=INK2, size=10, ha="left", mono=False,
          weight="normal"):
    ax.text(x, y, text, fontsize=size, color=color, ha=ha, va="center",
            family=MONO if mono else "DejaVu Sans", weight=weight)


def header(ax, x, y, text, sub=""):
    label(ax, x, y, text, color=GOLD, size=12, weight="bold")
    if sub:
        label(ax, x, y + 1.6, sub, color=MUTED, size=9)


def arrow(ax, start, end, color=BLUE, rad=0.0, lw=1.3, style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style,
                                 mutation_scale=11, color=color, lw=lw,
                                 linestyle=ls,
                                 connectionstyle="arc3,rad=%s" % rad,
                                 shrinkA=1, shrinkB=1))


def bits(ax, x, y, w, h, pattern, on=GOLD, off="#3a3a37"):
    step = w / len(pattern)
    for i, bit in enumerate(pattern):
        ax.add_patch(Rectangle((x + i * step + 0.06, y + 0.12),
                               step - 0.12, h - 0.24,
                               facecolor=on if bit == "1" else off,
                               edgecolor="none"))


def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, name), dpi=100)
    plt.close(fig)
    print("wrote", name)


# Shared example: the toy hash ignores the first character, so keys that
# differ only in their first character collide (as in the 2021 design).
RECORDS = [
    # link, key, value, next, bucket
    (0, "food", "pizza", None, 5),
    (1, "abcd", "candy", None, 6),
    (2, "baad", "eggplant", None, 2),
    (3, "good", "beer", 0, 5),
    (4, "dood", "milk", 3, 5),
    (5, "maad", "cake", 2, 2),
]
TOPS = {2: 5, 5: 4, 6: 1}
FILTERS = {2: "01000100", 5: "10010101", 6: "00100001"}
NULL = "∅"


def draw_hash_head(ax, x, y, w=25, rows=8, filtered=True, count=6):
    header(ax, x, y - 3.4, "head file", "[count][cell 0 .. cell buckets-1]")
    box(ax, x, y, 7, 2.2, "count", fc="#2f2f2c", color=MUTED, size=9)
    box(ax, x + 7, y, w - 7, 2.2, str(count), fc="#2f2f2c")
    cells = {}
    for b in range(rows):
        cy = y + 2.2 + b * 2.2
        label(ax, x - 1.0, cy + 1.1, str(b), color=MUTED, size=9, ha="right",
              mono=True)
        if filtered:
            fw = 9.5
            box(ax, x, cy, fw, 2.2, fc=CELL)
            bits(ax, x + 0.3, cy + 0.3, fw - 0.6, 1.6,
                 FILTERS.get(b, "00000000"))
            box(ax, x + fw, cy, w - fw, 2.2,
                str(TOPS[b]) if b in TOPS else NULL,
                color=INK if b in TOPS else MUTED)
        else:
            box(ax, x, cy, w, 2.2, str(TOPS[b]) if b in TOPS else NULL,
                color=INK if b in TOPS else MUTED)
        cells[b] = (x + w, cy + 1.1)
    return cells


def draw_hash_body(ax, x, y, records, slab=False):
    header(ax, x, y - 3.4, "body file",
           "[next][key][value] per element, appended")
    widths = (8, 8, 12)
    rows = {}
    for i, (link, key, value, nxt, _) in enumerate(records):
        cy = y + 2.2 + i * 2.2
        label(ax, x - 1.0, cy + 1.1, str(link), color=MUTED, size=9,
              ha="right", mono=True)
        box(ax, x, cy, widths[0], 2.2, NULL if nxt is None else str(nxt),
            color=MUTED if nxt is None else LIGHT)
        box(ax, x + widths[0], cy, widths[1], 2.2, key, color=GOLD)
        box(ax, x + sum(widths[:2]), cy, widths[2], 2.2, value)
        rows[link] = (x, cy + 1.1, x + sum(widths), cy)
    label(ax, x + 4, y + 1.1, "next", color=MUTED, size=9, ha="center")
    label(ax, x + 12, y + 1.1, "key", color=MUTED, size=9, ha="center")
    label(ax, x + 22, y + 1.1, "value", color=MUTED, size=9, ha="center")
    return rows


# ----------------------------------------------------------------------------

def fig_hashmap():
    fig, ax = figure("Hash map: hash head over a record body")
    cells = draw_hash_head(ax, 6, 12)
    rows = draw_hash_body(ax, 52, 12, RECORDS)
    for b, top in TOPS.items():
        arrow(ax, cells[b], (rows[top][0] - 2.6, rows[top][1]), color=BLUE,
              rad=-0.08)
    for link, key, value, nxt, _ in RECORDS:
        if nxt is not None:
            x0, y0 = rows[link][2], rows[link][1]
            x1, y1 = rows[nxt][2], rows[nxt][1]
            arrow(ax, (x0, y0), (x1, y1), color=LIGHT, rad=0.55)
    header(ax, 6, 36.5, "search(good)")
    steps = [
        ("bucket = low key bytes mod buckets = 5", INK2),
        ("cell 5 filter screens the key in, top = 4", INK2),
        ("4: dood ≠ good, next = 3", INK2),
        ("3: good = good, value = beer", GREEN),
    ]
    for i, (text, color) in enumerate(steps):
        label(ax, 6, 39.5 + i * 2.0, text, color=color, size=10, mono=True)
    header(ax, 52, 36.5, "put(maad, cake)")
    steps = [
        ("allocate and write record 5 (next unset)", INK2),
        ("exchange cell 2: next = old top 2, top = 5", INK2),
        ("the cell exchange publishes the record", GREEN),
    ]
    for i, (text, color) in enumerate(steps):
        label(ax, 52, 39.5 + i * 2.0, text, color=color, size=10, mono=True)
    note(ax, [
        "Each bucket cell holds the link of its newest element and filter bits above the link. "
        "Elements form a conflict stack through their next links.",
        "Links are record ordinals. A key's elements share a bucket, so duplicates are found by "
        "continuing the walk (iterator).",
    ], 52.0)
    save(fig, "hashmap.png")


def fig_cell():
    fig, ax = figure("Hash head cell: link and bucket filter in one word",
                     ymax=50)
    header(ax, 6, 9, "cell (CellSize bytes)",
           "filter bits are the cell bits above the link bits")
    fx, lx, y = 6, 40, 13
    box(ax, fx, y, 34, 3.2, fc=CELL)
    bits(ax, fx + 0.4, y + 0.4, 33.2, 2.4, "1001010100100010")
    box(ax, lx, y, 52, 3.2, "link (Link::bits)  = top element", color=INK,
        size=10.5)
    label(ax, fx + 17, y + 4.6, "filter (to_bits(CellSize) - Link::bits)",
          color=GOLD, size=10, ha="center")
    label(ax, lx + 26, y + 4.6, "masked with Link::terminal", color=MUTED,
          size=10, ha="center")

    def probe(y, name, pattern, hits, verdict, vcolor):
        header(ax, 6, y, name)
        box(ax, fx, y + 2.2, 34, 3.2, fc=CELL)
        bits(ax, fx + 0.4, y + 2.6, 33.2, 2.4, pattern)
        step = 33.2 / 16
        for i in hits:
            cx = fx + 0.4 + (i + 0.5) * step
            arrow(ax, (cx, y + 7.6), (cx, y + 5.6), color=INK2, lw=1.0)
        label(ax, fx, y + 8.6, "thumb(key), the key bytes after the bucket bytes, selects k = %d bits" % len(hits),
              color=INK2, size=10)
        label(ax, lx + 3, y + 3.8, verdict, color=vcolor, size=11, mono=True)

    probe(22, "search for a present key", "1001010100100010", (0, 3, 10),
          "all k bits set: walk the conflict stack", GREEN)
    probe(34, "search for an absent key", "1001010100100010", (3, 6, 13),
          "a bit clear: not present, no body read", ORANGE)
    note(ax, [
        "A push ORs the new key's k bits into the cell in the same atomic exchange that "
        "sets the link, so the filter never lags the stack.",
        "k is derived from the expected load factor (optimal_k) and can be overridden from "
        "the store envelope. With no spare bits the filter is disabled.",
    ], 46.0)
    save(fig, "hash-cell.png")


def fig_slab():
    fig, ax = figure("Hash map: hash head over a slab body", ymax=46)
    header(ax, 6, 9, "head file", "cells hold byte offsets into the body")
    cells = [(0, "∅"), (1, "41"), (2, "∅"), (3, "0"), (4, "∅")]
    for b, text in cells:
        label(ax, 5.0, 13.6 + b * 2.2, str(b), color=MUTED, size=9,
              ha="right", mono=True)
        box(ax, 6, 12.5 + b * 2.2, 14, 2.2, text,
            color=MUTED if text == "∅" else INK)
    header(ax, 28, 9, "body file", "variable width elements, links are byte offsets")
    slabs = [(0, 18, "∅", "txid a", "tx a (18 bytes)"),
             (18, 23, "∅", "txid b", "tx b (23 bytes)"),
             (41, 30, "18", "txid c", "tx c (30 bytes)")]
    scale = 0.95
    y = 14
    xs = {}
    for offset, size, nxt, key, value in slabs:
        x = 28 + offset * scale
        w = size * scale
        box(ax, x, y, 3.8, 3.2, nxt, color=MUTED if nxt == NULL else LIGHT,
            size=9)
        box(ax, x + 3.8, y, 5.0, 3.2, key.split()[1], color=GOLD, size=9)
        box(ax, x + 8.8, y, w - 8.8, 3.2, value, size=8.5)
        label(ax, x, y + 4.6, str(offset), color=MUTED, size=9, mono=True)
        xs[offset] = x
    label(ax, 28 + 71 * scale, y + 4.6, "71", color=MUTED, size=9, mono=True)
    arrow(ax, (20, 14.7), (xs[41], 14.2), color=BLUE, rad=-0.18)
    arrow(ax, (20, 19.1), (xs[0], 17.2), color=BLUE, rad=0.12)
    arrow(ax, (xs[41] + 1.9, 17.2), (xs[18] + 4, 17.2), color=LIGHT, rad=0.5)
    header(ax, 6, 28, "record vs slab")
    rows = [
        "record body: link = ordinal, position = link × row size",
        "slab body:   link = byte offset, element sizes vary",
        "a slab consumes the link domain by bytes, so its links are wider",
    ]
    for i, text in enumerate(rows):
        label(ax, 6, 31.5 + i * 2.2, text, color=INK2, size=10.5, mono=True)
    note(ax, [
        "Slab elements carry no length prefix: the element's own serialization "
        "(typically a varint count) determines its size.",
    ], 42.5)
    save(fig, "hashmap-slab.png")


def fig_array():
    fig, ax = figure("Array map: array head indexed by key over a body",
                     ymax=48)
    header(ax, 6, 9, "head file", "[count][bucket 0 .. buckets-1], key = index")
    heads = [(0, "0"), (1, "1"), (2, "2"), (3, "5"), (4, "4"), (5, NULL)]
    box(ax, 6, 12.5, 6, 2.2, "count", fc="#2f2f2c", color=MUTED, size=9)
    box(ax, 12, 12.5, 12, 2.2, "6", fc="#2f2f2c")
    for i, text in heads:
        y = 14.7 + i * 2.2
        label(ax, 5.0, y + 1.1, str(i), color=MUTED, size=9, ha="right",
              mono=True)
        box(ax, 6, y, 18, 2.2, text, color=MUTED if text == NULL else INK)
    header(ax, 48, 9, "body file", "records appended in arrival order")
    body = [(0, "a"), (1, "b"), (2, "c"), (3, "d (replaced)"), (4, "e"),
            (5, "d'")]
    for link, value in body:
        y = 14.7 + link * 2.2
        label(ax, 47.0, y + 1.1, str(link), color=MUTED, size=9, ha="right",
              mono=True)
        stale = "replaced" in value
        box(ax, 48, y, 24, 2.2, value, color=MUTED if stale else INK)
    for i, text in heads:
        if text != NULL:
            arrow(ax, (24, 14.7 + i * 2.2 + 1.1),
                  (45.4, 14.7 + int(text) * 2.2 + 1.1), color=BLUE, rad=-0.05)
    header(ax, 6, 31, "at(3)")
    for i, text in enumerate(["bucket 3 = 5", "get(5) = d'"]):
        label(ax, 6, 34 + i * 2.0, text, color=INK2, size=10.5, mono=True)
    header(ax, 48, 31, "put(3, d')")
    for i, text in enumerate([
            "append record 5",
            "store 5 into bucket 3 (head expands as needed)",
            "record 3 remains in the body, unreachable"]):
        label(ax, 48, 34 + i * 2.0, text, color=INK2, size=10.5, mono=True)
    note(ax, [
        "The key is a dense integer (such as a height), so no hash or search is "
        "needed. Buckets are mutable, the body is append-only.",
        "Buckets may be word aligned (Align) for atomic store, at the cost of "
        "padding links narrower than a word.",
    ], 44.0)
    save(fig, "arraymap.png")


def fig_nomap():
    fig, ax = figure("No map: record or slab body addressed only by link",
                     ymax=44)
    header(ax, 6, 9, "head file", "[count] only")
    box(ax, 6, 12.5, 6, 2.2, "count", fc="#2f2f2c", color=MUTED, size=9)
    box(ax, 12, 12.5, 12, 2.2, "5", fc="#2f2f2c")
    header(ax, 34, 9, "record body", "position = link × size")
    for link in range(5):
        y = 12.5 + link * 2.2
        label(ax, 33.0, y + 1.1, str(link), color=MUTED, size=9, ha="right",
              mono=True)
        box(ax, 34, y, 22, 2.2, "row %d" % link)
    header(ax, 64, 9, "slab body", "position = link (bytes)")
    for i, (offset, size) in enumerate([(0, 9), (9, 5), (14, 11), (25, 7)]):
        y = 12.5 + i * 2.2
        label(ax, 63.0, y + 1.1, str(offset), color=MUTED, size=9, ha="right",
              mono=True)
        box(ax, 64, y, size * 1.6, 2.2, "%d bytes" % size, size=8.5)
    header(ax, 6, 27, "uses")
    rows = [
        "the target of foreign keys: other tables store the link",
        "write order is the only order, there is no search",
        "count lives in the head, so a snapshot copies one word",
    ]
    for i, text in enumerate(rows):
        label(ax, 6, 30.5 + i * 2.2, text, color=INK2, size=10.5, mono=True)
    note(ax, [
        "Allocation advances the logical count, and the element is reachable once "
        "a foreign key to its link is published by another table.",
    ], 40.5)
    save(fig, "nomap.png")


def fig_headmap():
    fig, ax = figure("Head map: values stored in the head, no body", ymax=50)
    header(ax, 6, 9, "head file", "[cell 0 .. cell count-1], count = file size / cell")
    values = ["17", "18", "20", "21", "24", "25"]
    for i, text in enumerate(values):
        y = 12.5 + i * 2.2
        label(ax, 5.0, y + 1.1, str(i), color=MUTED, size=9, ha="right",
              mono=True)
        box(ax, 6, y, 16, 2.2, text)
    header(ax, 50, 9, "another table's body", "values are links into it")
    for i in range(9):
        link = 17 + i
        y = 12.5 + i * 2.2
        label(ax, 49.0, y + 1.1, str(link), color=MUTED, size=9, ha="right",
              mono=True)
        used = str(link) in values
        box(ax, 50, y, 22, 2.2, "header %d" % link if used else "fork header",
            color=INK if used else MUTED)
    for i, text in enumerate(values):
        arrow(ax, (22, 12.5 + i * 2.2 + 1.1),
              (46.4, 12.5 + (int(text) - 17) * 2.2 + 1.1), color=BLUE, rad=-0.04)
    header(ax, 6, 33.5, "operations")
    rows = [
        "push(link): append at count (single writer)",
        "truncate(count): pop, the next push rewrites the cell",
        "at(i): one aligned load, terminal past count",
    ]
    for i, text in enumerate(rows):
        label(ax, 6, 37 + i * 2.2, text, color=INK2, size=10.5, mono=True)
    note(ax, [
        "The logical file size is the count, so publishing the count publishes the cell. "
        "A head map is restored with the heads at snapshot.",
        "Values may be links (masked to terminal) or opaque integers. A cell size of "
        "max_size_t makes the head a byte-addressed slab.",
    ], 46.0)
    save(fig, "headmap.png")


def fig_records():
    fig, ax = figure("Records: each row is several records, one file each",
                     ymax=46)
    header(ax, 6, 9, "head file", "hash head over record 0")
    for b, text in enumerate(["3", NULL, "1", "4"]):
        y = 12.5 + b * 2.2
        box(ax, 6, y, 10, 2.2, text, color=MUTED if text == NULL else INK)
    files = [("record 0 (keyed)", ["next", "key", "value"], (5, 6, 7)),
             ("record 1", ["a"], (8,)),
             ("record 2", ["b", "c"], (5, 5))]
    x = 24
    starts = []
    for name, fields, widths in files:
        header(ax, x, 9, name, "<name>_%s.data" % name.split()[1])
        for row in range(5):
            y = 12.5 + row * 2.2
            if x == 24:
                label(ax, x - 1.0, y + 1.1, str(row), color=MUTED, size=9,
                      ha="right", mono=True)
            cx = x
            for field, w in zip(fields, widths):
                color = GOLD if field == "key" else (LIGHT if field == "next"
                                                      else INK)
                box(ax, cx, y, w, 2.2, field + str(row) if field not in
                    ("next",) else ("∅" if row in (0, 1, 2) else
                                    str(row - 3)), color=color, size=8.5)
                cx += w
        starts.append(x)
        x = cx + 6
    arrow(ax, (16, 13.6), (24, 12.5 + 3 * 2.2 + 1.1), color=BLUE, rad=-0.1)
    arrow(ax, (16, 18.0), (24, 12.5 + 1 * 2.2 + 1.1), color=BLUE, rad=0.05)
    arrow(ax, (16, 20.2), (24, 12.5 + 4 * 2.2 + 1.1), color=BLUE, rad=-0.05)
    ax.add_patch(Rectangle((23.6, 12.5 + 3 * 2.2 - 0.2), x - 29.2, 2.6,
                           facecolor="none", edgecolor=GREEN, lw=1.6,
                           linestyle="--"))
    label(ax, 24, 26.8, "row 3: one link addresses the same row in every record file",
          color=GREEN, size=10.5)
    header(ax, 6, 31, "properties")
    rows = [
        "allocation is unified across the record files under one lock",
        "only record 0 is searched, the others are read by link",
        "a query touches only the records it needs (cache locality)",
    ]
    for i, text in enumerate(rows):
        label(ax, 6, 34.5 + i * 2.2, text, color=INK2, size=10.5, mono=True)
    note(ax, [
        "A single-record row is the special case, record(1). The multi-record "
        "forms (hashmaps, arraymaps, nomaps) share one multi-file storage.",
    ], 43.0)
    save(fig, "records.png")


def fig_heads():
    fig, ax = figure("Head types", ymax=40)
    kinds = [
        ("hash head", "hashhead", ["count", "cell 0", "cell 1", "...", "cell n-1"],
         "cell = filter bits | link\nindex = low key bytes mod buckets\nfixed size, set at create",
         BLUE),
        ("array head", "arrayhead", ["count", "bucket 0", "bucket 1", "...",
                                      "bucket n-1"],
         "bucket = link\nindex = key (dense integer)\ngrows with the key range",
         LIGHT),
        ("no head", "nohead", ["count"],
         "count only\nno index\nbody addressed by link",
         GOLD),
        ("head map", "headmap", ["cell 0", "cell 1", "...", "cell count-1"],
         "cell = value or link\nno body, no count cell\ncount = file size / cell",
         GREEN),
    ]
    for i, (name, cls, cells, text, color) in enumerate(kinds):
        x = 5 + i * 24
        label(ax, x, 8.5, name, color=color, size=13, weight="bold")
        label(ax, x, 10.4, cls, color=MUTED, size=9.5, mono=True)
        for j, cell in enumerate(cells):
            y = 12.5 + j * 2.4
            is_count = cell == "count"
            box(ax, x, y, 19, 2.4, cell, fc="#2f2f2c" if is_count else CELL,
                color=MUTED if is_count or cell == "..." else INK, size=9.5)
        for k, line in enumerate(text.split("\n")):
            label(ax, x, 26.5 + k * 2.1, line, color=INK2, size=10)
    note(ax, [
        "A head is the small, fixed or slowly growing part of a table. Heads are copied "
        "at snapshot, bodies are append-only and are not.",
        "The body count in the head is the logical size of the body, so a restored head "
        "truncates any body growth after the snapshot.",
    ], 36.5)
    save(fig, "heads.png")


def fig_cells():
    fig, ax = figure("Hash head cells of the store, to bit scale", ymax=50)
    # table, cell bytes, link bits, link bytes
    cells = [
        ("header", 4, 23, 3, "block hash"),
        ("ins", 8, 32, 4, "point (hash:index)"),
        ("duplicate", 4, 24, 3, "point (hash:index)"),
        ("tx", 4, 31, 4, "txid"),
        ("outs (address)", 4, 32, 4, "script hash"),
        ("pool", 4, 32, 4, "tx link"),
        ("wtxid", 4, 32, 4, "wtxid"),
    ]
    scale = 0.9
    x0 = 24
    label(ax, x0, 8.0, "bit 63", color=MUTED, size=9, mono=True)
    label(ax, x0 + 64 * scale, 8.0, "bit 0", color=MUTED, size=9, mono=True,
          ha="right")
    for i, (name, size, link_bits, link_bytes, key) in enumerate(cells):
        y = 10 + i * 4.4
        label(ax, 3, y + 1.2, name, color=INK, size=11, weight="bold")
        label(ax, 3, y + 2.9, "key: " + key, color=MUTED, size=9)
        total = size * 8
        filter_bits = total - link_bits
        start = x0 + (64 - total) * scale
        if filter_bits > 1:
            box(ax, start, y, filter_bits * scale, 3.2,
                "filter %d bits" % filter_bits, fc="#3a3020", ec=RULE,
                color=GOLD, size=9.5)
        elif filter_bits == 1:
            box(ax, start, y, scale, 3.2, "", fc="#2f2f2c", ec=RULE)
        box(ax, start + filter_bits * scale, y, link_bits * scale, 3.2,
            "link %d bits" % link_bits, fc="#1f2a38", ec=RULE, color=BLUE,
            size=9.5)
        verdict = ("filter on" if filter_bits > 1 else
                   "1 spare bit" if filter_bits == 1 else "no filter")
        label(ax, x0 + 64 * scale + 1.5, y + 1.6, "%d-byte cell, %s" %
              (size, verdict), color=GREEN if filter_bits > 1 else MUTED,
              size=9.5)
    note(ax, [
        "filter_bits = cell bits - link bits. Only header, ins and duplicate carry a "
        "bucket filter. A link narrower than its bytes frees bits for flags elsewhere.",
        "The header link is 23 bits so the strong index can merge a flag into a header "
        "link. The tx link is 31 bits so prevout records can merge a coinbase flag.",
    ], 45.5)
    save(fig, "hash-cells.png")


if __name__ == "__main__":
    fig_cells()
    fig_heads()
    fig_hashmap()
    fig_cell()
    fig_slab()
    fig_array()
    fig_nomap()
    fig_headmap()
    fig_records()
