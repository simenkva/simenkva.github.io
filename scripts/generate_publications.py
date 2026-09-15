#!/usr/bin/env python3
"""Pre-render hook: turns the .bib files into formatted Markdown fragments.

kvaal_published.bib   -> _generated/publications_list.md
kvaal_preprints.bib   -> _generated/preprints_list.md
"""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLISHED_BIB = ROOT / "kvaal_published.bib"
PREPRINTS_BIB = ROOT / "kvaal_preprints.bib"
PUBLISHED_OUT = ROOT / "_generated" / "publications_list.md"
PREPRINTS_OUT = ROOT / "_generated" / "preprints_list.md"

HIGHLIGHT_NAME = "Simen Kvaal"


def strip_braces(value):
    value = value.strip()
    while value.startswith("{") and value.endswith("}"):
        inner = value[1:-1]
        depth = 0
        balanced = True
        for ch in inner:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth < 0:
                    balanced = False
                    break
        if balanced and depth == 0:
            value = inner.strip()
        else:
            break
    return value


def parse_entries(text):
    text = "\n".join(
        line for line in text.splitlines() if not line.strip().startswith("%")
    )
    entries = []
    pos = 0
    n = len(text)
    while True:
        at = text.find("@", pos)
        if at == -1:
            break
        m = re.match(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text[at:])
        if not m:
            pos = at + 1
            continue
        entry_type = m.group(1).lower()
        key = m.group(2)
        cursor = at + m.end()
        depth = 1
        fields = {}
        while depth > 0 and cursor < n:
            while cursor < n and text[cursor] in " \t\r\n,":
                cursor += 1
            if cursor >= n:
                break
            if text[cursor] == "}":
                depth -= 1
                cursor += 1
                continue
            fm = re.match(r"(\w+)\s*=\s*", text[cursor:])
            if not fm:
                cursor += 1
                continue
            field_name = fm.group(1).lower()
            cursor += fm.end()
            if text[cursor] == "{":
                vdepth = 0
                start = cursor
                while cursor < n:
                    if text[cursor] == "{":
                        vdepth += 1
                    elif text[cursor] == "}":
                        vdepth -= 1
                        if vdepth == 0:
                            cursor += 1
                            break
                    cursor += 1
                value = strip_braces(text[start:cursor])
            else:
                vm = re.match(r'"([^"]*)"|([^,}]+)', text[cursor:])
                value = (vm.group(1) or vm.group(2)).strip() if vm else ""
                cursor += vm.end() if vm else 0
            fields[field_name] = value
        fields["type"] = entry_type
        fields["key"] = key
        entries.append(fields)
        pos = cursor
    return entries


# ---------------------------------------------------------------------------
# Light LaTeX -> plain-text/unicode cleanup, for bib files exported by tools
# (e.g. Zotero) that escape accents, quotes and special characters.

LATEX_ACCENTS = {
    '"': {"a": "ä", "e": "ë", "i": "ï", "o": "ö", "u": "ü", "y": "ÿ",
          "A": "Ä", "E": "Ë", "O": "Ö", "U": "Ü"},
    "'": {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú", "y": "ý",
          "c": "ć", "n": "ń", "A": "Á", "E": "É"},
    "`": {"a": "à", "e": "è", "i": "ì", "o": "ò", "u": "ù"},
    "^": {"a": "â", "e": "ê", "i": "î", "o": "ô", "u": "û"},
    "~": {"a": "ã", "n": "ñ", "o": "õ"},
}

LATEX_COMMANDS = {
    "textbackslash": "\\",
    "textasciitilde": " ",  # LaTeX idiom `~` is a non-breaking space
    "textasciicircum": "^",
    "ss": "ß",
}


def clean_latex(text):
    if not text:
        return text
    # unwrap case-protection braces around zero-argument commands, e.g. {\textbackslash}
    text = re.sub(r"\{(\\[a-zA-Z]+)\}", r"\1", text)
    for name, repl in LATEX_COMMANDS.items():
        text = text.replace("\\" + name, repl)

    def accent_sub(m):
        accent, letter = m.group(1), m.group(2)
        return LATEX_ACCENTS.get(accent, {}).get(letter, letter)

    text = re.sub(r"\\([\"'`^~])\{?([a-zA-Z])\}?", accent_sub, text)
    for ch in "%&_$#":
        text = text.replace("\\" + ch, ch)
    text = text.replace("``", "\u201c").replace("''", "\u201d")
    # LaTeX-style dashes (rendered raw HTML bypasses pandoc's smart typography)
    text = text.replace("---", "\u2014").replace("--", "\u2013")
    # remaining case-protection braces are purely cosmetic in bibtex
    text = text.replace("{", "").replace("}", "")
    return text.strip()


def format_author_name(name):
    name = clean_latex(strip_braces(name.strip()))
    if "," in name:
        family, given = name.split(",", 1)
        return f"{given.strip()} {family.strip()}"
    return name


def format_authors(author_field):
    names = [format_author_name(a) for a in author_field.split(" and ")]
    names = [f"**{n}**" if n == HIGHLIGHT_NAME else n for n in names]
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return ", ".join(names[:-1]) + ", and " + names[-1]


def group_by_year(entries):
    by_year = {}
    for entry in entries:
        by_year.setdefault(entry.get("year", ""), []).append(entry)
    return by_year


def render_grouped(entries, formatter):
    by_year = group_by_year(entries)
    lines = []
    for year in sorted(by_year, reverse=True):
        lines.append(f"### {year}\n")
        for entry in by_year[year]:
            lines.append(formatter(entry))
            lines.append("")
    return "\n".join(lines).strip() + "\n"


# ---------------------------------------------------------------------------
# Peer-reviewed journal articles

def format_article(entry):
    authors = format_authors(entry["author"])
    title = clean_latex(entry["title"])
    journal = clean_latex(entry.get("journal", ""))
    volume = entry.get("volume", "")
    number = entry.get("number", "")
    pages = entry.get("pages", "")
    year = entry.get("year", "")
    doi = entry.get("doi", "")

    citation = f"{authors} ({year}). *{title}*. {journal}"
    if volume:
        citation += f", {volume}"
    if number:
        citation += f"({number})"
    if pages:
        citation += f", {pages}"
    citation += "."
    if doi:
        citation += f" [doi:{doi}](https://doi.org/{doi})"
    return f"- {citation}"


# ---------------------------------------------------------------------------
# Preprints (with abstract, shown collapsed)

def format_preprint(entry):
    authors = format_authors(entry["author"])
    title = clean_latex(entry["title"])
    year = entry.get("year", "")
    doi = entry.get("doi", "")
    url = entry.get("url", "")
    abstract = clean_latex(entry.get("abstract", ""))

    if doi:
        link, link_label = f"https://doi.org/{doi}", f"doi:{doi}"
    else:
        link, link_label = url, "arXiv"

    citation = f"{authors} ({year})."
    if link:
        citation += f" [{link_label}]({link})"

    block = [f"**{title}**", "", citation]
    if abstract:
        block += [
            "",
            "<details>",
            "<summary>Abstract</summary>",
            f"<p>{html.escape(abstract, quote=False)}</p>",
            "</details>",
        ]
    return "\n".join(block) + "\n\n---"


def main():
    articles = parse_entries(PUBLISHED_BIB.read_text(encoding="utf-8"))
    articles.sort(key=lambda e: (e.get("year", ""), e.get("title", "")), reverse=True)
    PUBLISHED_OUT.parent.mkdir(parents=True, exist_ok=True)
    PUBLISHED_OUT.write_text(render_grouped(articles, format_article), encoding="utf-8")
    print(f"Generated {PUBLISHED_OUT.relative_to(ROOT)} from {len(articles)} entries.")

    preprints = parse_entries(PREPRINTS_BIB.read_text(encoding="utf-8"))
    preprints.sort(key=lambda e: (e.get("year", ""), e.get("title", "")), reverse=True)
    PREPRINTS_OUT.parent.mkdir(parents=True, exist_ok=True)
    PREPRINTS_OUT.write_text(render_grouped(preprints, format_preprint), encoding="utf-8")
    print(f"Generated {PREPRINTS_OUT.relative_to(ROOT)} from {len(preprints)} entries.")


if __name__ == "__main__":
    main()
