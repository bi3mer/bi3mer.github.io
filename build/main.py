#!/usr/bin/env python3
"""Builds the site: python3 build/main.py [source] [output]

Every .md in the source folder (default: the repo root) becomes a finished page in the output folder (default
_site), and every other file is copied as is. Standard library only.
"""

import html
import json
import math
import re
import shutil
import string
import sys
import tomllib
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT / "build" / "vendor"))  # Pygments 2.21.0, vendored.
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

BASE_URL = "https://bi3mer.github.io"
SITE_TITLE = "Colan Biemer"
SECTIONS = {"posts": "Posts", "problems": "Problems"}
SKIP = {
    "build",
    "templates",
    "example-code",
    "_site",
    "public",
    "README.md",
    "PLAN.md",
    "make_new_problem_post.sh",
    "site.css",
    "search.js",
}
WORDS_PER_MINUTE = 213

MATHJAX = """<script>
MathJax = { tex: { displayMath: [['\\\\[', '\\\\]'], ['$$', '$$']], inlineMath: [['\\\\(', '\\\\)']] } };
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>"""

SEARCH_BODY = """<input id="search-box" type="search" placeholder="Search" aria-label="Search" autofocus>
<ul id="search-results" class="cards"></ul>
<script defer src="/search.js"></script>"""


# Inlines


def esc(text):
    return html.escape(text, quote=False)


def highlight_code(code, language):
    """Return CODE as HTML with token spans, or escaped if LANGUAGE is unknown."""
    try:
        lexer = get_lexer_by_name(language.lower(), stripnl=False)
    except ClassNotFound:
        return esc(code) + "\n"
    return highlight(code, lexer, HtmlFormatter(nowrap=True))


def attr(text):
    return html.escape(text, quote=True)


LINK_TAIL = re.compile(
    r"""\(\s*<?([^\s<>()]*(?:\([^\s()]*\)[^\s<>()]*)*)>?(?:\s+(?:"([^"]*)"|'([^']*)'))?\s*\)"""
)
RAW_TAG = re.compile(r"</?[a-zA-Z][^<>]*>|<!--.*?-->", re.S)
AUTOLINK = re.compile(r"<((?:https?://|mailto:)[^\s<>]+)>")
BARE_URL = re.compile(r"https?://[^\s<>]*[^\s<>.,:;!?'\")\]*_]")
PUNCTUATION = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
MATH_PAIRS = (("\\(", "\\)"), ("\\[", "\\]"), ("$$", "$$"))


class Delimiter:
    def __init__(self, char, count, can_open, can_close):
        self.char, self.count = char, count
        self.can_open, self.can_close = can_open, can_close
        self.original = count


def find_bracket_end(text, start):
    """Return the index of the ] matching the [ at start, or -1."""
    depth, i = 0, start
    while i < len(text):
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "`":
            run = len(text[i:]) - len(text[i:].lstrip("`"))
            close = text.find("`" * run, i + run)
            if close != -1:
                i = close + run
                continue
        depth += (c == "[") - (c == "]")
        if depth == 0:
            return i
        i += 1
    return -1


def scan_delimiter(text, i):
    char = text[i]
    end = i
    while end < len(text) and text[end] == char:
        end += 1
    before = text[i - 1] if i else " "
    after = text[end] if end < len(text) else " "
    before_space, after_space = before.isspace(), after.isspace()
    before_punct, after_punct = before in PUNCTUATION, after in PUNCTUATION
    left = not after_space and (not after_punct or before_space or before_punct)
    right = not before_space and (not before_punct or after_space or after_punct)
    if char == "_":
        return (
            end,
            left and (not right or before_punct),
            right and (not left or after_punct),
        )
    return end, left, right


def resolve_emphasis(tokens):
    """Pair * and _ runs in place, following the CommonMark delimiter rules."""
    closer = 0
    while closer < len(tokens):
        token = tokens[closer]
        if not (isinstance(token, Delimiter) and token.can_close and token.count):
            closer += 1
            continue
        opener = closer - 1
        while opener >= 0:
            other = tokens[opener]
            if (
                isinstance(other, Delimiter)
                and other.char == token.char
                and other.can_open
                and other.count
            ):
                both = other.can_close or token.can_open
                if not (
                    both
                    and (other.original + token.original) % 3 == 0
                    and not (other.original % 3 == 0 and token.original % 3 == 0)
                ):
                    break
            opener -= 1
        if opener < 0:
            closer += 1
            continue
        other = tokens[opener]
        size = 2 if other.count >= 2 and token.count >= 2 else 1
        tag = "strong" if size == 2 else "em"
        other.count -= size
        token.count -= size
        inner = tokens[opener + 1 : closer]
        tokens[opener + 1 : closer] = [f"<{tag}>", *inner, f"</{tag}>"]
        closer = opener + 1 + len(inner) + 2
        for t in inner:
            if isinstance(t, Delimiter):
                t.can_open = t.can_close = False
    return "".join(t if isinstance(t, str) else t.char * t.count for t in tokens)


class Inlines:
    """Turns the text of a paragraph, heading, or table cell into HTML."""

    def __init__(self, doc):
        self.doc = doc

    def render(self, text):
        tokens, buffer, i = [], [], 0

        def flush():
            if buffer:
                tokens.append(self.linkify("".join(buffer)))
                buffer.clear()

        while i < len(text):
            c = text[i]

            # Math goes first, so that the escape rule below leaves \( alone.
            pair = next((p for p in MATH_PAIRS if text.startswith(p[0], i)), None)
            if pair:
                close = text.find(pair[1], i + 2)
                if close != -1:
                    flush()
                    tokens.append(esc(text[i : close + 2]))
                    self.doc.has_math = True
                    i = close + 2
                    continue

            if c == "\\" and i + 1 < len(text):
                nxt = text[i + 1]
                if nxt == "\n":
                    flush()
                    tokens.append("<br>\n")
                    i += 2
                    continue
                if nxt in PUNCTUATION:
                    flush()
                    tokens.append(esc(nxt))
                    i += 2
                    continue

            if c == "`":
                end = i
                while end < len(text) and text[end] == "`":
                    end += 1
                match = re.compile(r"(?<!`)`{%d}(?!`)" % (end - i)).search(text, end)
                if match:
                    code = text[end : match.start()].replace("\n", " ")
                    if len(code) > 2 and code[0] == code[-1] == " " and code.strip():
                        code = code[1:-1]
                    flush()
                    tokens.append(f"<code>{esc(code)}</code>")
                    i = match.end()
                    continue
                buffer.append(text[i:end])
                i = end
                continue

            if c == "<":
                match = AUTOLINK.match(text, i)
                if match:
                    flush()
                    url = match.group(1)
                    tokens.append(f'<a href="{attr(url)}">{esc(url)}</a>')
                    i = match.end()
                    continue
                match = RAW_TAG.match(text, i)
                if match:
                    flush()
                    tokens.append(match.group(0))
                    i = match.end()
                    continue

            if text.startswith("![", i):
                link = self.link(text, i + 1)
                if link:
                    label, url, title, end = link
                    flush()
                    tokens.append(self.image(label, url, title))
                    i = end
                    continue

            if c == "[":
                if text.startswith("[^", i):
                    close = text.find("]", i)
                    if close != -1 and text[i + 2 : close] in self.doc.footnotes:
                        flush()
                        tokens.append(self.doc.footnote_ref(text[i + 2 : close]))
                        i = close + 1
                        continue
                link = self.link(text, i)
                if link:
                    label, url, title, end = link
                    flush()
                    title_attr = f' title="{attr(title)}"' if title else ""
                    tokens.append(
                        f'<a href="{attr(url)}"{title_attr}>{self.render(label)}</a>'
                    )
                    i = end
                    continue

            if text.startswith("~~", i):
                close = text.find("~~", i + 2)
                if close != -1:
                    flush()
                    tokens.append(f"<del>{self.render(text[i + 2 : close])}</del>")
                    i = close + 2
                    continue

            if c in "*_":
                end, can_open, can_close = scan_delimiter(text, i)
                if can_open or can_close:
                    flush()
                    tokens.append(Delimiter(c, end - i, can_open, can_close))
                else:
                    buffer.append(text[i:end])
                i = end
                continue

            if c == "\n":
                trailing = "".join(buffer)
                if trailing.endswith("  "):
                    buffer[:] = [trailing.rstrip(" ")]
                    flush()
                    tokens.append("<br>\n")
                    i += 1
                    continue

            buffer.append(c)
            i += 1

        flush()
        return resolve_emphasis(tokens)

    def linkify(self, text):
        pieces, last = [], 0
        for match in BARE_URL.finditer(text):
            url = match.group(0)
            pieces += [
                esc(text[last : match.start()]),
                f'<a href="{attr(url)}">{esc(url)}</a>',
            ]
            last = match.end()
        pieces.append(esc(text[last:]))
        return "".join(pieces)

    def link(self, text, start):
        close = find_bracket_end(text, start)
        if close == -1:
            return None
        match = LINK_TAIL.match(text, close + 1)
        if not match:
            return None
        title = match.group(2) or match.group(3) or ""
        return text[start + 1 : close], match.group(1), title, match.end()

    def image(self, label, url, title):
        caption = f"\n<small>{esc(title)}</small>" if title else ""
        tag = f'<img src="{attr(url)}" alt="{attr(label)}" loading="lazy">'
        return f"<figure>{tag}{caption}</figure>" if title or self.doc.alone else tag


# Blocks

FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})\s*([^\s`]*)")
HEADING = re.compile(r"^ {0,3}(#{1,6})(?:\s+(.*?))?\s*#*\s*$")
RULE = re.compile(r"^ {0,3}(?:(?:-\s*){3,}|(?:\*\s*){3,}|(?:_\s*){3,})$")
SETEXT = re.compile(r"^ {0,3}(=+|-+)\s*$")
LIST_ITEM = re.compile(r"^( {0,3})([-*+]|\d{1,9}[.)])( +|$)")
QUOTE = re.compile(r"^ {0,3}> ?")
TABLE_DELIMITER = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")
ATTRIBUTES = re.compile(r"^\{\s*((?:\.[\w-]+\s*)+)\}\s*$")
FOOTNOTE = re.compile(r"^\[\^([^\]]+)\]:\s?(.*)$")
RAW_ONLY = re.compile(r"^ {0,3}<(script|style|pre|textarea)\b", re.I)
RAW_BLOCK = re.compile(
    r"^ {0,3}</?(address|article|aside|blockquote|br|canvas|center|details|div|dl|embed|fieldset|figcaption"
    r"|figure|footer|form|h[1-6]|header|hr|iframe|li|main|nav|ol|p|section|summary|table|tbody|td|tfoot|th"
    r"|thead|tr|ul|video)\b|^ {0,3}<!--",
    re.I,
)


def indent_of(line):
    width = 0
    for c in line:
        if c == " ":
            width += 1
        elif c == "\t":
            width += 4 - width % 4
        else:
            break
    return width


def dedent(line, columns):
    """Remove up to COLUMNS of leading whitespace, counting a tab as up to 4."""
    width = i = 0
    while i < len(line) and width < columns and line[i] in " \t":
        width += 1 if line[i] == " " else 4 - width % 4
        i += 1
    return " " * max(width - columns, 0) + line[i:]


def split_cells(line):
    line = line.strip()
    line = line[1:] if line.startswith("|") else line
    cells, cell, i, in_code = [], [], 0, False
    while i < len(line):
        c = line[i]
        if c == "\\" and line[i + 1 : i + 2] == "|":
            cell.append("|")
            i += 2
            continue
        if c == "`":
            in_code = not in_code
        if c == "|" and not in_code:
            cells.append("".join(cell).strip())
            cell = []
        else:
            cell.append(c)
        i += 1
    if "".join(cell).strip():
        cells.append("".join(cell).strip())
    return cells


class Document:
    """One Markdown file: its footnotes, heading IDs, and whether it needs MathJax."""

    def __init__(self):
        self.footnotes = {}
        self.footnote_order = []
        self.heading_ids = {}
        self.headings = []
        self.has_math = False
        self.alone = False
        self.inlines = Inlines(self)

    def render(self, text):
        lines = self.take_footnotes(text.replace("\r\n", "\n").split("\n"))
        body = "\n".join(self.blocks(lines))
        return body + self.render_footnotes()

    def take_footnotes(self, lines):
        kept, i, fence = [], 0, None
        while i < len(lines):
            line = lines[i]
            match = FENCE.match(line)
            if match and (fence is None or match.group(1).startswith(fence)):
                fence = match.group(1) if fence is None else None
            definition = None if fence else FOOTNOTE.match(line)
            if not definition:
                kept.append(line)
                i += 1
                continue
            body, i = [definition.group(2)], i + 1
            while i < len(lines) and (indent_of(lines[i]) >= 4 or not lines[i].strip()):
                following = next((l for l in lines[i:] if l.strip()), "")
                if not lines[i].strip() and indent_of(following) < 4:
                    break
                body.append(dedent(lines[i], 4))
                i += 1
            self.footnotes[definition.group(1)] = body
        return kept

    def footnote_ref(self, name):
        if name not in self.footnote_order:
            self.footnote_order.append(name)
        n = self.footnote_order.index(name) + 1
        return f'<sup id="fnref:{n}"><a href="#fn:{n}" role="doc-noteref">{n}</a></sup>'

    def render_footnotes(self):
        items, done = [], 0
        while done < len(self.footnote_order):  # A footnote can cite another footnote.
            done += 1
            name = self.footnote_order[done - 1]
            body = "\n".join(self.blocks(self.footnotes[name]))
            back = f' <a href="#fnref:{done}" role="doc-backlink">↩</a>'
            if body.endswith("</p>"):
                body = body[:-4] + back + "</p>"
            else:
                body += back
            items.append(f'<li id="fn:{done}">{body}</li>')
        if not items:
            return ""
        return (
            '\n<section class="footnotes"><ol>\n'
            + "\n".join(items)
            + "\n</ol></section>"
        )

    def heading(self, level, text):
        plain = re.sub(r"\\[()\[\]]|[^\w\s-]", "", text.lower()).strip()
        slug = re.sub(r"\s", "-", plain)
        seen = self.heading_ids.get(slug, 0)
        self.heading_ids[slug] = seen + 1
        slug = f"{slug}-{seen}" if seen else slug
        rendered = self.inlines.render(text)
        self.headings.append((level, slug, rendered))
        return f'<h{level} id="{attr(slug)}">{rendered}</h{level}>'

    def paragraph(self, text):
        text = text.strip()
        self.alone = re.fullmatch(r"!\[[^\n]*\]\([^\n]*\)", text) is not None
        rendered = self.inlines.render(text)
        self.alone = False
        return (
            rendered
            if rendered.startswith("<figure>") and rendered.endswith("</figure>")
            else f"<p>{rendered}</p>"
        )

    def starts_block(self, line):
        """True if LINE ends an open paragraph."""
        item = LIST_ITEM.match(line)
        if (
            item
            and line[item.end() :].strip()
            and item.group(2) in ("-", "*", "+", "1.", "1)")
        ):
            return True
        return bool(
            FENCE.match(line)
            or HEADING.match(line)
            or RULE.match(line)
            or QUOTE.match(line)
            or RAW_BLOCK.match(line)
            or RAW_ONLY.match(line)
        )

    def blocks(self, lines):
        out, i = [], 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            if not stripped:
                i += 1
                continue

            match = ATTRIBUTES.match(stripped)
            if match and out:
                classes = " ".join(c.lstrip(".") for c in match.group(1).split())
                out[-1] = re.sub(
                    r"<(table|p|h[1-6]|ul|ol|pre|blockquote)\b",
                    rf'<\1 class="{classes}"',
                    out[-1],
                    count=1,
                )
                i += 1
                continue

            match = FENCE.match(line)
            if match:
                i = self.fence(lines, i, match, out)
                continue

            if indent_of(line) >= 4:
                i = self.indented_code(lines, i, out)
                continue

            if stripped.startswith(("$$", "\\[")):
                closer = "$$" if stripped.startswith("$$") else "\\]"
                end = i
                while end < len(lines) and closer not in (
                    lines[end].strip()[2:] if end == i else lines[end]
                ):
                    end += 1
                if end < len(lines):
                    self.has_math = True
                    out.append(
                        f'<div class="math">{esc(chr(10).join(lines[i : end + 1]))}</div>'
                    )
                    i = end + 1
                    continue

            match = HEADING.match(line)
            if match:
                out.append(self.heading(len(match.group(1)), match.group(2) or ""))
                i += 1
                continue

            if RULE.match(line):
                out.append("<hr>")
                i += 1
                continue

            if QUOTE.match(line):
                i = self.quote(lines, i, out)
                continue

            if LIST_ITEM.match(line):
                i = self.list(lines, i, out)
                continue

            match = RAW_ONLY.match(line)
            if match:
                closer = f"</{match.group(1).lower()}>"
                end = i
                while end < len(lines) - 1 and closer not in lines[end].lower():
                    end += 1
                out.append("\n".join(lines[i : end + 1]))
                i = end + 1
                continue

            if RAW_BLOCK.match(line):
                end = i
                while end < len(lines) and lines[end].strip():
                    end += 1
                out.append("\n".join(lines[i:end]))
                i = end
                continue

            if (
                "|" in line
                and i + 1 < len(lines)
                and "-" in lines[i + 1]
                and TABLE_DELIMITER.match(lines[i + 1])
            ):
                i = self.table(lines, i, out)
                continue

            i = self.paragraph_lines(lines, i, out)
        return out

    def fence(self, lines, i, match, out):
        marker, language = match.group(1), match.group(2)
        indent = indent_of(lines[i])
        closer = re.compile(
            r"^ {0,3}" + re.escape(marker[0]) + "{%d,}\\s*$" % len(marker)
        )
        body, i = [], i + 1
        while i < len(lines) and not closer.match(lines[i]):
            body.append(dedent(lines[i], indent))
            i += 1
        language_class = f' class="language-{attr(language)}"' if language else ""
        out.append(
            f"<pre><code{language_class}>{highlight_code(chr(10).join(body), language)}</code></pre>"
        )
        return i + 1

    def indented_code(self, lines, i, out):
        body = []
        while i < len(lines) and (indent_of(lines[i]) >= 4 or not lines[i].strip()):
            body.append(dedent(lines[i], 4))
            i += 1
        while body and not body[-1].strip():
            body.pop()
        out.append(f"<pre><code>{esc(chr(10).join(body))}\n</code></pre>")
        return i

    def quote(self, lines, i, out):
        body = []
        while i < len(lines) and lines[i].strip():
            match = QUOTE.match(lines[i])
            if not match and self.starts_block(lines[i]):
                break
            body.append(lines[i][match.end() :] if match else lines[i])
            i += 1
        out.append("<blockquote>\n" + "\n".join(self.blocks(body)) + "\n</blockquote>")
        return i

    def list(self, lines, i, out):
        first = LIST_ITEM.match(lines[i])
        ordered = first.group(2)[0].isdigit()
        kind = first.group(2)[-1]
        items, loose = [], False

        while i < len(lines):
            match = LIST_ITEM.match(lines[i])
            if (
                not match
                or match.group(2)[-1] != kind
                or match.group(2)[0].isdigit() != ordered
                or RULE.match(lines[i])
            ):
                break
            spaces = len(match.group(3))
            width = (
                len(match.group(1))
                + len(match.group(2))
                + (spaces if 1 <= spaces <= 4 else 1)
            )
            body, i = [lines[i][width:]], i + 1
            blank_inside = False
            while i < len(lines):
                line = lines[i]
                if not line.strip():
                    following = next((l for l in lines[i:] if l.strip()), None)
                    if following is None or indent_of(following) < width:
                        break
                    body.append("")
                    blank_inside = True
                elif indent_of(line) >= width:
                    body.append(dedent(line, width))
                elif (
                    body[-1].strip()
                    and not self.starts_block(line)
                    and not LIST_ITEM.match(line)
                ):
                    body.append(line.lstrip())  # A lazy continuation line.
                else:
                    break
                i += 1
            end = i
            while end < len(lines) and not lines[end].strip():
                end += 1
            following = (
                LIST_ITEM.match(lines[end]) if end < len(lines) and end > i else None
            )
            more = following is not None and following.group(2)[-1] == kind
            loose = loose or blank_inside or more
            items.append(body)
            if more:
                i = end

        rendered = []
        for body in items:
            blocks = self.blocks(body)
            if not loose:
                blocks = [
                    b[3:-4] if b.startswith("<p>") and b.endswith("</p>") else b
                    for b in blocks
                ]
            rendered.append("<li>" + "\n".join(blocks) + "</li>")
        start = int(first.group(2)[:-1]) if ordered else 1
        tag = "ol" if ordered else "ul"
        start_attr = f' start="{start}"' if start != 1 else ""
        out.append(f"<{tag}{start_attr}>\n" + "\n".join(rendered) + f"\n</{tag}>")
        return i

    def table(self, lines, i, out):
        aligns = []
        for cell in split_cells(lines[i + 1]):
            left, right = cell.startswith(":"), cell.endswith(":")
            aligns.append(
                "center"
                if left and right
                else "right"
                if right
                else "left"
                if left
                else ""
            )

        def row(cells, tag):
            parts = []
            for n, cell in enumerate(cells[: len(aligns)]):
                style = f' style="text-align:{aligns[n]}"' if aligns[n] else ""
                parts.append(f"<{tag}{style}>{self.inlines.render(cell)}</{tag}>")
            return "<tr>" + "".join(parts) + "</tr>"

        head = row(split_cells(lines[i]), "th")
        i += 2
        rows = []
        while i < len(lines) and lines[i].strip() and "|" in lines[i]:
            rows.append(row(split_cells(lines[i]), "td"))
            i += 1
        body = f"<tbody>\n{chr(10).join(rows)}\n</tbody>\n" if rows else ""
        out.append(f"<table>\n<thead>\n{head}\n</thead>\n{body}</table>")
        return i

    def paragraph_lines(self, lines, i, out):
        body = [lines[i]]
        i += 1
        while i < len(lines) and lines[i].strip():
            match = SETEXT.match(lines[i])
            if match:
                out.append(
                    self.heading(
                        1 if match.group(1)[0] == "=" else 2,
                        " ".join(l.strip() for l in body),
                    )
                )
                return i + 1
            if self.starts_block(lines[i]):
                break
            body.append(lines[i].lstrip())
            i += 1
        out.append(self.paragraph("\n".join(body)))
        return i


def wrap_tables(body):
    return re.sub(
        r"(<table\b.*?</table>)", r'<div class="table-wrap">\1</div>', body, flags=re.S
    )


# Pages


def parse_yaml(text):
    """Parse the flat "key: value" front matter the site uses."""
    data = {}
    for line in text.splitlines():
        match = re.match(r"^(\w+):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.groups()
        if value[:1] in ('"', "'"):
            value = value[1 : value.index(value[0], 1)]
        else:
            value = re.sub(r"\s+#.*$", "", value).strip()
            value = {"true": True, "false": False}.get(value, value)
        data[key] = value
    return data


def split_front_matter(text):
    for fence, parser in (("+++", tomllib.loads), ("---", parse_yaml)):
        if text.startswith(fence + "\n"):
            end = text.index("\n" + fence, len(fence))
            return parser(text[len(fence) + 1 : end + 1]), text[end + 1 + len(fence) :]
    raise ValueError("no front matter")


def parse_date(value):
    if not value:
        return None
    if not isinstance(value, datetime):
        value = re.sub(
            r"T(\d):", r"T0\1:", str(value)
        )  # Some files write 8:00 for 08:00.
    parsed = value if isinstance(value, datetime) else datetime.fromisoformat(value)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def plain_text(rendered):
    text = re.sub(r"<(script|style)\b.*?</\1>", " ", rendered, flags=re.S | re.I)
    text = re.sub(r"<sup id=\"fnref.*?</sup>", "", text)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", text)).split())


class Page:
    def __init__(self, source, relative):
        self.meta, self.markdown = split_front_matter(
            source.read_text(encoding="utf-8")
        )
        self.relative = relative
        self.title = str(self.meta.get("title", relative.stem))
        self.date = parse_date(self.meta.get("date"))
        self.section = relative.parts[0] if len(relative.parts) > 1 else None
        self.is_section_index = (
            relative.name in ("index.md", "_index.md") and self.section in SECTIONS
        )
        self.url = self.find_url()

    def find_url(self):
        override = self.meta.get("url")
        if override:
            url = "/" + str(override).strip("/")
            return url if url.endswith(".html") else url + "/"
        parts = list(self.relative.with_suffix("").parts)
        if parts[-1] in ("index", "_index"):
            parts.pop()
        return "/" + "".join(p + "/" for p in parts)

    @property
    def output(self):
        path = self.url.strip("/")
        return path if path.endswith(".html") else str(Path(path, "index.html"))

    def render(self):
        self.doc = Document()
        self.body = wrap_tables(self.doc.render(self.markdown))
        self.text = plain_text(self.body)
        self.minutes = max(1, math.ceil(len(self.text.split()) / WORDS_PER_MINUTE))
        self.summary = str(
            self.meta.get("summary") or self.text[:160].rsplit(" ", 1)[0]
        )

    @property
    def date_text(self):
        return self.date.strftime("%Y-%m-%d") if self.date else ""


def table_of_contents(page):
    links = [
        f'<li><a href="#{attr(slug)}">{title}</a></li>'
        for level, slug, title in page.doc.headings
        if level <= 3
    ]
    if not links:
        return ""
    return (
        '<details class="toc"><summary>Contents</summary><ul>'
        + "".join(links)
        + "</ul></details>\n"
    )


def article(page):
    parts = ["<article>"]
    if page.meta.get("showTitle", True):
        parts.append(f"<h1>{esc(page.title)}</h1>")
    if page.date and not page.meta.get("hideMeta"):
        details = [page.date_text]
        if page.meta.get("showReadingTime", True):
            details.append(f"{page.minutes} min read")
        parts.append(f'<p class="post-meta">{" · ".join(details)}</p>')
    if page.meta.get("showtoc"):
        parts.append(table_of_contents(page))
    parts.append(f'<div class="post-body">\n{page.body}\n</div>')
    if page.meta.get("layout") == "search":
        parts.append(SEARCH_BODY)
    parts.append("</article>")
    return "\n".join(parts)


def card_list(pages):
    items = []
    for page in pages:
        items.append(
            f'<li><a href="{attr(page.url)}">{esc(page.title)}</a>'
            f'<span class="card-meta">{page.date_text} · {page.minutes} min read</span></li>'
        )
    return '<ul class="cards">\n' + "\n".join(items) + "\n</ul>"


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def fill(template, title, description, url, main, head=""):
    page_title = SITE_TITLE if title == SITE_TITLE else f"{title} | {SITE_TITLE}"
    return template.substitute(
        title=attr(page_title),
        description=attr(description),
        canonical=BASE_URL + url,
        head=head,
        main=main,
    )


def newest_first(pages):
    dated = sorted((p for p in pages if p.date), key=lambda p: p.date, reverse=True)
    return dated + [p for p in pages if not p.date]


def rss(pages):
    items = []
    for page in pages:
        link = BASE_URL + page.url
        items.append(
            f"<item><title>{xml_escape(page.title)}</title><link>{link}</link>"
            f"<guid>{link}</guid><pubDate>{format_datetime(page.date)}</pubDate>"
            f"<description>{xml_escape(page.summary)}</description></item>"
        )
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n<rss version="2.0"><channel>'
        f"<title>{SITE_TITLE}</title><link>{BASE_URL}/</link><description>Recent content from {SITE_TITLE}"
        "</description><language>en-us</language>\n"
        + "\n".join(items)
        + "\n</channel></rss>\n"
    )


def sitemap(urls):
    rows = [f"<url><loc>{xml_escape(BASE_URL + url)}</loc></url>" for url in urls]
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows)
        + "\n</urlset>\n"
    )


def walk(source):
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        hidden = any(part.startswith(".") for part in relative.parts)
        if path.is_file() and not hidden and not (set(relative.parts) & SKIP):
            yield path, relative


def build(source, out):
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    template = string.Template(
        (ROOT / "templates" / "page.html").read_text(encoding="utf-8")
    )
    now = datetime.now(timezone.utc)
    pages = []

    for path, relative in walk(source):
        if relative.suffix != ".md":
            if relative.suffix == ".html" and path.with_suffix(".md").exists():
                raise SystemExit(f"{relative} has a Markdown file next to it")
            target = out / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            continue
        try:
            page = Page(path, relative)
        except ValueError as error:
            raise SystemExit(f"{relative}: {error}")
        if not page.meta.get("draft") and not (page.date and page.date > now):
            pages.append(page)

    for name in ("site.css", "search.js"):
        shutil.copy2(ROOT / name, out / name)

    seen = {}
    for page in pages:
        if page.url in seen:
            raise SystemExit(
                f"{page.relative} and {seen[page.url]} both build to {page.url}"
            )
        seen[page.url] = page.relative
        page.render()

    articles = [p for p in pages if p.section in SECTIONS and not p.is_section_index]
    section_pages = {
        name: newest_first([p for p in articles if p.section == name])
        for name in SECTIONS
    }
    index_pages = {p.section: p for p in pages if p.is_section_index}

    for page in pages:
        if page.is_section_index:
            continue
        head = MATHJAX if page.doc.has_math else ""
        write(
            out / page.output,
            fill(template, page.title, page.summary, page.url, article(page), head),
        )

    urls = [p.url for p in pages if not p.is_section_index]
    for name, title in SECTIONS.items():
        title = index_pages[name].title if name in index_pages else title
        main = f"<h1>{esc(title)}</h1>\n{card_list(section_pages[name])}"
        url = f"/{name}/"
        write(
            out / name / "index.html",
            fill(template, title, f"{title} by {SITE_TITLE}", url, main),
        )
        urls.append(url)
        write(out / name / "index.xml", rss([p for p in section_pages[name] if p.date]))

    write(
        out / "404.html",
        fill(
            template,
            "Page Not Found",
            "Page not found",
            "/404.html",
            '<h1>Page Not Found</h1>\n<p><a href="/">Go to the home page</a></p>',
        ),
    )

    feed = newest_first(articles)
    write(out / "index.xml", rss([p for p in feed if p.date]))
    write(out / "sitemap.xml", sitemap(sorted(urls)))
    index = [
        {"title": p.title, "url": p.url, "date": p.date_text, "content": p.text}
        for p in feed
    ]
    write(out / "index.json", json.dumps(index, ensure_ascii=False))
    print(f"Built {len(pages)} pages into {out}")


def main(args):
    if len(args) > 2:
        raise SystemExit(__doc__)
    build(
        Path(args[0]) if args else ROOT,
        Path(args[1]) if len(args) == 2 else ROOT / "_site",
    )


if __name__ == "__main__":
    main(sys.argv[1:])
