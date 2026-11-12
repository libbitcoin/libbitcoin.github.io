"""Set the Libraries and Builds columns of building/md/status.md from the
workflow files.

Usage: python tools/build-counts.py

In each table whose last column is Builds, a row that links a workflow
badge (github.com/libbitcoin/<repo>/actions/workflows/<file>.yml) gets,
in that cell, the number of matrix jobs that the workflow runs on master,
including the jobs of local reusable workflows that it calls. A job with
no matrix, or with `if: false`, is not counted. A Libraries column gets the
number of libbitcoin repositories that the workflow checks out to build.

In a section whose text has "Across all repositories,", that sentence,
to the end of its paragraph, is replaced by the number of times the rows
of the section build each repository.
"""
import math
import os
import re
import textwrap
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATUS = os.path.join(ROOT, "building", "md", "status.md")
RAW = "https://raw.githubusercontent.com/libbitcoin/{}/master/.github/workflows/{}"
CHECKOUT = re.compile(r"- name: Checkout (?:repository \[)?(libbitcoin-[a-z]+)")
CALL = re.compile(r"^    uses: \./\.github/workflows/([\w.-]+\.yml)", re.MULTILINE)
STACK = ["libbitcoin-system", "libbitcoin-database", "libbitcoin-network",
    "libbitcoin-node", "libbitcoin-server", "libbitcoin-explorer"]
MARKER = "Across all repositories,"
BADGE = re.compile(r"github\.com/libbitcoin/([\w-]+)/actions/workflows/([\w.-]+\.yml)")


def fetch(repo, name, cache={}):
    if (repo, name) not in cache:
        with urllib.request.urlopen(RAW.format(repo, name)) as response:
            cache[(repo, name)] = response.read().decode("utf-8")
    return cache[(repo, name)]


def indent(line):
    return len(line) - len(line.lstrip(" "))


def children(lines, start, depth):
    """Indexes of the lines at depth below lines[start], until it closes."""
    out = []
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if indent(line) <= indent(lines[start]):
            break
        if indent(line) == depth:
            out.append(index)
    return out


def items(lines, index):
    """The entries of the list under the key at lines[index], as line lists."""
    line = lines[index]
    value = line.split(":", 1)[1].strip()
    if value.startswith("["):
        return [[entry] for entry in value.strip("[]").split(",") if entry.strip()]

    entries = []
    for child in range(index + 1, len(lines)):
        text = lines[child]
        if not text.strip():
            continue
        if indent(text) <= indent(line):
            break
        if text.lstrip().startswith("- ") and (not entries or
            indent(text) == entries[0][1]):
            entries.append([[text], indent(text)])
        elif entries:
            entries[-1][0].append(text)
    return [entry[0] for entry in entries]


def combinations(lines, matrix):
    """The job count of a matrix: the cross product, less excludes, plus
    includes that set a matrix key (and so add a combination)."""
    depth = indent(lines[matrix]) + 2
    dimensions, include, exclude = {}, [], []
    for index in children(lines, matrix, depth):
        key = lines[index].strip().split(":", 1)[0]
        if key == "include":
            include = items(lines, index)
        elif key == "exclude":
            exclude = items(lines, index)
        else:
            dimensions[key] = len(items(lines, index))

    keys = re.compile(r"^\s*-?\s*(" + "|".join(map(re.escape, dimensions)) + r"):") \
        if dimensions else None
    added = [entry for entry in include if not dimensions or
        any(keys.match(text) for text in entry)]
    product = math.prod(dimensions.values()) if dimensions else 0
    return product - len(exclude) + len(added)


def count(repo, name):
    lines = fetch(repo, name).splitlines()
    jobs = next(index for index, line in enumerate(lines) if line == "jobs:")
    total = 0
    for job in children(lines, jobs, 2):
        body = range(job + 1, next((index for index in children(lines, jobs, 2)
            if index > job), len(lines)))
        if any(lines[index].strip() == "if: false" and
            indent(lines[index]) == 4 for index in body):
            continue

        for index in body:
            stripped = lines[index].strip()
            if indent(lines[index]) == 4 and stripped.startswith("uses: ./"):
                total += count(repo, stripped.rsplit("/", 1)[1])
            elif stripped == "matrix:":
                total += combinations(lines, index)
    return total


def projects(repo, name):
    """The libbitcoin repositories that the workflow checks out to build."""
    text = fetch(repo, name)
    found = set(CHECKOUT.findall(text))
    for called in CALL.findall(text):
        found |= projects(repo, called)
    return found


def totals(counts):
    """The sentence giving the builds of each repository across the rows."""
    sums = {}
    for builds, built in counts:
        for project in built:
            sums[project] = sums.get(project, 0) + builds

    order = [name for name in STACK if name in sums]
    parts = ["{} {}".format(name, sums[name]) for name in order]
    parts[0] += " times"
    listed = parts[0] if len(parts) == 1 else \
        ", ".join(parts[:-1]) + ", and " + parts[-1]
    sentence = (MARKER + " a run builds " + listed + ". Tests are run only "
        "for the last repository in each build.")
    return textwrap.fill(sentence, 74)


def main():
    with open(STATUS, encoding="utf-8") as file:
        text = file.read()

    sections = re.split(r"(?m)^(?=## )", text)
    for position, section in enumerate(sections):
        rows, header, counts = [], "", []
        for line in section.split("\n"):
            if not line.startswith("|"):
                header = ""
            elif not header:
                header = line
            match = BADGE.search(line) if header.endswith("| Builds |") else None
            if match:
                builds = count(*match.groups())
                built = projects(*match.groups())
                counts.append((builds, built))
                cells = line.split("|")
                cells[-2] = " {} ".format(builds)
                if header.endswith("| Libraries | Builds |"):
                    cells[-3] = " {} ".format(len(built) or "")
                line = "|".join(cells)
            rows.append(line)

        section = "\n".join(rows)
        if MARKER in section:
            begin = section.index(MARKER)
            stop = section.index("\n\n", begin)
            section = section[:begin] + totals(counts) + section[stop:]
        sections[position] = section

    with open(STATUS, "w", encoding="utf-8", newline="\n") as file:
        file.write("".join(sections))


if __name__ == "__main__":
    main()
